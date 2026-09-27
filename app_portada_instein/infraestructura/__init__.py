"""
Capa de infraestructura.

Agrupa constantes visuales, textos institucionales y utilidades
transversales que no pertenecen a ninguna capa específica.
"""

from .constantes_visuales import (
    NOMBRE_INSTITUTO,
    NOMBRE_COMPLETO_INSTITUTO,
    TELEFONO_PRINCIPAL,
    TELEFONO_SECUNDARIO,
    WHATSAPP_URL,
    DIRECCION,
    UBICACION_FISICA,
    HORARIO_ATENCION,
    SOMBRA_SUAVE,
    SOMBRA_MEDIA,
    SOMBRA_FUERTE,
    RADIO_PEQUENO,
    RADIO_MEDIO,
    RADIO_GRANDE,
    RADIO_EXTRA_GRANDE,
    RADIO_PASTILLA,
)
from .utilidades_color import invertir_color_hexadecimal

__all__ = [
    "NOMBRE_INSTITUTO",
    "NOMBRE_COMPLETO_INSTITUTO",
    "TELEFONO_PRINCIPAL",
    "TELEFONO_SECUNDARIO",
    "WHATSAPP_URL",
    "DIRECCION",
    "UBICACION_FISICA",
    "HORARIO_ATENCION",
    "SOMBRA_SUAVE",
    "SOMBRA_MEDIA",
    "SOMBRA_FUERTE",
    "RADIO_PEQUENO",
    "RADIO_MEDIO",
    "RADIO_GRANDE",
    "RADIO_EXTRA_GRANDE",
    "RADIO_PASTILLA",
    "invertir_color_hexadecimal",
]