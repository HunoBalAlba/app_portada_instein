"""
Capa de infraestructura.

Agrupa constantes visuales, textos institucionales y utilidades
transversales que no pertenecen a ninguna capa específica.
"""

from .constantes_visuales import (
    DIRECCION,
    HORARIO_ATENCION,
    NOMBRE_COMPLETO_INSTITUTO,
    NOMBRE_INSTITUTO,
    RADIO_EXTRA_GRANDE,
    RADIO_GRANDE,
    RADIO_MEDIO,
    RADIO_PASTILLA,
    RADIO_PEQUENO,
    SOMBRA_FUERTE,
    SOMBRA_MEDIA,
    SOMBRA_SUAVE,
    TELEFONO_PRINCIPAL,
    TELEFONO_SECUNDARIO,
    UBICACION_FISICA,
    WHATSAPP_URL,
)
from .utilidades_color import invertir_color_hexadecimal


__all__ = [
    "DIRECCION",
    "HORARIO_ATENCION",
    "NOMBRE_COMPLETO_INSTITUTO",
    "NOMBRE_INSTITUTO",
    "RADIO_EXTRA_GRANDE",
    "RADIO_GRANDE",
    "RADIO_MEDIO",
    "RADIO_PASTILLA",
    "RADIO_PEQUENO",
    "SOMBRA_FUERTE",
    "SOMBRA_MEDIA",
    "SOMBRA_SUAVE",
    "TELEFONO_PRINCIPAL",
    "TELEFONO_SECUNDARIO",
    "UBICACION_FISICA",
    "WHATSAPP_URL",
    "invertir_color_hexadecimal",
    "color_carrera_adaptativo",
    "color_suave_carrera_adaptativo",
]
