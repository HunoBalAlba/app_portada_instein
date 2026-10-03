# app_portada_instein/componentes/barra_navegacion.py

"""
Barra de navegación superior — estilo Neon adaptativo (dark/light).

Sistema de color (UX)
---------------------
- Fondo: glassmorphism adaptativo (`FONDO_BARRA_HOME`).
- Elemento activo: fondo azul marino translúcido + borde azul tenue.
- Elementos inactivos: texto adaptativo (`TEXTO_HOME_MAS_SUAVE`).
- Hover: fondo azul marino translúcido + texto adaptativo.
- Logo: badge con gradiente azul marino + texto "INSTEIN" adaptativo.
- Toggle de color_mode: a la derecha.

✅ ADAPTATIVO: la barra respeta el color_mode del usuario.
"""

import reflex as rx

from app_portada_instein.componentes.primitivos import enlace_navegacion
from app_portada_instein.dominio.estado_institucional import EstadoInstitucional
from app_portada_instein.infraestructura.constantes_visuales import (
    AZUL_MARINO_NEON,
    BORDE_HOME_AZUL,
    BORDE_HOME_MEDIO,
    BORDE_HOME_SUAVE,
    FONDO_AZUL_MUY_SUAVE,
    FONDO_AZUL_SUAVE,
    FONDO_BARRA_HOME,
    RADIO_MEDIO,
    TEXTO_HOME_MAS_SUAVE,
    TEXTO_HOME_PRINCIPAL,
)


# ======================================================================
# Constantes locales
# ======================================================================

TAMANO_ICONO_MENU = 20
TAMANO_ICONO_MENU_MOVIL = 22

ANCHO_MAXIMO_BARRA = "72rem"

SOMBRA_LOGO = f"0 0 20px {AZUL_MARINO_NEON}80"


# ======================================================================
# Elemento individual del menú
# ======================================================================


def elemento_menu(etiqueta: str, icono: str, ruta: str) -> rx.Component:
    """
    Elemento individual del menú de navegación, con estado activo.

    ✅ ADAPTATIVO: los colores se ajustan al color_mode del usuario.
    """
    esta_activo = EstadoInstitucional.ruta_activa_normalizada == ruta

    color_contenido = rx.cond(
        esta_activo,
        TEXTO_HOME_PRINCIPAL,
        TEXTO_HOME_MAS_SUAVE,
    )

    return enlace_navegacion(
        ruta,
        rx.flex(
            # Icono móvil (size=22)
            rx.mobile_only(
                rx.icon(
                    icono,
                    size=TAMANO_ICONO_MENU_MOVIL,
                    color=color_contenido,
                ),
            ),
            # Icono tablet/desktop (size=20) + texto
            rx.tablet_and_desktop(
                rx.icon(
                    icono,
                    size=TAMANO_ICONO_MENU,
                    color=color_contenido,
                ),
                rx.text(
                    etiqueta,
                    font_size="0.875rem",
                    font_weight=rx.cond(esta_activo, "700", "500"),
                    color=color_contenido,
                    white_space="nowrap",
                ),
                align="center",
                gap="0.4rem",
            ),
            align="center",
            gap="0.4rem",
        ),
        padding=rx.breakpoints(
            initial="0.5rem",
            lg="0.5rem 1rem",
        ),
        border_radius=RADIO_MEDIO,
        background=rx.cond(
            esta_activo,
            FONDO_AZUL_SUAVE,
            "transparent",
        ),
        border=rx.cond(
            esta_activo,
            f"1px solid {BORDE_HOME_MEDIO}",
            "1px solid transparent",
        ),
        transition="all 0.2s",
        display="inline-flex",
        align_items="center",
        justify_content="center",
        text_decoration="none",
        _hover={
            "background": FONDO_AZUL_MUY_SUAVE,
            "color": TEXTO_HOME_PRINCIPAL,
        },
    )


# ======================================================================
# Logo institucional
# ======================================================================


def _logo_institucional() -> rx.Component:
    """Logo textual del instituto con badge de gradiente azul marino."""
    return rx.flex(
        rx.box(
            rx.text(
                "I",
                font_size="1rem",
                font_weight="900",
                color="white",
                line_height="1",
            ),
            height="2rem",
            width="2rem",
            border_radius=RADIO_MEDIO,
            background=(
                f"linear-gradient(135deg, {AZUL_MARINO_NEON} 0%, "
                f"#1a237e 100%)"
            ),
            display="flex",
            align_items="center",
            justify_content="center",
            box_shadow=SOMBRA_LOGO,
            flex_shrink="0",
        ),
        rx.tablet_and_desktop(
            rx.text(
                "INSTEIN",
                font_size="0.9375rem",
                font_weight="800",
                color=TEXTO_HOME_PRINCIPAL,
                letter_spacing="0.1em",
            ),
        ),
        align="center",
        gap="0.625rem",
        flex_shrink="0",
    )


# ======================================================================
# Barra de navegación completa
# ======================================================================


def barra_navegacion_superior() -> rx.Component:
    """
    Barra de navegación superior fija (sticky) — estilo Neon adaptativo.

    ✅ ADAPTATIVO: el fondo glassmorphism cambia entre light y dark.
    """
    return rx.vstack(
        rx.flex(
            rx.flex(
                _logo_institucional(),
                rx.flex(
                    elemento_menu("Inicio", "home", "/"),
                    elemento_menu("Carreras", "graduation-cap", "/carreras"),
                    elemento_menu("Contacto", "map-pin", "/contacto"),
                    align="center",
                    gap="0.25rem",
                    flex_shrink="0",
                ),
                align="center",
                gap=rx.breakpoints(
                    initial="0.75rem",
                    md="1.5rem",
                    lg="2rem",
                ),
                flex_shrink="0",
                min_width="0",
            ),
            rx.flex(
                rx.color_mode.button(),
                align="center",
                gap="1rem",
                flex_shrink="0",
            ),
            align="center",
            justify="between",
            width="100%",
            max_width=ANCHO_MAXIMO_BARRA,
            margin="0 auto",
            gap="1rem",
        ),
        align="center",
        justify="between",
        width="100%",
        padding="0.875rem 1.5rem",
        position="sticky",
        top="0",
        z_index="30",
        background=FONDO_BARRA_HOME,
        backdrop_filter="blur(20px)",
        border_bottom=f"1px solid {BORDE_HOME_SUAVE}",
    )


__all__ = [
    "barra_navegacion_superior",
    "elemento_menu",
]