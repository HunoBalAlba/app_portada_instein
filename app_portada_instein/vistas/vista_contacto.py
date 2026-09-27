"""
Vista de contacto con teléfonos, dirección, horario y mapa (ruta "/contacto").
"""

import reflex as rx

from app_portada_instein.componentes.barra_navegacion import barra_navegacion_superior
from app_portada_instein.componentes.pie_pagina import pie_pagina_institucional
from app_portada_instein.infraestructura.constantes_visuales import (
    DIRECCION,
    HORARIO_ATENCION,
    NOMBRE_INSTITUTO,
    TELEFONO_PRINCIPAL,
    TELEFONO_SECUNDARIO,
    UBICACION_FISICA,
    WHATSAPP_URL,
)

# Nota: este componente proviene de un módulo externo que debes conservar.
from .tutorial_crear_cuenta import cuadro_de_tutorial


def _tarjeta_telefono() -> rx.Component:
    """Tarjeta con teléfonos y botones de acción (WhatsApp / llamar)."""
    return rx.box(
        rx.flex(
            rx.box(
                rx.icon("phone", color="#2563eb"),
                padding="0.75rem",
                border_radius="0.75rem",
                display="flex",
            ),
            rx.box(
                rx.text("Atención al Cliente"),
                rx.text(
                    f"{TELEFONO_PRINCIPAL} / {TELEFONO_SECUNDARIO}",
                    color_scheme="gray",
                ),
            ),
            align="center",
            gap="1rem",
        ),
        rx.flex(
            rx.link(
                rx.icon("message-circle", size=16, margin_right="0.5rem"),
                rx.text("WhatsApp", as_="span"),
                href=WHATSAPP_URL,
                flex="1",
                background="#22c55e",
                color="#ffffff",
                font_size="0.75rem",
                font_weight="700",
                padding="0.5rem 0.75rem",
                border_radius="0.5rem",
                display="flex",
                align_items="center",
                justify_content="center",
                text_decoration="none",
            ),
            rx.link(
                rx.icon("phone", size=16, margin_right="0.5rem"),
                rx.text("Llamar", as_="span"),
                href=f"tel:+591{TELEFONO_PRINCIPAL}",
                flex="1",
                background="#2563eb",
                color="#ffffff",
                font_size="0.75rem",
                font_weight="700",
                padding="0.5rem 0.75rem",
                border_radius="0.5rem",
                display="flex",
                align_items="center",
                justify_content="center",
                text_decoration="none",
            ),
            gap="0.5rem",
            margin_top="1rem",
        ),
        padding="1.25rem",
        border_radius="1.5rem",
        border=f"1px solid {rx.color('accent', 8)}",
        box_shadow="0 1px 2px 0 rgb(0 0 0 / 0.05)",
        width="100%",
    )


def _tarjeta_direccion() -> rx.Component:
    """Tarjeta con la dirección física exacta."""
    return rx.box(
        rx.flex(
            rx.box(
                rx.icon("map-pin", color="#dc2626"),
                padding="0.75rem",
                border_radius="0.75rem",
                display="flex",
            ),
            rx.box(
                rx.text("Dirección Exacta"),
                rx.text(DIRECCION, color_scheme="gray"),
            ),
            align="center",
            gap="1rem",
            margin_bottom="0.75rem",
        ),
        rx.card(rx.text(UBICACION_FISICA)),
        padding="1.25rem",
        border_radius="1.5rem",
        border=f"1px solid {rx.color('accent', 8)}",
        box_shadow="0 1px 2px 0 rgb(0 0 0 / 0.05)",
        width="100%",
    )


def _tarjeta_horario() -> rx.Component:
    """Tarjeta con el horario de atención."""
    return rx.box(
        rx.flex(
            rx.box(
                rx.icon("clock", color="#2563eb"),
                padding="0.75rem",
                border_radius="0.75rem",
                display="flex",
            ),
            rx.box(
                rx.text(
                    "Horario de Atención",
                    font_size="0.875rem",
                    font_weight="700",
                ),
                rx.text(
                    HORARIO_ATENCION,
                    font_size="0.875rem",
                    color_scheme="gray",
                ),
            ),
            align="center",
            gap="1rem",
        ),
        padding="1.25rem",
        border_radius="1.5rem",
        border=f"1px solid {rx.color('accent', 8)}",
        box_shadow="0 1px 2px 0 rgb(0 0 0 / 0.05)",
        width="100%",
    )


def _bloque_mapa() -> rx.Component:
    """Bloque con placeholder del mapa de ubicación."""
    return rx.box(
        rx.text("Ubícanos en el mapa"),
        rx.box(
            rx.image(
                src="/placeholder.svg",
                width="100%",
                height="10rem",
                object_fit="cover",
                border_radius="1.5rem",
                filter="grayscale(1)",
                opacity="0.7",
            ),
            rx.flex(
                rx.icon("map", size=32, color="#2563eb"),
                position="absolute",
                top="0",
                left="0",
                right="0",
                bottom="0",
                align="center",
                justify="center",
            ),
            position="relative",
            border=f"1px solid {rx.color('accent', 8)}",
            border_radius="1.5rem",
            overflow="hidden",
            box_shadow="0 1px 2px 0 rgb(0 0 0 / 0.05)",
        ),
        width="100%",
    )


@rx.page(route="/contacto", title=f"Contacto | {NOMBRE_INSTITUTO}")
def vista_contacto() -> rx.Component:
    """Página con toda la información de contacto."""
    return rx.vstack(
        barra_navegacion_superior(),
        rx.box(
            rx.vstack(cuadro_de_tutorial(), justify="center", align="center"),
            rx.vstack(
                rx.text("MANTENTE EN CONTACTO"),
                rx.heading("Comunícate con nosotros", size="6"),
                rx.vstack(
                    _tarjeta_telefono(),
                    _tarjeta_direccion(),
                    _tarjeta_horario(),
                    gap="1rem",
                    width="100%",
                ),
                _bloque_mapa(),
                padding="1.5rem 1.5rem 6rem 1.5rem",
            ),
            max_width="72rem",
            width="100%",
        ),
        pie_pagina_institucional(),
        align="center",
        min_height="100vh",
        width="100%",
    )
