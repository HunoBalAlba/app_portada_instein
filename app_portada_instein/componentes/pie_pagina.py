"""
Pie de página institucional con:
- Sección de feedback ("¿Te resultó útil?").
- Grid de enlaces organizados por columnas.
- Barra inferior con copyright y estado del servidor.
"""

import reflex as rx

from app_portada_instein.infraestructura.constantes_visuales import (
    ANIO_COPYRIGHT,
    EMAIL_CONTACTO,
    NOMBRE_INSTITUTO,
    TELEFONO_PRINCIPAL,
    WHATSAPP_URL,
)


# ======================================================================
# Estructura de los enlaces del footer
# ======================================================================


def _enlaces_footer() -> list[dict]:
    """
    Define las columnas de enlaces del footer.

    Cada columna tiene un título y una lista de items con
    etiqueta, ruta y si es enlace externo.
    """
    return [
        {
            "titulo": "Documentación",
            "items": [
                {"etiqueta": "Inicio", "ruta": "/", "externo": False},
                {"etiqueta": "Carreras", "ruta": "/carreras", "externo": False},
                {"etiqueta": "Contacto", "ruta": "/contacto", "externo": False},
            ],
        },
        {
            "titulo": "Institucional",
            "items": [
                {"etiqueta": "Sobre nosotros", "ruta": "/", "externo": False},
                {"etiqueta": "Misión y visión", "ruta": "/", "externo": False},
                {"etiqueta": "Autoridades", "ruta": "/", "externo": False},
            ],
        },
        {
            "titulo": "Recursos",
            "items": [
                {"etiqueta": "Blog", "ruta": "/", "externo": False},
                {"etiqueta": "FAQ", "ruta": "/", "externo": False},
                {"etiqueta": "Calendario académico", "ruta": "/", "externo": False},
            ],
        },
        {
            "titulo": "Contacto",
            "items": [
                {
                    "etiqueta": "WhatsApp",
                    "ruta": WHATSAPP_URL,
                    "externo": True,
                },
                {
                    "etiqueta": f"Tel: {TELEFONO_PRINCIPAL}",
                    "ruta": f"tel:+591{TELEFONO_PRINCIPAL}",
                    "externo": True,
                },
                {
                    "etiqueta": EMAIL_CONTACTO,
                    "ruta": f"mailto:{EMAIL_CONTACTO}",
                    "externo": True,
                },
            ],
        },
    ]


# ======================================================================
# Sección de feedback ("¿Te resultó útil?")
# ======================================================================


def _seccion_feedback() -> rx.Component:
    """
    Sección con pregunta de feedback y botones Sí/No.

    En una app real, los botones dispararían eventos al backend
    para registrar la respuesta del usuario.
    """
    return rx.flex(
        rx.text(
            "¿Te resultó útil esta página?",
            font_weight="600",
            font_size="0.875rem",
            color=rx.color_mode_cond(light="#1e293b", dark="#e2e8f0"),
        ),
        rx.flex(
            rx.button(
                rx.icon("thumbs_up", size=14),
                rx.text("Sí", as_="span"),
                size="1",
                variant="soft",
                color_scheme="green",
                cursor="pointer",
            ),
            rx.button(
                rx.icon("thumbs_down", size=14),
                rx.text("No", as_="span"),
                size="1",
                variant="soft",
                color_scheme="red",
                cursor="pointer",
            ),
            rx.link(
                rx.icon("message_square_warning", size=14),
                rx.text("Reportar un problema", as_="span"),
                href="/",
                is_external=True,
                size="1",
                variant="soft",
                color_scheme="gray",
                text_decoration="none",
                display="inline-flex",
                align_items="center",
                gap="0.4rem",
                padding="0.375rem 0.75rem",
                border_radius="0.5rem",
                background=rx.color("gray", 3),
                color=rx.color("gray", 12),
            ),
            gap="0.5rem",
            align="center",
            wrap="wrap",
        ),
        direction="column",
        gap="0.75rem",
        padding="1.5rem 0",
        border_bottom=("1px solid " + rx.color_mode_cond(light="#e2e8f0", dark="#1e293b")),
    )


# ======================================================================
# Columna individual de enlaces
# ======================================================================


def _columna_enlaces(columna: dict) -> rx.Component:
    """Renderiza una columna del footer con su título y sus enlaces."""
    return rx.vstack(
        # --- Título de la columna ---
        rx.text(
            columna["titulo"],
            font_size="0.75rem",
            font_weight="700",
            text_transform="uppercase",
            letter_spacing="0.1em",
            color=rx.color_mode_cond(light="#64748b", dark="#94a3b8"),
            margin_bottom="0.5rem",
        ),
        # --- Enlaces ---
        rx.vstack(
            *[
                rx.link(
                    item["etiqueta"],
                    href=item["ruta"],
                    is_external=item["externo"],
                    font_size="0.875rem",
                    color=rx.color_mode_cond(light="#334155", dark="#cbd5e1"),
                    text_decoration="none",
                    transition="color 0.2s",
                    _hover={
                        "color": rx.color_mode_cond(light="#2563eb", dark="#60a5fa"),
                    },
                )
                for item in columna["items"]
            ],
            gap="0.5rem",
            align="start",
            width="100%",
        ),
        align="start",
        spacing="1",
        width="100%",
    )


# ======================================================================
# Barra inferior con copyright y estado
# ======================================================================
def _barra_inferior() -> rx.Component:
    """Barra inferior del footer con copyright y estado del servidor."""
    return rx.flex(
        # --- Copyright ---
        rx.text(
            f"Copyright © {ANIO_COPYRIGHT} {NOMBRE_INSTITUTO}",
            font_size="0.75rem",
            color=rx.color_mode_cond(light="#64748b", dark="#94a3b8"),
        ),
        # --- Estado del servidor (con borderPulse) ---
        rx.flex(
            rx.box(
                height="0.5rem",
                width="0.5rem",
                border_radius="9999px",
                background="#22c55e",
                animation="pulse 2s ease-in-out infinite",
            ),
            rx.text(
                "Todos los servicios operativos",
                font_size="0.75rem",
                color=rx.color_mode_cond(light="#64748b", dark="#94a3b8"),
            ),
            align="center",
            gap="0.5rem",
            padding="0.5rem 0.875rem",
            border_radius="9999px",
            border="1px solid transparent",
            animation="borderPulse 2.5s ease-in-out infinite",
        ),
        align="center",
        justify="between",
        width="100%",
        padding_top="1.5rem",
        wrap="wrap",
        gap="1rem",
    )


# ======================================================================
# Footer completo
# ======================================================================


def pie_pagina_institucional() -> rx.Component:
    """
    Footer institucional completo con:
    - Sección de feedback.
    - Grid de enlaces por columnas.
    - Barra inferior con copyright y estado del servidor.
    """
    columnas = _enlaces_footer()

    return rx.box(
        rx.vstack(
            # --- Sección de feedback ---
            _seccion_feedback(),
            # --- Grid de columnas de enlaces ---
            rx.grid(
                *[_columna_enlaces(col) for col in columnas],
                columns=rx.breakpoints(
                    initial="1",
                    sm="2",
                    md="2",
                    lg="4",
                ),
                spacing="6",
                width="100%",
                padding="2.5rem 0",
            ),
            # --- Barra inferior ---
            _barra_inferior(),
            spacing="0",
            width="100%",
        ),
        # --- Estilos del contenedor principal ---
        width="100%",
        padding="0 1.5rem",
        max_width="72rem",
        margin="0 auto",
        border_top=("1px solid " + rx.color_mode_cond(light="#e2e8f0", dark="#1e293b")),
        background=rx.color_mode_cond(
            light="linear-gradient(180deg, #ffffff 0%, #f8fafc 100%)",
            dark="linear-gradient(180deg, #0f1117 0%, #0b0914 100%)",
        ),
    )
