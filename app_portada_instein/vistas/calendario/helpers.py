"""
Helpers de color para la vista del Calendario Académico.
"""

from .datos import TIPOS_EVENTO, TIPOS_FECHA


def color_por_tipo_evento(tipo: str) -> dict:
    """
    Devuelve el color scheme del tipo de evento del instituto.

    Args:
        tipo: Clave del tipo de evento (ej: "taller", "seminario").
    """
    return TIPOS_EVENTO.get(tipo, TIPOS_EVENTO["institucional"])


def color_por_tipo_fecha(tipo: str) -> dict:
    """
    Devuelve el color scheme del tipo de fecha importante.

    Args:
        tipo: Clave del tipo de fecha (ej: "feriado_nacional").
    """
    return TIPOS_FECHA.get(tipo, TIPOS_FECHA["internacional"])


__all__ = ["color_por_tipo_evento", "color_por_tipo_fecha"]