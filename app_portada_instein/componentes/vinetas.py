"""
Viñetas reutilizables para listas con icono (perfil, campo laboral, etc.).
"""

import reflex as rx

from ..dominio.estado_institucional import EstadoInstitucional


def vineta_perfil_profesional(elemento: str) -> rx.Component:
    """Viñeta con icono de check para el perfil profesional."""
    return rx.flex(
        rx.icon(
            "check",
            size=16,
            color=EstadoInstitucional.carrera_seleccionada["color_principal"],
            margin_top="0.125rem",
            flex_shrink="0",
        ),
        rx.text(elemento),
        gap="0.75rem",
        align="start",
    )


def vineta_campo_laboral(elemento: str) -> rx.Component:
    """Viñeta con icono de maletín para el campo laboral."""
    return rx.flex(
        rx.icon(
            "briefcase-business",
            size=16,
            color=EstadoInstitucional.carrera_seleccionada["color_principal"],
            margin_top="0.125rem",
            flex_shrink="0",
        ),
        rx.text(elemento),
        gap="0.75rem",
        align="start",
    )