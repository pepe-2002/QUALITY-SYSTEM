# Ouvrir ARA depuis l'extérieur, par un tunnel

Votre PC garde l'agent ; Cloudflare ne fait que transporter la connexion.
Aucun hébergeur, aucun compte, aucun abonnement.

```bash
cd agent
bash deploy/tunnel/tunnel.sh
```

Le script affiche une adresse de la forme :

```
https://quelque-chose.trycloudflare.com/?token=UN-JETON-LONG
```

Ouvrez-la sur le téléphone, puis **Ajouter à l'écran d'accueil**.

## Ce qu'il faut savoir avant de partager quoi que ce soit

**Ce lien est la clé.** Qui l'a pilote votre agent : il lance des recherches,
produit des fichiers, consomme votre connexion. Ne le publiez pas, ne le
collez pas dans un groupe.

Trois garde-fous sont en place, et il faut savoir ce que chacun couvre :

| Garde-fou | Ce qu'il protège |
|---|---|
| **Jeton obligatoire** | toutes les routes `/api/` refusent sans lui |
| **Écoute sur 127.0.0.1** | l'agent n'est pas exposé sur votre Wi-Fi, seulement à travers le tunnel |
| **Liste blanche d'outils** | `share_file`, `delete_file`, `publish` restent bloqués ou demandent confirmation |

Ce qu'ils ne couvrent **pas** : la page d'accueil elle-même reste servie sans
jeton. C'est une coquille HTML sans donnée — elle ne montre rien et ne peut
rien faire — mais quelqu'un qui tombe sur l'adresse verra qu'un agent tourne
là.

## Arrêter

`Ctrl+C`. L'adresse disparaît immédiatement, le serveur aussi. Rien ne
subsiste : la prochaine adresse sera différente.

## Garder le même jeton d'une fois sur l'autre

```bash
export ARA_TOKEN="une-phrase-longue-que-vous-choisissez"
bash deploy/tunnel/tunnel.sh
```

L'adresse changera quand même — c'est le propre des tunnels temporaires.

## Une adresse permanente

Il faut un compte Cloudflare (gratuit) et un nom de domaine que vous y avez
délégué :

```bash
cloudflared tunnel login
cloudflared tunnel create ara
cloudflared tunnel route dns ara ara.votre-domaine.fr
ARA_TOKEN="votre-jeton" ARA_HOST=127.0.0.1 python -m ara.cli --serve &
cloudflared tunnel run --url http://127.0.0.1:8800 ara
```

L'adresse devient `https://ara.votre-domaine.fr/?token=…` et ne change plus.
Le jeton reste indispensable.

## Si le tunnel refuse de s'ouvrir

Le script recopie les journaux à l'écran. Les deux causes habituelles :

- `cloudflared` absent — le script donne la commande d'installation ;
- un pare-feu d'entreprise qui bloque la sortie ; dans ce cas, l'option 1
  (téléphone + Termux) reste disponible et ne dépend d'aucun réseau tiers.
