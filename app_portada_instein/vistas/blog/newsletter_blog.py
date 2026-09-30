"""
Bloque de newsletter inline al pie del blog.
"""

import reflex as rx

from app_portada_instein.infraestructura.constantes_visuales import (
    COLOR_ACENTO_FONDO,
    COLOR_ACENTO_TEXTO,
    COLOR_TEXTO_CUERPO,
    COLOR_TEXTO_PRINCIPAL,
    COLOR_TEXTO_SECUNDARIO,
    RADIO_EXTRA_GRANDE,
)


def newsletter_blog() -> rx.Component:
    """Bloque de newsletter inline al pie del blog."""
    return rx.box(
        rx.vstack(
            rx.icon("mail", size=32, color=COLOR_ACENTO_TEXTO),
            rx.heading(
                "Recibe los nuevos artículos",
                size="5",
                font_weight="800",
                color=COLOR_TEXTO_PRINCIPAL,
                text_align="center",
            ),
            rx.text(
                "Suscríbete a nuestro newsletter y recibe las novedades "
                "del blog directamente en tu correo.",
                font_size="0.875rem",
                color=COLOR_TEXTO_SECUNDARIO,
                text_align="center",
                max_width="32rem",
                line_height="1.6",
            ),
            rx.flex(
                rx.input(
                    placeholder="tu@email.com",
                    type="email",
                    size="3",
                    width="100%",
                    flex="1",
                    min_width="0",
                ),
                rx.button(
                    rx.icon("send", size=16),
                    rx.text("Suscribirme", as_="span", font_weight="700"),
                    size="3",
                    variant="solid",
                    color_scheme="crimson",
                    cursor="pointer",
                    flex_shrink="0",
                ),
                gap="0.5rem",
                width="100%",
                max_width="32rem",
                align="center",
                flex_direction=rx.breakpoints(initial="column", sm="row"),
                margin_top="0.5rem",
            ),
            align="center",
            spacing="2",
            width="100%",
        ),
        padding="2.5rem 1.5rem",
        border_radius=RADIO_EXTRA_GRANDE,
        background=COLOR_ACENTO_FONDO,
        border=f"1px solid {COLOR_ACENTO_TEXTO}",
        width="100%",
        margin_top="3rem",
    )


__all__ = ["newsletter_blog"]