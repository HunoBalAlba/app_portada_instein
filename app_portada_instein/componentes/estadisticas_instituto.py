"""
Bloque de estadísticas del instituto con gráfico de barras horizontales.

Estructura:
1. Grid de 4 tarjetas con cifras clave:
   - Carreras Técnicas (5)
   - Años de Experiencia (15+)
   - Egresados (500+)
   - Empleabilidad (100%)
2. Gráfico de barras horizontales con la distribución histórica de
   egresados por cada una de las 5 carreras del instituto.

Sistema de color (UX)
---------------------
- Cards: cada stat tiene su color de marca (azul, cyan, violeta, verde),
  coherente con el catálogo de carreras y la sección "¿Por qué INSTEIN?".
- Gráfico: usa el accent institucional (crimson) para todas las barras
  y mantiene la coherencia con el resto del sitio.
- Textos: neutros (`gray-11`/`gray-12`) para máxima legibilidad.

Layout responsive
-----------------
- Desktop (lg): 4 columnas de cards + gráfico full width.
- Tablet (md):  2 columnas de cards + gráfico full width.
- Móvil (sm):   1 columna de cards + gráfico full width.
"""

import reflex as rx

from app_portada_instein.infraestructura.constantes_visuales import (
    COLOR_BORDE_SUAVE,
    COLOR_FONDO_CARTA,
    COLOR_TEXTO_PRINCIPAL,
    COLOR_TEXTO_SECUNDARIO,
    RADIO_EXTRA_GRANDE,
    RADIO_GRANDE,
)


# ======================================================================
# Constantes locales
# ======================================================================

# Padding del bloque de estadísticas.
PADDING_BLOQUE = "2rem 1.5rem"

# Tamaño del icono en cada stat card.
TAMANO_ICONO_STAT = 20

# Altura del gráfico de barras (px).
ALTURA_GRAFICO = 260


# ======================================================================
# Estructura de estadísticas (para las cards)
# ======================================================================

ESTADISTICAS: list[dict] = [
    {
        "valor": "5",
        "sufijo": "",
        "etiqueta": "Carreras Técnicas",
        "icono": "graduation-cap",
        "color_light": "#2563eb",
        "color_dark": "#60a5fa",
    },
    {
        "valor": "15",
        "sufijo": "+",
        "etiqueta": "Años de Experiencia",
        "icono": "award",
        "color_light": "#0891b2",
        "color_dark": "#22d3ee",
    },
    {
        "valor": "500",
        "sufijo": "+",
        "etiqueta": "Egresados",
        "icono": "users",
        "color_light": "#7c3aed",
        "color_dark": "#a78bfa",
    },
    {
        "valor": "100",
        "sufijo": "%",
        "etiqueta": "Empleabilidad",
        "icono": "trending-up",
        "color_light": "#16a34a",
        "color_dark": "#4ade80",
    },
]


# ======================================================================
# Data del gráfico (egresados por carrera)
# ======================================================================

DATA_EGRESADOS: list[dict] = [
    {"carrera": "Sistemas", "egresados": 234},
    {"carrera": "Contaduría", "egresados": 198},
    {"carrera": "Secretariado", "egresados": 156},
    {"carrera": "Comercio Int.", "egresados": 145},
    {"carrera": "Electrónica", "egresados": 178},
]


# ======================================================================
# Helpers internos
# ======================================================================


def _color_adaptativo(stat: dict) -> rx.Var:
    """Devuelve el color del stat adaptado al color_mode."""
    return rx.color_mode_cond(
        light=stat["color_light"],
        dark=stat["color_dark"],
    )


def _fondo_tintado(stat: dict) -> rx.Var:
    """Devuelve el fondo tintado del color de marca (para el icono)."""
    return rx.color_mode_cond(
        light=f"{stat['color_light']}15",
        dark=f"{stat['color_dark']}20",
    )


# ======================================================================
# Tarjeta individual de estadística
# ======================================================================


def _tarjeta_estadistica(stat: dict) -> rx.Component:
    """
    Tarjeta individual de estadística.

    UX:
    - Icono pequeño arriba con fondo tintado del color de marca.
    - Número grande con sufijo (+/%/etc) en el mismo bloque.
    - Etiqueta descriptiva en gris.
    - Hover: elevación + borde del color de marca.

    Args:
        stat: Dict con `valor`, `sufijo`, `etiqueta`, `icono`,
            `color_light`, `color_dark`.
    """
    color_stat = _color_adaptativo(stat)

    return rx.box(
        rx.vstack(
            # ==========================================================
            # Icono con fondo tintado
            # ==========================================================
            rx.flex(
                rx.icon(
                    stat["icono"],
                    size=TAMANO_ICONO_STAT,
                    color=color_stat,
                ),
                height="2.5rem",
                width="2.5rem",
                border_radius=RADIO_GRANDE,
                background=_fondo_tintado(stat),
                border=f"1px solid {color_stat}",
                align="center",
                justify="center",
                margin_bottom="0.75rem",
            ),
            # ==========================================================
            # Valor grande + sufijo
            # ==========================================================
            rx.flex(
                rx.text(
                    stat["valor"],
                    font_size="2.25rem",
                    font_weight="900",
                    color=COLOR_TEXTO_PRINCIPAL,
                    line_height="1",
                    letter_spacing="-0.03em",
                ),
                rx.text(
                    stat["sufijo"],
                    font_size="1.5rem",
                    font_weight="800",
                    color=color_stat,
                    line_height="1",
                    margin_left="0.125rem",
                ),
                align="end",
                gap="0",
            ),
            # ==========================================================
            # Etiqueta
            # ==========================================================
            rx.text(
                stat["etiqueta"],
                font_size="0.75rem",
                font_weight="600",
                letter_spacing="0.05em",
                text_transform="uppercase",
                color=COLOR_TEXTO_SECUNDARIO,
            ),
            align="start",
            spacing="1",
            width="100%",
        ),
        padding="1.5rem",
        border_radius=RADIO_EXTRA_GRANDE,
        border=f"1px solid {COLOR_BORDE_SUAVE}",
        background=COLOR_FONDO_CARTA,
        width="100%",
        height="100%",
        transition="all 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
        _hover={
            "transform": "translateY(-4px)",
            "border_color": color_stat,
            "box_shadow": f"0 20px 40px -10px {color_stat}",
        },
    )


# ======================================================================
# Gráfico de barras horizontales
# ======================================================================


def _grafico_egresados() -> rx.Component:
    """
    Gráfico de barras horizontales con egresados por carrera.

    Usa Recharts con `layout="vertical"` para que las barras sean
    horizontales. El eje X es numérico (cantidad de egresados) y el
    eje Y es categórico (nombre de la carrera).

    UX:
    - Encabezado con título y subtítulo.
    - Barras en accent institucional (crimson) con hover tooltip.
    - Grid cartesiano horizontal sutil para guiar la lectura.
    """
    return rx.box(
        # ==========================================================
        # Encabezado del gráfico
        # ==========================================================
        rx.flex(
            rx.vstack(
                rx.text(
                    "Egresados por carrera",
                    font_size="0.9375rem",
                    font_weight="700",
                    color=COLOR_TEXTO_PRINCIPAL,
                    line_height="1.2",
                ),
                rx.text(
                    "Distribución histórica de egresados en las 5 carreras.",
                    font_size="0.75rem",
                    color=COLOR_TEXTO_SECUNDARIO,
                    line_height="1.4",
                ),
                spacing="0",
                align="start",
            ),
            align="start",
            width="100%",
            margin_bottom="1rem",
        ),
        # ==========================================================
        # Gráfico Recharts
        # ==========================================================
        rx.recharts.bar_chart(
            rx.recharts.bar(
                data_key="egresados",
                stroke=rx.color("accent", 8),
                fill=rx.color("accent", 9),
                radius=[0, 6, 6, 0],  # esquinas redondeadas a la derecha
            ),
            rx.recharts.x_axis(type_="number"),
            rx.recharts.y_axis(
                data_key="carrera",
                type_="category",
                width=110,
            ),
            rx.recharts.cartesian_grid(
                stroke_dasharray="3 3",
                horizontal=False,
                vertical=True,
                stroke=rx.color("gray", 5),
            ),
            rx.recharts.tooltip(),
            data=DATA_EGRESADOS,
            layout="vertical",
            margin={"top": 10, "right": 20, "left": 10, "bottom": 10},
            width="100%",
            height=ALTURA_GRAFICO,
        ),
        # ==========================================================
        # Estilos del contenedor
        # ==========================================================
        padding="1.5rem",
        border_radius=RADIO_EXTRA_GRANDE,
        border=f"1px solid {COLOR_BORDE_SUAVE}",
        background=COLOR_FONDO_CARTA,
        width="100%",
    )


# ======================================================================
# Sección completa
# ======================================================================


def seccion_estadisticas() -> rx.Component:
    """
    Bloque completo con las estadísticas del instituto:

    1. Grid de 4 tarjetas con cifras clave.
    2. Gráfico de barras horizontales con egresados por carrera.

    Layout responsive:
    - Desktop: 4 columnas de stats + gráfico full width.
    - Tablet:  2 columnas de stats + gráfico full width.
    - Móvil:   1 columna de stats + gráfico full width.
    """
    return rx.box(
        rx.vstack(
            # ==========================================================
            # Grid de estadísticas
            # ==========================================================
            rx.grid(
                *[_tarjeta_estadistica(s) for s in ESTADISTICAS],
                columns=rx.breakpoints(initial="1", sm="2", md="2", lg="4"),
                spacing="4",
                width="100%",
            ),
            # ==========================================================
            # Gráfico de egresados
            # ==========================================================
            _grafico_egresados(),
            spacing="6",
            width="100%",
        ),
        width="100%",
        padding=PADDING_BLOQUE,
    )


__all__ = [
    "DATA_EGRESADOS",
    "ESTADISTICAS",
    "seccion_estadisticas",
]