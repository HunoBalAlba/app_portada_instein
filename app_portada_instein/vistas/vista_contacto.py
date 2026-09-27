"""
Vista de contacto con teléfonos, dirección, horario y mapa (ruta "/contacto").

Diseño UX:
- Hero de bienvenida con título y subtítulo.
- Grid de 3 tarjetas de contacto (teléfono, dirección, horario).
- Mapa de Google Maps embebido con coordenadas reales del instituto.
- CTA final con WhatsApp.
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


# ======================================================================
# Constantes locales
# ======================================================================

# Coordenadas del INSTEIN (16°30'30.3"S 68°09'48.7"W → decimal).
LATITUD = -16.5084167
LONGITUD = -68.1635278

# Colores semánticos reutilizados.
COLOR_AZUL = "#2563eb"
COLOR_VERDE = "#22c55e"
COLOR_ROJO = "#dc2626"
COLOR_AZUL_SUAVE = "#eff6ff"
COLOR_VERDE_SUAVE = "#f0fdf4"
COLOR_ROJO_SUAVE = "#fef2f2"


# ======================================================================
# Tarjeta base reutilizable (patrón DRY)
# ======================================================================


def _tarjeta_base(
    *children: rx.Component,
    **props,
) -> rx.Component:
    """
    Tarjeta base con estilos consistentes.

    Reutilizada por todas las tarjetas de contacto para mantener
    coherencia visual (padding, border-radius, hover).
    """
    props.setdefault("padding", "1.5rem")
    props.setdefault("border_radius", "1.25rem")
    props.setdefault(
        "background",
        rx.color_mode_cond(light="#ffffff", dark="#0f1117"),
    )
    props.setdefault(
        "border",
        "1px solid " + rx.color_mode_cond(light="#e2e8f0", dark="#1e293b"),
    )
    props.setdefault("box_shadow", "0 1px 3px 0 rgb(0 0 0 / 0.05)")
    props.setdefault("width", "100%")
    props.setdefault("height", "100%")
    props.setdefault(
        "transition",
        "all 0.25s cubic-bezier(0.4, 0, 0.2, 1)",
    )

    return rx.box(*children, **props)


def _icono_tarjeta(icono: str, color: str) -> rx.Component:
    """Icono con fondo tintado, reutilizado en todas las tarjetas."""
    return rx.box(
        rx.icon(tag=icono, size=22, color=color),
        padding="0.75rem",
        border_radius="0.875rem",
        background=color + "15",
        display="flex",
        align_items="center",
        justify_content="center",
        flex_shrink="0",
    )


# ======================================================================
# Tarjeta de teléfono
# ======================================================================


def _tarjeta_telefono() -> rx.Component:
    """
    Tarjeta con teléfonos y botones de acción.

    Jerarquía:
    1. WhatsApp (primario, verde).
    2. Llamar (secundario, azul).
    """
    return _tarjeta_base(
        rx.vstack(
            # --- Header: icono + título ---
            rx.flex(
                _icono_tarjeta("phone", COLOR_AZUL),
                rx.vstack(
                    rx.text(
                        "Atención al Cliente",
                        font_size="0.75rem",
                        font_weight="700",
                        color=rx.color_mode_cond(light="#64748b", dark="#94a3b8"),
                        text_transform="uppercase",
                        letter_spacing="0.05em",
                        line_height="1.1",
                    ),
                    rx.text(
                        f"{TELEFONO_PRINCIPAL}",
                        font_size="1.125rem",
                        font_weight="800",
                        color=rx.color_mode_cond(light="#0f172a", dark="#f1f5f9"),
                        line_height="1.2",
                    ),
                    rx.text(
                        f"Alterno: {TELEFONO_SECUNDARIO}",
                        font_size="0.75rem",
                        color=rx.color_mode_cond(light="#64748b", dark="#94a3b8"),
                        line_height="1.2",
                    ),
                    spacing="1",
                    align="start",
                    flex="1",
                ),
                align="start",
                gap="1rem",
                width="100%",
            ),
            # --- Botones ---
            rx.flex(
                _boton_accion(
                    icono="message-circle",
                    etiqueta="WhatsApp",
                    href=WHATSAPP_URL,
                    color=COLOR_VERDE,
                    externo=True,
                ),
                _boton_accion(
                    icono="phone",
                    etiqueta="Llamar",
                    href=f"tel:+591{TELEFONO_PRINCIPAL}",
                    color=COLOR_AZUL,
                    externo=True,
                ),
                gap="0.5rem",
                width="100%",
                margin_top="1.25rem",
                flex_direction=["column", "row", "row"],
            ),
            spacing="0",
            width="100%",
            height="100%",
        ),
        _hover={
            "border_color": COLOR_AZUL + "55",
            "transform": "translateY(-2px)",
            "box_shadow": "0 12px 30px -10px rgb(37 99 235 / 0.2)",
        },
    )


# ======================================================================
# Tarjeta de dirección
# ======================================================================


def _tarjeta_direccion() -> rx.Component:
    """Tarjeta con la dirección física exacta y referencia."""
    return _tarjeta_base(
        rx.vstack(
            # --- Header ---
            rx.flex(
                _icono_tarjeta("map-pin", COLOR_ROJO),
                rx.vstack(
                    rx.text(
                        "Dirección Exacta",
                        font_size="0.75rem",
                        font_weight="700",
                        color=rx.color_mode_cond(light="#64748b", dark="#94a3b8"),
                        text_transform="uppercase",
                        letter_spacing="0.05em",
                        line_height="1.1",
                    ),
                    rx.text(
                        DIRECCION,
                        font_size="0.9375rem",
                        font_weight="700",
                        color=rx.color_mode_cond(light="#0f172a", dark="#f1f5f9"),
                        line_height="1.3",
                    ),
                    spacing="1",
                    align="start",
                    flex="1",
                ),
                align="start",
                gap="1rem",
                width="100%",
            ),
            # --- Referencia ---
            rx.box(
                rx.flex(
                    rx.icon("building-2", size=14, color=COLOR_ROJO),
                    rx.text(
                        UBICACION_FISICA,
                        font_size="0.8125rem",
                        font_weight="600",
                        color=rx.color_mode_cond(light="#334155", dark="#cbd5e1"),
                    ),
                    align="center",
                    gap="0.5rem",
                ),
                padding="0.75rem 1rem",
                border_radius="0.75rem",
                background=rx.color_mode_cond(light="#fef2f2", dark="#1e293b"),
                border="1px solid " + rx.color_mode_cond(light="#fecaca", dark="#334155"),
                margin_top="1.25rem",
                width="100%",
            ),
            spacing="0",
            width="100%",
            height="100%",
        ),
        _hover={
            "border_color": COLOR_ROJO + "55",
            "transform": "translateY(-2px)",
            "box_shadow": "0 12px 30px -10px rgb(220 38 38 / 0.2)",
        },
    )


# ======================================================================
# Tarjeta de horario
# ======================================================================


def _tarjeta_horario() -> rx.Component:
    """Tarjeta con el horario de atención + badge de abierto/cerrado."""
    return _tarjeta_base(
        rx.vstack(
            # --- Header ---
            rx.flex(
                _icono_tarjeta("clock", COLOR_AZUL),
                rx.vstack(
                    rx.text(
                        "Horario de Atención",
                        font_size="0.75rem",
                        font_weight="700",
                        color=rx.color_mode_cond(light="#64748b", dark="#94a3b8"),
                        text_transform="uppercase",
                        letter_spacing="0.05em",
                        line_height="1.1",
                    ),
                    rx.text(
                        HORARIO_ATENCION,
                        font_size="0.9375rem",
                        font_weight="700",
                        color=rx.color_mode_cond(light="#0f172a", dark="#f1f5f9"),
                        line_height="1.3",
                    ),
                    spacing="1",
                    align="start",
                    flex="1",
                ),
                align="start",
                gap="1rem",
                width="100%",
            ),
            # --- Badge de disponibilidad ---
            rx.flex(
                rx.box(
                    width="0.5rem",
                    height="0.5rem",
                    border_radius="9999px",
                    background=COLOR_VERDE,
                    animation="pulse 2s ease-in-out infinite",
                ),
                rx.text(
                    "Atención presencial y telefónica",
                    font_size="0.75rem",
                    font_weight="600",
                    color=rx.color_mode_cond(light="#15803d", dark="#4ade80"),
                ),
                align="center",
                gap="0.5rem",
                padding="0.5rem 0.875rem",
                border_radius="9999px",
                background=COLOR_VERDE_SUAVE,
                margin_top="1.25rem",
                width="fit-content",
            ),
            spacing="0",
            width="100%",
            height="100%",
        ),
        _hover={
            "border_color": COLOR_AZUL + "55",
            "transform": "translateY(-2px)",
            "box_shadow": "0 12px 30px -10px rgb(37 99 235 / 0.2)",
        },
    )


# ======================================================================
# Botón de acción reutilizable
# ======================================================================


def _boton_accion(
    icono: str,
    etiqueta: str,
    href: str,
    color: str,
    externo: bool = False,
) -> rx.Component:
    """Botón de acción con icono + etiqueta, reutilizable."""
    return rx.link(
        rx.icon(tag=icono, size=16, color="#ffffff"),
        rx.text(
            etiqueta,
            font_size="0.8125rem",
            font_weight="700",
            color="#ffffff",
        ),
        href=href,
        is_external=externo,
        display="flex",
        align_items="center",
        justify_content="center",
        gap="0.5rem",
        padding="0.625rem 1rem",
        border_radius="0.75rem",
        background=color,
        text_decoration="none",
        flex="1",
        transition="all 0.2s",
        _hover={
            "transform": "translateY(-1px)",
            "filter": "brightness(1.1)",
            "box_shadow": f"0 8px 16px -4px {color}80",
        },
    )


# ======================================================================
# Bloque de mapa con Google Maps embebido
# ======================================================================


def _bloque_mapa() -> rx.Component:
    """
    Bloque con Google Maps embebido en la ubicación real del instituto.

    Coordenadas: 16°30'30.3"S 68°09'48.7"W → -16.5084167, -68.1635278
    """
    url_mapa = (
        f"https://www.google.com/maps"
        f"?q={LATITUD},{LONGITUD}"
        f"&hl=es"
        f"&z=17"
        f"&output=embed"
    )

    url_como_llegar = (
        f"https://www.google.com/maps/dir/?api=1"
        f"&destination={LATITUD},{LONGITUD}"
    )

    return rx.vstack(
        # --- Encabezado ---
        rx.flex(
            rx.icon("map-pin", size=22, color=COLOR_ROJO),
            rx.vstack(
                rx.heading(
                    "Ubícanos en el mapa",
                    size="5",
                    font_weight="700",
                    color=rx.color_mode_cond(light="#0f172a", dark="#f1f5f9"),
                ),
                rx.text(
                    "Estamos en una ubicación céntrica y de fácil acceso.",
                    font_size="0.875rem",
                    color=rx.color_mode_cond(light="#64748b", dark="#94a3b8"),
                ),
                spacing="1",
                align="start",
            ),
            align="center",
            gap="0.75rem",
            width="100%",
            margin_bottom="1.5rem",
        ),
        # --- Iframe de Google Maps ---
        rx.box(
            rx.el.iframe(
                src=url_mapa,
                width="100%",
                height="100%",
                style={"border": "0"},
                loading="lazy",
                referrer_policy="no-referrer-when-downgrade",
                allow_fullscreen=True,
            ),
            width="100%",
            height=["20rem", "24rem", "28rem"],
            border_radius="1.5rem",
            overflow="hidden",
            border="1px solid " + rx.color_mode_cond(light="#e2e8f0", dark="#334155"),
            box_shadow="0 4px 12px -2px rgb(0 0 0 / 0.08)",
        ),
        # --- Grid de datos de ubicación ---
        rx.flex(
            _ubicacion_item(
                icono="map-pin",
                etiqueta="Dirección",
                valor=DIRECCION,
                color=COLOR_ROJO,
            ),
            _ubicacion_item(
                icono="building-2",
                etiqueta="Referencia",
                valor=UBICACION_FISICA,
                color=COLOR_AZUL,
            ),
            _ubicacion_item(
                icono="compass",
                etiqueta="Coordenadas",
                valor='16°30\'30.3"S 68°09\'48.7"W',
                color=COLOR_VERDE,
            ),
            gap="1rem",
            width="100%",
            margin_top="1.5rem",
            flex_wrap="wrap",
        ),
        # --- Botón "Cómo llegar" ---
        rx.link(
            rx.flex(
                rx.icon("navigation", size=16, color="#ffffff"),
                rx.text(
                    "Cómo llegar",
                    font_size="0.875rem",
                    font_weight="700",
                    color="#ffffff",
                ),
                align="center",
                gap="0.5rem",
            ),
            href=url_como_llegar,
            is_external=True,
            text_decoration="none",
            padding="0.75rem 1.5rem",
            border_radius="9999px",
            background=COLOR_AZUL,
            box_shadow="0 8px 20px -4px rgb(37 99 235 / 0.4)",
            transition="all 0.2s",
            margin_top="1.5rem",
            width="fit-content",
            _hover={
                "transform": "translateY(-2px)",
                "box_shadow": "0 12px 30px -6px rgb(37 99 235 / 0.5)",
            },
        ),
        spacing="0",
        width="100%",
        align="start",
    )


def _ubicacion_item(
    icono: str,
    etiqueta: str,
    valor: str,
    color: str,
) -> rx.Component:
    """Item de ubicación (dirección, referencia, coordenadas)."""
    return rx.flex(
        _icono_tarjeta(icono, color),
        rx.vstack(
            rx.text(
                etiqueta,
                font_size="0.6875rem",
                font_weight="700",
                color=rx.color_mode_cond(light="#64748b", dark="#94a3b8"),
                text_transform="uppercase",
                letter_spacing="0.05em",
                line_height="1.1",
            ),
            rx.text(
                valor,
                font_size="0.8125rem",
                font_weight="600",
                color=rx.color_mode_cond(light="#0f172a", dark="#f1f5f9"),
                line_height="1.3",
            ),
            spacing="1",
            align="start",
        ),
        align="center",
        gap="0.75rem",
        flex="1",
        min_width="220px",
        padding="1rem",
        border_radius="1rem",
        background=rx.color_mode_cond(light="#f8fafc", dark="#1e293b"),
        border="1px solid " + rx.color_mode_cond(light="#e2e8f0", dark="#334155"),
    )


# ======================================================================
# Vista completa
# ======================================================================


@rx.page(route="/contacto", title=f"Contacto | {NOMBRE_INSTITUTO}")
def vista_contacto() -> rx.Component:
    """
    Página de contacto con:
    1. Barra de navegación superior.
    2. Hero de bienvenida.
    3. Grid de 3 tarjetas de contacto.
    4. Mapa embebido + datos de ubicación.
    5. Sección de tutorial (cuenta institucional).
    6. Pie de página.
    """
    return rx.vstack(
        # --- Barra de navegación ---
        barra_navegacion_superior(),
        # --- Contenido principal ---
        rx.box(
            # =========================================================
            # HERO: Título + Subtítulo
            # =========================================================
            rx.vstack(
                rx.flex(
                    rx.box(
                        width="0.5rem",
                        height="0.5rem",
                        border_radius="9999px",
                        background=COLOR_VERDE,
                        animation="pulse 2s ease-in-out infinite",
                    ),
                    rx.text(
                        "MANTENTE EN CONTACTO",
                        font_size="0.75rem",
                        font_weight="700",
                        color=rx.color_mode_cond(light="#64748b", dark="#94a3b8"),
                        letter_spacing="0.15em",
                    ),
                    align="center",
                    gap="0.5rem",
                ),
                rx.heading(
                    "Comunícate con nosotros",
                    size="8",
                    font_weight="800",
                    color=rx.color_mode_cond(light="#0f172a", dark="#f1f5f9"),
                    text_align="center",
                    line_height="1.1",
                ),
                rx.text(
                    "Estamos disponibles para resolver tus dudas sobre admisiones, "
                    "carreras, horarios y toda la información institucional.",
                    font_size="1rem",
                    color=rx.color_mode_cond(light="#64748b", dark="#94a3b8"),
                    text_align="center",
                    max_width="42rem",
                    line_height="1.6",
                ),
                align="center",
                spacing="3",
                margin_bottom="3rem",
                width="100%",
            ),
            # =========================================================
            # GRID DE TARJETAS DE CONTACTO
            # =========================================================
            rx.grid(
                _tarjeta_telefono(),
                _tarjeta_direccion(),
                _tarjeta_horario(),
                columns=rx.breakpoints(
                    initial="1",
                    sm="1",
                    md="2",
                    lg="3",
                ),
                spacing="4",
                width="100%",
                margin_bottom="3rem",
                align_items="stretch",
            ),
            # =========================================================
            # MAPA
            # =========================================================
            rx.box(
                _bloque_mapa(),
                width="100%",
                margin_bottom="3rem",
            ),
            # =========================================================
            # TUTORIAL (cuenta institucional)
            # =========================================================
            rx.box(
                rx.vstack(
                    rx.heading(
                        "Plataforma de Seguimiento Académico",
                        size="6",
                        font_weight="700",
                        color=rx.color_mode_cond(light="#0f172a", dark="#f1f5f9"),
                        text_align="center",
                    ),
                    rx.text(
                        "Crea tu cuenta institucional y accede a tu historial académico.",
                        font_size="0.9375rem",
                        color=rx.color_mode_cond(light="#64748b", dark="#94a3b8"),
                        text_align="center",
                        max_width="42rem",
                    ),
                    rx.box(
                        cuadro_de_tutorial(),
                        margin_top="1.5rem",
                        width="100%",
                        display="flex",
                        justify_content="center",
                    ),
                    align="center",
                    spacing="2",
                    width="100%",
                ),
                width="100%",
            ),
            # --- Layout del contenedor principal ---
            max_width="72rem",
            margin="0 auto",
            padding="3rem 1.5rem 6rem 1.5rem",
            width="100%",
        ),
        # --- Pie de página ---
        pie_pagina_institucional(),
        align="center",
        min_height="100vh",
        width="100%",
    )