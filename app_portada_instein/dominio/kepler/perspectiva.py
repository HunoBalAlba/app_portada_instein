"""
Transformación de la órbita 2D a una vista 3D con perspectiva y rotación.

Dos operaciones independientes:
1. Aplanamiento vertical (`factor_perspectiva`): simula ver el disco
   orbital de lado.
2. Rotación en el plano (`angulo_inicial`): orienta la elipse.
"""

from __future__ import annotations

import math
from typing import NamedTuple


class CoordenadaPerspectiva(NamedTuple):
    """Coordenada (x, y) tras aplicar perspectiva y rotación.

    Attributes:
        x: Coordenada horizontal final.
        y: Coordenada vertical final.
        y_perspectiva: Coordenada Y tras aplanar, antes de rotar.
            Útil para calcular escala y opacidad (el "alejamiento").
    """

    x: float
    y: float
    y_perspectiva: float


def aplicar_perspectiva_y_rotacion(
    x_elipse: float,
    y_elipse: float,
    factor_perspectiva: float,
    angulo_inicial_grados: float,
) -> CoordenadaPerspectiva:
    """
    Aplica aplanamiento vertical y rotación 2D a una posición orbital.

    Pasos:
    1. Aplanar Y: y_plano = y · factor_perspectiva
    2. Rotar el vector (x, y_plano) por `angulo_inicial_grados`.

    Args:
        x_elipse: Coordenada X sin transformar.
        y_elipse: Coordenada Y sin transformar.
        factor_perspectiva: Factor de aplanamiento vertical ∈ (0, 1].
            1.0 = vista cenital (círculo), 0.5 = disco de lado.
        angulo_inicial_grados: Ángulo de rotación en grados.

    Returns:
        CoordenadaPerspectiva con la posición final y la Y intermedia.

    Examples:
        >>> c = aplicar_perspectiva_y_rotacion(1.0, 0.0, 0.5, 0.0)
        >>> round(c.x, 6), round(c.y, 6)
        (1.0, 0.0)
    """
    if not (0.0 < factor_perspectiva <= 1.0):
        raise ValueError(f"factor_perspectiva debe estar en (0, 1]: {factor_perspectiva}")

    y_plano = y_elipse * factor_perspectiva
    rad = math.radians(angulo_inicial_grados)
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)

    x_rot = x_elipse * cos_a - y_plano * sin_a
    y_rot = x_elipse * sin_a + y_plano * cos_a

    return CoordenadaPerspectiva(x=x_rot, y=y_rot, y_perspectiva=y_plano)


def convertir_a_rem(valor_pct: float, factor_conversion: float) -> float:
    """
    Convierte un valor en porcentaje a rem.

    Args:
        valor_pct: Valor en porcentaje del contenedor.
        factor_conversion: Factor de conversión (rem por unidad de %).

    Returns:
        Valor en rem.
    """
    return valor_pct * factor_conversion


__all__ = [
    "CoordenadaPerspectiva",
    "aplicar_perspectiva_y_rotacion",
    "convertir_a_rem",
]
