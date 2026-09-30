"""
CTA final del blog: hacia /carreras o /contacto.
"""

import reflex as rx

from app_portada_instein.infraestructura.constantes_visuales import (
    COLOR_ACENTO_SOLIDO,
    COLOR_BORDE_SUAVE,
    COLOR_TEXTO_CUERPO,
    COLOR_TEXTO_PRINCIPAL,
    RADIO_PASTILLA,
)


# ======================================================================
# Constantes locales
# ======================================================================

ANCHO_MAXIMO = "72rem"
PADDING_LATERAL = "1.5rem"


def cta_blog() -> rx.Component:
    """CTA final hacia contacto o carreras."""
    return rx.box(
        rx.vstack(
            rx.heading(
                "¿Listo para ser parte de INSTEIN?",
                size="7",
                font_weight="900",
                color=COLOR_TEXTO_PRINCIPAL,
                text_align="center",
                letter_spacing="-0.03em",
            ),
            rx.text(
                "La teoría está en el blog. La práctica te espera en "
                "nuestras aulas.",
                font_size="1rem",
                color=COLOR_TEXTO_CUERPO,
                text_align="center",
                max_width="42rem",
                line_height="1.6",
                margin_top="0.5rem",
            ),
            rx.flex(
                # --- CTA primario ---
                rx.link(
                    rx.icon("graduation-cap", size=18),
                    rx.text("Ver carreras", as_="span", font_weight="700"),
                    href="/carreras",
                    text_decoration="none",
                    display="inline-flex",
                    align_items="center",
                    gap="0.5rem",
                    background=COLOR_ACENTO_SOLIDO,
                    color="white",
                    padding="1rem 2rem",
                    border_radius=RADIO_PASTILLA,
                    font_size="1rem",
                    box_shadow=f"0 10px 25px -5px {COLOR_ACENTO_SOLIDO}",
                    transition="all 0.2s",
                    _hover={
                        "transform": "translateY(-2px)",
                        "filter": "brightness(1.1)",
                    },
                ),
                # --- CTA secundario ---
                rx.link(
                    rx.icon("message-circle", size=18),
                    rx.text("Contactar", as_="span", font_weight="600"),
                    href="/contacto",
                    text_decoration="none",
                    display="inline-flex",
                    align_items="center",
                    gap="0.5rem",
                    background="transparent",
                    color=COLOR_TEXTO_PRINCIPAL,
                    padding="1rem 2rem",
                    border_radius=RADIO_PASTILLA,
                    font_size="1rem",
                    border=f"1px solid {COLOR_BORDE_SUAVE}",
                    transition="all 0.2s",
                    _hover={
                        "transform": "translateY(-2px)",
                        "border_color": COLOR_ACENTO_SOLIDO,
                    },
                ),
                gap="0.75rem",
                flex_direction=rx.breakpoints(initial="column", sm="row"),
                align="center",
                justify="center",
                margin_top="1.5rem",
            ),
            align="center",
            spacing="2",
        ),
        max_width=ANCHO_MAXIMO,
        margin="0 auto",
        padding=f"4rem {PADDING_LATERAL} 5rem {PADDING_LATERAL}",
        width="100%",
    )


__all__ = ["cta_blog"]