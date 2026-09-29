"""
Vista "Sobre nosotros" (ruta "/sobre-nosotros").

Contenido:
- Hero con nombre del instituto + tagline.
- Sección de historia.
- Misión, visión y valores.
- Llamado a la acción final.

Nota sobre `rx.flex(direction=...)`
-----------------------------------
En `rx.flex` de Radix Themes, el prop `direction` NO acepta listas de
breakpoints (a diferencia de props CSS como `gap` o `padding`).
Se debe usar `rx.breakpoints(...)` explícito.
"""

import reflex as rx

from app_portada_instein.componentes.barra_navegacion import (
    barra_navegacion_superior,
)
from app_portada_instein.componentes.pie_pagina import (
    pie_pagina_institucional,
)
from app_portada_instein.infraestructura.constantes_visuales import (
    COLOR_ACENTO_FONDO,
    COLOR_ACENTO_TEXTO,
    COLOR_BORDE_SUAVE,
    COLOR_FONDO_CARTA,
    COLOR_FONDO_SUAVE,
    COLOR_TEXTO_CUERPO,
    COLOR_TEXTO_PRINCIPAL,
    COLOR_TEXTO_SECUNDARIO,
    NOMBRE_COMPLETO_INSTITUTO,
    NOMBRE_INSTITUTO,
    RADIO_EXTRA_GRANDE,
    RADIO_GRANDE,
)


# ======================================================================
# Constantes locales
# ======================================================================

VALORES: list[dict] = [
    {
        "icono": "award",
        "titulo": "Excelencia",
        "descripcion": "Formamos profesionales que destacan en su campo.",
    },
    {
        "icono": "users",
        "titulo": "Comunidad",
        "descripcion": "Una red de egresados que se apoyan mutuamente.",
    },
    {
        "icono": "book-open",
        "titulo": "Aprendizaje continuo",
        "descripcion": "Actualizamos nuestros planes cada gestión.",
    },
    {
        "icono": "target",
        "titulo": "Compromiso",
        "descripcion": "Tu éxito profesional es nuestra misión.",
    },
]


# ======================================================================
# Componentes internos
# ======================================================================


def _hero_sobre_nosotros() -> rx.Component:
    """Hero con nombre completo + tagline."""
    return rx.vstack(
        rx.text(
            "SOBRE NOSOTROS",
            font_size="0.75rem",
            font_weight="700",
            letter_spacing="0.15em",
            color=COLOR_ACENTO_TEXTO,
        ),
        rx.heading(
            NOMBRE_INSTITUTO,
            size="9",
            font_weight="900",
            color=COLOR_TEXTO_PRINCIPAL,
            text_align="center",
            letter_spacing="-0.03em",
        ),
        rx.text(
            "Instituto Técnico Integrado San Antonio de Padua",
            font_size="1.125rem",
            color=COLOR_TEXTO_SECUNDARIO,
            text_align="center",
        ),
        rx.text(
            "Formamos Técnicos Superiores de excelencia con títulos de "
            "Provisión Nacional, comprometidos con el desarrollo profesional "
            "y humano de cada estudiante.",
            font_size="1rem",
            color=COLOR_TEXTO_CUERPO,
            text_align="center",
            max_width="48rem",
            line_height="1.7",
            margin_top="1rem",
        ),
        align="center",
        spacing="3",
        padding="5rem 1.5rem 3rem 1.5rem",
        max_width="72rem",
        margin="0 auto",
        width="100%",
    )


def _seccion_historia() -> rx.Component:
    """
    Sección de historia con dos columnas.

    ⚠️ `direction` en `rx.flex` (Radix Themes) NO acepta listas.
    Se usa `rx.breakpoints(...)`.
    """
    return rx.box(
        rx.flex(
            rx.vstack(
                rx.text(
                    "NUESTRA HISTORIA",
                    font_size="0.75rem",
                    font_weight="700",
                    letter_spacing="0.15em",
                    color=COLOR_ACENTO_TEXTO,
                ),
                rx.heading(
                    "15 años formando profesionales",
                    size="6",
                    font_weight="800",
                    color=COLOR_TEXTO_PRINCIPAL,
                    line_height="1.2",
                ),
                rx.text(
                    "Desde 2010, INSTEIN ha sido un referente en formación "
                    "técnica en Bolivia. Con más de 500 egresados activos en "
                    "el mercado laboral, hemos construido una comunidad "
                    "sólida de profesionales técnicos de excelencia.",
                    font_size="0.9375rem",
                    color=COLOR_TEXTO_CUERPO,
                    line_height="1.7",
                ),
                rx.text(
                    "Nuestro compromiso es ofrecer una formación práctica, "
                    "actualizada y conectada con las necesidades reales "
                    "del mercado laboral boliviano.",
                    font_size="0.9375rem",
                    color=COLOR_TEXTO_CUERPO,
                    line_height="1.7",
                ),
                align="start",
                spacing="3",
                flex="1",
                min_width="0",
            ),
            rx.box(
                rx.flex(
                    rx.icon(
                        "building-2",
                        size=64,
                        color=COLOR_ACENTO_TEXTO,
                    ),
                    height="12rem",
                    width="12rem",
                    border_radius=RADIO_EXTRA_GRANDE,
                    background=COLOR_ACENTO_FONDO,
                    border=f"1px solid {COLOR_ACENTO_TEXTO}",
                    align="center",
                    justify="center",
                ),
                flex_shrink="0",
            ),
            # ✅ direction con rx.breakpoints() en lugar de lista
            direction=rx.breakpoints(
                initial="column",
                sm="column",
                md="row",
                lg="row",
            ),
            gap="3rem",
            align="center",
            width="100%",
        ),
        max_width="72rem",
        margin="0 auto",
        padding="3rem 1.5rem",
        width="100%",
    )


def _tarjeta_myv(
    icono: str,
    titulo: str,
    contenido: str,
) -> rx.Component:
    """Tarjeta de misión o visión."""
    return rx.box(
        rx.vstack(
            rx.box(
                rx.icon(icono, size=24, color=COLOR_ACENTO_TEXTO),
                padding="0.75rem",
                border_radius=RADIO_GRANDE,
                background=COLOR_ACENTO_FONDO,
                border=f"1px solid {COLOR_ACENTO_TEXTO}",
                display="flex",
                align_items="center",
                justify_content="center",
                width="fit-content",
                margin_bottom="1rem",
            ),
            rx.heading(
                titulo,
                size="4",
                font_weight="700",
                color=COLOR_TEXTO_PRINCIPAL,
            ),
            rx.text(
                contenido,
                font_size="0.9375rem",
                color=COLOR_TEXTO_CUERPO,
                line_height="1.7",
            ),
            align="start",
            spacing="2",
            width="100%",
        ),
        padding="2rem",
        border_radius=RADIO_EXTRA_GRANDE,
        border=f"1px solid {COLOR_BORDE_SUAVE}",
        background=COLOR_FONDO_CARTA,
        width="100%",
        height="100%",
    )


def _seccion_mision_vision() -> rx.Component:
    """Sección con misión y visión lado a lado."""
    return rx.box(
        rx.grid(
            _tarjeta_myv(
                "target",
                "Misión",
                "Formar Técnicos Superiores competentes, con sólidos valores "
                "éticos y humanos, capaces de responder a las demandas del "
                "sector productivo y contribuir al desarrollo del país.",
            ),
            _tarjeta_myv(
                "eye",
                "Visión",
                "Ser el instituto técnico de referencia en Bolivia, reconocido "
                "por la calidad de sus egresados y por su contribución al "
                "desarrollo técnico y profesional de la región.",
            ),
            columns=rx.breakpoints(initial="1", md="2"),
            spacing="4",
            width="100%",
        ),
        max_width="72rem",
        margin="0 auto",
        padding="3rem 1.5rem",
        width="100%",
    )


def _tarjeta_valor(valor: dict) -> rx.Component:
    """Tarjeta de valor institucional."""
    return rx.box(
        rx.vstack(
            rx.box(
                rx.icon(valor["icono"], size=20, color=COLOR_ACENTO_TEXTO),
                padding="0.625rem",
                border_radius=RADIO_GRANDE,
                background=COLOR_ACENTO_FONDO,
                display="flex",
                align_items="center",
                justify_content="center",
                width="fit-content",
                margin_bottom="0.75rem",
            ),
            rx.heading(
                valor["titulo"],
                size="3",
                font_weight="700",
                color=COLOR_TEXTO_PRINCIPAL,
            ),
            rx.text(
                valor["descripcion"],
                font_size="0.875rem",
                color=COLOR_TEXTO_SECUNDARIO,
                line_height="1.5",
            ),
            align="start",
            spacing="1",
            width="100%",
        ),
        padding="1.5rem",
        border_radius=RADIO_GRANDE,
        border=f"1px solid {COLOR_BORDE_SUAVE}",
        background=COLOR_FONDO_SUAVE,
        width="100%",
        height="100%",
    )


def _seccion_valores() -> rx.Component:
    """Sección de valores institucionales."""
    return rx.box(
        rx.vstack(
            rx.vstack(
                rx.text(
                    "NUESTROS VALORES",
                    font_size="0.75rem",
                    font_weight="700",
                    letter_spacing="0.15em",
                    color=COLOR_ACENTO_TEXTO,
                ),
                rx.heading(
                    "Lo que nos define",
                    size="6",
                    font_weight="800",
                    color=COLOR_TEXTO_PRINCIPAL,
                    text_align="center",
                ),
                align="center",
                spacing="2",
                margin_bottom="2rem",
            ),
            rx.grid(
                *[_tarjeta_valor(v) for v in VALORES],
                columns=rx.breakpoints(initial="1", sm="2", lg="4"),
                spacing="3",
                width="100%",
            ),
            width="100%",
            align="center",
        ),
        max_width="72rem",
        margin="0 auto",
        padding="3rem 1.5rem 5rem 1.5rem",
        width="100%",
    )


# ======================================================================
# Vista completa
# ======================================================================


@rx.page(
    route="/sobre-nosotros",
    title=f"Sobre nosotros | {NOMBRE_INSTITUTO}",
)
def vista_sobre_nosotros() -> rx.Component:
    """Página "Sobre nosotros" del instituto."""
    return rx.vstack(
        barra_navegacion_superior(),
        _hero_sobre_nosotros(),
        _seccion_historia(),
        _seccion_mision_vision(),
        _seccion_valores(),
        pie_pagina_institucional(),
        align="center",
        min_height="100vh",
        width="100%",
        spacing="0",
    )