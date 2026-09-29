"""
Panel flotante de selección de carrera (botón + overlay + panel).
"""

import reflex as rx

from app_portada_instein.componentes.primitivos import contenedor_clicable
from app_portada_instein.dominio.estado_institucional import EstadoInstitucional
from app_portada_instein.infraestructura.constantes_visuales import (
    COLOR_ACENTO_SOLIDO,
    COLOR_BORDE_SUAVE,
    COLOR_FONDO_CARTA,
    COLOR_FONDO_SUAVE,
    COLOR_TEXTO_PRINCIPAL,
    COLOR_TEXTO_SECUNDARIO,
    RADIO_EXTRA_GRANDE,
    RADIO_PASTILLA,
    RADIO_PEQUENO,
)

from .buscador import _card_imagen_carrera
from .constantes import TAMANO_BOTON_FLOTANTE


def _panel_flotante_selector() -> rx.Component:
    """
    Botón flotante que abre un panel con todas las carreras.

    Cada tarjeta del panel NAVEGA al detalle de la carrera.

    UX:
    - Botón con accent institucional (crimson) — es un control global.
    - Overlay oscuro cuando está abierto.
    - Panel desplegable con grid de carreras.
    """
    return rx.box(
        # --- Overlay de fondo (solo cuando está abierto) ---
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
        # --- Botón flotante (accent institucional) ---
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
        # --- Panel desplegable ---
        rx.cond(
            EstadoInstitucional.mostrar_panel_flotante,
            rx.box(
                rx.vstack(
                    # --- Cabecera del panel ---
                    rx.flex(
                        rx.heading(
                            "Elige una carrera",
                            size="4",
                            color=COLOR_TEXTO_PRINCIPAL,
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
                            _hover={"background": COLOR_FONDO_SUAVE},
                        ),
                        align="center",
                        justify="between",
                        width="100%",
                        margin_bottom="1rem",
                    ),
                    # --- Grid de carreras ---
                    rx.grid(
                        rx.foreach(
                            EstadoInstitucional.carreras,
                            _card_imagen_carrera,
                        ),
                        columns=rx.breakpoints(initial="1", sm="2"),
                        spacing="3",
                        width="100%",
                    ),
                    spacing="2",
                    width="100%",
                ),
                position="fixed",
                bottom="6rem",
                right="2rem",
                width=[
                    "calc(100% - 4rem)",
                    "calc(100% - 4rem)",
                    "24rem",
                    "28rem",
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