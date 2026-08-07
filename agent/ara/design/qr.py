"""Générateur de QR code en Python pur — et son vérificateur (spec §9).

Aucune dépendance : le prototype doit rester installable sur un téléphone.
L'encodeur suit ISO/IEC 18004 en mode octet, versions 1 à 10, tous niveaux de
correction.

**Le QR est vérifié avant d'être inséré**, comme l'exige la spec. La
vérification ne fait pas confiance à l'encodeur : elle relit la matrice
produite comme le ferait un lecteur — format, démasquage, dé-entrelacement,
contrôle des syndromes Reed-Solomon, décodage — et compare au texte d'origine.
Un QR qui ne se relit pas n'est jamais posé sur une création.
"""

from __future__ import annotations

from dataclasses import dataclass

# --- Arithmétique de Galois GF(256) ------------------------------------------

_EXP = [0] * 512
_LOG = [0] * 256


def _init_tables() -> None:
    value = 1
    for i in range(255):
        _EXP[i] = value
        _LOG[value] = i
        value <<= 1
        if value & 0x100:
            value ^= 0x11D  # polynôme primitif du standard QR
    for i in range(255, 512):
        _EXP[i] = _EXP[i - 255]


_init_tables()


def _mul(a: int, b: int) -> int:
    if a == 0 or b == 0:
        return 0
    return _EXP[_LOG[a] + _LOG[b]]


def _generator_poly(degree: int) -> list[int]:
    poly = [1]
    for i in range(degree):
        poly = _poly_mul(poly, [1, _EXP[i]])
    return poly


def _poly_mul(a: list[int], b: list[int]) -> list[int]:
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] ^= _mul(x, y)
    return out


def _rs_encode(data: list[int], ec_count: int) -> list[int]:
    """Codewords de correction d'erreur Reed-Solomon."""
    generator = _generator_poly(ec_count)
    remainder = list(data) + [0] * ec_count
    for i in range(len(data)):
        factor = remainder[i]
        if factor == 0:
            continue
        for j, coefficient in enumerate(generator):
            remainder[i + j] ^= _mul(coefficient, factor)
    return remainder[len(data) :]


def _syndromes(block: list[int], ec_count: int) -> list[int]:
    """Syndromes d'un bloc : tous nuls si le bloc est intègre."""
    return [
        _poly_eval(block, _EXP[i])
        for i in range(ec_count)
    ]


def _poly_eval(poly: list[int], x: int) -> int:
    result = 0
    for coefficient in poly:
        result = _mul(result, x) ^ coefficient
    return result


# --- Tables du standard -------------------------------------------------------

#: Nombre total de codewords par version (1 à 10)
_TOTAL_CODEWORDS = [26, 44, 70, 100, 134, 172, 196, 242, 292, 346]

#: (version, niveau) → (codewords EC par bloc, [(nombre de blocs, données par bloc)])
_BLOCKS: dict[tuple[int, str], tuple[int, list[tuple[int, int]]]] = {
    (1, "L"): (7, [(1, 19)]),   (1, "M"): (10, [(1, 16)]),
    (1, "Q"): (13, [(1, 13)]),  (1, "H"): (17, [(1, 9)]),
    (2, "L"): (10, [(1, 34)]),  (2, "M"): (16, [(1, 28)]),
    (2, "Q"): (22, [(1, 22)]),  (2, "H"): (28, [(1, 16)]),
    (3, "L"): (15, [(1, 55)]),  (3, "M"): (26, [(1, 44)]),
    (3, "Q"): (18, [(2, 17)]),  (3, "H"): (22, [(2, 13)]),
    (4, "L"): (20, [(1, 80)]),  (4, "M"): (18, [(2, 32)]),
    (4, "Q"): (26, [(2, 24)]),  (4, "H"): (16, [(4, 9)]),
    (5, "L"): (26, [(1, 108)]), (5, "M"): (24, [(2, 43)]),
    (5, "Q"): (18, [(2, 15), (2, 16)]),
    (5, "H"): (22, [(2, 11), (2, 12)]),
    (6, "L"): (18, [(2, 68)]),  (6, "M"): (16, [(4, 27)]),
    (6, "Q"): (24, [(4, 19)]),  (6, "H"): (28, [(4, 15)]),
    (7, "L"): (20, [(2, 78)]),  (7, "M"): (18, [(4, 31)]),
    (7, "Q"): (18, [(2, 14), (4, 15)]),
    (7, "H"): (26, [(4, 13), (1, 14)]),
    (8, "L"): (24, [(2, 97)]),
    (8, "M"): (22, [(2, 38), (2, 39)]),
    (8, "Q"): (22, [(4, 18), (2, 19)]),
    (8, "H"): (26, [(4, 14), (2, 15)]),
    (9, "L"): (30, [(2, 116)]),
    (9, "M"): (22, [(3, 36), (2, 37)]),
    (9, "Q"): (20, [(4, 16), (4, 17)]),
    (9, "H"): (24, [(4, 12), (4, 13)]),
    (10, "L"): (18, [(2, 68), (2, 69)]),
    (10, "M"): (26, [(4, 43), (1, 44)]),
    (10, "Q"): (24, [(6, 19), (2, 20)]),
    (10, "H"): (28, [(6, 15), (2, 16)]),
}

#: Centres des motifs d'alignement par version
_ALIGNMENT = {
    1: [], 2: [6, 18], 3: [6, 22], 4: [6, 26], 5: [6, 30],
    6: [6, 34], 7: [6, 22, 38], 8: [6, 24, 42], 9: [6, 26, 46], 10: [6, 28, 50],
}

#: Bits restants après les codewords (versions 1-10)
_REMAINDER = {1: 0, 2: 7, 3: 7, 4: 7, 5: 7, 6: 7, 7: 0, 8: 0, 9: 0, 10: 0}

#: Indicateur de niveau de correction dans l'information de format
_EC_BITS = {"L": 0b01, "M": 0b00, "Q": 0b11, "H": 0b10}
_EC_FROM_BITS = {v: k for k, v in _EC_BITS.items()}

MAX_VERSION = 10


class QRError(Exception):
    """Le QR code n'a pas pu être produit ou relu."""


# --- Encodage des données -----------------------------------------------------


def _capacity(version: int, level: str) -> int:
    ec_per_block, groups = _BLOCKS[(version, level)]
    return sum(count * data for count, data in groups)


def _choose_version(payload: bytes, level: str) -> int:
    for version in range(1, MAX_VERSION + 1):
        header = 4 + (8 if version < 10 else 16)
        if len(payload) * 8 + header <= _capacity(version, level) * 8:
            return version
    raise QRError(
        f"Contenu trop long pour un QR de version {MAX_VERSION} "
        f"({len(payload)} octets). Raccourcissez l'URL."
    )


def _encode_data(payload: bytes, version: int, level: str) -> list[int]:
    bits: list[int] = []

    def push(value: int, length: int) -> None:
        for shift in range(length - 1, -1, -1):
            bits.append((value >> shift) & 1)

    push(0b0100, 4)                                  # mode octet
    push(len(payload), 8 if version < 10 else 16)    # longueur
    for byte in payload:
        push(byte, 8)

    capacity_bits = _capacity(version, level) * 8
    push(0, min(4, capacity_bits - len(bits)))       # terminateur
    while len(bits) % 8:
        bits.append(0)

    codewords = [int("".join(str(b) for b in bits[i : i + 8]), 2) for i in range(0, len(bits), 8)]
    pad = [0xEC, 0x11]
    while len(codewords) < _capacity(version, level):
        codewords.append(pad[(len(codewords) - len(bits) // 8) % 2])
    return codewords


def _interleave(codewords: list[int], version: int, level: str) -> list[int]:
    ec_count, groups = _BLOCKS[(version, level)]

    blocks: list[list[int]] = []
    offset = 0
    for count, data_size in groups:
        for _ in range(count):
            blocks.append(codewords[offset : offset + data_size])
            offset += data_size

    ec_blocks = [_rs_encode(block, ec_count) for block in blocks]

    out: list[int] = []
    for index in range(max(len(b) for b in blocks)):
        for block in blocks:
            if index < len(block):
                out.append(block[index])
    for index in range(ec_count):
        for block in ec_blocks:
            out.append(block[index])
    return out


# --- Construction de la matrice ----------------------------------------------


def _blank(size: int) -> list[list[int | None]]:
    return [[None] * size for _ in range(size)]


def _place_finder(matrix, row: int, col: int) -> None:
    for r in range(-1, 8):
        for c in range(-1, 8):
            y, x = row + r, col + c
            if not (0 <= y < len(matrix) and 0 <= x < len(matrix)):
                continue
            inside = 0 <= r <= 6 and 0 <= c <= 6
            dark = inside and (
                r in (0, 6) or c in (0, 6) or (2 <= r <= 4 and 2 <= c <= 4)
            )
            matrix[y][x] = 1 if dark else 0


def _place_alignment(matrix, version: int) -> None:
    centers = _ALIGNMENT[version]
    size = len(matrix)
    for row in centers:
        for col in centers:
            # Pas de motif sous les repères de position
            if (row < 8 and col < 8) or (row < 8 and col > size - 9) or (
                row > size - 9 and col < 8
            ):
                continue
            for r in range(-2, 3):
                for c in range(-2, 3):
                    dark = max(abs(r), abs(c)) != 1
                    matrix[row + r][col + c] = 1 if dark else 0


def _place_static(matrix, version: int) -> None:
    size = len(matrix)
    _place_finder(matrix, 0, 0)
    _place_finder(matrix, 0, size - 7)
    _place_finder(matrix, size - 7, 0)
    _place_alignment(matrix, version)

    for i in range(8, size - 8):  # motifs de synchronisation
        bit = 1 if i % 2 == 0 else 0
        matrix[6][i] = bit
        matrix[i][6] = bit

    matrix[size - 8][8] = 1  # module noir obligatoire

    for i in range(9):  # zones réservées au format
        if matrix[8][i] is None:
            matrix[8][i] = 0
        if matrix[i][8] is None:
            matrix[i][8] = 0
    for i in range(8):
        if matrix[8][size - 1 - i] is None:
            matrix[8][size - 1 - i] = 0
        if matrix[size - 1 - i][8] is None:
            matrix[size - 1 - i][8] = 0

    if version >= 7:  # zones réservées à la version
        for i in range(6):
            for j in range(3):
                matrix[size - 11 + j][i] = 0
                matrix[i][size - 11 + j] = 0


def _data_positions(size: int) -> list[tuple[int, int]]:
    """Parcours en zigzag, de bas en haut, colonnes par paires."""
    positions = []
    col = size - 1
    upward = True
    while col > 0:
        if col == 6:  # colonne de synchronisation, ignorée
            col -= 1
        rows = range(size - 1, -1, -1) if upward else range(size)
        for row in rows:
            positions.append((row, col))
            positions.append((row, col - 1))
        col -= 2
        upward = not upward
    return positions


def _mask_condition(mask: int, row: int, col: int) -> bool:
    if mask == 0:
        return (row + col) % 2 == 0
    if mask == 1:
        return row % 2 == 0
    if mask == 2:
        return col % 3 == 0
    if mask == 3:
        return (row + col) % 3 == 0
    if mask == 4:
        return (row // 2 + col // 3) % 2 == 0
    if mask == 5:
        return (row * col) % 2 + (row * col) % 3 == 0
    if mask == 6:
        return ((row * col) % 2 + (row * col) % 3) % 2 == 0
    return ((row + col) % 2 + (row * col) % 3) % 2 == 0


def _format_bits(level: str, mask: int) -> list[int]:
    value = (_EC_BITS[level] << 3) | mask
    # Division polynomiale BCH(15,5) par x¹⁰+x⁸+x⁵+x⁴+x²+x+1
    remainder = value << 10
    for shift in range(4, -1, -1):
        if remainder & (1 << (shift + 10)):
            remainder ^= 0x537 << shift
    bits_value = ((value << 10) | remainder) ^ 0x5412
    return [(bits_value >> i) & 1 for i in range(14, -1, -1)]


def _version_bits(version: int) -> list[int]:
    remainder = version << 12
    for shift in range(5, -1, -1):
        if remainder & (1 << (shift + 12)):
            remainder ^= 0x1F25 << shift
    value = (version << 12) | remainder
    return [(value >> i) & 1 for i in range(17, -1, -1)]


def _format_positions(size: int) -> tuple[list[tuple[int, int]], list[tuple[int, int]]]:
    """Emplacements des 15 bits de format, dans l'ordre de la chaîne.

    La chaîne est posée du bit le plus significatif au moins significatif.
    ⚠️ La seconde copie ne compte que 7 modules du côté bas-gauche : le
    huitième, (taille-8, 8), est le **module noir obligatoire**. L'écraser
    rend le symbole illisible — erreur constatée en comparant la matrice à
    une bibliothèque de référence.
    """
    copy1 = (
        [(8, i) for i in range(6)]
        + [(8, 7), (8, 8), (7, 8)]
        + [(5, 8), (4, 8), (3, 8), (2, 8), (1, 8), (0, 8)]
    )
    copy2 = [(size - 1 - j, 8) for j in range(7)] + [
        (8, size - 8 + k) for k in range(8)
    ]
    return copy1, copy2


def _apply_format(matrix, level: str, mask: int) -> None:
    bits = _format_bits(level, mask)
    copy1, copy2 = _format_positions(len(matrix))
    for bit, (row, col) in zip(bits, copy1 + copy2):
        matrix[row][col] = bit
    for bit, (row, col) in zip(bits, copy2):
        matrix[row][col] = bit


def _apply_version(matrix, version: int) -> None:
    if version < 7:
        return
    size = len(matrix)
    bits = list(reversed(_version_bits(version)))  # bits[i] = bit i
    for i in range(18):
        row, col = i // 3, i % 3
        matrix[size - 11 + col][row] = bits[i]
        matrix[row][size - 11 + col] = bits[i]


def _penalty(matrix: list[list[int]]) -> int:
    size = len(matrix)
    score = 0

    # Règle 1 : suites de 5 modules ou plus de même couleur
    for line in list(matrix) + [list(col) for col in zip(*matrix)]:
        run, previous = 1, line[0]
        for cell in line[1:]:
            if cell == previous:
                run += 1
            else:
                if run >= 5:
                    score += 3 + (run - 5)
                run, previous = 1, cell
        if run >= 5:
            score += 3 + (run - 5)

    # Règle 2 : blocs 2×2 uniformes
    for row in range(size - 1):
        for col in range(size - 1):
            block = {
                matrix[row][col], matrix[row][col + 1],
                matrix[row + 1][col], matrix[row + 1][col + 1],
            }
            if len(block) == 1:
                score += 3

    # Règle 3 : motifs ressemblant à un repère de position
    pattern_a = [1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0]
    pattern_b = list(reversed(pattern_a))
    for line in list(matrix) + [list(col) for col in zip(*matrix)]:
        for i in range(size - 10):
            window = list(line[i : i + 11])
            if window == pattern_a or window == pattern_b:
                score += 40

    # Règle 4 : déséquilibre global noir / blanc
    dark = sum(sum(row) for row in matrix)
    ratio = dark * 100 // (size * size)
    score += 10 * (abs(ratio - 50) // 5)
    return score


@dataclass
class QRCode:
    """Une matrice de QR code et ses métadonnées."""

    matrix: list[list[int]]
    version: int
    level: str
    mask: int
    text: str

    @property
    def size(self) -> int:
        return len(self.matrix)

    def to_dict(self) -> dict:
        return {
            "version": self.version,
            "level": self.level,
            "mask": self.mask,
            "size": self.size,
            "text": self.text,
        }

    def to_svg_path(self, module: float = 1.0, quiet: float = 4.0) -> str:
        """Chemin SVG des modules noirs, décalé de la zone de silence."""
        parts = []
        for row, line in enumerate(self.matrix):
            col = 0
            while col < len(line):
                if line[col]:
                    start = col
                    while col < len(line) and line[col]:
                        col += 1
                    x = (quiet + start) * module
                    y = (quiet + row) * module
                    parts.append(f"M{x:.2f} {y:.2f}h{(col - start) * module:.2f}v{module:.2f}h{-(col - start) * module:.2f}z")
                else:
                    col += 1
        return "".join(parts)

    def to_text(self) -> str:
        """Rendu texte, pratique pour un contrôle visuel rapide."""
        return "\n".join("".join("██" if cell else "  " for cell in row) for row in self.matrix)


def encode(text: str, level: str = "M") -> QRCode:
    """Produit un QR code en mode octet.

    >>> qr = encode("https://moheligo.com")
    >>> qr.version, qr.level
    (2, 'M')
    """
    level = level.upper()
    if level not in _EC_BITS:
        raise QRError(f"Niveau de correction inconnu : {level} (attendu L, M, Q ou H)")
    if not text:
        raise QRError("Contenu vide : rien à encoder.")

    payload = text.encode("utf-8")
    version = _choose_version(payload, level)
    size = 17 + version * 4

    codewords = _interleave(_encode_data(payload, version, level), version, level)
    bits = [(byte >> shift) & 1 for byte in codewords for shift in range(7, -1, -1)]
    bits += [0] * _REMAINDER[version]

    base = _blank(size)
    _place_static(base, version)

    positions = [pos for pos in _data_positions(size) if base[pos[0]][pos[1]] is None]
    for (row, col), bit in zip(positions, bits):
        base[row][col] = bit

    best: QRCode | None = None
    best_score = None
    for mask in range(8):
        candidate = [list(row) for row in base]
        for row, col in positions:
            if _mask_condition(mask, row, col):
                candidate[row][col] ^= 1
        _apply_format(candidate, level, mask)
        _apply_version(candidate, version)
        filled = [[cell or 0 for cell in row] for row in candidate]
        score = _penalty(filled)
        if best_score is None or score < best_score:
            best_score = score
            best = QRCode(filled, version, level, mask, text)

    assert best is not None
    return best


# --- Vérification -------------------------------------------------------------


def _read_format(matrix: list[list[int]]) -> tuple[str, int]:
    copy1, _copy2 = _format_positions(len(matrix))
    bits = [matrix[row][col] for row, col in copy1]

    value = 0
    for bit in bits:                       # du plus significatif au moins
        value = (value << 1) | bit
    value ^= 0x5412
    data = value >> 10
    level = _EC_FROM_BITS.get((data >> 3) & 0b11)
    mask = data & 0b111
    if level is None:
        raise QRError("Information de format illisible dans la matrice.")
    return level, mask


def decode(matrix: list[list[int]]) -> str:
    """Relit une matrice de QR code comme le ferait un lecteur.

    Lève :class:`QRError` si la matrice n'est pas un QR valide. C'est cette
    fonction qui donne son sens à « le QR code doit être vérifié avant
    insertion » : on ne fait pas confiance à l'encodeur, on relit.
    """
    size = len(matrix)
    if size < 21 or (size - 17) % 4 or any(len(row) != size for row in matrix):
        raise QRError(f"Matrice de taille invalide : {size}")
    version = (size - 17) // 4
    if version > MAX_VERSION:
        raise QRError(f"Version {version} non prise en charge (max {MAX_VERSION}).")

    level, mask = _read_format(matrix)

    reserved = _blank(size)
    _place_static(reserved, version)
    positions = [pos for pos in _data_positions(size) if reserved[pos[0]][pos[1]] is None]

    bits = []
    for row, col in positions:
        bit = matrix[row][col]
        if _mask_condition(mask, row, col):
            bit ^= 1
        bits.append(bit)

    total = _TOTAL_CODEWORDS[version - 1]
    codewords = [
        int("".join(str(b) for b in bits[i * 8 : i * 8 + 8]), 2) for i in range(total)
    ]

    # Dé-entrelacement, inverse exact de `_interleave`
    ec_count, groups = _BLOCKS[(version, level)]
    sizes = [data for count, data in groups for _ in range(count)]
    blocks: list[list[int]] = [[] for _ in sizes]
    index = 0
    for position in range(max(sizes)):
        for block_index, block_size in enumerate(sizes):
            if position < block_size:
                blocks[block_index].append(codewords[index])
                index += 1
    ec_blocks: list[list[int]] = [[] for _ in sizes]
    for position in range(ec_count):
        for block_index in range(len(sizes)):
            ec_blocks[block_index].append(codewords[index])
            index += 1

    # Contrôle d'intégrité : les syndromes doivent être nuls.
    for data_block, ec_block in zip(blocks, ec_blocks):
        if any(_syndromes(data_block + ec_block, ec_count)):
            raise QRError("Contrôle Reed-Solomon en échec : la matrice est corrompue.")

    payload = [byte for block in blocks for byte in block]
    stream = "".join(f"{byte:08b}" for byte in payload)

    mode = int(stream[:4], 2)
    if mode != 0b0100:
        raise QRError(f"Mode {mode:04b} inattendu (seul le mode octet est produit).")
    count_len = 8 if version < 10 else 16
    length = int(stream[4 : 4 + count_len], 2)
    start = 4 + count_len
    data = bytes(
        int(stream[start + i * 8 : start + i * 8 + 8], 2) for i in range(length)
    )
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        # Beaucoup de QR du commerce encodent en ISO-8859-1 : un lecteur qui
        # ne sait lire que l'UTF-8 échouerait sur des codes parfaitement valides.
        try:
            return data.decode("iso-8859-1")
        except UnicodeDecodeError as exc:
            raise QRError(f"Contenu illisible après décodage : {exc}") from exc


def make_verified(text: str, level: str = "M") -> QRCode:
    """Produit un QR **et le relit** avant de le rendre (spec §9).

    >>> make_verified("https://moheligo.com").text
    'https://moheligo.com'
    """
    qr = encode(text, level)
    relu = decode(qr.matrix)
    if relu != text:
        raise QRError(
            f"Le QR produit ne se relit pas correctement : « {relu[:60]} » "
            f"au lieu de « {text[:60]} »."
        )
    return qr
