# app_portada_instein/componentes/vinetas.py

"""
Viñetas reutilizables para listas con icono — estilo Neon dark.

Se usan en las secciones de "Perfil profesional" y "Campo laboral"
del detalle de carrera.

Sistema de color (UX)
---------------------
✅ REFACTORIZADO: TODAS las viñetas usan azul marino neon
   (`AZUL_MARINO_NEON` = `#3b5bdb`). Ya no dependen del color de la
   carrera seleccionada porque el home es dark con un único acento.

- Iconos: azul marino neon.
- Texto: blanco suave (`TEXTO_OSCURO_SUAVE`).
"""

import reflex as rx

from app_portada_instein.dominio.estado_institucional import EstadoInstitucional  # noqa: F401
from app_portada_instein.infraestructura.constantes_visuales import (
    AZUL_MARINO_NEON,
    TEXTO_OSCURO_SUAVE,
)


# ======================================================================
# Constantes locales
# ======================================================================

TAMANO_ICONO = 16
"""Tamaño en px de los iconos de las viñetas."""

MARGEN_TOP_ICONO = "0.125rem"
"""Alineación óptica del icono con la primera línea de texto."""

COLOR_ICONO = AZUL_MARINO_NEON
"""Color único de los iconos (azul marino neon)."""


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
            color=COLOR_ICONO,
            margin_top=MARGEN_TOP_ICONO,
            flex_shrink="0",
        ),
        rx.text(
            elemento,
            color=TEXTO_OSCURO_SUAVE,
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
            color=COLOR_ICONO,
            margin_top=MARGEN_TOP_ICONO,
            flex_shrink="0",
        ),
        rx.text(
            elemento,
            color=TEXTO_OSCURO_SUAVE,
            line_height="1.6",
        ),
        gap="0.75rem",
        align="start",
    )






__all__ = [
    "vineta_campo_laboral",
    "vineta_perfil_profesional",
]