# app_portada_instein/componentes/explorador/panel_flotante.py

"""
Panel flotante de selección de carrera — estilo Neon adaptativo.

Estructura:
- Botón flotante (esquina inferior derecha) con azul marino neon.
- Overlay adaptativo cuando el panel está abierto.
- Panel desplegable con grid de cards de carrera.

UX:
- Cada carrera se muestra como una card con imagen destacada arriba
  (patrón `rx.card` + `rx.inset`) y datos debajo.
- Hover de card: borde azul marino + glow azul.
- Click en card: navega al detalle `/carrera/{id}`.

Sistema de color (UX)
---------------------
✅ ADAPTATIVO: todos los colores respetan el color_mode del usuario.

- Fondo del panel: `FONDO_HOME_CARD_ADAPTATIVO`.
- Acentos: azul marino neon (`AZUL_MARINO_NEON` = `#3b5bdb`) en AMBOS modos.
- Texto: `TEXTO_HOME_PRINCIPAL` / `TEXTO_HOME_MAS_SUAVE`.
- Bordes: `BORDE_HOME_AZUL` / `BORDE_HOME_SUAVE`.
- Overlay: negro translúcido con blur (más suave en light).
- Fondo tintado del icono: `FONDO_AZUL_SUAVE`.
"""

import reflex as rx

from app_portada_instein.componentes.primitivos import contenedor_clicable
from app_portada_instein.dominio.estado_institucional import EstadoInstitucional
from app_portada_instein.infraestructura.constantes_visuales import (
    AZUL_MARINO_NEON,
    BORDE_HOME_AZUL,
    BORDE_HOME_SUAVE,
    FONDO_AZUL_SUAVE,
    FONDO_HOME_CARD_ADAPTATIVO,
    RADIO_EXTRA_GRANDE,
    RADIO_MEDIO,
    RADIO_PASTILLA,
    RADIO_PEQUENO,
    SOMBRA_HOVER_CARD_HOME,
    TEXTO_HOME_MAS_SUAVE,
    TEXTO_HOME_PRINCIPAL,
)

from .constantes import TAMANO_BOTON_FLOTANTE


# ======================================================================
# Constantes locales
# ======================================================================

ANCHO_CARD_PANEL = "100%"
ALTURA_BANNER_CARD = "5rem"
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

    ✅ ADAPTATIVO: fondo, textos y borde cambian según el modo.

    Estilo Neon:
    - Fondo con glassmorphism adaptativo.
    - Overlay con gradiente azul marino sobre la imagen.
    - Hover: borde azul + glow azul.
    """
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
                    # Overlay con gradiente azul marino
                    rx.box(
                        position="absolute",
                        top="0",
                        left="0",
                        right="0",
                        bottom="0",
                        background=(
                            f"linear-gradient(180deg, transparent 40%, "
                            f"rgba(59, 91, 219, 0.3) 100%)"
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
                # Icono de la carrera con fondo tintado
                rx.flex(
                    rx.icon(
                        carrera["icono"],
                        size=16,
                        color=AZUL_MARINO_NEON,
                    ),
                    height="2rem",
                    width="2rem",
                    border_radius=RADIO_MEDIO,
                    background=FONDO_AZUL_SUAVE,       # ✅ adaptativo
                    border=f"1px solid {BORDE_HOME_AZUL}",
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
                        color=TEXTO_HOME_PRINCIPAL,    # ✅ adaptativo
                        line_height="1.2",
                    ),
                    rx.text(
                        carrera["duracion"],
                        font_size="0.6875rem",
                        color=TEXTO_HOME_MAS_SUAVE,    # ✅ adaptativo
                        line_height="1.2",
                    ),
                    spacing="0",
                    align="start",
                    flex="1",
                    min_width="0",
                ),
                # Icono de flecha
                rx.icon(
                    "arrow-up-right",
                    size=14,
                    color=TEXTO_HOME_MAS_SUAVE,        # ✅ adaptativo
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
            background=FONDO_HOME_CARD_ADAPTATIVO,      # ✅ adaptativo
            backdrop_filter="blur(12px)",
            border=f"1px solid {BORDE_HOME_SUAVE}",     # ✅ adaptativo
            transition="all 0.2s cubic-bezier(0.4, 0, 0.2, 1)",
            _hover={
                "transform": "translateY(-2px)",
                "border_color": BORDE_HOME_AZUL,
                "box_shadow": SOMBRA_HOVER_CARD_HOME,   # ✅ adaptativo
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

    ✅ ADAPTATIVO: overlay, panel, textos y bordes cambian según el modo.

    Estilo Neon:
    - Botón flotante con azul marino neon + glow.
    - Overlay adaptativo (más suave en light).
    - Panel con glassmorphism y borde azul marino.
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
                background=rx.color_mode_cond(       # ✅ adaptativo
                    light="rgba(15, 23, 42, 0.4)",   # más suave en light
                    dark="rgba(0, 0, 0, 0.6)",
                ),
                backdrop_filter="blur(8px)",
                z_index="998",
                on_click=EstadoInstitucional.cerrar_panel_flotante,
                cursor="pointer",
            ),
            rx.fragment(),
        ),
        # ==========================================================
        # Botón flotante (azul marino neon + glow)
        # ==========================================================
        contenedor_clicable(
            rx.icon("layout-grid", size=22, color="white"),
            position="fixed",
            bottom="2rem",
            right="2rem",
            height=TAMANO_BOTON_FLOTANTE,
            width=TAMANO_BOTON_FLOTANTE,
            border_radius=RADIO_PASTILLA,
            background=AZUL_MARINO_NEON,
            display="flex",
            align_items="center",
            justify_content="center",
            box_shadow=rx.color_mode_cond(           # ✅ adaptativo
                light=f"0 0 30px {AZUL_MARINO_NEON}50",
                dark=f"0 0 40px {AZUL_MARINO_NEON}80",
            ),
            z_index="999",
            transition="all 0.3s",
            al_hacer_clic=EstadoInstitucional.alternar_panel_flotante,
            _hover={
                "transform": "scale(1.1)",
                "box_shadow": f"0 0 60px {AZUL_MARINO_NEON}cc",
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
                                color=TEXTO_HOME_PRINCIPAL,   # ✅ adaptativo
                                line_height="1.2",
                                letter_spacing="-0.02em",
                            ),
                            rx.text(
                                "Accede rápido al detalle",
                                font_size="0.75rem",
                                color=TEXTO_HOME_MAS_SUAVE,   # ✅ adaptativo
                                line_height="1.3",
                            ),
                            spacing="0",
                            align="start",
                        ),
                        contenedor_clicable(
                            rx.icon(
                                "x",
                                size=18,
                                color=TEXTO_HOME_MAS_SUAVE,   # ✅ adaptativo
                            ),
                            padding="0.5rem",
                            border_radius=RADIO_PEQUENO,
                            al_hacer_clic=(
                                EstadoInstitucional.cerrar_panel_flotante
                            ),
                            _hover={
                                "background": rx.color_mode_cond(   # ✅ adaptativo
                                    light="rgba(15, 23, 42, 0.05)",
                                    dark="rgba(255, 255, 255, 0.05)",
                                ),
                                "color": TEXTO_HOME_PRINCIPAL,       # ✅ adaptativo
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
                background=FONDO_HOME_CARD_ADAPTATIVO,       # ✅ adaptativo
                border=f"1px solid {BORDE_HOME_AZUL}",       # ✅ adaptativo
                box_shadow=rx.color_mode_cond(                # ✅ adaptativo
                    light=(
                        f"0 30px 60px -15px rgba(0, 0, 0, 0.15), "
                        f"0 0 40px -10px {AZUL_MARINO_NEON}20"
                    ),
                    dark=(
                        f"0 30px 60px -15px rgba(0, 0, 0, 0.5), "
                        f"0 0 40px -10px {AZUL_MARINO_NEON}40"
                    ),
                ),
                z_index="999",
                animation="deslizar_desde_abajo 0.3s ease-out",
            ),
            rx.fragment(),
        ),
    )


__all__ = ["_panel_flotante_selector"]