"""Client HTTP minimal, 100 % bibliothèque standard.

Choix assumé : pas de `requests` ni `httpx`. Le prototype doit s'installer sur
un téléphone (Termux) sans chaîne de compilation, et `urllib` gère déjà les
proxys (`HTTP_PROXY` / `HTTPS_PROXY`) et le magasin de certificats
(`SSL_CERT_FILE`) via l'environnement.

Garde-fous : délai maximal, taille maximale téléchargée, refus des schémas
autres que http/https, refus des adresses locales (anti-SSRF de base).
"""

from __future__ import annotations

import gzip
import ipaddress
import json
import socket
import ssl
import time
import urllib.error
import urllib.parse
import urllib.request
import zlib
from dataclasses import dataclass

from .config import get_settings
from .errors import ToolError

#: Statuts qui méritent un réessai : limitation de débit et pannes passagères.
RETRYABLE_STATUS = frozenset({429, 500, 502, 503, 504})
#: Nombre de réessais après le premier envoi
MAX_RETRIES = 2
#: Retrait progressif : 1 s, puis 2 s (plafonné)
BACKOFF_BASE = 1.0
MAX_BACKOFF = 8.0


@dataclass
class HttpResponse:
    url: str
    status: int
    body: bytes
    content_type: str = ""
    truncated: bool = False

    def text(self) -> str:
        charset = "utf-8"
        if "charset=" in self.content_type:
            charset = self.content_type.split("charset=", 1)[1].split(";")[0].strip() or "utf-8"
        try:
            return self.body.decode(charset, errors="replace")
        except LookupError:
            return self.body.decode("utf-8", errors="replace")


def _is_private_host(host: str) -> bool:
    """Bloque localhost et les plages privées (garde-fou SSRF)."""
    host = host.strip("[]").lower()
    if host in {"localhost", ""} or host.endswith(".local") or host.endswith(".internal"):
        return True
    try:
        infos = socket.getaddrinfo(host, None)
    except (socket.gaierror, UnicodeError):
        # Nom non résolu : on laisse la requête échouer plus loin.
        return False
    for info in infos:
        address = info[4][0]
        try:
            ip = ipaddress.ip_address(address)
        except ValueError:
            continue
        if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved:
            return True
    return False


def _decode_body(raw: bytes, encoding: str) -> bytes:
    encoding = (encoding or "").lower()
    try:
        if encoding == "gzip":
            return gzip.decompress(raw)
        if encoding == "deflate":
            return zlib.decompress(raw, -zlib.MAX_WBITS)
    except (OSError, zlib.error):
        return raw
    return raw


def request(
    url: str,
    *,
    method: str = "GET",
    data: dict[str, str] | None = None,
    json_body: dict | None = None,
    headers: dict[str, str] | None = None,
    timeout: int | None = None,
    max_bytes: int | None = None,
    allow_private: bool = False,
) -> HttpResponse:
    """Exécute une requête HTTP(S) avec garde-fous.

    Lève :class:`ToolError` sur toute erreur réseau — jamais d'exception brute
    remontant jusqu'à l'interface.
    """
    settings = get_settings()
    timeout = timeout or settings.http_timeout
    max_bytes = max_bytes or settings.http_max_bytes

    parsed = urllib.parse.urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        raise ToolError(f"Schéma d'URL non autorisé : {parsed.scheme or '(vide)'}")
    if not parsed.netloc:
        raise ToolError(f"URL invalide : {url}")
    if not allow_private and _is_private_host(parsed.hostname or ""):
        raise ToolError(f"Adresse locale ou privée refusée : {parsed.hostname}")

    if json_body is not None:
        body: bytes | None = json.dumps(json_body).encode("utf-8")
    elif data:
        body = urllib.parse.urlencode(data).encode()
    else:
        body = None

    final_headers = {
        "User-Agent": settings.user_agent,
        "Accept": "text/html,application/xhtml+xml,application/json;q=0.9,*/*;q=0.8",
        "Accept-Language": "fr-FR,fr;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate",
    }
    if json_body is not None:
        final_headers["Content-Type"] = "application/json"
    final_headers.update(headers or {})

    req = urllib.request.Request(url, data=body, headers=final_headers, method=method)
    context = ssl.create_default_context()
    last: ToolError | None = None

    for attempt in range(MAX_RETRIES + 1):
        try:
            with urllib.request.urlopen(req, timeout=timeout, context=context) as response:
                raw = response.read(max_bytes + 1)
                truncated = len(raw) > max_bytes
                raw = raw[:max_bytes]
                raw = _decode_body(raw, response.headers.get("Content-Encoding", ""))
                return HttpResponse(
                    url=response.geturl(),
                    status=response.status,
                    body=raw,
                    content_type=response.headers.get("Content-Type", ""),
                    truncated=truncated,
                )
        except urllib.error.HTTPError as exc:
            last = ToolError(f"HTTP {exc.code} sur {url}")
            if exc.code not in RETRYABLE_STATUS:
                raise last from exc
            delay = _retry_after(exc) or BACKOFF_BASE * (2**attempt)
        except urllib.error.URLError as exc:
            # `URLError` couvre aussi les coupures de connexion transitoires.
            last = ToolError(f"Réseau indisponible pour {url} : {exc.reason}")
            delay = BACKOFF_BASE * (2**attempt)
        except (TimeoutError, socket.timeout) as exc:
            raise ToolError(f"Délai dépassé ({timeout}s) sur {url}") from exc
        except ssl.SSLError as exc:
            raise ToolError(f"Erreur TLS sur {url} : {exc}") from exc

        if attempt == MAX_RETRIES:
            break
        time.sleep(min(delay, MAX_BACKOFF))

    raise last or ToolError(f"Échec de la requête vers {url}")


def _retry_after(exc: urllib.error.HTTPError) -> float:
    """Respecte l'en-tête `Retry-After` du serveur quand il en fournit un."""
    raw = exc.headers.get("Retry-After") if exc.headers else None
    try:
        return max(0.0, float(raw)) if raw else 0.0
    except (TypeError, ValueError):
        return 0.0


def get(url: str, **kwargs) -> HttpResponse:
    return request(url, method="GET", **kwargs)


def post(url: str, data: dict[str, str], **kwargs) -> HttpResponse:
    kwargs.setdefault("headers", {})["Content-Type"] = "application/x-www-form-urlencoded"
    return request(url, method="POST", data=data, **kwargs)


def post_json(url: str, payload: dict, **kwargs) -> dict:
    """POST JSON, retourne le JSON décodé."""
    response = request(url, method="POST", json_body=payload, **kwargs)
    try:
        return json.loads(response.text())
    except json.JSONDecodeError as exc:
        raise ToolError(f"Réponse non-JSON depuis {url}") from exc
