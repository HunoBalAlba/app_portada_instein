"""Helpers compartidos entre tests del motor kepleriano."""

from __future__ import annotations

import re

_PATRON_SCALE = re.compile(r"scale\(([\d.]+)\)")
_PATRON_TRANSLATE = re.compile(
    r"translate\(([-\d.]+)rem,\s*([-\d.]+)rem\)"
)


def extraer_scale(transform: str) -> float:
    """Extrae el valor de `scale(s)` en un transform CSS."""
    match = _PATRON_SCALE.search(transform)
    if match is None:
        raise AssertionError(f"No se encontró scale en: {transform!r}")
    return float(match.group(1))


def extraer_translate(transform: str) -> tuple[float, float]:
    """Extrae los valores (x, y) de `translate(xrem, yrem)`."""
    match = _PATRON_TRANSLATE.search(transform)
    if match is None:
        raise AssertionError(f"No se encontró translate en: {transform!r}")
    return float(match.group(1)), float(match.group(2))


def normalizar_transform(transform: str) -> str:
    """Normaliza `-0.000rem` → `0.000rem` y colapsa espacios."""
    normalizado = transform.replace("-0.000", "0.000")
    return re.sub(r"\s+", " ", normalizado).strip()


__all__ = ["extraer_scale", "extraer_translate", "normalizar_transform"]