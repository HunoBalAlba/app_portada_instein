"""
Resolución de la Ecuación de Kepler: M = E - e·sin(E).

M (anomalía media) y E (anomalía excéntrica) están en radianes.
e es la excentricidad orbital (0 ≤ e < 1).

Se usa el método de Newton-Raphson con convergencia cuadrática.
"""

from __future__ import annotations

import math

from .constantes import (
    EXCENTRICIDAD_MAXIMA,
    EXCENTRICIDAD_MINIMA,
    MAX_ITERACIONES_KEPLER,
    TOLERANCIA_KEPLER,
)


class ErrorKepler(ValueError):
    """Error en los parámetros del motor kepleriano."""


def _validar_excentricidad(excentricidad: float) -> None:
    """Valida que la excentricidad esté en rango [0, 1)."""
    if not (EXCENTRICIDAD_MINIMA <= excentricidad <= EXCENTRICIDAD_MAXIMA):
        raise ErrorKepler(
            f"Excentricidad fuera de rango [0, {EXCENTRICIDAD_MAXIMA}]: {excentricidad}"
        )


def resolver_kepler(
    anomalia_media: float,
    excentricidad: float,
    *,
    max_iteraciones: int = MAX_ITERACIONES_KEPLER,
    tolerancia: float = TOLERANCIA_KEPLER,
) -> float:
    """
    Resuelve la Ecuación de Kepler para la anomalía excéntrica E.

    Dado M (anomalía media) y e (excentricidad), encuentra E tal que:

        M = E - e · sin(E)

    Args:
        anomalia_media: Ángulo M en radianes. Puede ser cualquier real;
            internamente se normaliza al rango [-π, π] para acelerar
            la convergencia.
        excentricidad: Excentricidad orbital e ∈ [0, 0.99].
        max_iteraciones: Máximo de iteraciones de Newton-Raphson.
        tolerancia: Umbral de convergencia para |ΔE|.

    Returns:
        Anomalía excéntrica E en radianes, en el mismo rango que M.

    Raises:
        ErrorKepler: Si la excentricidad está fuera de rango.

    Examples:
        >>> resolver_kepler(0.0, 0.0)  # órbita circular
        0.0
        >>> round(resolver_kepler(math.pi, 0.5), 6)
        3.141593
    """
    _validar_excentricidad(excentricidad)

    # Órbita circular: E = M trivialmente.
    if excentricidad == 0.0:
        return anomalia_media

    # Normalización a [-π, π] para mejorar la convergencia.
    # La función M(E) = E - e·sin(E) es monótona creciente, y
    # E(M + 2πk) = E(M) + 2πk, así que basta con resolver en un periodo.
    dos_pi = 2.0 * math.pi
    k = math.floor((anomalia_media + math.pi) / dos_pi)
    M_norm = anomalia_media - k * dos_pi

    # Semilla: E ≈ M es buena para e pequeña; para e grande conviene
    # acercarse al signo de M.
    E = M_norm

    for _ in range(max_iteraciones):
        f = E - excentricidad * math.sin(E) - M_norm
        f_prima = 1.0 - excentricidad * math.cos(E)

        # Para e < 1, f_prima > 0 siempre (nunca cero). La guarda es
        # defensiva y no es alcanzable desde la API pública.
        if abs(f_prima) < tolerancia:  # pragma: no cover
            break

        delta = f / f_prima
        E -= delta

        # Convergencia por paso pequeño. Esta es la salida normal del
        # bucle para la mayoría de combinaciones (M, e).
        if abs(delta) < tolerancia:
            break

    # Desnormalizar: E(M) = E_norm(M_norm) + 2πk.
    return E + k * dos_pi


__all__ = ["ErrorKepler", "resolver_kepler"]
