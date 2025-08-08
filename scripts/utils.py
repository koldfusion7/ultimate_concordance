"""Shared utility functions for the Concordance Project."""

import unicodedata
from typing import Dict


def normalize(text: str) -> str:
    """Normalize a string to Unicode NFC and strip whitespace."""
    return unicodedata.normalize("NFC", text or "").strip()


def gematria(value: str, method: str = "standard") -> int:
    """Compute the gematria value of a Hebrew word.

    Supported methods: 'standard', 'ordinal', 'reduced', 'atbash'.  The
    implementation here is a stub; you will need to implement the actual
    numerical mappings according to the chosen method.
    """
    # TODO: Implement gematria calculations
    raise NotImplementedError("Gematria calculation is not yet implemented")
