"""
Tab 2: Fechas importantes de Bolivia y el mundo.
"""

import reflex as rx

from app_portada_instein.infraestructura.constantes_visuales import (
    COLOR_ACENTO_TEXTO,
    COLOR_BORDE_SUAVE,
    COLOR_DIVISOR,
    COLOR_FONDO_CARTA,
    COLOR_FONDO_SUAVE,
    COLOR_TEXTO_PRINCIPAL,
    COLOR_TEXTO_SECUNDARIO,
    RADIO_GRANDE,
    RADIO_PASTILLA,
)

from .datos import FECHAS_IMPORTANTES, TIPOS_FECHA
from .helpers import color_por_tipo_fecha


# ======================================================================
# Leyenda
# ======================================================================


def _leyenda_fechas() -> rx.Component:
    """Leyenda con los tipos de fecha importante."""
    return rx.flex(
        *[
            rx.flex(
                rx.box(
                    height="0.75rem",
                    width="0.75rem",
                    border_radius=RADIO_PASTILLA,
                    background=rx.color(info["color"], 9),
                    flex_shrink="0",
                ),
                rx.text(
                    info["etiqueta"],
                    font_size="0.75rem",
                    font_weight="600",
                    color=COLOR_TEXTO_SECUNDARIO,
                ),
                align="center",
                gap="0.375rem",
            )
            for info in TIPOS_FECHA.values()
        ],
        gap="1rem",
        flex_wrap="wrap",
        margin_bottom="1.5rem",
    )


# ======================================================================
# Badge de tipo de fecha
# ======================================================================


def _badge_tipo_fecha(tipo: str) -> rx.Component:
    """Badge con el tipo de fecha importante."""
    info = color_por_tipo_fecha(tipo)

    return rx.flex(
        rx.icon(
            info["icono"],
            size=12,
            color=rx.color(info["color"], 11),
        ),
        rx.text(
            info["etiqueta"],
            font_size="0.6875rem",
            font_weight="700",
            color=rx.color(info["color"], 11),
            text_transform="uppercase",
            letter_spacing="0.05em",
        ),
        align="center",
        gap="0.25rem",
        padding="0.25rem 0.625rem",
        border_radius=RADIO_PASTILLA,
        background=rx.color(info["color"], 3),
        border=f"1px solid {rx.color(info['color'], 7)}",
        width="fit-content",
    )


# ======================================================================
# Card de fecha importante
# ======================================================================


def _card_fecha_importante(fecha: dict) -> rx.Component:
    """Card de fecha importante (feriado, efeméride, día internacional)."""
    info = color_por_tipo_fecha(fecha["tipo"])

    return rx.flex(
        # --- Columna izquierda: día ---
        rx.box(
            rx.vstack(
                rx.text(
                    "DÍA",
                    font_size="0.5625rem",
                    font_weight="700",
                    color=rx.color(info["color"], 11),
                    text_transform="uppercase",
                    letter_spacing="0.05em",
                ),
                rx.text(
                    fecha["dia"],
                    font_size="1.5rem",
                    font_weight="900",
                    color=COLOR_TEXTO_PRINCIPAL,
                    line_height="1",
                    letter_spacing="-0.03em",
                ),
                align="center",
                spacing="0",
            ),
            height="4.5rem",
            width="4.5rem",
            border_radius=RADIO_GRANDE,
            background=rx.color(info["color"], 3),
            border=f"2px solid {rx.color(info['color'], 7)}",
            display="flex",
            align_items="center",
            justify_content="center",
            flex_shrink="0",
        ),
        # --- Columna derecha: título + tipo ---
        rx.vstack(
            _badge_tipo_fecha(fecha["tipo"]),
            rx.text(
                fecha["titulo"],
                font_size="0.9375rem",
                font_weight="600",
                color=COLOR_TEXTO_PRINCIPAL,
                line_height="1.4",
            ),
            align="start",
            spacing="1",
            flex="1",
            min_width="0",
        ),
        align="center",
        gap="1rem",
        width="100%",
        padding="1rem",
        border_radius=RADIO_GRANDE,
        background=COLOR_FONDO_CARTA,
        border=f"1px solid {COLOR_BORDE_SUAVE}",
        transition="all 0.2s",
        _hover={
            "transform": "translateY(-2px)",
            "border_color": rx.color(info["color"], 7),
            "box_shadow": f"0 8px 20px -8px {rx.color(info['color'], 9)}",
        },
    )


# ======================================================================
# Grupo por mes
# ======================================================================


def _grupo_mes(mes: str, fechas: list[dict]) -> rx.Component:
    """Grupo de fechas de un mismo mes."""
    return rx.box(
        # --- Encabezado del mes ---
        rx.flex(
            rx.text(
                mes,
                font_size="0.875rem",
                font_weight="800",
                color=COLOR_ACENTO_TEXTO,
                letter_spacing="0.1em",
                text_transform="uppercase",
            ),
            rx.box(
                flex="1",
                height="1px",
                background=COLOR_DIVISOR,
            ),
            rx.text(
                str(len(fechas)),
                font_size="0.75rem",
                font_weight="700",
                color=COLOR_TEXTO_SECUNDARIO,
                padding="0.125rem 0.5rem",
                background=COLOR_FONDO_SUAVE,
                border_radius=RADIO_PASTILLA,
            ),
            align="center",
            gap="0.75rem",
            width="100%",
            margin_bottom="1rem",
        ),
        # --- Grid de fechas del mes ---
        rx.grid(
            *[_card_fecha_importante(f) for f in fechas],
            columns=rx.breakpoints(initial="1", md="2"),
            spacing="3",
            width="100%",
        ),
        width="100%",
        margin_bottom="2rem",
    )


# ======================================================================
# Tab completo
# ======================================================================


def tab_fechas_importantes() -> rx.Component:
    """
    Contenido del tab 'Fechas importantes'.

    Agrupa las fechas por mes (orden cronológico), mostrando cada mes
    como un bloque con su grid de fechas.
    """
    # Agrupamos por mes manteniendo el orden de aparición
    meses_ordenados: list[str] = []
    fechas_por_mes: dict[str, list[dict]] = {}

    for fecha in FECHAS_IMPORTANTES:
        mes = fecha["mes"]
        if mes not in fechas_por_mes:
            meses_ordenados.append(mes)
            fechas_por_mes[mes] = []
        fechas_por_mes[mes].append(fecha)

    return rx.vstack(
        _leyenda_fechas(),
        *[
            _grupo_mes(mes, fechas_por_mes[mes])
            for mes in meses_ordenados
        ],
        spacing="0",
        width="100%",
    )


__all__ = ["tab_fechas_importantes"]