-- ============================================================
-- RA-QDMS — Schéma Supabase (PostgreSQL)
-- EXÉCUTEZ LA PARTIE 1 SEULE D'ABORD. Si elle réussit,
-- l'application fonctionne déjà. La partie 2 est optionnelle.
-- ============================================================

-- ================= PARTIE 1 : L'ESSENTIEL =================
-- (sélectionnez uniquement ces lignes, puis Run)

create table if not exists public.qdms_state (
  id text primary key,
  state jsonb not null,
  updated_at timestamptz not null default now()
);

alter table public.qdms_state enable row level security;

drop policy if exists qdms_state_read on public.qdms_state;
create policy qdms_state_read on public.qdms_state
  for select using (true);

drop policy if exists qdms_state_insert on public.qdms_state;
create policy qdms_state_insert on public.qdms_state
  for insert with check (true);

drop policy if exists qdms_state_update on public.qdms_state;
create policy qdms_state_update on public.qdms_state
  for update using (true);

-- ============ FIN DE LA PARTIE 1 — l'app peut fonctionner ============


-- ========= PARTIE 2 (OPTIONNELLE) : sauvegardes automatiques =========
-- Conserve les 30 dernières versions à chaque modification.
-- Exécutez-la dans une NOUVELLE requête, après la partie 1.

create table if not exists public.qdms_backups (
  id bigint generated always as identity primary key,
  state jsonb not null,
  created_at timestamptz not null default now()
);

alter table public.qdms_backups enable row level security;

create or replace function public.qdms_backup_on_update()
returns trigger
language plpgsql
security definer
as $$
begin
  insert into public.qdms_backups (state) values (old.state);
  delete from public.qdms_backups
   where id not in (select id from public.qdms_backups order by id desc limit 30);
  return new;
end;
$$;

drop trigger if exists trg_qdms_backup on public.qdms_state;
create trigger trg_qdms_backup
  before update on public.qdms_state
  for each row execute function public.qdms_backup_on_update();
