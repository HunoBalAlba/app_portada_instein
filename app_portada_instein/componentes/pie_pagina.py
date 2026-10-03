# app_portada_instein/componentes/pie_pagina.py

"""
Pie de página institucional — estilo Neon adaptativo (dark/light).

Contiene:
- Brand block (logo + tagline + redes sociales).
- Newsletter (input de email + botón suscribir).
- Sección de feedback ("¿Te resultó útil?").
- Grid de enlaces organizados por columnas.
- Barra inferior con copyright, links legales y estado del servidor.

Sistema de color (UX)
---------------------
✅ ADAPTATIVO: todos los colores respetan el color_mode del usuario.

- Fondo: `FONDO_HOME` (light: claro, dark: oscuro).
- Acentos: azul marino neon (`AZUL_MARINO_NEON` = `#3b5bdb`) en AMBOS modos.
- Texto: `TEXTO_HOME_PRINCIPAL` / `TEXTO_HOME_SUAVE` / `TEXTO_HOME_MAS_SUAVE`.
- Bordes: `BORDE_HOME_SUAVE` / `BORDE_HOME_MEDIO` / `BORDE_HOME_AZUL`.
- Redes sociales: colores corporativos oficiales (hex fijos), NO
  cambian con el tema (son colores de marca de terceros).
- Estado del servidor: verde semántico con pulse + borderPulse.

⚠️ Toggle de color mode
-----------------------
El toggle está en la **barra de navegación superior** (arriba a la
derecha) para que sea más visible. El usuario puede cambiar el modo
desde ahí.

Referencia visual
-----------------
Inspirado en el footer de reflex.dev y neon.com:
- Brand block con logo + tagline + redes.
- Newsletter con input y botón.
- Grid de enlaces por columnas.
- Barra inferior con copyright + estado del sistema.
"""

import reflex as rx

from app_portada_instein.infraestructura.constantes_visuales import (
    ANIO_COPYRIGHT,
    AZUL_MARINO_NEON,
    BORDE_HOME_AZUL,
    BORDE_HOME_MEDIO,
    BORDE_HOME_SUAVE,
    EMAIL_CONTACTO,
    FONDO_AZUL_MUY_SUAVE,
    FONDO_AZUL_SUAVE,
    FONDO_HOME,
    NOMBRE_INSTITUTO,
    RADIO_EXTRA_GRANDE,
    RADIO_MEDIO,
    RADIO_PASTILLA,
    REDES_SOCIALES,
    TELEFONO_PRINCIPAL,
    TEXTO_HOME_MAS_SUAVE,
    TEXTO_HOME_PRINCIPAL,
    TEXTO_HOME_SUAVE,
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

# Sombra del logo (glow azul marino).
SOMBRA_LOGO = f"0 0 20px {AZUL_MARINO_NEON}80"

# Color del punto verde semántico (activo).
COLOR_VERDE_ACTIVO = "#22c55e"


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
                {
                    "etiqueta": "Carreras",
                    "ruta": "/carreras",
                    "externo": False,
                },
                {
                    "etiqueta": "Contacto",
                    "ruta": "/contacto",
                    "externo": False,
                },
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
    """
    Logo textual del instituto con badge de gradiente azul marino.

    ✅ ADAPTATIVO: el texto "INSTEIN" y el subtítulo cambian según el modo.
    """
    return rx.flex(
        # Badge "I" con gradiente azul marino
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
            background=(
                f"linear-gradient(135deg, {AZUL_MARINO_NEON} 0%, "
                f"#1a237e 100%)"
            ),
            display="flex",
            align_items="center",
            justify_content="center",
            box_shadow=SOMBRA_LOGO,
            flex_shrink="0",
        ),
        # Texto INSTEIN + subtítulo (adaptativos)
        rx.vstack(
            rx.text(
                NOMBRE_INSTITUTO,
                font_size="0.9375rem",
                font_weight="900",
                color=TEXTO_HOME_PRINCIPAL,      # ✅ adaptativo
                letter_spacing="0.1em",
                line_height="1.1",
            ),
            rx.text(
                "Instituto Técnico Integrado",
                font_size="0.6875rem",
                font_weight="500",
                color=TEXTO_HOME_MAS_SUAVE,      # ✅ adaptativo
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

    ⚠️ Los colores de marca de las redes NO cambian con el modo
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

    ✅ ADAPTATIVO: la descripción cambia de color según el modo.
    """
    return rx.vstack(
        # --- Logo + nombre ---
        _logo_institucional(),
        # --- Descripción ---
        rx.text(
            DESCRIPCION_INSTITUCIONAL,
            font_size="0.8125rem",
            color=TEXTO_HOME_MAS_SUAVE,          # ✅ adaptativo
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

    ✅ ADAPTATIVO: input, textos y botón cambian según el modo.

    Estilo Neon:
    - Input con fondo translúcido adaptativo.
    - Botón "Suscribir" con azul marino neon + glow.
    - Hover del botón intensifica el glow.

    Nota: en una implementación real, el input dispararía un evento
    al backend para guardar el email en la base de datos.
    """
    return rx.vstack(
        rx.text(
            "Recibe novedades",
            font_size="0.875rem",
            font_weight="700",
            color=TEXTO_HOME_PRINCIPAL,          # ✅ adaptativo
            line_height="1.2",
        ),
        rx.text(
            "Noticias, fechas de inscripción y eventos del instituto.",
            font_size="0.75rem",
            color=TEXTO_HOME_MAS_SUAVE,          # ✅ adaptativo
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
                background=rx.color_mode_cond(     # ✅ adaptativo
                    light="rgba(15, 23, 42, 0.03)",
                    dark="rgba(255, 255, 255, 0.05)",
                ),
                border=f"1px solid {BORDE_HOME_MEDIO}",   # ✅ adaptativo
                color=TEXTO_HOME_PRINCIPAL,               # ✅ adaptativo
                _placeholder={"color": TEXTO_HOME_MAS_SUAVE},
                _focus={
                    "border_color": BORDE_HOME_AZUL,
                    "box_shadow": f"0 0 0 1px {AZUL_MARINO_NEON}",
                },
            ),
            rx.button(
                rx.icon("send", size=14),
                rx.text("Suscribir", as_="span"),
                size="2",
                cursor="pointer",
                flex_shrink="0",
                background=AZUL_MARINO_NEON,
                color="white",
                border_radius=RADIO_MEDIO,
                box_shadow=rx.color_mode_cond(     # ✅ adaptativo
                    light=f"0 4px 12px -2px {AZUL_MARINO_NEON}40",
                    dark=f"0 4px 12px -2px {AZUL_MARINO_NEON}80",
                ),
                transition="all 0.2s",
                _hover={
                    "transform": "translateY(-1px)",
                    "box_shadow": f"0 6px 16px -2px {AZUL_MARINO_NEON}cc",
                },
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

    ✅ ADAPTATIVO: textos, link y borde cambian según el modo.

    UX:
    - Pregunta con texto destacado.
    - Botones semánticos: verde para Sí, rojo para No.
    - Link "Reportar un problema" con glassmorphism adaptativo.
    - Borde inferior sutil que la separa del grid de enlaces.

    Nota: los botones Sí/No usan colores semánticos (verde/rojo),
    NO el azul marino, porque representan estados del sistema.
    """
    return rx.flex(
        rx.text(
            "¿Te resultó útil esta página?",
            font_weight="600",
            font_size="0.875rem",
            color=TEXTO_HOME_PRINCIPAL,          # ✅ adaptativo
        ),
        rx.flex(
            rx.button(
                rx.icon("thumbs-up", size=14),
                rx.text("Sí", as_="span"),
                size="1",
                variant="soft",
                color_scheme="green",
                cursor="pointer",
            ),
            rx.button(
                rx.icon("thumbs-down", size=14),
                rx.text("No", as_="span"),
                size="1",
                variant="soft",
                color_scheme="red",
                cursor="pointer",
            ),
            rx.link(
                rx.icon("message-square-warning", size=14),
                rx.text("Reportar un problema", as_="span"),
                href="/",
                is_external=True,
                text_decoration="none",
                display="inline-flex",
                align_items="center",
                gap="0.4rem",
                padding="0.375rem 0.75rem",
                border_radius=RADIO_MEDIO,
                background=rx.color_mode_cond(     # ✅ adaptativo
                    light="rgba(15, 23, 42, 0.04)",
                    dark="rgba(255, 255, 255, 0.05)",
                ),
                border=f"1px solid {BORDE_HOME_SUAVE}",   # ✅ adaptativo
                color=TEXTO_HOME_SUAVE,                    # ✅ adaptativo
                font_size="0.75rem",
                font_weight="600",
                transition="all 0.2s",
                _hover={
                    "background": rx.color_mode_cond(
                        light="rgba(15, 23, 42, 0.08)",
                        dark="rgba(255, 255, 255, 0.1)",
                    ),
                    "border_color": BORDE_HOME_MEDIO,
                    "color": TEXTO_HOME_PRINCIPAL,
                },
            ),
            gap="0.5rem",
            align="center",
            wrap="wrap",
        ),
        direction="column",
        gap="0.75rem",
        padding="2rem 0",
        border_bottom=f"1px solid {BORDE_HOME_SUAVE}",   # ✅ adaptativo
        width="100%",
    )


# ======================================================================
# Columna individual de enlaces
# ======================================================================


def _columna_enlaces(columna: dict) -> rx.Component:
    """
    Renderiza una columna del footer con su título y sus enlaces.

    ✅ ADAPTATIVO: los textos y el hover cambian según el modo.
    """
    return rx.vstack(
        # --- Título de la columna ---
        rx.text(
            columna["titulo"],
            font_size="0.75rem",
            font_weight="700",
            text_transform="uppercase",
            letter_spacing="0.1em",
            color=TEXTO_HOME_MAS_SUAVE,          # ✅ adaptativo
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
                    color=TEXTO_HOME_SUAVE,      # ✅ adaptativo
                    text_decoration="none",
                    transition="color 0.2s",
                    _hover={"color": AZUL_MARINO_NEON},
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
    """Enlace legal pequeño en la barra inferior (adaptativo)."""
    return rx.link(
        etiqueta,
        href=ruta,
        font_size="0.75rem",
        color=TEXTO_HOME_MAS_SUAVE,              # ✅ adaptativo
        text_decoration="none",
        transition="color 0.2s",
        _hover={"color": AZUL_MARINO_NEON},
    )


def _barra_inferior() -> rx.Component:
    """
    Barra inferior del footer con copyright, links legales y estado
    del servidor.

    ✅ ADAPTATIVO: textos, borde y fondo del indicador cambian según
    el modo.

    UX:
    - Copyright + links legales a la izquierda.
    - Estado del servidor a la derecha.
    - Estilo inspirado en reflex.dev.

    Nota: el toggle de color mode está en la barra de navegación
    superior (arriba a la derecha) para que sea más visible.
    """
    return rx.flex(
        # ==========================================================
        # Copyright + links legales (izquierda)
        # ==========================================================
        rx.flex(
            rx.text(
                f"© {ANIO_COPYRIGHT} {NOMBRE_INSTITUTO} · "
                f"Todos los derechos reservados",
                font_size="0.75rem",
                color=TEXTO_HOME_MAS_SUAVE,      # ✅ adaptativo
            ),
            rx.text(
                "·",
                font_size="0.75rem",
                color=TEXTO_HOME_MAS_SUAVE,      # ✅ adaptativo
            ),
            _enlace_legal("Términos", "/terminos"),
            rx.text(
                "·",
                font_size="0.75rem",
                color=TEXTO_HOME_MAS_SUAVE,      # ✅ adaptativo
            ),
            _enlace_legal("Privacidad", "/privacidad"),
            align="center",
            gap="0.5rem",
            flex_wrap="wrap",
        ),
        # ==========================================================
        # Estado del servidor (derecha)
        # ==========================================================
        rx.flex(
            rx.box(
                height="0.5rem",
                width="0.5rem",
                border_radius=RADIO_PASTILLA,
                background=COLOR_VERDE_ACTIVO,
                box_shadow=f"0 0 12px {COLOR_VERDE_ACTIVO}",
                animation="pulse 2s ease-in-out infinite",
            ),
            rx.text(
                "Todos los servicios operativos",
                font_size="0.75rem",
                color=TEXTO_HOME_MAS_SUAVE,      # ✅ adaptativo
            ),
            align="center",
            gap="0.5rem",
            padding="0.5rem 0.875rem",
            border_radius=RADIO_PASTILLA,
            border=f"1px solid {BORDE_HOME_SUAVE}",     # ✅ adaptativo
            background=rx.color_mode_cond(              # ✅ adaptativo
                light="rgba(34, 197, 94, 0.08)",
                dark="rgba(34, 197, 94, 0.05)",
            ),
            animation="borderPulse 2.5s ease-in-out infinite",
        ),
        # ==========================================================
        # Layout de la barra inferior
        # ==========================================================
        align="center",
        justify="between",
        width="100%",
        padding_top="2rem",
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

    ✅ ADAPTATIVO: el borde inferior cambia según el modo.

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
        padding="3rem 0",
        border_bottom=f"1px solid {BORDE_HOME_SUAVE}",   # ✅ adaptativo
    )


# ======================================================================
# Footer completo
# ======================================================================


def pie_pagina_institucional() -> rx.Component:
    """
    Footer institucional completo — estilo Neon adaptativo.

    Contiene:
    - Bloque superior: brand (logo + tagline + redes) + newsletter.
    - Sección de feedback ("¿Te resultó útil?").
    - Grid de enlaces por columnas.
    - Barra inferior con copyright + legales + estado del servidor.

    ✅ ADAPTATIVO: fondo, textos y bordes respetan el color_mode.

    El toggle de color mode está en la barra de navegación superior.
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
                padding="3rem 0",
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
        border_top=f"1px solid {BORDE_HOME_SUAVE}",   # ✅ adaptativo
        background=FONDO_HOME,                         # ✅ adaptativo
    )


__all__ = ["pie_pagina_institucional"]