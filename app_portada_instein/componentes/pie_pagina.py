"""
Pie de página institucional con:
- Brand block (logo + tagline + redes sociales).
- Newsletter (input de email + botón suscribir).
- Sección de feedback ("¿Te resultó útil?").
- Grid de enlaces organizados por columnas.
- Barra inferior con copyright, links legales y estado del servidor.

Sistema de color (UX)
---------------------
- Fondo neutro (`gray-1`) con borde superior sutil.
- Textos en `gray-11`/`gray-12`.
- Hover de enlaces: accent institucional (crimson).
- Botones de feedback: semánticos (`green`/`red`).
- Estado del servidor: `green` con animación pulse + borderPulse.
- Redes sociales: colores de marca oficiales (no cambian con el modo).

Referencia visual
-----------------
Inspirado en el footer de reflex.dev:
- Brand block con logo + tagline + redes.
- Newsletter con input y botón.
- Grid de enlaces por columnas.
- Barra inferior con copyright + estado del sistema.
"""

import reflex as rx

from app_portada_instein.infraestructura.constantes_visuales import (
    ANIO_COPYRIGHT,
    COLOR_ACENTO_TEXTO,
    COLOR_BORDE_HOVER,
    COLOR_BORDE_SUAVE,
    COLOR_DIVISOR,
    COLOR_FONDO_CARTA,
    COLOR_FONDO_SUAVE,
    COLOR_TEXTO_CUERPO,
    COLOR_TEXTO_PRINCIPAL,
    COLOR_TEXTO_SECUNDARIO,
    EMAIL_CONTACTO,
    NOMBRE_COMPLETO_INSTITUTO,
    NOMBRE_INSTITUTO,
    RADIO_EXTRA_GRANDE,
    RADIO_MEDIO,
    RADIO_PASTILLA,
    REDES_SOCIALES,
    TELEFONO_PRINCIPAL,
    WHATSAPP_URL,
)


# ======================================================================
# Constantes locales
# ======================================================================

ANCHO_MAXIMO_FOOTER = "72rem"
PADDING_LATERAL_FOOTER = "1.5rem"

# Descripción institucional para el brand block.
DESCRIPCION_INSTITUCIONAL = (
    "Formación técnica de excelencia con títulos de Provisión Nacional. "
    "5 carreras, equipamiento moderno y docentes especializados."
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
            "titulo": "Plataforma",
            "items": [
                {"etiqueta": "Inicio", "ruta": "/", "externo": False},
                {"etiqueta": "Carreras", "ruta": "/carreras", "externo": False},
                {"etiqueta": "Contacto", "ruta": "/contacto", "externo": False},
            ],
        },
        {
            "titulo": "Institucional",
            "items": [
                {
                    "etiqueta": "Sobre nosotros",
                    "ruta": "/sobre-nosotros",
                    "externo": False,
                },
                
                {
                    "etiqueta": "Preguntas frecuentes",
                    "ruta": "/faq",
                    "externo": False,
                },
                {
                    "etiqueta": "Calendario académico",
                    "ruta": "/calendario",
                    "externo": False,
                },
            ],
        },
        {
            "titulo": "Recursos",
            "items": [
                {"etiqueta": "Blog", "ruta": "/blog", "externo": False},
                {
                    "etiqueta": "Guía de admisión",
                    "ruta": "/admision",
                    "externo": False,
                },
                {
                    "etiqueta": "Becas y descuentos",
                    "ruta": "/becas",
                    "externo": False,
                },
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
# Brand block (logo + tagline + redes sociales)
# ======================================================================


def _logo_institucional() -> rx.Component:
    """Logo textual del instituto con badge accent."""
    return rx.flex(
        rx.box(
            rx.text(
                "I",
                font_size="1.125rem",
                font_weight="900",
                color="white",
                line_height="1",
            ),
            height="2.25rem",
            width="2.25rem",
            border_radius=RADIO_MEDIO,
            background=rx.color("accent", 9),
            display="flex",
            align_items="center",
            justify_content="center",
            flex_shrink="0",
        ),
        rx.vstack(
            rx.text(
                NOMBRE_INSTITUTO,
                font_size="0.9375rem",
                font_weight="900",
                color=COLOR_TEXTO_PRINCIPAL,
                letter_spacing="0.05em",
                line_height="1.1",
            ),
            rx.text(
                "Instituto Técnico Integrado",
                font_size="0.6875rem",
                font_weight="500",
                color=COLOR_TEXTO_SECUNDARIO,
                line_height="1.2",
            ),
            spacing="0",
            align="start",
        ),
        align="center",
        gap="0.75rem",
    )


def _red_social_boton(red: dict) -> rx.Component:
    """
    Botón de red social con el color corporativo oficial.

    Los colores de marca de las redes NO cambian con el modo
    (son colores oficiales de cada plataforma).
    """
    return rx.link(
        rx.icon(red["icono"], size=16, color="white"),
        href=red["url"],
        is_external=True,
        text_decoration="none",
        height="2rem",
        width="2rem",
        border_radius=RADIO_MEDIO,
        background=red["color"],
        display="flex",
        align_items="center",
        justify_content="center",
        transition="all 0.2s",
        _hover={
            "transform": "translateY(-2px)",
            "filter": "brightness(1.15)",
        },
    )


def _brand_block() -> rx.Component:
    """
    Bloque de marca con logo + tagline + redes sociales.

    Similar al brand block de reflex.dev: agrupa la identidad
    institucional en la parte superior del footer.
    """
    return rx.vstack(
        # --- Logo + nombre ---
        _logo_institucional(),
        # --- Descripción ---
        rx.text(
            DESCRIPCION_INSTITUCIONAL,
            font_size="0.8125rem",
            color=COLOR_TEXTO_SECUNDARIO,
            line_height="1.6",
            max_width="20rem",
        ),
        # --- Redes sociales ---
        rx.flex(
            *[_red_social_boton(red) for red in REDES_SOCIALES],
            gap="0.5rem",
            flex_wrap="wrap",
            margin_top="0.25rem",
        ),
        align="start",
        spacing="3",
        width="100%",
        max_width="22rem",
    )


# ======================================================================
# Newsletter
# ======================================================================


def _newsletter() -> rx.Component:
    """
    Bloque de newsletter con input de email + botón suscribir.

    Similar al "Get Updates" de reflex.dev. En una implementación
    real, el input dispararía un evento al backend para guardar
    el email en la base de datos.
    """
    return rx.vstack(
        rx.text(
            "Recibe novedades",
            font_size="0.875rem",
            font_weight="700",
            color=COLOR_TEXTO_PRINCIPAL,
            line_height="1.2",
        ),
        rx.text(
            "Noticias, fechas de inscripción y eventos del instituto.",
            font_size="0.75rem",
            color=COLOR_TEXTO_SECUNDARIO,
            line_height="1.4",
        ),
        rx.flex(
            rx.input(
                placeholder="tu@email.com",
                type="email",
                size="2",
                width="100%",
                flex="1",
                min_width="0",
            ),
            rx.button(
                rx.icon("send", size=14),
                rx.text("Suscribir", as_="span"),
                size="2",
                variant="solid",
                color_scheme="crimson",
                cursor="pointer",
                flex_shrink="0",
            ),
            gap="0.5rem",
            width="100%",
            align="center",
        ),
        align="start",
        spacing="2",
        width="100%",
        max_width="22rem",
    )


# ======================================================================
# Sección de feedback ("¿Te resultó útil?")
# ======================================================================


def _seccion_feedback() -> rx.Component:
    """
    Sección con pregunta de feedback y botones Sí/No.

    UX:
    - Pregunta con texto neutro destacado.
    - Botones semánticos: verde para Sí, rojo para No.
    - Link "Reportar un problema" en gris neutro.
    - Borde inferior sutil que la separa del grid de enlaces.
    """
    return rx.flex(
        rx.text(
            "¿Te resultó útil esta página?",
            font_weight="600",
            font_size="0.875rem",
            color=COLOR_TEXTO_PRINCIPAL,
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
                border_radius=RADIO_MEDIO,
                background=COLOR_FONDO_SUAVE,
                color=COLOR_TEXTO_PRINCIPAL,
            ),
            gap="0.5rem",
            align="center",
            wrap="wrap",
        ),
        direction="column",
        gap="0.75rem",
        padding="1.5rem 0",
        border_bottom=f"1px solid {COLOR_DIVISOR}",
        width="100%",
    )


# ======================================================================
# Columna individual de enlaces
# ======================================================================


def _columna_enlaces(columna: dict) -> rx.Component:
    """
    Renderiza una columna del footer con su título y sus enlaces.

    Los enlaces tienen hover con accent institucional.
    """
    return rx.vstack(
        # --- Título de la columna ---
        rx.text(
            columna["titulo"],
            font_size="0.75rem",
            font_weight="700",
            text_transform="uppercase",
            letter_spacing="0.1em",
            color=COLOR_TEXTO_SECUNDARIO,
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
                    color=COLOR_TEXTO_CUERPO,
                    text_decoration="none",
                    transition="color 0.2s",
                    _hover={"color": COLOR_ACENTO_TEXTO},
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


def _enlace_legal(etiqueta: str, ruta: str) -> rx.Component:
    """Enlace legal pequeño en la barra inferior."""
    return rx.link(
        etiqueta,
        href=ruta,
        font_size="0.75rem",
        color=COLOR_TEXTO_SECUNDARIO,
        text_decoration="none",
        transition="color 0.2s",
        _hover={"color": COLOR_ACENTO_TEXTO},
    )


def _barra_inferior() -> rx.Component:
    """
    Barra inferior del footer con copyright, links legales y estado
    del servidor.

    UX:
    - Copyright + links legales a la izquierda.
    - Indicador de estado del servidor a la derecha.
    - Estilo inspirado en reflex.dev.
    """
    return rx.flex(
        # ==========================================================
        # Copyright + links legales
        # ==========================================================
        rx.flex(
            rx.text(
                f"© {ANIO_COPYRIGHT} {NOMBRE_INSTITUTO} · "
                f"Todos los derechos reservados",
                font_size="0.75rem",
                color=COLOR_TEXTO_SECUNDARIO,
            ),
            rx.text(
                "·",
                font_size="0.75rem",
                color=COLOR_TEXTO_SECUNDARIO,
            ),
            _enlace_legal("Términos", "/terminos"),
            rx.text(
                "·",
                font_size="0.75rem",
                color=COLOR_TEXTO_SECUNDARIO,
            ),
            _enlace_legal("Privacidad", "/privacidad"),
            align="center",
            gap="0.5rem",
            flex_wrap="wrap",
        ),
        # ==========================================================
        # Estado del servidor
        # ==========================================================
        rx.flex(
            rx.box(
                height="0.5rem",
                width="0.5rem",
                border_radius=RADIO_PASTILLA,
                background=rx.color("green", 9),
                animation="pulse 2s ease-in-out infinite",
            ),
            rx.text(
                "Todos los servicios operativos",
                font_size="0.75rem",
                color=COLOR_TEXTO_SECUNDARIO,
            ),
            align="center",
            gap="0.5rem",
            padding="0.5rem 0.875rem",
            border_radius=RADIO_PASTILLA,
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
# Bloque superior: brand + newsletter
# ======================================================================


def _bloque_superior() -> rx.Component:
    """
    Bloque superior del footer: brand block + newsletter.

    En desktop se muestran lado a lado; en móvil se apilan.

    ⚠️ `direction` en rx.flex (Radix Themes) NO acepta listas.
    Se usa `rx.breakpoints(...)` explícito.
    """
    return rx.flex(
        _brand_block(),
        _newsletter(),
        direction=rx.breakpoints(
            initial="column",
            sm="column",
            md="row",
            lg="row",
        ),
        justify="between",
        align="start",
        gap="2rem",
        width="100%",
        padding="2.5rem 0",
        border_bottom=f"1px solid {COLOR_DIVISOR}",
    )


# ======================================================================
# Footer completo
# ======================================================================


def pie_pagina_institucional() -> rx.Component:
    """
    Footer institucional completo con:
    - Bloque superior: brand (logo + tagline + redes) + newsletter.
    - Sección de feedback.
    - Grid de enlaces por columnas.
    - Barra inferior con copyright + legales + estado del servidor.

    Usa tokens Radix adaptativos al color_mode. El fondo es neutro
    (`gray-1`) con un borde superior sutil.
    """
    columnas = _enlaces_footer()

    return rx.box(
        rx.vstack(
            # ==========================================================
            # Bloque superior: brand + newsletter
            # ==========================================================
            _bloque_superior(),
            # ==========================================================
            # Sección de feedback
            # ==========================================================
            _seccion_feedback(),
            # ==========================================================
            # Grid de columnas de enlaces
            # ==========================================================
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
            # ==========================================================
            # Barra inferior
            # ==========================================================
            _barra_inferior(),
            spacing="0",
            width="100%",
        ),
        # ==========================================================
        # Estilos del contenedor principal
        # ==========================================================
        width="100%",
        padding=f"0 {PADDING_LATERAL_FOOTER}",
        max_width=ANCHO_MAXIMO_FOOTER,
        margin="0 auto",
        border_top=f"1px solid {COLOR_DIVISOR}",
        background=COLOR_FONDO_CARTA,
    )


__all__ = ["pie_pagina_institucional"]