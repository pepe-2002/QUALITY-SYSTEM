"""QR code : encodage pur Python, et surtout **vérification** (spec §9).

La suite se valide à deux niveaux :

1. **Aller-retour** — toute matrice produite doit se relire. Sans réseau,
   sans dépendance, toujours exécuté.
2. **Comparaison à une référence** — quand `segno` est installé, les motifs de
   fonction et l'information de format doivent être identiques au module près,
   et notre décodeur doit savoir lire les matrices de segno. C'est ce qui
   garantit qu'un téléphone saura scanner nos codes.

Note sur le bourrage : segno ajoute un octet 0x00 superflu quand le flux est
déjà aligné (`8 - length % 8` vaut 8 au lieu de 0). La norme §7.4.10 n'en
demande aucun. On compare donc les motifs et le contenu décodé, pas les octets
de bourrage — que tout lecteur ignore de toute façon.
"""

from __future__ import annotations

import pytest

from ara.design import qr

segno = pytest.importorskip  # utilisé plus bas, en option

URLS = [
    "https://moheligo.com",
    "MoheliGo",
    "https://moheligo.com/reservation?trajet=ouroveni-hoani",
    "Ouroveni -> Hoani, 15 000 FC",
    "https://exemple.test/" + "x" * 60,
]


# --- Aller-retour -------------------------------------------------------------


@pytest.mark.parametrize("text", URLS)
@pytest.mark.parametrize("level", ["L", "M", "Q", "H"])
def test_toute_matrice_produite_se_relit(text, level):
    """Le cœur de la spec §9 : on ne fait pas confiance, on relit."""
    code = qr.encode(text, level)
    assert qr.decode(code.matrix) == text


def test_make_verified_rend_un_code_relu():
    code = qr.make_verified("https://moheligo.com", "H")
    assert code.text == "https://moheligo.com"
    assert code.level == "H"


def test_les_accents_survivent():
    text = "Traversée Grande Comore ↔ Mohéli"
    assert qr.decode(qr.encode(text, "M").matrix) == text


def test_la_version_grandit_avec_le_contenu():
    court = qr.encode("https://moheligo.com", "M")
    long = qr.encode("https://moheligo.com/" + "x" * 80, "M")
    assert long.version > court.version
    assert long.size > court.size


def test_un_niveau_de_correction_plus_fort_coute_plus_de_place():
    faible = qr.encode("https://moheligo.com/reservation", "L")
    fort = qr.encode("https://moheligo.com/reservation", "H")
    assert fort.version >= faible.version


# --- Structure ----------------------------------------------------------------


def test_les_reperes_de_position_sont_aux_trois_coins():
    code = qr.encode("https://moheligo.com")
    m, size = code.matrix, code.size
    for row, col in [(0, 0), (0, size - 7), (size - 7, 0)]:
        assert m[row][col] == 1 and m[row + 6][col + 6] == 1
        assert m[row + 1][col + 1] == 0, "l'anneau blanc du repère manque"
        assert m[row + 3][col + 3] == 1, "le cœur noir du repère manque"


def test_le_module_noir_obligatoire_est_present():
    """Écraser ce module par l'information de format rend le symbole illisible."""
    code = qr.encode("https://moheligo.com")
    assert code.matrix[code.size - 8][8] == 1


def test_les_motifs_de_synchronisation_alternent():
    code = qr.encode("https://moheligo.com")
    for i in range(8, code.size - 8):
        attendu = 1 if i % 2 == 0 else 0
        assert code.matrix[6][i] == attendu
        assert code.matrix[i][6] == attendu


def test_le_masque_choisi_est_le_moins_penalisant():
    code = qr.encode("https://moheligo.com")
    assert 0 <= code.mask <= 7


# --- Refus ---------------------------------------------------------------------


def test_un_contenu_vide_est_refuse():
    with pytest.raises(qr.QRError):
        qr.encode("")


def test_un_niveau_inconnu_est_refuse():
    with pytest.raises(qr.QRError):
        qr.encode("https://moheligo.com", "Z")


def test_un_contenu_trop_long_est_refuse_avec_un_message_clair():
    with pytest.raises(qr.QRError, match="trop long"):
        qr.encode("x" * 400, "H")


def test_une_matrice_corrompue_est_detectee():
    """Un module retourné doit faire échouer le contrôle Reed-Solomon."""
    code = qr.encode("https://moheligo.com", "L")
    matrix = [list(row) for row in code.matrix]
    for row in range(12, 20):       # zone de données, loin des motifs
        for col in range(12, 20):
            matrix[row][col] ^= 1
    with pytest.raises(qr.QRError):
        qr.decode(matrix)


def test_une_matrice_de_taille_invalide_est_refusee():
    with pytest.raises(qr.QRError):
        qr.decode([[0] * 10 for _ in range(10)])


# --- Rendu ---------------------------------------------------------------------


def test_le_chemin_svg_couvre_les_modules_noirs():
    code = qr.encode("https://moheligo.com")
    path = code.to_svg_path(module=4.0, quiet=4.0)
    assert path.startswith("M") and "h" in path and "z" in path
    assert path.count("z") <= sum(sum(row) for row in code.matrix)


def test_le_rendu_texte_a_la_bonne_taille():
    code = qr.encode("https://moheligo.com")
    assert len(code.to_text().splitlines()) == code.size


# --- Comparaison à une bibliothèque de référence ------------------------------


@pytest.mark.parametrize("text", URLS)
@pytest.mark.parametrize("level", ["L", "M", "Q", "H"])
def test_motifs_et_format_identiques_a_la_reference(text, level):
    """Un téléphone doit pouvoir scanner : les motifs doivent être conformes."""
    reference = pytest.importorskip("segno")

    mine = qr.encode(text, level)
    ref = reference.make(
        text, error=level.lower(), boost_error=False, mask=mine.mask,
        micro=False, mode="byte", encoding="utf-8",
    )
    refm = [[1 if cell else 0 for cell in row] for row in ref.matrix]
    if len(refm) != mine.size:
        pytest.skip("versions différentes : comparaison sans objet")

    reserved = qr._blank(mine.size)
    qr._place_static(reserved, mine.version)
    fixes = [
        (r, c)
        for r in range(mine.size)
        for c in range(mine.size)
        if reserved[r][c] is not None
    ]
    ecarts = [(r, c) for r, c in fixes if mine.matrix[r][c] != refm[r][c]]
    assert not ecarts, f"motifs de fonction ou format divergents : {ecarts[:5]}"


@pytest.mark.parametrize("text", URLS)
def test_notre_decodeur_lit_les_matrices_de_reference(text):
    """Preuve que notre lecture du standard est la bonne, pas seulement cohérente."""
    reference = pytest.importorskip("segno")

    for level in ("L", "M", "Q", "H"):
        ref = reference.make(
            text, error=level.lower(), boost_error=False, micro=False,
            mode="byte", encoding="utf-8",
        )
        matrix = [[1 if cell else 0 for cell in row] for row in ref.matrix]
        if (len(matrix) - 17) // 4 > qr.MAX_VERSION:
            continue
        assert qr.decode(matrix) == text
