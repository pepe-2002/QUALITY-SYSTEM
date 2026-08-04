"""Synthèse des voix (edge-tts) et fabrication des sous-titres SRT.

Chaque réplique devient un fichier mp3 nommé plan-XX.mp3, avec l'empreinte vocale
du personnage (voix + débit + hauteur). Le narrateur utilise la voix de marque.
"""

import os
import re
import subprocess
import shutil

CA = "/root/.ccr/ca-bundle.crt"


def _env():
    e = os.environ.copy()
    if os.path.exists(CA):
        e["SSL_CERT_FILE"] = CA
        e["REQUESTS_CA_BUNDLE"] = CA
    return e


def _duree_audio(chemin):
    """Durée d'un fichier audio. ffprobe si présent, sinon lecture de la sortie ffmpeg
    (certaines installations, dont les ffmpeg statiques via pip, n'ont pas ffprobe)."""
    if shutil.which("ffprobe"):
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=nw=1:nk=1", chemin],
            capture_output=True, text=True,
        )
        try:
            return float(out.stdout.strip())
        except ValueError:
            pass
    out = subprocess.run(["ffmpeg", "-i", chemin], capture_output=True, text=True)
    m = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.?\d*)", out.stderr)
    if m:
        h, mn, s = m.groups()
        return int(h) * 3600 + int(mn) * 60 + float(s)
    return 0.0


def synthetiser(texte, voix, rate, pitch, sortie):
    """Appelle edge-tts. Renvoie la durée obtenue (0.0 si échec)."""
    # --rate=-6% doit rester collé : sinon argparse prend « -6% » pour une option
    cmd = ["edge-tts", "--voice", voix, "--rate=%s" % rate, "--pitch=%s" % pitch,
           "--text", texte, "--write-media", sortie]
    proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
    if proxy:
        cmd[1:1] = ["--proxy", proxy]
    r = subprocess.run(cmd, capture_output=True, text=True, env=_env(), stdin=subprocess.DEVNULL)
    if r.returncode != 0 or not os.path.exists(sortie):
        raise RuntimeError("edge-tts a échoué : %s" % (r.stderr.strip()[:400] or "sortie absente"))
    _ebarber(sortie)
    return _duree_audio(sortie)


def _ebarber(chemin):
    """Retire les silences de tête et de queue laissés par edge-tts.

    Sans ça, chaque réplique traîne près d'une seconde de vide et un film de 30 s
    en fait 36. Le studio place lui-même les respirations, au montage.
    """
    brut = chemin + ".brut.mp3"
    os.replace(chemin, brut)
    filtre = ("silenceremove=start_periods=1:start_duration=0:start_threshold=-45dB,"
              "areverse,"
              "silenceremove=start_periods=1:start_duration=0:start_threshold=-45dB,"
              "areverse")
    r = subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", brut,
                        "-af", filtre, chemin], capture_output=True, text=True)
    if r.returncode != 0 or not os.path.exists(chemin):
        os.replace(brut, chemin)  # en cas d'échec, on garde la voix telle quelle
        return
    os.remove(brut)


def repliques(scenario):
    """Liste des répliques à dire : (plan, type, avatar_id|None, texte)."""
    sortie = []
    for p in scenario["plans"]:
        if p.get("dialogue"):
            sortie.append((p["n"], "dialogue", p["dialogue"]["avatar"], p["dialogue"]["texte"]))
        if p.get("voix_off"):
            sortie.append((p["n"], "voix_off", None, p["voix_off"]))
    return sortie


def produire(bible, scenario, dossier):
    """Synthétise toutes les répliques. Renvoie la liste des pistes avec leurs durées."""
    dossier_audio = os.path.join(dossier, "audio")
    os.makedirs(dossier_audio, exist_ok=True)
    langue = scenario["langue"]
    pistes = []

    for n, genre, avatar_id, texte in repliques(scenario):
        nom = "plan-%02d-%s.mp3" % (n, "vo" if genre == "voix_off" else "dlg")
        chemin = os.path.join(dossier_audio, nom)
        if genre == "voix_off":
            voix, rate, pitch = bible.narrateur(langue)
        else:
            empreinte = bible.empreinte_vocale(avatar_id, langue)
            if empreinte is None:
                raise RuntimeError(
                    "Aucune voix disponible pour %s en %s (mineur, ou langue non couverte)."
                    % (avatar_id, langue)
                )
            voix, rate, pitch = empreinte
        duree = synthetiser(texte, voix, rate, pitch, chemin)
        pistes.append({
            "plan": n, "genre": genre, "avatar": avatar_id, "texte": texte,
            "fichier": os.path.relpath(chemin, dossier), "voix": voix,
            "rate": rate, "pitch": pitch, "duree": round(duree, 2),
        })
    return pistes


def caler(scenario, pistes):
    """Ajuste la durée des plans pour qu'aucune réplique ne soit coupée,
    et calcule le point de départ de chaque piste dans le montage."""
    par_plan = {}
    for p in pistes:
        par_plan.setdefault(p["plan"], []).append(p)

    for plan in scenario["plans"]:
        besoin = sum(x["duree"] for x in par_plan.get(plan["n"], [])) + 0.45
        if besoin > plan["duree"]:
            plan["duree"] = round(besoin, 1)

    debut = 0.0
    for plan in scenario["plans"]:
        curseur = debut + 0.2
        for x in par_plan.get(plan["n"], []):
            x["debut"] = round(curseur, 2)
            curseur += x["duree"] + 0.12
        plan["debut"] = round(debut, 2)
        debut += plan["duree"]
    scenario["duree_reelle"] = round(debut, 2)
    return scenario, pistes


def _hms(t):
    h = int(t // 3600)
    m = int(t % 3600 // 60)
    s = t % 60
    return "%02d:%02d:%02d,%03d" % (h, m, int(s), round((s - int(s)) * 1000))


def _decouper(texte, largeur=42):
    mots, lignes, courante = texte.split(), [], ""
    for mot in mots:
        if len(courante) + len(mot) + 1 <= largeur:
            courante = (courante + " " + mot).strip()
        else:
            lignes.append(courante)
            courante = mot
    if courante:
        lignes.append(courante)
    return lignes[:2] if len(lignes) <= 2 else [" ".join(lignes[:-1]), lignes[-1]]


def srt(pistes, chemin):
    blocs = []
    for i, p in enumerate(sorted(pistes, key=lambda x: x.get("debut", 0)), 1):
        debut = p.get("debut", 0)
        fin = debut + max(p["duree"], 1.2)
        blocs.append("%d\n%s --> %s\n%s\n" % (
            i, _hms(debut), _hms(fin), "\n".join(_decouper(p["texte"]))))
    with open(chemin, "w", encoding="utf-8") as f:
        f.write("\n".join(blocs))
    return chemin


def disponible():
    return shutil.which("edge-tts") is not None
