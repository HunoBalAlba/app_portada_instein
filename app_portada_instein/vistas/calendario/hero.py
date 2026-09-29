"""
Hero + grid de info rápida del Calendario Académico.
"""

import reflex as rx

from app_portada_instein.infraestructura.constantes_visuales import (
    COLOR_ACENTO_FONDO,
    COLOR_ACENTO_TEXTO,
    COLOR_BORDE_SUAVE,
    COLOR_FONDO_CARTA,
    COLOR_TEXTO_CUERPO,
    COLOR_TEXTO_PRINCIPAL,
    COLOR_TEXTO_SECUNDARIO,
    RADIO_EXTRA_GRANDE,
    RADIO_GRANDE,
    RADIO_PASTILLA,
)

from .datos import INFO_RAPIDA


# ======================================================================
# Constantes locales
# ======================================================================

ANCHO_MAXIMO = "72rem"
PADDING_LATERAL = "1.5rem"


# ======================================================================
# Hero
# ======================================================================


def hero_calendario() -> rx.Component:
    """Hero con título + subtítulo + badge."""
    return rx.vstack(
        # --- Badge de inscripciones abiertas ---
        rx.flex(
            rx.box(
                height="0.5rem",
                width="0.5rem",
                border_radius=RADIO_PASTILLA,
                background=rx.color("green", 9),
                animation="pulse 2s ease-in-out infinite",
            ),
            rx.text(
                "INSCRIPCIONES ABIERTAS TODO EL AÑO",
                font_size="0.75rem",
                font_weight="700",
                color=COLOR_TEXTO_PRINCIPAL,
                letter_spacing="0.05em",
            ),
            align="center",
            gap="0.5rem",
            padding="0.5rem 1rem",
            border_radius=RADIO_PASTILLA,
            background=COLOR_ACENTO_FONDO,
            border=f"1px solid {COLOR_ACENTO_TEXTO}",
            width="fit-content",
            margin_bottom="1rem",
        ),
        # --- Título ---
        rx.heading(
            "Calendario ",
            rx.text.span(
                "Académico",
                color=COLOR_ACENTO_TEXTO,
            ),
            "",
            size="9",
            font_weight="900",
            color=COLOR_TEXTO_PRINCIPAL,
            text_align="center",
            letter_spacing="-0.03em",
            line_height="1.1",
        ),
        # --- Subtítulo ---
        rx.text(
            "Todas las actividades del instituto y las fechas importantes "
            "de Bolivia en un solo lugar. En INSTEIN puedes inscribirte "
            "en cualquier momento del año.",
            font_size="1rem",
            color=COLOR_TEXTO_CUERPO,
            text_align="center",
            max_width="48rem",
            line_height="1.7",
            margin_top="0.5rem",
        ),
        align="center",
        spacing="3",
        padding=f"5rem {PADDING_LATERAL} 3rem {PADDING_LATERAL}",
        max_width=ANCHO_MAXIMO,
        margin="0 auto",
        width="100%",
    )


# ======================================================================
# Cards de info rápida
# ======================================================================


def _card_info_rapida(item: dict) -> rx.Component:
    """Card con info rápida (inscripciones, inicio, duración, modalidad)."""
    color_scheme = item["color"]

    return rx.box(
        rx.vstack(
            rx.flex(
                rx.icon(
                    item["icono"],
                    size=20,
                    color=rx.color(color_scheme, 11),
                ),
                height="2.5rem",
                width="2.5rem",
                border_radius=RADIO_GRANDE,
                background=rx.color(color_scheme, 3),
                border=f"1px solid {rx.color(color_scheme, 7)}",
                align="center",
                justify="center",
                margin_bottom="0.75rem",
            ),
            rx.text(
                item["titulo"],
                font_size="0.6875rem",
                font_weight="700",
                color=COLOR_TEXTO_SECUNDARIO,
                text_transform="uppercase",
                letter_spacing="0.05em",
            ),
            rx.text(
                item["valor"],
                font_size="0.9375rem",
                font_weight="800",
                color=COLOR_TEXTO_PRINCIPAL,
                line_height="1.3",
            ),
            rx.text(
                item["descripcion"],
                font_size="0.75rem",
                color=COLOR_TEXTO_SECUNDARIO,
                line_height="1.5",
                margin_top="0.25rem",
            ),
            align="start",
            spacing="1",
            width="100%",
        ),
        padding="1.25rem",
        border_radius=RADIO_EXTRA_GRANDE,
        border=f"1px solid {COLOR_BORDE_SUAVE}",
        background=COLOR_FONDO_CARTA,
        width="100%",
        height="100%",
        transition="all 0.2s",
        _hover={
            "transform": "translateY(-2px)",
            "border_color": rx.color(color_scheme, 7),
        },
    )


def grid_info_rapida() -> rx.Component:
    """Grid con las 4 cards de info rápida."""
    return rx.box(
        rx.grid(
            *[_card_info_rapida(item) for item in INFO_RAPIDA],
            columns=rx.breakpoints(initial="1", sm="2", md="2", lg="4"),
            spacing="4",
            width="100%",
        ),
        max_width=ANCHO_MAXIMO,
        margin="0 auto",
        padding=f"0 {PADDING_LATERAL} 3rem {PADDING_LATERAL}",
        width="100%",
    )


__all__ = ["grid_info_rapida", "hero_calendario"]