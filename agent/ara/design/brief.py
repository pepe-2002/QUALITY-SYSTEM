"""Le brief marketing : ce que l'agent créatif reçoit (spec §5).

    Brief marketing
       ↓
    Recherche du marché
       ↓
    Analyse des concurrents
       ↓
    Création de 3 concepts
       ↓
    Critique automatique
       ↓
    Amélioration
       ↓
    Version finale

Ce module ne couvre que la première marche : transformer une phrase du type
« fais-moi un flyer premium pour la traversée Ouroveni → Hoani à 15 000 FC »
en un brief exploitable, complété par la mémoire de marque.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from .brand import BrandProfile

#: Formats courants, en pixels
FORMATS = {
    "flyer": (2160, 2700),      # 4:5, impression et réseaux
    "affiche": (2480, 3508),    # A4 à 300 dpi
    "carre": (2160, 2160),      # feed
    "story": (1080, 1920),      # statuts et stories
    "banniere": (2400, 1260),   # couverture
}

_URL = re.compile(r"https?://\S+")
_PRICE = re.compile(
    r"(\d{1,3}(?:[\s   .]\d{3})*|\d+)\s*(FC|KMF|francs?\s+comoriens?|€|euros?|\$)",
    re.IGNORECASE,
)
_PHONE = re.compile(r"(?:\+\d{1,3}[\s.-]?)?(?:\d[\s.-]?){7,}\d")

_AUDIENCES = {
    "touriste": {"touriste", "touristes", "voyageur", "voyageurs", "vacancier", "visiteur"},
    "famille": {"famille", "familles", "enfant", "enfants", "parents"},
    "professionnel": {"professionnel", "entreprise", "affaires", "business", "pro"},
    "local": {"local", "locaux", "habitant", "habitants", "residents", "diaspora"},
}

_OBJECTIFS = {
    "notoriete": {"notoriete", "connaitre", "faire connaitre", "visibilite", "lancement"},
    "conversion": {"reserver", "reservation", "vendre", "vente", "acheter", "inscription"},
    "trafic": {"visiter", "site", "trafic", "telecharger", "application"},
    "fidelisation": {"fidelite", "fideliser", "revenir", "abonnes"},
}


@dataclass
class Brief:
    """Tout ce qu'il faut savoir avant de dessiner."""

    subject: str = ""
    title: str = ""
    subtitle: str = ""
    bullets: list[str] = field(default_factory=list)
    price: str = ""
    contact: str = ""
    url: str = ""
    logo: str = ""
    images: list[str] = field(default_factory=list)
    audience: str = "grand public"
    objective: str = "notoriete"
    format: str = "flyer"
    width: int = 2160
    height: int = 2700
    brand: BrandProfile = field(default_factory=BrandProfile)
    #: enseignements tirés de la recherche marché (phase 2)
    market: list[str] = field(default_factory=list)
    competitors: list[str] = field(default_factory=list)

    @property
    def has_qr(self) -> bool:
        return bool(self.url)

    def to_dict(self) -> dict:
        return {
            "subject": self.subject, "title": self.title, "subtitle": self.subtitle,
            "bullets": self.bullets, "price": self.price, "contact": self.contact,
            "url": self.url, "audience": self.audience, "objective": self.objective,
            "format": self.format, "size": [self.width, self.height],
            "brand": self.brand.name, "market": self.market,
            "competitors": self.competitors,
        }


def _normalize(text: str) -> str:
    import unicodedata

    text = unicodedata.normalize("NFKD", text.lower())
    return "".join(ch for ch in text if not unicodedata.combining(ch))


def detect_format(prompt: str) -> str:
    text = _normalize(prompt)
    for name in ("story", "banniere", "affiche", "carre"):
        if name in text:
            return name
    return "flyer"


def from_prompt(prompt: str, brand: BrandProfile | None = None) -> Brief:
    """Construit un brief depuis la demande, complété par la mémoire de marque.

    >>> b = from_prompt("Fais un flyer pour la traversée à 15 000 FC — https://moheligo.com")
    >>> b.price, b.url
    ('15 000 FC', 'https://moheligo.com')
    """
    brand = brand or BrandProfile.load()
    text = _normalize(prompt)

    urls = _URL.findall(prompt)
    price_match = _PRICE.search(prompt)
    fmt = detect_format(prompt)
    width, height = FORMATS[fmt]
    if brand.dimensions and fmt == "flyer":
        width, height = brand.dimensions[0], brand.dimensions[1]

    audience = "grand public"
    for name, words in _AUDIENCES.items():
        if any(word in text for word in words):
            audience = name
            break

    objective = "notoriete"
    for name, words in _OBJECTIFS.items():
        if any(word in text for word in words):
            objective = name
            break

    # Le sujet : la demande débarrassée des consignes de fabrication.
    # On réutilise le nettoyage des requêtes de recherche, pour ne pas tenir
    # deux listes de mots à retirer qui finiraient par diverger.
    from ..providers.llm.offline import subject as _subject

    subject = " ".join(_subject(_URL.sub("", prompt)).split()).strip(" ,.;:—-")

    return Brief(
        subject=subject or prompt.strip(),
        title="",
        price=price_match.group(0).strip() if price_match else "",
        contact=brand.contact,
        url=urls[0] if urls else brand.website,
        logo=brand.logo,
        audience=audience,
        objective=objective,
        format=fmt,
        width=width,
        height=height,
        brand=brand,
    )
