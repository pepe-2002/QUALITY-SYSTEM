# Études de sécurité — Département Qualité / SGS Royal Air

| Référence | Objet | Source | Sortie |
|---|---|---|---|
| RA-SGS-ETU-26-01 | Ouverture d'une desserte de Mayotte (FMCZ / DZA) depuis les Comores, LET 410 | `generateur/etude_mayotte.py` | `RA-SGS-ETU-26-01-desserte-mayotte.html` + `.pdf` |

## Règle

Le document HTML **est généré par le script** : on corrige le registre des risques et le
texte dans `generateur/etude_mayotte.py`, jamais dans le HTML de sortie.

La cotation (indice OACI, score P×G, tolérabilité) est calculée par le script avec
**exactement les mêmes règles** que le module *Risk Management* du RA-QDMS (`app.js`,
fonction `riskCalc`) : matrice OACI 5×5 du Doc 9859.

## Regénérer

```bash
python3 etudes/generateur/etude_mayotte.py
# PDF (Chromium headless) :
chromium --headless --no-pdf-header-footer \
  --print-to-pdf=etudes/RA-SGS-ETU-26-01-desserte-mayotte.pdf \
  file://$PWD/etudes/RA-SGS-ETU-26-01-desserte-mayotte.html
```
