"""
Helpers para resolver la categoría de un post.

Como `clave` puede ser un Var reactivo (dentro de `rx.foreach`), NO
podemos hacer lookups de Python. Usamos `rx.match` para resolver los
valores en el cliente.
"""

import reflex as rx

from app_portada_instein.infraestructura.constantes_visuales import (
    COLOR_BORDE_SUAVE,
    COLOR_FONDO_SUAVE,
    RADIO_PASTILLA,
)


# ======================================================================
# Helpers de UI: categoría → color/icono
# ======================================================================


def badge_categoria(clave) -> rx.Component:
    """
    Badge con el nombre de la categoría.

    Acepta un `str` estático O un `Var` reactivo.
    """
    return rx.match(
        clave,
        ("tecnologia", _badge_ui("blue", "cpu", "Tecnología")),
        ("contaduria", _badge_ui("violet", "calculator", "Contaduría")),
        ("empleabilidad", _badge_ui("green", "trending-up", "Empleabilidad")),
        ("institucional", _badge_ui("crimson", "landmark", "Institucional")),
        ("estudiantes", _badge_ui("orange", "graduation-cap", "Estudiantes")),
        ("tutoriales", _badge_ui("cyan", "book-open", "Tutoriales")),
        _badge_ui("gray", "list", "Todas"),
    )


def _badge_ui(color: str, icono: str, etiqueta: str) -> rx.Component:
    """Construye el componente del badge con valores fijos."""
    return rx.flex(
        rx.icon(icono, size=12, color=rx.color(color, 11)),
        rx.text(
            etiqueta,
            font_size="0.6875rem",
            font_weight="700",
            color=rx.color(color, 11),
            text_transform="uppercase",
            letter_spacing="0.05em",
        ),
        align="center",
        gap="0.25rem",
        padding="0.25rem 0.625rem",
        border_radius=RADIO_PASTILLA,
        background=rx.color(color, 3),
        border=f"1px solid {rx.color(color, 7)}",
        width="fit-content",
    )


def icono_categoria(clave) -> rx.Component:
    """Icono grande de la categoría (placeholder de imagen)."""
    return rx.match(
        clave,
        ("tecnologia", rx.icon("cpu", size=40, color=rx.color("blue", 11))),
        ("contaduria", rx.icon("calculator", size=40, color=rx.color("violet", 11))),
        ("empleabilidad", rx.icon("trending-up", size=40, color=rx.color("green", 11))),
        ("institucional", rx.icon("landmark", size=40, color=rx.color("crimson", 11))),
        ("estudiantes", rx.icon("graduation-cap", size=40, color=rx.color("orange", 11))),
        ("tutoriales", rx.icon("book-open", size=40, color=rx.color("cyan", 11))),
        rx.icon("list", size=40, color=rx.color("gray", 11)),
    )


def fondo_categoria(clave) -> rx.Var:
    """Fondo suave del placeholder de imagen."""
    return rx.match(
        clave,
        ("tecnologia", rx.color("blue", 3)),
        ("contaduria", rx.color("violet", 3)),
        ("empleabilidad", rx.color("green", 3)),
        ("institucional", rx.color("crimson", 3)),
        ("estudiantes", rx.color("orange", 3)),
        ("tutoriales", rx.color("cyan", 3)),
        COLOR_FONDO_SUAVE,
    )


def borde_categoria(clave) -> rx.Var:
    """Borde del placeholder de imagen."""
    return rx.match(
        clave,
        ("tecnologia", f"1px solid {rx.color('blue', 7)}"),
        ("contaduria", f"1px solid {rx.color('violet', 7)}"),
        ("empleabilidad", f"1px solid {rx.color('green', 7)}"),
        ("institucional", f"1px solid {rx.color('crimson', 7)}"),
        ("estudiantes", f"1px solid {rx.color('orange', 7)}"),
        ("tutoriales", f"1px solid {rx.color('cyan', 7)}"),
        f"1px solid {COLOR_BORDE_SUAVE}",
    )


__all__ = [
    "badge_categoria",
    "borde_categoria",
    "fondo_categoria",
    "icono_categoria",
]