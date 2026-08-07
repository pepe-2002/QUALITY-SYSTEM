"""Moteurs de recherche interchangeables."""

from .base import SearchProvider
from .registry import available_engines, get_search

__all__ = ["SearchProvider", "get_search", "available_engines"]
