"""
Meta info del post: autor · fecha · minutos de lectura.
"""

import reflex as rx

from app_portada_instein.infraestructura.constantes_visuales import (
    COLOR_TEXTO_SECUNDARIO,
)


def meta_info_post(post) -> rx.Component:
    """
    Meta info: autor · fecha · minutos de lectura.

    Args:
        post: Dict del post (puede ser estático o Var).
    """
    return rx.flex(
        rx.icon("user", size=12, color=COLOR_TEXTO_SECUNDARIO),
        rx.text(
            post["autor"],
            font_size="0.75rem",
            color=COLOR_TEXTO_SECUNDARIO,
        ),
        rx.text("·", font_size="0.75rem", color=COLOR_TEXTO_SECUNDARIO),
        rx.icon("calendar", size=12, color=COLOR_TEXTO_SECUNDARIO),
        rx.text(
            post["fecha"],
            font_size="0.75rem",
            color=COLOR_TEXTO_SECUNDARIO,
        ),
        rx.text("·", font_size="0.75rem", color=COLOR_TEXTO_SECUNDARIO),
        rx.icon("clock", size=12, color=COLOR_TEXTO_SECUNDARIO),
        rx.text(
            f"{post['minutos_lectura']} min",
            font_size="0.75rem",
            color=COLOR_TEXTO_SECUNDARIO,
        ),
        align="center",
        gap="0.375rem",
        flex_wrap="wrap",
    )


__all__ = ["meta_info_post"]