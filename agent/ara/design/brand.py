"""Mémoire de marque (spec §10) — `brand_profile.json`.

Ce que l'agent apprend d'une marque doit servir la fois suivante : couleurs,
typographies, slogans, dimensions habituelles, ton, exemples approuvés, et
surtout **ce qu'il ne faut pas faire**.

Cette dernière liste est la plus précieuse. Sur MoheliGo, le patron a dit
« pas d'emojis » et « logo Facebook officiel, pas l'emoji livre ». Sans mémoire,
l'agent refait la même erreur à chaque session.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path

from ..core.config import get_settings
from . import color as colors

#: Profil neutre utilisé quand aucune marque n'est enregistrée
DEFAULT_PALETTE = ("#0a2550", "#1b6ca8", "#facc15", "#f7fafc", "#0b1220")


@dataclass
class BrandProfile:
    """Tout ce que l'agent sait d'une marque."""

    name: str = "Sans marque"
    #: la première couleur est la dominante, la troisième l'accent
    palette: list[str] = field(default_factory=lambda: list(DEFAULT_PALETTE))
    fonts: list[str] = field(
        default_factory=lambda: ["Georgia, 'Times New Roman', serif", "Helvetica, Arial, sans-serif"]
    )
    slogans: list[str] = field(default_factory=list)
    tone: str = "clair, direct, sans esbroufe"
    style: str = "sobre, contrasté, beaucoup d'espace"
    #: dimensions préférées en pixels (largeur, hauteur)
    dimensions: list[int] = field(default_factory=lambda: [2160, 2700])
    logo: str = ""
    website: str = ""
    contact: str = ""
    #: exemples validés par l'humain — servent de référence
    approved: list[str] = field(default_factory=list)
    #: interdits explicites, formulés par le propriétaire de la marque
    avoid: list[str] = field(default_factory=list)

    # -- accès pratiques ---------------------------------------------------

    @property
    def primary(self) -> str:
        return self.palette[0] if self.palette else DEFAULT_PALETTE[0]

    @property
    def secondary(self) -> str:
        return self.palette[1] if len(self.palette) > 1 else colors.lighten(self.primary, 0.3)

    @property
    def accent(self) -> str:
        return self.palette[2] if len(self.palette) > 2 else "#facc15"

    @property
    def paper(self) -> str:
        return self.palette[3] if len(self.palette) > 3 else "#ffffff"

    @property
    def ink(self) -> str:
        return self.palette[4] if len(self.palette) > 4 else "#0b1220"

    @property
    def title_font(self) -> str:
        return self.fonts[0] if self.fonts else "Georgia, serif"

    @property
    def body_font(self) -> str:
        return self.fonts[1] if len(self.fonts) > 1 else "Helvetica, Arial, sans-serif"

    def forbids(self, what: str) -> bool:
        """Vrai si la marque interdit explicitement quelque chose.

        >>> BrandProfile(avoid=["pas d'emojis"]).forbids("emoji")
        True
        """
        needle = what.lower().rstrip("s")
        return any(needle in rule.lower() for rule in self.avoid)

    # -- persistance -------------------------------------------------------

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "BrandProfile":
        known = set(cls.__dataclass_fields__)
        return cls(**{k: v for k, v in data.items() if k in known})

    def save(self, path: Path | None = None) -> Path:
        path = Path(path or get_settings().brand_profile_path())
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(self.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8"
        )
        return path

    @classmethod
    def load(cls, path: Path | None = None) -> "BrandProfile":
        """Charge le profil, ou retourne un profil neutre s'il n'existe pas."""
        path = Path(path or get_settings().brand_profile_path())
        if not path.is_file():
            return cls()
        try:
            return cls.from_dict(json.loads(path.read_text(encoding="utf-8")))
        except (json.JSONDecodeError, TypeError, OSError):
            # Un profil corrompu ne doit pas empêcher de travailler.
            return cls()

    def remember(self, **changes) -> "BrandProfile":
        """Met à jour le profil sans écraser ce qui n'est pas fourni."""
        for key, value in changes.items():
            if key not in self.__dataclass_fields__ or value in (None, "", [], {}):
                continue
            current = getattr(self, key)
            if isinstance(current, list) and isinstance(value, list):
                for item in value:
                    if item not in current:
                        current.append(item)
            else:
                setattr(self, key, value)
        return self


def moheligo_profile() -> BrandProfile:
    """Profil MoheliGo, tiré des consignes déjà données par le propriétaire.

    Sert d'exemple concret de mémoire de marque : ces règles ont été énoncées
    une fois et doivent s'appliquer à toutes les créations suivantes.
    """
    return BrandProfile(
        name="MoheliGo",
        palette=["#0a2550", "#1b6ca8", "#facc15", "#f7fafc", "#0b1220"],
        slogans=["MoheliGo point com", "Traversées maritimes des Comores"],
        tone="sobre et direct, jamais racoleur",
        style="premium, contrasté, dégradés marins, beaucoup d'espace",
        dimensions=[2160, 2700],
        website="https://moheligo.com",
        avoid=[
            "pas d'emojis — utiliser des icônes dessinées",
            "pas de « Embarquez » en fin d'affiche — rester sobre",
            "ne pas écrire Chindini comme port de départ : c'est Ouroveni",
            "logo Facebook officiel uniquement, jamais un emoji",
        ],
    )
