"""
Vista de contacto con teléfonos, dirección, horario y mapa (ruta "/contacto").

Diseño UX:
- Hero de bienvenida con título y subtítulo.
- Grid de 3 tarjetas de contacto (teléfono, dirección, horario).
- Mapa de Google Maps embebido con coordenadas reales del instituto.
- Sección de tutorial (crear cuenta institucional).
- CTA final con WhatsApp.

Todos los colores usan tokens Radix adaptativos al color_mode.
Los colores semánticos (azul, verde, rojo) se expresan como `rx.color()`
con la escala correcta para fondos, bordes y textos.
"""

import reflex as rx

from app_portada_instein.componentes.barra_navegacion import barra_navegacion_superior
from app_portada_instein.componentes.pie_pagina import pie_pagina_institucional
from app_portada_instein.infraestructura.constantes_visuales import (
    ANCHO_CONTENIDO,
    COLOR_BORDE_SUAVE,
    COLOR_FONDO_CARTA,
    COLOR_FONDO_SUAVE,
    COLOR_TEXTO_CUERPO,
    COLOR_TEXTO_PRINCIPAL,
    COLOR_TEXTO_SECUNDARIO,
    DIRECCION,
    HORARIO_ATENCION,
    NOMBRE_INSTITUTO,
    PADDING_LATERAL,
    RADIO_EXTRA_GRANDE,
    RADIO_GRANDE,
    RADIO_MEDIO,
    RADIO_PASTILLA,
    SOMBRA_SUAVE,
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

# Cadenas de coordenadas formateadas (evitan escapes en el JSX).
COORDENADAS_TEXTO = '16°30\'30.3"S 68°09\'48.7"W'

# Paleta semántica (tokens Radix — adaptativos al color_mode).
# Cada "color" agrupa: fondo suave, borde, texto y sólido.
COLOR_AZUL_TEXTO = rx.color("blue", 11)
COLOR_AZUL_FONDO = rx.color("blue", 3)
COLOR_AZUL_BORDE = rx.color("blue", 7)
COLOR_AZUL_SOLIDO = rx.color("blue", 9)

COLOR_VERDE_TEXTO = rx.color("green", 11)
COLOR_VERDE_FONDO = rx.color("green", 3)
COLOR_VERDE_BORDE = rx.color("green", 7)
COLOR_VERDE_SOLIDO = rx.color("green", 9)

COLOR_ROJO_TEXTO = rx.color("red", 11)
COLOR_ROJO_FONDO = rx.color("red", 3)
COLOR_ROJO_BORDE = rx.color("red", 7)
COLOR_ROJO_SOLIDO = rx.color("red", 9)


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

    Usa tokens Radix para el fondo y el borde, por lo que se adapta
    automáticamente al modo claro/oscuro.
    """
    props.setdefault("padding", "1.5rem")
    props.setdefault("border_radius", RADIO_EXTRA_GRANDE)
    props.setdefault("background", COLOR_FONDO_CARTA)
    props.setdefault("border", f"1px solid {COLOR_BORDE_SUAVE}")
    props.setdefault("box_shadow", SOMBRA_SUAVE)
    props.setdefault("width", "100%")
    props.setdefault("height", "100%")
    props.setdefault(
        "transition",
        "all 0.25s cubic-bezier(0.4, 0, 0.2, 1)",
    )

    return rx.box(*children, **props)


def _icono_tarjeta(icono: str, color_texto: rx.Var, color_fondo: rx.Var) -> rx.Component:
    """
    Icono con fondo tintado.

    Args:
        icono: Nombre del icono Lucide.
        color_texto: Color del icono (token de texto, step 11).
        color_fondo: Fondo suave del icono (token de fondo, step 3).
    """
    return rx.box(
        rx.icon(tag=icono, size=22, color=color_texto),
        padding="0.75rem",
        border_radius="0.875rem",
        background=color_fondo,
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
                _icono_tarjeta("phone", COLOR_AZUL_TEXTO, COLOR_AZUL_FONDO),
                rx.vstack(
                    rx.text(
                        "Atención al Cliente",
                        font_size="0.75rem",
                        font_weight="700",
                        color=COLOR_TEXTO_SECUNDARIO,
                        text_transform="uppercase",
                        letter_spacing="0.05em",
                        line_height="1.1",
                    ),
                    rx.text(
                        f"{TELEFONO_PRINCIPAL}",
                        font_size="1.125rem",
                        font_weight="800",
                        color=COLOR_TEXTO_PRINCIPAL,
                        line_height="1.2",
                    ),
                    rx.text(
                        f"Alterno: {TELEFONO_SECUNDARIO}",
                        font_size="0.75rem",
                        color=COLOR_TEXTO_SECUNDARIO,
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
                    icono="message_circle",
                    etiqueta="WhatsApp",
                    href=WHATSAPP_URL,
                    color_solido=COLOR_VERDE_SOLIDO,
                    externo=True,
                ),
                _boton_accion(
                    icono="phone",
                    etiqueta="Llamar",
                    href=f"tel:+591{TELEFONO_PRINCIPAL}",
                    color_solido=COLOR_AZUL_SOLIDO,
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
            "border_color": COLOR_AZUL_BORDE,
            "transform": "translateY(-2px)",
            "box_shadow": f"0 12px 30px -10px {COLOR_AZUL_SOLIDO}",
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
                _icono_tarjeta("map-pin", COLOR_ROJO_TEXTO, COLOR_ROJO_FONDO),
                rx.vstack(
                    rx.text(
                        "Dirección Exacta",
                        font_size="0.75rem",
                        font_weight="700",
                        color=COLOR_TEXTO_SECUNDARIO,
                        text_transform="uppercase",
                        letter_spacing="0.05em",
                        line_height="1.1",
                    ),
                    rx.text(
                        DIRECCION,
                        font_size="0.9375rem",
                        font_weight="700",
                        color=COLOR_TEXTO_PRINCIPAL,
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
                    rx.icon("building-2", size=14, color=COLOR_ROJO_TEXTO),
                    rx.text(
                        UBICACION_FISICA,
                        font_size="0.8125rem",
                        font_weight="600",
                        color=COLOR_TEXTO_CUERPO,
                    ),
                    align="center",
                    gap="0.5rem",
                ),
                padding="0.75rem 1rem",
                border_radius=RADIO_MEDIO,
                background=COLOR_ROJO_FONDO,
                border=f"1px solid {COLOR_ROJO_BORDE}",
                margin_top="1.25rem",
                width="100%",
            ),
            spacing="0",
            width="100%",
            height="100%",
        ),
        _hover={
            "border_color": COLOR_ROJO_BORDE,
            "transform": "translateY(-2px)",
            "box_shadow": f"0 12px 30px -10px {COLOR_ROJO_SOLIDO}",
        },
    )


# ======================================================================
# Tarjeta de horario
# ======================================================================


def _tarjeta_horario() -> rx.Component:
    """Tarjeta con el horario de atención + badge de disponibilidad."""
    return _tarjeta_base(
        rx.vstack(
            # --- Header ---
            rx.flex(
                _icono_tarjeta("clock", COLOR_AZUL_TEXTO, COLOR_AZUL_FONDO),
                rx.vstack(
                    rx.text(
                        "Horario de Atención",
                        font_size="0.75rem",
                        font_weight="700",
                        color=COLOR_TEXTO_SECUNDARIO,
                        text_transform="uppercase",
                        letter_spacing="0.05em",
                        line_height="1.1",
                    ),
                    rx.text(
                        HORARIO_ATENCION,
                        font_size="0.9375rem",
                        font_weight="700",
                        color=COLOR_TEXTO_PRINCIPAL,
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
                    border_radius=RADIO_PASTILLA,
                    background=COLOR_VERDE_SOLIDO,
                    animation="pulse 2s ease-in-out infinite",
                ),
                rx.text(
                    "Atención presencial y telefónica",
                    font_size="0.75rem",
                    font_weight="600",
                    color=COLOR_VERDE_TEXTO,
                ),
                align="center",
                gap="0.5rem",
                padding="0.5rem 0.875rem",
                border_radius=RADIO_PASTILLA,
                background=COLOR_VERDE_FONDO,
                margin_top="1.25rem",
                width="fit-content",
            ),
            spacing="0",
            width="100%",
            height="100%",
        ),
        _hover={
            "border_color": COLOR_AZUL_BORDE,
            "transform": "translateY(-2px)",
            "box_shadow": f"0 12px 30px -10px {COLOR_AZUL_SOLIDO}",
        },
    )


# ======================================================================
# Botón de acción reutilizable
# ======================================================================


def _boton_accion(
    icono: str,
    etiqueta: str,
    href: str,
    color_solido: rx.Var,
    externo: bool = False,
) -> rx.Component:
    """
    Botón de acción con icono + etiqueta.

    Args:
        icono: Nombre del icono Lucide.
        etiqueta: Texto visible del botón.
        href: URL destino.
        color_solido: Color de fondo (token step 9).
        externo: Si True, abre en nueva pestaña.
    """
    return rx.link(
        rx.icon(tag=icono, size=16, color="white"),
        rx.text(
            etiqueta,
            font_size="0.8125rem",
            font_weight="700",
            color="white",
        ),
        href=href,
        is_external=externo,
        display="flex",
        align_items="center",
        justify_content="center",
        gap="0.5rem",
        padding="0.625rem 1rem",
        border_radius=RADIO_MEDIO,
        background=color_solido,
        text_decoration="none",
        flex="1",
        transition="all 0.2s",
        _hover={
            "transform": "translateY(-1px)",
            "filter": "brightness(1.1)",
            "box_shadow": f"0 8px 16px -4px {color_solido}",
        },
    )


# ======================================================================
# Bloque de mapa con Google Maps embebido
# ======================================================================


def _ubicacion_item(
    icono: str,
    etiqueta: str,
    valor: str,
    color_texto: rx.Var,
    color_fondo: rx.Var,
) -> rx.Component:
    """Item de ubicación (dirección, referencia, coordenadas)."""
    return rx.flex(
        _icono_tarjeta(icono, color_texto, color_fondo),
        rx.vstack(
            rx.text(
                etiqueta,
                font_size="0.6875rem",
                font_weight="700",
                color=COLOR_TEXTO_SECUNDARIO,
                text_transform="uppercase",
                letter_spacing="0.05em",
                line_height="1.1",
            ),
            rx.text(
                valor,
                font_size="0.8125rem",
                font_weight="600",
                color=COLOR_TEXTO_PRINCIPAL,
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
        border_radius=RADIO_GRANDE,
        background=COLOR_FONDO_SUAVE,
        border=f"1px solid {COLOR_BORDE_SUAVE}",
    )


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
            rx.icon("map-pin", size=22, color=COLOR_ROJO_TEXTO),
            rx.vstack(
                rx.heading(
                    "Ubícanos en el mapa",
                    size="5",
                    font_weight="700",
                    color=COLOR_TEXTO_PRINCIPAL,
                ),
                rx.text(
                    "Estamos en una ubicación céntrica y de fácil acceso.",
                    font_size="0.875rem",
                    color=COLOR_TEXTO_SECUNDARIO,
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
            border_radius=RADIO_EXTRA_GRANDE,
            overflow="hidden",
            border=f"1px solid {COLOR_BORDE_SUAVE}",
            box_shadow="0 4px 12px -2px rgb(0 0 0 / 0.08)",
        ),
        # --- Grid de datos de ubicación ---
        rx.flex(
            _ubicacion_item(
                icono="map-pin",
                etiqueta="Dirección",
                valor=DIRECCION,
                color_texto=COLOR_ROJO_TEXTO,
                color_fondo=COLOR_ROJO_FONDO,
            ),
            _ubicacion_item(
                icono="building-2",
                etiqueta="Referencia",
                valor=UBICACION_FISICA,
                color_texto=COLOR_AZUL_TEXTO,
                color_fondo=COLOR_AZUL_FONDO,
            ),
            _ubicacion_item(
                icono="compass",
                etiqueta="Coordenadas",
                valor=COORDENADAS_TEXTO,
                color_texto=COLOR_VERDE_TEXTO,
                color_fondo=COLOR_VERDE_FONDO,
            ),
            gap="1rem",
            width="100%",
            margin_top="1.5rem",
            flex_wrap="wrap",
        ),
        # --- Botón "Cómo llegar" ---
        rx.link(
            rx.flex(
                rx.icon("navigation", size=16, color="white"),
                rx.text(
                    "Cómo llegar",
                    font_size="0.875rem",
                    font_weight="700",
                    color="white",
                ),
                align="center",
                gap="0.5rem",
            ),
            href=url_como_llegar,
            is_external=True,
            text_decoration="none",
            padding="0.75rem 1.5rem",
            border_radius=RADIO_PASTILLA,
            background=COLOR_AZUL_SOLIDO,
            box_shadow=f"0 8px 20px -4px {COLOR_AZUL_SOLIDO}",
            transition="all 0.2s",
            margin_top="1.5rem",
            width="fit-content",
            _hover={
                "transform": "translateY(-2px)",
                "box_shadow": f"0 12px 30px -6px {COLOR_AZUL_SOLIDO}",
            },
        ),
        spacing="0",
        width="100%",
        align="start",
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
                        border_radius=RADIO_PASTILLA,
                        background=COLOR_VERDE_SOLIDO,
                        animation="pulse 2s ease-in-out infinite",
                    ),
                    rx.text(
                        "MANTENTE EN CONTACTO",
                        font_size="0.75rem",
                        font_weight="700",
                        color=COLOR_TEXTO_SECUNDARIO,
                        letter_spacing="0.15em",
                    ),
                    align="center",
                    gap="0.5rem",
                ),
                rx.heading(
                    "Comunícate con nosotros",
                    size="8",
                    font_weight="800",
                    color=COLOR_TEXTO_PRINCIPAL,
                    text_align="center",
                    line_height="1.1",
                ),
                rx.text(
                    "Estamos disponibles para resolver tus dudas sobre admisiones, "
                    "carreras, horarios y toda la información institucional.",
                    font_size="1rem",
                    color=COLOR_TEXTO_SECUNDARIO,
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
                        color=COLOR_TEXTO_PRINCIPAL,
                        text_align="center",
                    ),
                    rx.text(
                        "Crea tu cuenta institucional y accede a tu historial académico.",
                        font_size="0.9375rem",
                        color=COLOR_TEXTO_SECUNDARIO,
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
            max_width=ANCHO_CONTENIDO,
            margin="0 auto",
            padding=f"3rem {PADDING_LATERAL} 6rem {PADDING_LATERAL}",
            width="100%",
        ),
        # --- Pie de página ---
        pie_pagina_institucional(),
        align="center",
        min_height="100vh",
        width="100%",
    )