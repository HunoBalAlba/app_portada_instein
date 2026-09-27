"""
Generador de keyframes CSS para órbitas keplerianas.

Produce un diccionario compatible con la API de Reflex (`style=`),
donde cada clave es `@keyframes nombre` y el valor es un dict de
pasos (porcentaje → propiedades CSS).
"""

from __future__ import annotations

import math
from typing import TypedDict

from .constantes import (
    ESCALA_BASE,
    ESCALA_MAXIMA,
    ESCALA_MINIMA,
    ESCALA_VARIACION,
    FACTOR_CONVERSION_REM,
    NUM_PASOS_KEYFRAMES,
    OPACIDAD_BASE,
    OPACIDAD_MAXIMA,
    OPACIDAD_MINIMA,
    OPACIDAD_VARIACION,
)
from .perspectiva import aplicar_perspectiva_y_rotacion
from .posicion import calcular_posicion_orbital


class KeyframeStep(TypedDict, total=False):
    """Propiedades CSS de un paso de keyframe."""

    transform: str
    opacity: str


class DefinicionKeyframe(TypedDict):
    """Definición completa de un keyframe."""

    nombre: str
    pasos: dict[str, KeyframeStep]


def _calcular_escala_opacidad(
    y_perspectiva: float,
    semieje_mayor: float,
) -> tuple[float, float]:
    """
    Calcula escala y opacidad de un icono según su "alejamiento" vertical.

    Los iconos que están más "arriba" en la perspectiva (y negativa)
    se ven más pequeños y transparentes, simulando profundidad.

    Args:
        y_perspectiva: Coordenada Y tras el aplanamiento (con signo).
        semieje_mayor: Semieje mayor de la órbita (a). Debe ser > 0;
            la validación se hace en `generar_pasos_orbita` antes de
            llamar a esta función.

    Returns:
        Tupla (escala, opacidad) ya recortadas a sus límites.
    """
    # Guarda defensiva: `generar_pasos_orbita` ya valida semieje_mayor > 0,
    # pero la mantenemos por seguridad si esta función se usa aislada.
    if semieje_mayor <= 0:  # pragma: no cover
        raise ValueError(f"semieje_mayor debe ser > 0: {semieje_mayor}")

    # Normalizamos Y al rango [-1, 1] dividiendo por el semieje mayor.
    y_norm = y_perspectiva / semieje_mayor

    escala = ESCALA_BASE + y_norm * ESCALA_VARIACION
    opacidad = OPACIDAD_BASE + y_norm * OPACIDAD_VARIACION

    escala = max(ESCALA_MINIMA, min(ESCALA_MAXIMA, escala))
    opacidad = max(OPACIDAD_MINIMA, min(OPACIDAD_MAXIMA, opacidad))

    return escala, opacidad


def generar_pasos_orbita(
    semieje_mayor: float,
    excentricidad: float,
    factor_perspectiva: float,
    angulo_inicial_grados: float,
    *,
    num_pasos: int = NUM_PASOS_KEYFRAMES,
    factor_conversion_rem: float = FACTOR_CONVERSION_REM,
) -> dict[str, KeyframeStep]:
    """
    Genera los pasos (0% … 100%) de una órbita kepleriana.

    Para cada fracción f ∈ [0, 1]:
        M = 2π · f
        (x, y) = posición orbital
        (x', y') = perspectiva + rotación
        transform = translate(-50%,-50%) translate(x'rem, y'rem) scale(s)

    Args:
        semieje_mayor: Semieje mayor en % del contenedor.
        excentricidad: Excentricidad orbital e ∈ [0, 0.99].
        factor_perspectiva: Aplanamiento vertical ∈ (0, 1].
        angulo_inicial_grados: Orientación de la elipse en grados.
        num_pasos: Número de pasos (por defecto 60).
        factor_conversion_rem: Factor % → rem.

    Returns:
        Dict con claves "0%", "1%", …, "100%" y valores KeyframeStep.

    Raises:
        ValueError: Si num_pasos < 2 o semieje_mayor <= 0.
    """
    if num_pasos < 2:
        raise ValueError(f"num_pasos debe ser >= 2: {num_pasos}")

    if semieje_mayor <= 0:
        raise ValueError(f"semieje_mayor debe ser > 0: {semieje_mayor}")

    pasos: dict[str, KeyframeStep] = {}

    for i in range(num_pasos + 1):
        fraccion = i / num_pasos
        M = 2.0 * math.pi * fraccion

        pos = calcular_posicion_orbital(M, semieje_mayor, excentricidad)
        coord = aplicar_perspectiva_y_rotacion(
            pos.x, pos.y, factor_perspectiva, angulo_inicial_grados
        )

        x_rem = coord.x * factor_conversion_rem
        y_rem = coord.y * factor_conversion_rem

        escala, opacidad = _calcular_escala_opacidad(coord.y_perspectiva, semieje_mayor)

        pasos[f"{int(fraccion * 100)}%"] = {
            "transform": (
                f"translate(-50%, -50%) "
                f"translate({x_rem:.3f}rem, {y_rem:.3f}rem) "
                f"scale({escala:.2f})"
            ),
            "opacity": f"{opacidad:.2f}",
        }

    return pasos


def generar_keyframes_css(
    definiciones: list[DefinicionKeyframe],
) -> dict[str, dict[str, KeyframeStep]]:
    """
    Genera el diccionario completo de `@keyframes` para Reflex.

    Args:
        definiciones: Lista de DefinicionKeyframe con `nombre` y `pasos`.

    Returns:
        Dict con claves `@keyframes <nombre>` y valores de pasos.

    Examples:
        >>> defs = [{"nombre": "orbita_0_55", "pasos": {"0%": {...}}}]
        >>> generar_keyframes_css(defs)
        {'@keyframes orbita_0_55': {'0%': {...}}}
    """
    return {f"@keyframes {d['nombre']}": d["pasos"] for d in definiciones}


__all__ = [
    "DefinicionKeyframe",
    "KeyframeStep",
    "generar_keyframes_css",
    "generar_pasos_orbita",
]
