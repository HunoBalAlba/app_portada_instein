"""
Constantes físicas y de conversión del motor kepleriano.

Todas las constantes están en unidades adimensionales (porcentaje del
contenedor) excepto donde se indique lo contrario.
"""

from __future__ import annotations

from typing import Final

# ======================================================================
# Conversión de porcentaje a rem
# ======================================================================

ANCHO_CONTENEDOR_REM: Final[float] = 32.0
"""Ancho del contenedor orbital en rem.

Se usa para convertir los porcentajes de las órbitas (0–100) a
desplazamientos CSS en rem.
"""

FACTOR_CONVERSION_REM: Final[float] = ANCHO_CONTENEDOR_REM / 100.0
"""Factor para convertir un porcentaje de la órbita a rem.

Ejemplo: 50 (% del contenedor) → 50 * 0.32 = 16 rem.
"""

# ======================================================================
# Parámetros de la resolución numérica
# ======================================================================

MAX_ITERACIONES_KEPLER: Final[int] = 8
"""Iteraciones máximas del método de Newton-Raphson.

Con 8 iteraciones se alcanza precisión de máquina para
excentricidades típicas (e < 0.5).
"""

TOLERANCIA_KEPLER: Final[float] = 1e-10
"""Umbral de convergencia para |f'(E)|. Si es menor, se detiene."""

# ======================================================================
# Parámetros del generador de keyframes
# ======================================================================

NUM_PASOS_KEYFRAMES: Final[int] = 60
"""Número de keyframes por órbita (0% a 100%).

Un valor más alto da más suavidad pero produce más CSS.
"""

ESCALA_BASE: Final[float] = 0.85
"""Escala mínima de un icono en el punto más lejano."""

ESCALA_VARIACION: Final[float] = 0.35
"""Variación de escala entre el punto más lejano y el más cercano."""

ESCALA_MINIMA: Final[float] = 0.55
"""Límite inferior de la escala tras aplicar el factor 3D."""

ESCALA_MAXIMA: Final[float] = 1.2
"""Límite superior de la escala tras aplicar el factor 3D."""

OPACIDAD_BASE: Final[float] = 0.65
"""Opacidad mínima de un icono en el punto más lejano."""

OPACIDAD_VARIACION: Final[float] = 0.35
"""Variación de opacidad entre el punto más lejano y el más cercano."""

OPACIDAD_MINIMA: Final[float] = 0.45
"""Límite inferior de opacidad."""

OPACIDAD_MAXIMA: Final[float] = 1.0
"""Límite superior de opacidad."""

# ======================================================================
# Validaciones
# ======================================================================

EXCENTRICIDAD_MINIMA: Final[float] = 0.0
"""Excentricidad mínima válida (círculo perfecto)."""

EXCENTRICIDAD_MAXIMA: Final[float] = 0.99
"""Excentricidad máxima válida (elipse muy alargada).

En e = 1 la órbita es parabólica y la fórmula falla.
"""


__all__ = [
    "ANCHO_CONTENEDOR_REM",
    "FACTOR_CONVERSION_REM",
    "MAX_ITERACIONES_KEPLER",
    "TOLERANCIA_KEPLER",
    "NUM_PASOS_KEYFRAMES",
    "ESCALA_BASE",
    "ESCALA_VARIACION",
    "ESCALA_MINIMA",
    "ESCALA_MAXIMA",
    "OPACIDAD_BASE",
    "OPACIDAD_VARIACION",
    "OPACIDAD_MINIMA",
    "OPACIDAD_MAXIMA",
    "EXCENTRICIDAD_MINIMA",
    "EXCENTRICIDAD_MAXIMA",
]