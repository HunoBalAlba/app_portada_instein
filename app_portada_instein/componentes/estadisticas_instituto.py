# app_portada_instein/componentes/estadisticas_instituto.py

"""
Estadísticas del instituto — estilo Neon adaptativo (dark/light).

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
✅ ADAPTATIVO: todos los colores respetan el color_mode del usuario.

- Cards: `FONDO_HOME_CARD_ADAPTATIVO` (light: blanco translúcido,
  dark: azul oscuro translúcido).
- Acentos: azul marino neon (`AZUL_MARINO_NEON` = `#3b5bdb`) en AMBOS modos.
- Texto: `TEXTO_HOME_PRINCIPAL` / `TEXTO_HOME_MAS_SUAVE`.
- Bordes: `BORDE_HOME_SUAVE` / `BORDE_HOME_AZUL`.
- Fondo tintado del icono: `FONDO_AZUL_SUAVE`.
- Sombra hover: `SOMBRA_HOVER_CARD_HOME`.
- Gráfico: barras en azul marino neon, ejes en `TEXTO_HOME_MAS_SUAVE`,
  grid adaptativo.

Estilo Neon:
- Tipografía masiva (valores `2.5rem` con `font_weight="900"`).
- Glassmorphism (blur + bordes translúcidos).
- Hover con glow azul marino.
- Padding generoso.
"""

import reflex as rx

from app_portada_instein.infraestructura.constantes_visuales import (
    AZUL_MARINO_NEON,
    BORDE_HOME_AZUL,
    BORDE_HOME_MEDIO,
    BORDE_HOME_SUAVE,
    FONDO_AZUL_SUAVE,
    FONDO_HOME_CARD_ADAPTATIVO,
    RADIO_EXTRA_GRANDE,
    RADIO_GRANDE,
    SOMBRA_HOVER_CARD_HOME,
    TEXTO_HOME_MAS_SUAVE,
    TEXTO_HOME_PRINCIPAL,
)


# ======================================================================
# Constantes locales
# ======================================================================

# Padding del bloque de estadísticas.
PADDING_BLOQUE = "4rem 1.5rem"

# Tamaño del icono en cada stat card.
TAMANO_ICONO_STAT = 20

# Altura del gráfico de barras (px).
ALTURA_GRAFICO = 280

# Ancho máximo del contenido.
ANCHO_MAXIMO_CONTENIDO = "72rem"


# ======================================================================
# Estructura de estadísticas (para las cards)
# ======================================================================

ESTADISTICAS: list[dict] = [
    {
        "valor": "5",
        "sufijo": "",
        "etiqueta": "Carreras Técnicas",
        "icono": "graduation-cap",
    },
    {
        "valor": "15",
        "sufijo": "+",
        "etiqueta": "Años de Experiencia",
        "icono": "award",
    },
    {
        "valor": "500",
        "sufijo": "+",
        "etiqueta": "Egresados",
        "icono": "users",
    },
    {
        "valor": "100",
        "sufijo": "%",
        "etiqueta": "Empleabilidad",
        "icono": "trending-up",
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
# Tarjeta individual de estadística
# ======================================================================


def _tarjeta_estadistica(stat: dict) -> rx.Component:
    """
    Tarjeta individual de estadística — estilo Neon adaptativo.

    UX:
    - Icono pequeño arriba con fondo tintado azul marino + borde azul.
    - Número grande con sufijo (+/%) en azul marino neon.
    - Etiqueta descriptiva adaptativa.
    - Hover: elevación + borde azul + glow azul marino (adaptativo).

    ✅ ADAPTATIVO: fondo, texto, borde y sombra cambian según el modo.

    Args:
        stat: Dict con `valor`, `sufijo`, `etiqueta`, `icono`.
    """
    return rx.box(
        rx.vstack(
            # ==========================================================
            # Icono con fondo tintado azul marino
            # ==========================================================
            rx.flex(
                rx.icon(
                    stat["icono"],
                    size=TAMANO_ICONO_STAT,
                    color=AZUL_MARINO_NEON,
                ),
                height="2.75rem",
                width="2.75rem",
                border_radius=RADIO_GRANDE,
                background=FONDO_AZUL_SUAVE,      # ✅ adaptativo
                border=f"1px solid {BORDE_HOME_AZUL}",
                align="center",
                justify="center",
                margin_bottom="1rem",
            ),
            # ==========================================================
            # Valor grande + sufijo
            # ==========================================================
            rx.flex(
                rx.text(
                    stat["valor"],
                    font_size="2.5rem",
                    font_weight="900",
                    color=TEXTO_HOME_PRINCIPAL,   # ✅ adaptativo
                    line_height="1",
                    letter_spacing="-0.04em",
                ),
                rx.text(
                    stat["sufijo"],
                    font_size="1.5rem",
                    font_weight="800",
                    color=AZUL_MARINO_NEON,       # mismo en ambos modos
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
                letter_spacing="0.1em",
                text_transform="uppercase",
                color=TEXTO_HOME_MAS_SUAVE,      # ✅ adaptativo
                margin_top="0.5rem",
            ),
            align="start",
            spacing="1",
            width="100%",
        ),
        padding="1.75rem",
        border_radius=RADIO_EXTRA_GRANDE,
        border=f"1px solid {BORDE_HOME_SUAVE}",              # ✅ adaptativo
        background=FONDO_HOME_CARD_ADAPTATIVO,                # ✅ adaptativo
        backdrop_filter="blur(12px)",
        width="100%",
        height="100%",
        transition="all 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
        _hover={
            "transform": "translateY(-4px)",
            "border_color": BORDE_HOME_AZUL,
            "box_shadow": SOMBRA_HOVER_CARD_HOME,             # ✅ adaptativo
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

    ✅ ADAPTATIVO: fondo, ejes y grid cambian según el color_mode.

    UX:
    - Encabezado con título y subtítulo.
    - Barras en azul marino neon con hover tooltip.
    - Grid cartesiano horizontal sutil para guiar la lectura.
    - Fondo adaptativo con glassmorphism y borde azul en hover.
    """
    return rx.box(
        # ==========================================================
        # Encabezado del gráfico
        # ==========================================================
        rx.flex(
            rx.vstack(
                rx.text(
                    "Egresados por carrera",
                    font_size="1rem",
                    font_weight="700",
                    color=TEXTO_HOME_PRINCIPAL,   # ✅ adaptativo
                    line_height="1.2",
                ),
                rx.text(
                    "Distribución histórica de egresados en las 5 carreras.",
                    font_size="0.8125rem",
                    color=TEXTO_HOME_MAS_SUAVE,   # ✅ adaptativo
                    line_height="1.4",
                ),
                spacing="0",
                align="start",
            ),
            align="start",
            width="100%",
            margin_bottom="1.5rem",
        ),
        # ==========================================================
        # Gráfico Recharts
        # ==========================================================
        rx.recharts.bar_chart(
            rx.recharts.bar(
                data_key="egresados",
                stroke=AZUL_MARINO_NEON,
                fill=AZUL_MARINO_NEON,
                radius=[0, 6, 6, 0],  # esquinas redondeadas a la derecha
            ),
            rx.recharts.x_axis(
                type_="number",
                stroke=TEXTO_HOME_MAS_SUAVE,   # ✅ adaptativo
            ),
            rx.recharts.y_axis(
                data_key="carrera",
                type_="category",
                width=110,
                stroke=TEXTO_HOME_MAS_SUAVE,   # ✅ adaptativo
            ),
            rx.recharts.cartesian_grid(
                stroke_dasharray="3 3",
                horizontal=False,
                vertical=True,
                stroke=rx.color_mode_cond(     # ✅ adaptativo
                    light="rgba(15, 23, 42, 0.08)",
                    dark="rgba(255, 255, 255, 0.06)",
                ),
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
        padding="2rem",
        border_radius=RADIO_EXTRA_GRANDE,
        border=f"1px solid {BORDE_HOME_SUAVE}",              # ✅ adaptativo
        background=FONDO_HOME_CARD_ADAPTATIVO,                # ✅ adaptativo
        backdrop_filter="blur(12px)",
        width="100%",
        transition="all 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
        _hover={
            "border_color": BORDE_HOME_AZUL,
        },
    )


# ======================================================================
# Sección completa
# ======================================================================


def seccion_estadisticas() -> rx.Component:
    """
    Bloque completo con las estadísticas del instituto.

    1. Grid de 4 tarjetas con cifras clave.
    2. Gráfico de barras horizontales con egresados por carrera.

    Layout responsive:
    - Desktop: 4 columnas de stats + gráfico full width.
    - Tablet:  2 columnas de stats + gráfico full width.
    - Móvil:   1 columna de stats + gráfico full width.

    Contenido centrado con `max_width="72rem"` (como el resto del home).

    ✅ ADAPTATIVO: todo el bloque respeta el color_mode del usuario.
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
        max_width=ANCHO_MAXIMO_CONTENIDO,
        margin="0 auto",
        padding=PADDING_BLOQUE,
    )


__all__ = [
    "DATA_EGRESADOS",
    "ESTADISTICAS",
    "seccion_estadisticas",
]