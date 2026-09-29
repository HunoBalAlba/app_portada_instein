"""
Barra de navegación superior con enlaces a las rutas principales
y botón de cambio de tema (claro/oscuro).

Sistema de color (UX)
---------------------
- Elemento activo: fondo sólido con accent institucional (crimson)
  y texto blanco para máximo contraste.
- Elementos inactivos: texto neutro con hover en accent.
- Contenedor del menú: fondo accent suave para agrupar visualmente.
- Fondo de la barra: `rgba` intencionales con `backdrop-filter: blur`
  para efecto glassmorphism (funciona igual en light/dark).
"""

import reflex as rx

from app_portada_instein.componentes.primitivos import enlace_navegacion
from app_portada_instein.dominio.estado_institucional import EstadoInstitucional
from app_portada_instein.infraestructura.constantes_visuales import (
    COLOR_ACENTO_BORDE,
    COLOR_ACENTO_FONDO,
    COLOR_ACENTO_SOLIDO,
    COLOR_ACENTO_TEXTO,
    COLOR_ACENTO_TEXTO_SOLIDO,
    COLOR_TEXTO_SECUNDARIO,
    RADIO_MEDIO,
    SOMBRA_CAJA,
)


# ======================================================================
# Constantes locales
# ======================================================================

TAMANO_ICONO_MENU = 22
TAMANO_ICONO_MENU_MOVIL = 24

# Colores de fondo de la barra con `backdrop-filter: blur` para
# efecto glassmorphism. Los `rgba` son intencionales: combinan con
# cualquier contenido que se muestre detrás de la barra sticky.
FONDO_BARRA_LIGHT = "rgba(255, 255, 255, 0.85)"
FONDO_BARRA_DARK = "rgba(15, 17, 23, 0.85)"


# ======================================================================
# Elemento individual del menú
# ======================================================================


def elemento_menu(etiqueta: str, icono: str, ruta: str) -> rx.Component:
    """
    Elemento individual del menú de navegación, con estado activo.

    Compara la ruta activa normalizada para marcar correctamente el
    elemento activo, incluyendo la raíz "/".

    UX:
    - Estado activo: fondo sólido accent crimson + texto blanco.
    - Estado inactivo: texto neutro. Hover: texto accent crimson.
    - Vista móvil: solo icono. Vista desktop: icono + texto.

    Args:
        etiqueta: Texto visible del elemento.
        icono: Nombre del icono de Lucide.
        ruta: Ruta de navegación (ej: "/", "/carreras").
    """
    esta_activo = EstadoInstitucional.ruta_activa_normalizada == ruta

    # Color del contenido (icono + texto):
    # - Activo: blanco (sobre fondo sólido accent).
    # - Inactivo: neutro secundario.
    color_contenido = rx.cond(
        esta_activo,
        "white",
        COLOR_TEXTO_SECUNDARIO,
    )

    return enlace_navegacion(
        ruta,
        # ==========================================================
        # Vista móvil: solo icono
        # ==========================================================
        rx.mobile_only(
            rx.flex(
                rx.icon(
                    icono,
                    size=TAMANO_ICONO_MENU_MOVIL,
                    color=color_contenido,
                ),
            ),
        ),
        # ==========================================================
        # Vista tablet/desktop: icono + texto
        # ==========================================================
        rx.tablet_and_desktop(
            rx.flex(
                rx.icon(
                    icono,
                    size=TAMANO_ICONO_MENU,
                    color=color_contenido,
                ),
                rx.text(
                    etiqueta,
                    font_size="0.875rem",
                    font_weight=rx.cond(esta_activo, "700", "600"),
                    color=color_contenido,
                    white_space="nowrap",
                ),
                align="center",
                gap="0.4rem",
            ),
        ),
        # ==========================================================
        # Estilos del botón
        # ==========================================================
        padding="0.5rem 0.875rem",
        border_radius=RADIO_MEDIO,
        background=rx.cond(
            esta_activo,
            COLOR_ACENTO_SOLIDO,
            "transparent",
        ),
        border=rx.cond(
            esta_activo,
            f"1px solid {COLOR_ACENTO_SOLIDO}",
            "1px solid transparent",
        ),
        box_shadow=rx.cond(
            esta_activo,
            f"0 4px 12px -2px {COLOR_ACENTO_SOLIDO}",
            "none",
        ),
        transition="all 0.2s",
        display="inline-flex",
        align_items="center",
        justify_content="center",
        text_decoration="none",
        _hover=rx.cond(
            esta_activo,
            {},
            {
                "background": COLOR_ACENTO_FONDO,
                "color": COLOR_ACENTO_TEXTO,
            },
        ),
    )


# ======================================================================
# Barra de navegación completa
# ======================================================================


def barra_navegacion_superior() -> rx.Component:
    """
    Barra de navegación superior fija (sticky) con botón de cambio de tema.

    Estructura:
    - Espaciador izquierdo (para centrar el menú).
    - Menú de navegación centrado (contenedor con fondo accent suave).
    - Botón de cambio de tema (derecha).
    - Fondo con efecto glassmorphism (blur).
    """
    return rx.vstack(
        rx.flex(
            # ==========================================================
            # Espaciador izquierdo
            # ==========================================================
            rx.box(),
            # ==========================================================
            # Menú de navegación centrado
            # ==========================================================
            rx.flex(
                elemento_menu("Inicio", "home", "/"),
                elemento_menu("Carreras", "graduation-cap", "/carreras"),
                elemento_menu("Contacto", "map-pin", "/contacto"),
                align="center",
                gap="0.25rem",
                background=COLOR_ACENTO_FONDO,
                border=f"1px solid {COLOR_ACENTO_BORDE}",
                border_radius=RADIO_MEDIO,
                padding="0.25rem",
                flex_shrink="0",
            ),
            # ==========================================================
            # Botón de cambio de tema
            # ==========================================================
            rx.color_mode.button(),
            align="center",
            justify="between",
            width="100%",
            gap="1rem",
        ),
        # ==============================================================
        # Estilos del contenedor de la barra
        # ==============================================================
        align="center",
        justify="between",
        width="100%",
        padding="0.625rem 1rem",
        position="sticky",
        top="0",
        z_index="30",
        background=rx.color_mode_cond(
            light=FONDO_BARRA_LIGHT,
            dark=FONDO_BARRA_DARK,
        ),
        backdrop_filter="blur(12px)",
        border_bottom=f"1px solid {COLOR_ACENTO_BORDE}",
    )


__all__ = [
    "barra_navegacion_superior",
    "elemento_menu",
]