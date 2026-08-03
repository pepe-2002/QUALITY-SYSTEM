-- ══════════════════════════════════════════════════════════════════════
--  « Nous » — messagerie privée : base de données
--
--  À COLLER UNE SEULE FOIS dans VOTRE PROPRE projet Supabase
--  (SQL Editor → Run). ⚠️ Un projet créé exprès pour « Nous » —
--  JAMAIS celui de MoheliGo : les deux applications ne partagent rien.
--  (On peut le relancer sans risque : tout est « if not exists » /
--   « create or replace ».)
--
--  Utile seulement si vous voulez relier DEUX téléphones. Sur un seul
--  appareil, l'application se sert de sa base intégrée et n'a besoin
--  de rien de tout ça.
--
--  PRINCIPE DE CONFIDENTIALITÉ
--  Le serveur ne stocke que :
--    · « salon »  : l'empreinte SHA-256 du code du salon (jamais le code) ;
--    · « corps » et « media » : des blocs CHIFFRÉS sur le téléphone
--      (AES-GCM 256, clé dérivée du code du salon par PBKDF2).
--  Sans le code, ces lignes sont illisibles — y compris pour
--  l'administrateur de la base. Les tables ne sont accessibles par
--  AUCUNE requête directe : on passe obligatoirement par les
--  fonctions ci-dessous, qui exigent l'empreinte du salon.
-- ══════════════════════════════════════════════════════════════════════

-- ───────────────────────── 1. LES TABLES ─────────────────────────

create table if not exists public.nous_message(
  id          bigint generated always as identity primary key,
  salon       text        not null check (salon ~ '^[0-9a-f]{64}$'),
  corps       text        not null,              -- bloc chiffré (auteur, texte, type…)
  media       text,                              -- bloc chiffré (photo ou vocal)
  visible_le  timestamptz not null default now(),-- messages programmés : dans le futur
  cree_le     timestamptz not null default now()
);
create index if not exists nous_message_salon_id  on public.nous_message(salon, id);
create index if not exists nous_message_salon_vis on public.nous_message(salon, visible_le);

-- État partagé du salon : « je suis occupé jusqu'à… », réglages communs.
create table if not exists public.nous_etat(
  salon   text not null check (salon ~ '^[0-9a-f]{64}$'),
  cle     text not null check (length(cle) <= 80),
  valeur  text not null,                         -- bloc chiffré
  maj     timestamptz not null default now(),
  primary key (salon, cle)
);

-- Personne ne lit ni n'écrit ces tables directement.
alter table public.nous_message enable row level security;
alter table public.nous_etat    enable row level security;
revoke all on public.nous_message from anon, authenticated;
revoke all on public.nous_etat    from anon, authenticated;

-- ──────────────────────── 2. LES FONCTIONS ────────────────────────

-- Envoyer (p_visible_le dans le futur = message programmé).
create or replace function public.nous_envoyer(
  p_salon text, p_corps text, p_media text default null, p_visible_le timestamptz default null)
returns bigint
language plpgsql security definer set search_path = public as $$
declare v_id bigint; v_n int;
begin
  if p_salon !~ '^[0-9a-f]{64}$'        then raise exception 'salon invalide'; end if;
  if p_corps is null or p_corps = ''    then raise exception 'message vide';   end if;
  if length(p_corps) > 40000            then raise exception 'message trop long'; end if;
  if p_media is not null and length(p_media) > 4000000 then
    raise exception 'piece jointe trop lourde'; end if;

  -- garde-fou anti-emballement (un salon = deux personnes, pas un robot)
  select count(*) into v_n from nous_message
   where salon = p_salon and cree_le > now() - interval '1 minute';
  if v_n > 240 then raise exception 'trop de messages, reessayez dans une minute'; end if;

  insert into nous_message(salon, corps, media, visible_le)
  values (p_salon, p_corps, p_media, coalesce(p_visible_le, now()))
  returning id into v_id;
  return v_id;
end $$;

-- Lire la suite : uniquement ce qui est ARRIVÉ À ÉCHÉANCE (visible_le <= maintenant).
-- Un message programmé reste invisible pour tout le monde jusqu'à son heure.
--
-- Deuxième condition, moins évidente mais nécessaire : un message écrit hier
-- pour ce matin porte un petit numéro. Une fois que le téléphone d'en face a
-- reçu des messages plus récents, il ne redemande plus les petits numéros —
-- le message programmé serait arrivé avec beaucoup de retard. On renvoie donc
-- aussi les messages PROGRAMMÉS (échéance nettement après l'écriture) devenus
-- visibles dans les trois dernières minutes. Le téléphone ignore les doublons.
create or replace function public.nous_lire(
  p_salon text, p_depuis bigint default 0, p_limite int default 100)
returns table(id bigint, corps text, media text, visible_le timestamptz, cree_le timestamptz)
language sql security definer set search_path = public as $$
  select m.id, m.corps, m.media, m.visible_le, m.cree_le
    from nous_message m
   where m.salon = p_salon
     and m.visible_le <= now()
     and ( m.id > coalesce(p_depuis, 0)
        or ( m.visible_le > m.cree_le + interval '30 seconds'
         and m.visible_le > now() - interval '3 minutes' ) )
   order by m.id
   limit least(greatest(coalesce(p_limite, 100), 1), 300);
$$;

-- Rattrapage : la liste des messages échus (juste les identifiants, c'est léger).
-- Sert à récupérer un message programmé devenu visible APRÈS des messages
-- envoyés en direct, et à repérer ceux qui ont été effacés.
create or replace function public.nous_ids(p_salon text, p_limite int default 400)
returns table(id bigint, vide boolean)
language sql security definer set search_path = public as $$
  select m.id, (m.corps = '.') as vide
    from nous_message m
   where m.salon = p_salon and m.visible_le <= now()
   order by m.id desc
   limit least(greatest(coalesce(p_limite, 400), 1), 1000);
$$;

-- Récupérer des messages précis (ceux que le rattrapage a trouvés manquants).
create or replace function public.nous_par_ids(p_salon text, p_ids bigint[])
returns table(id bigint, corps text, media text, visible_le timestamptz, cree_le timestamptz)
language sql security definer set search_path = public as $$
  select m.id, m.corps, m.media, m.visible_le, m.cree_le
    from nous_message m
   where m.salon = p_salon and m.visible_le <= now()
     and m.id = any(coalesce(p_ids, '{}'::bigint[]))
   order by m.id
   limit 60;
$$;

-- Effacer pour tout le monde. Le contenu part vraiment ; la ligne reste
-- marquée « effacée » (corps = '.') pour que l'autre téléphone le sache.
create or replace function public.nous_effacer(p_salon text, p_id bigint)
returns boolean
language plpgsql security definer set search_path = public as $$
begin
  update nous_message set corps = '.', media = null
   where salon = p_salon and id = p_id;
  return found;
end $$;

-- Annuler un message programmé qui n'est pas encore parti.
create or replace function public.nous_annuler(p_salon text, p_id bigint)
returns boolean
language plpgsql security definer set search_path = public as $$
begin
  delete from nous_message
   where salon = p_salon and id = p_id and visible_le > now();
  return found;
end $$;

-- État partagé (« occupé jusqu'à 18 h »…) : on écrase la valeur précédente.
create or replace function public.nous_etat_ecrire(p_salon text, p_cle text, p_valeur text)
returns boolean
language plpgsql security definer set search_path = public as $$
begin
  if p_salon !~ '^[0-9a-f]{64}$' then raise exception 'salon invalide'; end if;
  if length(coalesce(p_valeur,'')) > 20000 then raise exception 'valeur trop longue'; end if;
  insert into nous_etat(salon, cle, valeur, maj) values (p_salon, p_cle, p_valeur, now())
  on conflict (salon, cle) do update set valeur = excluded.valeur, maj = now();
  return true;
end $$;

create or replace function public.nous_etat_lire(p_salon text)
returns table(cle text, valeur text, maj timestamptz)
language sql security definer set search_path = public as $$
  select e.cle, e.valeur, e.maj from nous_etat e where e.salon = p_salon limit 40;
$$;

-- ────────────────────── 3. LES DROITS D'APPEL ──────────────────────
-- Seules ces fonctions sont ouvertes, et chacune exige l'empreinte du salon.

revoke all on function public.nous_envoyer(text,text,text,timestamptz)  from public;
revoke all on function public.nous_lire(text,bigint,int)                from public;
revoke all on function public.nous_ids(text,int)                        from public;
revoke all on function public.nous_par_ids(text,bigint[])               from public;
revoke all on function public.nous_effacer(text,bigint)                 from public;
revoke all on function public.nous_annuler(text,bigint)                 from public;
revoke all on function public.nous_etat_ecrire(text,text,text)          from public;
revoke all on function public.nous_etat_lire(text)                      from public;

grant execute on function public.nous_envoyer(text,text,text,timestamptz) to anon, authenticated;
grant execute on function public.nous_lire(text,bigint,int)               to anon, authenticated;
grant execute on function public.nous_ids(text,int)                       to anon, authenticated;
grant execute on function public.nous_par_ids(text,bigint[])              to anon, authenticated;
grant execute on function public.nous_effacer(text,bigint)                to anon, authenticated;
grant execute on function public.nous_annuler(text,bigint)                to anon, authenticated;
grant execute on function public.nous_etat_ecrire(text,text,text)         to anon, authenticated;
grant execute on function public.nous_etat_lire(text)                     to anon, authenticated;

-- ───────────────────── 4. MÉNAGE (facultatif) ─────────────────────
-- Pour ne pas garder les vocaux et photos éternellement, on peut appeler
-- ceci de temps en temps (SQL Editor), ou le brancher sur pg_cron :
--   select public.nous_menage();
create or replace function public.nous_menage()
returns int
language plpgsql security definer set search_path = public as $$
declare n int;
begin
  with vieux as (
    delete from nous_message
     where media is not null and cree_le < now() - interval '180 days'
     returning 1)
  select count(*) into n from vieux;
  return n;
end $$;
revoke all on function public.nous_menage() from public;
