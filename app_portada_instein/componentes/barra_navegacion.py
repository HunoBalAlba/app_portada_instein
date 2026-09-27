"""
Barra de navegación superior con enlaces a las rutas principales
y botón de cambio de tema (claro/oscuro).
"""

import reflex as rx

from app_portada_instein.componentes.primitivos import enlace_navegacion
from app_portada_instein.dominio.estado_institucional import EstadoInstitucional


def elemento_menu(etiqueta: str, icono: str, ruta: str) -> rx.Component:
    """
    Elemento individual del menú de navegación, con estado activo.

    Compara la ruta activa normalizada para marcar correctamente
    el elemento activo, incluyendo la raíz "/".
    """
    # Comparamos contra la ruta normalizada para manejar "/", "", "/index"
    esta_activo = EstadoInstitucional.ruta_activa_normalizada == ruta

    return enlace_navegacion(
        ruta,
        # --- Vista móvil: solo icono ---
        rx.mobile_only(
            rx.flex(
                rx.icon(
                    icono,
                    size=26,
                    color=rx.cond(
                        esta_activo,
                        rx.color("accent", 6),
                        rx.color("accent", 11),
                    ),
                ),
            ),
        ),
        # --- Vista tablet/desktop: icono + texto ---
        rx.tablet_and_desktop(
            rx.flex(
                rx.icon(
                    icono,
                    size=26,
                    color=rx.cond(
                        esta_activo,
                        rx.color("accent", 6),
                        rx.color("accent", 11),
                    ),
                ),
                rx.text(
                    etiqueta,
                    color=rx.cond(
                        esta_activo,
                        rx.color("accent", 6),
                        rx.color("accent", 11),
                    ),
                ),
                align="center",
                gap="0.4rem",
            ),
        ),
        padding="0.5rem",
        border_radius="0.75rem",
        background=rx.cond(esta_activo, rx.color("accent", 11), "transparent"),
        border=rx.cond(
            esta_activo,
            f"1px solid {rx.color('accent', 11)}",
            f"1px solid {rx.color('accent', 8)}",
        ),
        box_shadow=rx.cond(
            esta_activo,
            "0 4px 12px -2px rgb(37 99 235 / 0.3)",
            "none",
        ),
        transition="all 0.2s",
        display="inline-flex",
        align_items="center",
        justify_content="center",
    )


def barra_navegacion_superior() -> rx.Component:
    """Barra de navegación superior fija con botón de cambio de tema."""
    return rx.vstack(
        rx.flex(
            # --- Espaciador izquierdo ---
            rx.box(),
            # --- Menú de navegación centrado ---
            rx.flex(
                elemento_menu("Inicio", "home", "/"),
                elemento_menu("Carreras", "graduation-cap", "/carreras"),
                elemento_menu("Contacto", "map-pin", "/contacto"),
                align="center",
                gap="0.25rem",
                background=rx.color("accent", 1),
                border_radius="0.75rem",
                padding="0.25rem",
                flex_shrink="0",
            ),
            # --- Botón de cambio de tema ---
            rx.color_mode.button(),
            align="center",
            justify="between",
            width="100%",
            gap="1rem",
        ),
        align="center",
        justify="between",
        width="100%",
        padding="0.625rem 1rem",
        position="sticky",
        top="0",
        z_index="30",
        background=rx.color_mode_cond(
            light="rgba(255,255,255,0.85)",
            dark="rgba(15,15,20,0.85)",
        ),
        backdrop_filter="blur(12px)",
    )
