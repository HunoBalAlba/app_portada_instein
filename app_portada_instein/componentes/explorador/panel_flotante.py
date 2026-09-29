"""
Panel flotante de selección de carrera.

Estructura:
- Botón flotante (esquina inferior derecha) con accent institucional.
- Overlay oscuro cuando el panel está abierto.
- Panel desplegable con grid de cards de carrera.

UX:
- Cada carrera se muestra como una card con imagen destacada arriba
  (patrón `rx.card` + `rx.inset`) y datos debajo.
- Hover de card: borde + sombra del color de la carrera.
- Click en card: navega al detalle `/carrera/{id}`.
"""

import reflex as rx

from app_portada_instein.componentes.primitivos import contenedor_clicable
from app_portada_instein.dominio.estado_institucional import EstadoInstitucional
from app_portada_instein.infraestructura.constantes_visuales import (
    COLOR_ACENTO_SOLIDO,
    COLOR_BORDE_SUAVE,
    COLOR_FONDO_CARTA,
    COLOR_FONDO_SUAVE,
    COLOR_TEXTO_CUERPO,
    COLOR_TEXTO_PRINCIPAL,
    COLOR_TEXTO_SECUNDARIO,
    RADIO_EXTRA_GRANDE,
    RADIO_GRANDE,
    RADIO_MEDIO,
    RADIO_PASTILLA,
    RADIO_PEQUENO,
)

# ✅ Imports relativos (NO absolutos desde el propio paquete)
from .constantes import TAMANO_BOTON_FLOTANTE
from .helpers import color_carrera


# ======================================================================
# Constantes locales
# ======================================================================

# Ancho de las cards de carrera en el panel.
ANCHO_CARD_PANEL = "100%"

# Altura del banner (imagen) de la card.
ALTURA_BANNER_CARD = "5rem"

# Ancho máximo del panel flotante.
ANCHO_MAXIMO_PANEL = ["24rem", "28rem"]


# ======================================================================
# Card individual de carrera en el panel
# ======================================================================


def _card_carrera_panel(carrera: dict) -> rx.Component:
    """
    Card de carrera con imagen destacada arriba + datos debajo.

    Sigue el patrón `rx.card` + `rx.inset(side="top", pb="current")`:
    - Inset top: imagen horizontal (banner).
    - Contenido: nombre + duración + icono.

    UX:
    - La imagen usa `imagen_banner` de la carrera.
    - El borde y hover usan el color de marca de la carrera.
    - Click navega al detalle.
    """
    color = color_carrera(carrera)

    return rx.link(
        rx.card(
            # ==========================================================
            # Inset top: imagen de la carrera
            # ==========================================================
            rx.inset(
                rx.box(
                    rx.image(
                        src="/" + carrera["imagen_banner"],
                        alt=carrera["nombre"],
                        width="100%",
                        height="100%",
                        object_fit="cover",
                    ),
                    # Overlay sutil con el color de la carrera
                    rx.box(
                        position="absolute",
                        top="0",
                        left="0",
                        right="0",
                        bottom="0",
                        background=rx.color_mode_cond(
                            light=(
                                f"linear-gradient(180deg, transparent 40%, "
                                f"{carrera['color_principal']}33 100%)"
                            ),
                            dark=(
                                f"linear-gradient(180deg, transparent 40%, "
                                f"{carrera['color_principal_dark']}33 100%)"
                            ),
                        ),
                        pointer_events="none",
                    ),
                    position="relative",
                    width="100%",
                    height=ALTURA_BANNER_CARD,
                    overflow="hidden",
                    border_radius=RADIO_MEDIO,
                ),
                side="top",
                pb="current",
            ),
            # ==========================================================
            # Contenido: nombre + duración
            # ==========================================================
            rx.flex(
                # Icono de la carrera con fondo suave
                rx.flex(
                    rx.icon(
                        carrera["icono"],
                        size=16,
                        color=color,
                    ),
                    height="2rem",
                    width="2rem",
                    border_radius=RADIO_MEDIO,
                    background=rx.color_mode_cond(
                        light=f"{carrera['color_principal']}15",
                        dark=f"{carrera['color_principal_dark']}20",
                    ),
                    border=f"1px solid {color}",
                    align="center",
                    justify="center",
                    flex_shrink="0",
                ),
                # Nombre + duración
                rx.vstack(
                    rx.text(
                        carrera["nombre_corto"],
                        font_size="0.875rem",
                        font_weight="700",
                        color=COLOR_TEXTO_PRINCIPAL,
                        line_height="1.2",
                    ),
                    rx.text(
                        carrera["duracion"],
                        font_size="0.6875rem",
                        color=COLOR_TEXTO_SECUNDARIO,
                        line_height="1.2",
                    ),
                    spacing="0",
                    align="start",
                    flex="1",
                    min_width="0",
                ),
                # Icono de flecha (indica navegación)
                rx.icon(
                    "arrow-up-right",
                    size=14,
                    color=COLOR_TEXTO_SECUNDARIO,
                    flex_shrink="0",
                ),
                align="center",
                gap="0.625rem",
                width="100%",
            ),
            # ==========================================================
            # Estilos de la card
            # ==========================================================
            width=ANCHO_CARD_PANEL,
            padding="0.5rem",
            cursor="pointer",
            transition="all 0.2s cubic-bezier(0.4, 0, 0.2, 1)",
            _hover={
                "transform": "translateY(-2px)",
                "border_color": color,
                "box_shadow": f"0 10px 25px -8px {color}",
            },
        ),
        href=f"/carrera/{carrera['id']}",
        text_decoration="none",
        width="100%",
    )


# ======================================================================
# Panel flotante completo
# ======================================================================


def _panel_flotante_selector() -> rx.Component:
    """
    Botón flotante que abre un panel con todas las carreras.

    Cada card del panel NAVEGA al detalle de la carrera.

    UX:
    - Botón con accent institucional (crimson) — es un control global.
    - Overlay oscuro cuando está abierto (con cierre al hacer click).
    - Panel desplegable con grid responsive de cards de carrera.
    """
    return rx.box(
        # ==========================================================
        # Overlay de fondo (solo cuando está abierto)
        # ==========================================================
        rx.cond(
            EstadoInstitucional.mostrar_panel_flotante,
            rx.box(
                position="fixed",
                top="0",
                left="0",
                right="0",
                bottom="0",
                background="rgba(0,0,0,0.5)",
                backdrop_filter="blur(4px)",
                z_index="998",
                on_click=EstadoInstitucional.cerrar_panel_flotante,
                cursor="pointer",
            ),
            rx.fragment(),
        ),
        # ==========================================================
        # Botón flotante (accent institucional)
        # ==========================================================
        contenedor_clicable(
            rx.icon("layout-grid", size=22, color="white"),
            position="fixed",
            bottom="2rem",
            right="2rem",
            height=TAMANO_BOTON_FLOTANTE,
            width=TAMANO_BOTON_FLOTANTE,
            border_radius=RADIO_PASTILLA,
            background=COLOR_ACENTO_SOLIDO,
            display="flex",
            align_items="center",
            justify_content="center",
            box_shadow=f"0 20px 40px -10px {COLOR_ACENTO_SOLIDO}",
            z_index="999",
            transition="all 0.3s",
            al_hacer_clic=EstadoInstitucional.alternar_panel_flotante,
            _hover={
                "transform": "scale(1.1)",
                "box_shadow": f"0 25px 50px -12px {COLOR_ACENTO_SOLIDO}",
            },
        ),
        # ==========================================================
        # Panel desplegable
        # ==========================================================
        rx.cond(
            EstadoInstitucional.mostrar_panel_flotante,
            rx.box(
                rx.vstack(
                    # ==================================================
                    # Cabecera: título + botón cerrar
                    # ==================================================
                    rx.flex(
                        rx.vstack(
                            rx.text(
                                "Elige una carrera",
                                font_size="1rem",
                                font_weight="800",
                                color=COLOR_TEXTO_PRINCIPAL,
                                line_height="1.2",
                            ),
                            rx.text(
                                "Accede rápido al detalle",
                                font_size="0.75rem",
                                color=COLOR_TEXTO_SECUNDARIO,
                                line_height="1.3",
                            ),
                            spacing="0",
                            align="start",
                        ),
                        contenedor_clicable(
                            rx.icon(
                                "x",
                                size=18,
                                color=COLOR_TEXTO_SECUNDARIO,
                            ),
                            padding="0.5rem",
                            border_radius=RADIO_PEQUENO,
                            al_hacer_clic=EstadoInstitucional.cerrar_panel_flotante,
                            _hover={
                                "background": COLOR_FONDO_SUAVE,
                                "color": COLOR_TEXTO_PRINCIPAL,
                            },
                        ),
                        align="center",
                        justify="between",
                        width="100%",
                        margin_bottom="1rem",
                    ),
                    # ==================================================
                    # Grid de cards de carreras
                    # ==================================================
                    rx.grid(
                        rx.foreach(
                            EstadoInstitucional.carreras,
                            _card_carrera_panel,
                        ),
                        columns=rx.breakpoints(initial="1", sm="1"),
                        spacing="3",
                        width="100%",
                    ),
                    spacing="2",
                    width="100%",
                ),
                # ==================================================
                # Estilos del panel
                # ==================================================
                position="fixed",
                bottom="6rem",
                right="2rem",
                width=[
                    "calc(100% - 4rem)",
                    "calc(100% - 4rem)",
                    "22rem",
                    "26rem",
                ],
                max_height="70vh",
                overflow_y="auto",
                padding="1.5rem",
                border_radius=RADIO_EXTRA_GRANDE,
                background=COLOR_FONDO_CARTA,
                border=f"1px solid {COLOR_BORDE_SUAVE}",
                box_shadow="0 30px 60px -15px rgba(0,0,0,0.4)",
                z_index="999",
                animation="deslizar_desde_abajo 0.3s ease-out",
            ),
            rx.fragment(),
        ),
    )


__all__ = ["_panel_flotante_selector"]