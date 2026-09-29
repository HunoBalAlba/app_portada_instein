"""
Viñetas reutilizables para listas con icono (perfil, campo laboral, etc.).

Sistema de color
----------------
El color del icono se obtiene del helper `color_carrera_adaptativo()`
aplicado a la carrera seleccionada. El helper devuelve un `Var` reactivo
que cambia automáticamente entre light y dark mode según el color de
marca de la carrera activa.
"""

import reflex as rx

from app_portada_instein.dominio.estado_institucional import EstadoInstitucional
from app_portada_instein.infraestructura.constantes_visuales import (
    COLOR_TEXTO_CUERPO,
    color_carrera_adaptativo,
)


# ======================================================================
# Constantes locales
# ======================================================================

TAMANO_ICONO = 16
"""Tamaño en px de los iconos de las viñetas."""

MARGEN_TOP_ICONO = "0.125rem"
"""Alineación óptica del icono con la primera línea de texto."""


# ======================================================================
# Helper interno
# ======================================================================


def _color_actual() -> rx.Var:
    """Color principal de la carrera seleccionada, adaptado al modo."""
    return color_carrera_adaptativo(EstadoInstitucional.carrera_seleccionada)


# ======================================================================
# Viñeta de perfil profesional
# ======================================================================


def vineta_perfil_profesional(elemento: str) -> rx.Component:
    """
    Viñeta con icono de check para el perfil profesional.

    Args:
        elemento: Texto de la habilidad o competencia.
    """
    return rx.flex(
        rx.icon(
            "check",
            size=TAMANO_ICONO,
            color=_color_actual(),
            margin_top=MARGEN_TOP_ICONO,
            flex_shrink="0",
        ),
        rx.text(
            elemento,
            color=COLOR_TEXTO_CUERPO,
            line_height="1.6",
        ),
        gap="0.75rem",
        align="start",
    )


# ======================================================================
# Viñeta de campo laboral
# ======================================================================


def vineta_campo_laboral(elemento: str) -> rx.Component:
    """
    Viñeta con icono de maletín para el campo laboral.

    Args:
        elemento: Texto de la salida laboral.
    """
    return rx.flex(
        rx.icon(
            "briefcase-business",
            size=TAMANO_ICONO,
            color=_color_actual(),
            margin_top=MARGEN_TOP_ICONO,
            flex_shrink="0",
        ),
        rx.text(
            elemento,
            color=COLOR_TEXTO_CUERPO,
            line_height="1.6",
        ),
        gap="0.75rem",
        align="start",
    )


__all__ = [
    "vineta_campo_laboral",
    "vineta_perfil_profesional",
]