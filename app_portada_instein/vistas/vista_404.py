"""
Vista 404: página de error cuando una ruta o recurso no existe.

Se usa para:
- Posts del blog con `post_id` inválido (`/blog/1555`).
- Carreras con `carrera_id` inválido (`/carrera/2gfg`, `/carrera/999`).
- Cualquier ruta no registrada (si configuras `not_found_page`).

Sistema de color (UX)
---------------------
- Número "404" grande con gradiente accent.
- Icono grande en gris para indicar error neutro.
- Título en color principal.
- Descripción en gris secundario.
- Dos CTAs principales: "Volver al inicio" (solid crimson) y
  "Ver blog" o "Ver carreras" (outline), según el `origen`.
- Bloque de "Quizá buscabas" con enlaces rápidos, filtrados según
  el origen (no sugiere "Carreras" si el error vino de una carrera,
  ni "Blog" si vino del blog).

Origen del error
----------------
La 404 acepta un query param opcional `origen` para adaptar los CTAs:

- `/404?origen=blog`     → CTA secundario "Ver blog"
- `/404?origen=carrera`  → CTA secundario "Ver carreras"
- `/404` (sin origen)    → CTAs genéricos

Esto permite que la redirección desde `on_load` comunique al 404
dónde se originó el error, para mostrar acciones relevantes.

Nota técnica: PROPS RESPONSIVE
------------------------------
En Reflex + Radix Themes hay que distinguir dos tipos de props:

1. **Props CSS** (font_size, padding, width, height, gap, margin, etc.)
   → Aceptan listas: `["1rem", "1.5rem", "2rem"]`.

2. **Props de Radix** (size, variant, color_scheme, radius, etc.)
   → Aceptan UN SOLO valor.

Nota técnica: QUERY PARAMS
--------------------------
El query param `origen` se lee con `self.router.page.params.get("origen", "")`.
Si no viene, se asume un error genérico.

Nota técnica: FOREACH CON LISTAS REACTIVAS
------------------------------------------
`rx.foreach` NO acepta listas reactivas construidas dinámicamente
desde un `@rx.var` que devuelva `list[tuple]`. Por eso, la lista
de enlaces sugeridos se calcula en tiempo de compilación dentro de
`vista_404()` (pasándole el origen "real" del State como Var), y se
filtra usando `rx.cond` a nivel de componente para las secciones
que deben cambiar.
"""

import reflex as rx

from app_portada_instein.componentes.barra_navegacion import (
    barra_navegacion_superior,
)
from app_portada_instein.componentes.pie_pagina import (
    pie_pagina_institucional,
)
from app_portada_instein.componentes.primitivos import enlace_navegacion
from app_portada_instein.infraestructura.constantes_visuales import (
    COLOR_ACENTO_FONDO,
    COLOR_ACENTO_SOLIDO,
    COLOR_ACENTO_TEXTO,
    COLOR_BORDE_SUAVE,
    COLOR_FONDO_CARTA,
    COLOR_FONDO_SUAVE,
    COLOR_TEXTO_CUERPO,
    COLOR_TEXTO_PRINCIPAL,
    COLOR_TEXTO_SECUNDARIO,
    NOMBRE_INSTITUTO,
    PADDING_LATERAL,
    RADIO_EXTRA_GRANDE,
    RADIO_GRANDE,
    RADIO_PASTILLA,
)


# ======================================================================
# Constantes locales
# ======================================================================

ANCHO_CONTENIDO = "48rem"


# ======================================================================
# Estado de la vista 404
# ======================================================================


class Estado404(rx.State):
    """Estado de la vista 404."""

    @rx.var
    def origen(self) -> str:
        """
        Origen del error, leído desde el query param `origen`.

        Valores posibles:
        - "blog"     → CTA secundario "Ver blog"
        - "carrera"  → CTA secundario "Ver carreras"
        - ""         → CTAs genéricos
        """
        return self.router.page.params.get("origen", "")

    @rx.var
    def mensaje_contextual(self) -> str:
        """
        Mensaje descriptivo según el origen.

        Personaliza la descripción de la 404 para dar contexto al
        usuario.
        """
        origen = self.router.page.params.get("origen", "")
        if origen == "blog":
            return (
                "El artículo que buscas no existe o fue movido. "
                "Puedes volver al blog o explorar otras secciones."
            )
        if origen == "carrera":
            return (
                "La carrera que buscas no existe o fue movida. "
                "Puedes ver todas las carreras disponibles o volver al inicio."
            )
        return (
            "Lo sentimos, el recurso que buscas no existe o fue movido. "
            "Puedes volver al inicio o explorar nuestro blog."
        )


# ======================================================================
# Hero con el número 404
# ======================================================================


def _hero_404() -> rx.Component:
    """Bloque central con el número 404 grande + mensaje + CTAs."""
    return rx.vstack(
        # ==========================================================
        # Número 404 grande con degradado accent
        # ==========================================================
        rx.text(
            "404",
            font_size=["6rem", "8rem", "10rem"],
            font_weight="900",
            line_height="1",
            letter_spacing="-0.04em",
            background=(
                f"linear-gradient(135deg, "
                f"{COLOR_ACENTO_SOLIDO} 0%, "
                f"{COLOR_ACENTO_TEXTO} 100%)"
            ),
            background_clip="text",
            color="transparent",
            css={"-webkit-background-clip": "text"},
            margin_bottom="0.5rem",
        ),
        # ==========================================================
        # Icono grande en caja gris
        # ==========================================================
        rx.box(
            rx.icon(
                "search-x",
                size=48,
                color=COLOR_TEXTO_SECUNDARIO,
            ),
            padding="1.5rem",
            border_radius=RADIO_EXTRA_GRANDE,
            background=COLOR_FONDO_SUAVE,
            border=f"1px solid {COLOR_BORDE_SUAVE}",
            display="flex",
            align_items="center",
            justify_content="center",
            margin_bottom="1.5rem",
        ),
        # ==========================================================
        # Título
        # ==========================================================
        rx.heading(
            "Página no encontrada",
            size="8",
            font_weight="900",
            color=COLOR_TEXTO_PRINCIPAL,
            text_align="center",
            line_height="1.15",
            letter_spacing="-0.02em",
        ),
        # ==========================================================
        # Descripción (dinámica según origen)
        # ==========================================================
        rx.text(
            Estado404.mensaje_contextual,
            font_size=["0.9375rem", "1rem", "1.0625rem"],
            color=COLOR_TEXTO_SECUNDARIO,
            text_align="center",
            max_width="32rem",
            line_height="1.6",
        ),
        # ==========================================================
        # CTAs (adaptados según origen)
        # ==========================================================
        _ctas_adaptados_por_origen(),
        align="center",
        spacing="0",
        width="100%",
    )


def _cta_primario_comun() -> rx.Component:
    """CTA primario 'Volver al inicio' (siempre visible)."""
    return enlace_navegacion(
        "/",
        rx.icon("home", size=18),
        rx.text("Volver al inicio", as_="span", font_weight="700"),
        display="inline-flex",
        align_items="center",
        gap="0.5rem",
        background=COLOR_ACENTO_SOLIDO,
        color="white",
        padding="0.875rem 1.75rem",
        border_radius=RADIO_PASTILLA,
        font_size="0.9375rem",
        box_shadow=f"0 10px 25px -5px {COLOR_ACENTO_SOLIDO}",
        transition="all 0.2s",
        text_decoration="none",
        _hover={
            "transform": "translateY(-2px)",
            "filter": "brightness(1.1)",
        },
    )


def _cta_secundario_blog() -> rx.Component:
    """CTA secundario 'Ver blog'."""
    return enlace_navegacion(
        "/blog",
        rx.icon("newspaper", size=18),
        rx.text("Ver blog", as_="span", font_weight="600"),
        display="inline-flex",
        align_items="center",
        gap="0.5rem",
        background="transparent",
        color=COLOR_TEXTO_PRINCIPAL,
        padding="0.875rem 1.75rem",
        border_radius=RADIO_PASTILLA,
        font_size="0.9375rem",
        border=f"1px solid {COLOR_BORDE_SUAVE}",
        transition="all 0.2s",
        text_decoration="none",
        _hover={
            "transform": "translateY(-2px)",
            "border_color": COLOR_ACENTO_TEXTO,
        },
    )


def _cta_secundario_carreras() -> rx.Component:
    """CTA secundario 'Ver carreras'."""
    return enlace_navegacion(
        "/carreras",
        rx.icon("graduation-cap", size=18),
        rx.text("Ver carreras", as_="span", font_weight="600"),
        display="inline-flex",
        align_items="center",
        gap="0.5rem",
        background="transparent",
        color=COLOR_TEXTO_PRINCIPAL,
        padding="0.875rem 1.75rem",
        border_radius=RADIO_PASTILLA,
        font_size="0.9375rem",
        border=f"1px solid {COLOR_BORDE_SUAVE}",
        transition="all 0.2s",
        text_decoration="none",
        _hover={
            "transform": "translateY(-2px)",
            "border_color": COLOR_ACENTO_TEXTO,
        },
    )


def _ctas_adaptados_por_origen() -> rx.Component:
    """
    Fila de CTAs que cambia el botón secundario según el origen del error.

    - `origen=carrera` → "Ver carreras"
    - `origen=blog`    → "Ver blog"
    - sin origen       → "Ver blog" (por defecto)
    """
    return rx.flex(
        _cta_primario_comun(),
        rx.cond(
            Estado404.origen == "carrera",
            _cta_secundario_carreras(),
            _cta_secundario_blog(),
        ),
        gap="0.75rem",
        flex_direction=["column", "row"],
        align="center",
        justify="center",
        margin_top="2rem",
        width="100%",
    )


# ======================================================================
# Enlaces sugeridos (con filtrado por origen)
# ======================================================================


# Catálogo completo de enlaces sugeridos: (icono, etiqueta, ruta, origen_excluido)
# `origen_excluido` indica el origen para el que este enlace NO debe
# mostrarse (porque el usuario ya viene de ahí).
ENLACES_404: list[tuple[str, str, str, str]] = [
    ("graduation-cap", "Carreras", "/carreras", "carrera"),
    ("calendar", "Calendario", "/calendario", ""),
    ("book-open", "Admisión", "/admision", ""),
    ("trophy", "Becas", "/becas", ""),
    ("map-pin", "Contacto", "/contacto", ""),
    ("newspaper", "Blog", "/blog", "blog"),
]


def _enlace_sugerido(
    icono: str,
    etiqueta: str,
    ruta: str,
) -> rx.Component:
    """Enlace individual del bloque 'Quizá buscabas'."""
    return enlace_navegacion(
        ruta,
        rx.icon(icono, size=14, color=COLOR_ACENTO_TEXTO),
        rx.text(etiqueta, font_size="0.875rem", font_weight="600"),
        display="inline-flex",
        align_items="center",
        gap="0.5rem",
        padding="0.625rem 1rem",
        border_radius=RADIO_PASTILLA,
        background=COLOR_FONDO_CARTA,
        border=f"1px solid {COLOR_BORDE_SUAVE}",
        color=COLOR_TEXTO_PRINCIPAL,
        text_decoration="none",
        transition="all 0.2s",
        _hover={
            "border_color": COLOR_ACENTO_TEXTO,
            "transform": "translateY(-2px)",
        },
    )


def _enlaces_sugeridos(origen: str) -> rx.Component:
    """
    Bloque con enlaces rápidos a las secciones más visitadas.

    Filtra el enlace del origen del error para no sugerir la misma
    sección que acaba de fallar (ej: si el usuario viene de un error
    de carrera, no se le sugiere "Carreras").

    Args:
        origen: Valor del query param `origen` ("blog", "carrera" o "").
    """
    enlaces_filtrados = [
        item for item in ENLACES_404 if item[3] != origen
    ]

    return rx.box(
        rx.vstack(
            rx.text(
                "Quizá buscabas",
                font_size="0.75rem",
                font_weight="700",
                color=COLOR_TEXTO_SECUNDARIO,
                text_transform="uppercase",
                letter_spacing="0.075em",
                margin_bottom="1rem",
            ),
            rx.flex(
                *[
                    _enlace_sugerido(icono, etiqueta, ruta)
                    for icono, etiqueta, ruta, _ in enlaces_filtrados
                ],
                gap="0.5rem",
                flex_wrap="wrap",
                justify="center",
                width="100%",
            ),
            align="center",
            spacing="0",
            width="100%",
        ),
        max_width=ANCHO_CONTENIDO,
        margin="0 auto",
        padding=f"0 {PADDING_LATERAL} 4rem {PADDING_LATERAL}",
        width="100%",
    )


# ======================================================================
# Vista completa
# ======================================================================


@rx.page(
    route="/404",
    title=f"Página no encontrada | {NOMBRE_INSTITUTO}",
)
def vista_404() -> rx.Component:
    """
    Página de error 404.

    Se activa cuando:
    - El usuario navega a `/404` directamente.
    - Un `on_load` redirige aquí con `?origen=blog` o `?origen=carrera`.

    Los CTAs y los enlaces sugeridos se adaptan al origen del error.
    """
    return rx.vstack(
        barra_navegacion_superior(),
        # --- Bloque central ---
        rx.box(
            _hero_404(),
            max_width=ANCHO_CONTENIDO,
            margin="0 auto",
            padding=[
                "4rem 1.25rem 2rem 1.25rem",
                "6rem 1.5rem 3rem 1.5rem",
                "8rem 1.5rem 3rem 1.5rem",
            ],
            width="100%",
        ),
        # --- Enlaces sugeridos (con filtrado por origen) ---
        rx.cond(
            Estado404.origen == "carrera",
            _enlaces_sugeridos("carrera"),
            rx.cond(
                Estado404.origen == "blog",
                _enlaces_sugeridos("blog"),
                _enlaces_sugeridos(""),
            ),
        ),
        # --- Pie de página ---
        pie_pagina_institucional(),
        align="center",
        min_height="100vh",
        width="100%",
        spacing="0",
    )


__all__ = ["vista_404"]