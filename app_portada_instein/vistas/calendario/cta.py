"""
CTA final del Calendario Académico.
"""

import reflex as rx

from app_portada_instein.infraestructura.constantes_visuales import (
    COLOR_ACENTO_SOLIDO,
    COLOR_TEXTO_PRINCIPAL,
    COLOR_TEXTO_SECUNDARIO,
    RADIO_PASTILLA,
)


# ======================================================================
# Constantes locales
# ======================================================================

ANCHO_MAXIMO = "72rem"
PADDING_LATERAL = "1.5rem"


def cta_calendario() -> rx.Component:
    """Bloque CTA final hacia /contacto."""
    return rx.box(
        rx.vstack(
            rx.heading(
                "¿Tienes dudas sobre el calendario?",
                size="6",
                font_weight="800",
                color=COLOR_TEXTO_PRINCIPAL,
                text_align="center",
            ),
            rx.text(
                "Contáctanos para más información sobre fechas, "
                "inscripciones y actividades académicas.",
                font_size="0.9375rem",
                color=COLOR_TEXTO_SECUNDARIO,
                text_align="center",
                max_width="36rem",
            ),
            rx.link(
                rx.icon("message-circle", size=18),
                rx.text("Contactar ahora", as_="span", font_weight="700"),
                href="/contacto",
                text_decoration="none",
                display="inline-flex",
                align_items="center",
                gap="0.5rem",
                background=COLOR_ACENTO_SOLIDO,
                color="white",
                padding="0.875rem 1.75rem",
                border_radius=RADIO_PASTILLA,
                font_size="0.9375rem",
                margin_top="1.5rem",
                box_shadow=f"0 10px 25px -5px {COLOR_ACENTO_SOLIDO}",
                transition="all 0.2s",
                _hover={
                    "transform": "translateY(-2px)",
                    "filter": "brightness(1.1)",
                },
            ),
            align="center",
            spacing="2",
        ),
        max_width=ANCHO_MAXIMO,
        margin="0 auto",
        padding=f"4rem {PADDING_LATERAL} 5rem {PADDING_LATERAL}",
        width="100%",
    )


__all__ = ["cta_calendario"]