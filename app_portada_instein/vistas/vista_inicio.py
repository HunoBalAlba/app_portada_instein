"""
Vista de la página de inicio (ruta "/").
"""

import reflex as rx

from ..componentes.barra_navegacion import barra_navegacion_superior
from ..componentes.widgets_home import hero_bienvenida
from ..infraestructura.constantes_visuales import (
    NOMBRE_COMPLETO_INSTITUTO,
    NOMBRE_INSTITUTO,
    TELEFONO_PRINCIPAL,
    UBICACION_FISICA,
)

# Nota: estas dos importaciones provienen de módulos externos
# que debes conservar en tu proyecto (portada con video y tutoriales).
from .portada_con_video import portada_inicio_con_video


def _tarjeta_certificacion_institucional() -> rx.Component:
    """Tarjeta con las certificaciones legales del instituto."""
    return rx.box(
        rx.heading(
            "Certificación Institucional",
            size="3",
            text_transform="uppercase",
            margin_bottom="1rem",
        ),
        rx.flex(
            rx.icon("shield-check", size=20, color="#22c55e", margin_top="0.25rem"),
            rx.box(
                rx.text("Resoluciones Ministeriales Vigentes", font_weight="bold"),
                rx.text(
                    "Autorización legal R.M. 0871/2016",
                    color_scheme="gray",
                ),
            ),
            gap="0.75rem",
        ),
        rx.flex(
            rx.icon("award", size=20, color="#3b82f6", margin_top="0.25rem"),
            rx.box(
                rx.text("Nivel Técnico Superior", font_weight="bold"),
                rx.text(
                    "Título en Provisión Nacional.",
                    color_scheme="gray",
                ),
            ),
            gap="0.75rem",
            padding_top="1rem",
            margin_top="1rem",
        ),
        padding="1.5rem",
        border_radius="1.5rem",
        border=f"1px solid {rx.color('accent', 8)}",
        box_shadow="0 1px 2px 0 rgb(0 0 0 / 0.05)",
        margin="0 1rem 1rem 1rem",
    )


def _boton_ver_carreras() -> rx.Component:
    """CTA principal hacia la vista de carreras."""
    return rx.box(
        rx.link(
            rx.flex(
                rx.icon("book-open", size=20, color="#ffffff"),
                rx.text(
                    "Ver Carreras Disponibles",
                    as_="span",
                    font_weight="700",
                ),
                align="center",
                gap="0.75rem",
            ),
            rx.icon("arrow-right", size=20, color="rgba(255,255,255,0.7)"),
            href="/carreras",
            display="flex",
            align_items="center",
            justify_content="space-between",
            width="100%",
            background=rx.color("accent", 11),
            padding="1.25rem",
            border_radius="1rem",
            color="#ffffff",
            box_shadow="0 10px 25px -5px rgb(37 99 235 / 0.25)",
            transition="all 0.2s",
            text_decoration="none",
        ),
        padding="0 1rem",
        margin_bottom="2rem",
    )


def _tarjetas_informacion_rapida() -> rx.Component:
    """Bloque con ubicación e informes de contacto rápido."""
    return rx.flex(
        rx.box(
            rx.icon(
                "map-pin", size=20, color="#60a5fa", margin_bottom="0.5rem"
            ),
            rx.text(
                "Ubicación",
                color_scheme="gray",
                font_weight="700",
                text_transform="uppercase",
            ),
            rx.text(UBICACION_FISICA),
            padding="1rem",
            border_radius="1rem",
            border=f"1px solid {rx.color('accent', 8)}",
            flex="1",
            box_shadow="0 1px 2px 0 rgb(0 0 0 / 0.05)",
            min_width="0",
        ),
        rx.box(
            rx.icon(
                "phone-call", size=20, color="#60a5fa", margin_bottom="0.5rem"
            ),
            rx.text(
                "Informes",
                font_size="0.625rem",
                color_scheme="gray",
                font_weight="700",
                text_transform="uppercase",
            ),
            rx.text(
                TELEFONO_PRINCIPAL,
                font_size="0.75rem",
                font_weight="700",
            ),
            padding="1rem",
            border_radius="1rem",
            border=f"1px solid {rx.color('accent', 8)}",
            flex="1",
            box_shadow="0 1px 2px 0 rgb(0 0 0 / 0.05)",
        ),
        gap="1rem",
        padding="1.5rem 1rem",
    )


@rx.page(route="/", title=f"Inicio | {NOMBRE_INSTITUTO}")
def vista_inicio() -> rx.Component:
    """Página principal de bienvenida del instituto."""
    return rx.vstack(
        barra_navegacion_superior(),
        rx.box(
            rx.flex(hero_bienvenida(), direction="column", spacing="4"),
            rx.box(
                rx.vstack(
                    rx.box(
                        rx.icon("graduation-cap", size=40, color="#ffffff"),
                        background=rx.color("accent", 11),
                        padding="0.75rem",
                        border_radius="1rem",
                        box_shadow="0 10px 25px -5px rgb(37 99 235 / 0.25)",
                        display="flex",
                    ),
                    rx.heading(NOMBRE_INSTITUTO, size="8"),
                    rx.text(
                        NOMBRE_COMPLETO_INSTITUTO,
                        color=rx.color("accent", 11),
                        text_transform="uppercase",
                        text_align="center",
                        max_width="280px",
                    ),
                    align="center",
                    text_align="center",
                    padding="3rem 1.5rem",
                ),
            ),
            rx.vstack(portada_inicio_con_video(), margin_bottom="1rem"),
            _tarjeta_certificacion_institucional(),
            _boton_ver_carreras(),
            _tarjetas_informacion_rapida(),
            padding_bottom="3rem",
            max_width="72rem",
            width="100%",
        ),
        align="center",
        min_height="100vh",
        width="100%",
    )