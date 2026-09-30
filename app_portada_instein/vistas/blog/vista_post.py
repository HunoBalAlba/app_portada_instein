"""
Vista de detalle de un post del blog (ruta dinámica "/blog/[post_id]").

Reemplaza el antiguo `dialogos.py`. En vez de un modal, el post se
muestra en una página completa, con:

- Hero editorial con imagen de fondo + título + meta info.
- Cuerpo de lectura con tipografía optimizada (max_width ~65ch).
- Navegación al post anterior / siguiente (si existen).
- CTA al final hacia /contacto.
- Botón "Volver al blog".

Ventajas sobre el diálogo modal
-------------------------------
- **URL compartible**: `/blog/3` se puede enviar por WhatsApp.
- **SEO**: Google indexa cada post.
- **Scroll natural**: sin peleas con flexbox.
- **Botón atrás del navegador** funciona.
- **Mejor lectura larga**: patrón Medium/Substack/NYT.

Nota técnica: PATH PARAMS
-------------------------
`post_id` viene como string en `self.router.page.params["post_id"]`.
El State `EstadoBlog` lo resuelve con la var `post_seleccionado`.

Nota técnica: VALIDACIÓN DE RUTA
--------------------------------
El decorador `@rx.page` incluye `on_load=EstadoBlog.redirigir_si_post_invalido`.
Este evento se ejecuta al cargar la página y redirige a `/404` si el
`post_id` no corresponde a ningún post real.

Gracias a esta validación:
- `/blog/0`   → muestra el post 0.
- `/blog/12`  → muestra el post 12.
- `/blog/1555` → **redirige a `/404`**.
- `/blog/abc`  → **redirige a `/404`**.

Nota técnica: `rx.cond` con dicts
---------------------------------
`EstadoBlog.post_anterior` y `post_siguiente` devuelven `dict` (no
`dict | None`, porque Reflex no serializa `None` en Vars). Cuando no
hay post, devuelven `{}`. `rx.cond({}, ...)` evalúa `{}` como falsy,
así que los `rx.cond(var, ...)` funcionan igual que con `None`.
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
    COLOR_DIVISOR,
    COLOR_FONDO_CARTA,
    COLOR_FONDO_SUAVE,
    COLOR_TEXTO_CUERPO,
    COLOR_TEXTO_PRINCIPAL,
    COLOR_TEXTO_SECUNDARIO,
    NOMBRE_INSTITUTO,
    PADDING_LATERAL,
    RADIO_EXTRA_GRANDE,
    RADIO_GRANDE,
    RADIO_MEDIO,
    RADIO_PASTILLA,
)

from .estado_blog import EstadoBlog
from .helpers_categoria import badge_categoria, fondo_categoria
from .meta_info import meta_info_post


# ======================================================================
# Constantes locales
# ======================================================================

# Ancho máximo de la columna de lectura (tipografía cómoda).
ANCHO_LECTURA = "65ch"

# Ancho máximo del contenido central (botón volver + cuerpo + CTA).
ANCHO_CONTENIDO = "64rem"


# ======================================================================
# Hero editorial del post
# ======================================================================


def _hero_post() -> rx.Component:
    """
    Hero del artículo: imagen de fondo con overlay + badge + título
    + meta info. Altura responsive (no ocupa toda la pantalla).

    Usa `EstadoBlog.post_seleccionado` como fuente de datos.
    """
    post = EstadoBlog.post_seleccionado

    return rx.box(
        # ==========================================================
        # CAPA 1: Fondo de fallback (color de la categoría)
        # ==========================================================
        rx.box(
            position="absolute",
            top="0",
            left="0",
            right="0",
            bottom="0",
            background=fondo_categoria(post["categoria"]),
            z_index="0",
        ),
        # ==========================================================
        # CAPA 2: Imagen real
        # ==========================================================
        rx.image(
            src=f"/blog/{post['imagen']}",
            alt=post["titulo"],
            width="100%",
            height="100%",
            object_fit="cover",
            position="absolute",
            top="0",
            left="0",
            z_index="1",
        ),
        # ==========================================================
        # CAPA 3: Overlay con gradiente
        # ==========================================================
        rx.box(
            position="absolute",
            top="0",
            left="0",
            right="0",
            bottom="0",
            background=(
                "linear-gradient(180deg, "
                "rgba(0,0,0,0.35) 0%, "
                "rgba(0,0,0,0.15) 40%, "
                "rgba(0,0,0,0.85) 100%)"
            ),
            z_index="2",
            pointer_events="none",
        ),
        # ==========================================================
        # CAPA 4: Contenido (badge + título + meta)
        # ==========================================================
        rx.vstack(
            rx.vstack(
                # --- Badge de categoría ---
                rx.box(
                    badge_categoria(post["categoria"]),
                    background="rgba(255,255,255,0.92)",
                    backdrop_filter="blur(8px)",
                    border_radius=RADIO_PASTILLA,
                    padding="0.125rem",
                    box_shadow="0 4px 12px -2px rgba(0,0,0,0.15)",
                    width="fit-content",
                ),
                # --- Título ---
                rx.heading(
                    post["titulo"],
                    size="8",
                    font_weight="900",
                    color="white",
                    line_height="1.15",
                    letter_spacing="-0.02em",
                    text_shadow="0 2px 16px rgba(0,0,0,0.6)",
                    max_width="48rem",
                ),
                # --- Meta info con color blanco forzado ---
                rx.box(
                    meta_info_post(post),
                    css={
                        "& *": {"color": "rgba(255,255,255,0.85) !important"},
                    },
                ),
                spacing="4",
                align="start",
                width="100%",
                max_width=ANCHO_CONTENIDO,
                margin="0 auto",
            ),
            justify="end",
            align="start",
            width="100%",
            padding=[
                "6rem 1.25rem 2rem 1.25rem",
                "8rem 1.5rem 2.5rem 1.5rem",
                "10rem 1.5rem 3rem 1.5rem",
            ],
            min_height=["20rem", "24rem", "28rem"],
            position="relative",
            z_index="3",
        ),
        position="relative",
        width="100%",
        overflow="hidden",
    )


# ======================================================================
# Botón "Volver al blog"
# ======================================================================


def _boton_volver() -> rx.Component:
    """Botón para volver a la lista de posts."""
    return enlace_navegacion(
        "/blog",
        rx.icon("arrow-left", size=16),
        rx.text("Volver al blog", as_="span", font_weight="600"),
        display="inline-flex",
        align_items="center",
        gap="0.5rem",
        padding="0.5rem 1rem",
        border_radius=RADIO_MEDIO,
        background=COLOR_FONDO_CARTA,
        color=COLOR_TEXTO_PRINCIPAL,
        border=f"1px solid {COLOR_BORDE_SUAVE}",
        font_size="0.875rem",
        text_decoration="none",
        transition="all 0.2s",
        width="fit-content",
        _hover={
            "background": COLOR_FONDO_SUAVE,
            "border_color": COLOR_ACENTO_TEXTO,
            "transform": "translateX(-2px)",
        },
    )


# ======================================================================
# Cuerpo del artículo
# ======================================================================


def _cuerpo_post() -> rx.Component:
    """
    Cuerpo del artículo con:
    - Extracto destacado (lead) con borde izquierdo accent.
    - Separador.
    - Contenido completo con tipografía de lectura larga.
    """
    post = EstadoBlog.post_seleccionado

    return rx.vstack(
        # --- Extracto destacado (lead) ---
        rx.box(
            rx.text(
                post["extracto"],
                font_size=["1rem", "1.0625rem", "1.125rem"],
                font_weight="500",
                color=COLOR_TEXTO_PRINCIPAL,
                line_height="1.75",
                font_style="italic",
            ),
            padding_left="1.25rem",
            border_left=f"4px solid {COLOR_ACENTO_TEXTO}",
            width="100%",
        ),
        # --- Separador ---
        rx.box(
            height="1px",
            width="100%",
            background=COLOR_DIVISOR,
            margin_y="1.5rem",
        ),
        # --- Contenido completo ---
        rx.box(
            rx.text(
                post["contenido"],
                font_size=["1rem", "1.0625rem", "1.125rem"],
                color=COLOR_TEXTO_CUERPO,
                line_height="1.85",
                white_space="pre-line",
                max_width=ANCHO_LECTURA,
            ),
            width="100%",
        ),
        spacing="0",
        align="start",
        width="100%",
    )


# ======================================================================
# Navegación entre posts (anterior / siguiente)
# ======================================================================


def _tarjeta_navegacion_post(
    post: rx.Var,
    direccion: str,
) -> rx.Component:
    """
    Tarjeta de navegación a un post adyacente.

    Args:
        post: Var con el dict del post (post_anterior o post_siguiente).
        direccion: "anterior" o "siguiente" (determina el layout).
    """
    es_anterior = direccion == "anterior"

    icono = "arrow-left" if es_anterior else "arrow-right"
    etiqueta = "Anterior" if es_anterior else "Siguiente"
    alineacion_texto = "start" if es_anterior else "end"
    justify_contenido = "start" if es_anterior else "end"

    # --- Bloque de texto compartido (título + etiqueta) ---
    bloque_texto = rx.vstack(
        rx.text(
            etiqueta,
            font_size="0.6875rem",
            font_weight="700",
            color=COLOR_TEXTO_SECUNDARIO,
            text_transform="uppercase",
            letter_spacing="0.05em",
        ),
        rx.text(
            post["titulo"],
            font_size="0.875rem",
            font_weight="600",
            color=COLOR_TEXTO_PRINCIPAL,
            line_height="1.3",
            max_width="18rem",
        ),
        spacing="0",
        align=alineacion_texto,
        flex="1",
        min_width="0",
    )

    # --- Icono (izquierda si es "anterior", derecha si es "siguiente") ---
    icono_componente = rx.icon(icono, size=16, color=COLOR_TEXTO_SECUNDARIO)

    # --- Orden de los hijos según la dirección ---
    if es_anterior:
        contenido_interno = [icono_componente, bloque_texto]
    else:
        contenido_interno = [bloque_texto, icono_componente]

    return enlace_navegacion(
        # Var reactiva: construye la URL según el id del post
        f"/blog/{post['id']}",
        *contenido_interno,
        display="flex",
        align_items="center",
        gap="0.75rem",
        padding="1rem",
        border_radius=RADIO_GRANDE,
        background=COLOR_FONDO_CARTA,
        border=f"1px solid {COLOR_BORDE_SUAVE}",
        text_decoration="none",
        flex="1",
        justify=justify_contenido,
        transition="all 0.2s",
        height="100%",
        min_width="0",
        _hover={
            "border_color": COLOR_ACENTO_TEXTO,
            "transform": "translateY(-2px)",
            "box_shadow": f"0 8px 20px -8px {COLOR_ACENTO_SOLIDO}",
        },
    )


def _navegacion_posts() -> rx.Component:
    """
    Navegación al post anterior y siguiente.

    Solo renderiza las tarjetas que existan. Si no hay ni anterior
    ni siguiente, el bloque completo desaparece.

    ⚠️ Usamos `rx.cond(var, ...)` con la Var directa, NO `.is_not(None)`,
    porque `post_anterior` y `post_siguiente` devuelven `{}` (dict vacío)
    cuando no hay post, y `{}.is_not(None)` sería siempre True.
    """
    hay_anterior = EstadoBlog.post_anterior
    hay_siguiente = EstadoBlog.post_siguiente

    return rx.cond(
        hay_anterior | hay_siguiente,
        rx.box(
            rx.text(
                "Continúa leyendo",
                font_size="0.75rem",
                font_weight="700",
                color=COLOR_TEXTO_SECUNDARIO,
                text_transform="uppercase",
                letter_spacing="0.075em",
                margin_bottom="1rem",
            ),
            rx.flex(
                rx.cond(
                    hay_anterior,
                    _tarjeta_navegacion_post(
                        EstadoBlog.post_anterior,
                        "anterior",
                    ),
                    rx.fragment(),
                ),
                rx.cond(
                    hay_siguiente,
                    _tarjeta_navegacion_post(
                        EstadoBlog.post_siguiente,
                        "siguiente",
                    ),
                    rx.fragment(),
                ),
                gap="1rem",
                width="100%",
                flex_direction=["column", "row"],
                align="stretch",
            ),
            width="100%",
            margin_top="3rem",
        ),
        rx.fragment(),
    )


# ======================================================================
# CTA al final del artículo
# ======================================================================


def _cta_final_post() -> rx.Component:
    """
    Bloque CTA al final del artículo:
    - Título invitando a contactar.
    - Dos botones: "Consultar" (solid crimson) y "Ver más artículos" (outline).
    """
    return rx.box(
        rx.vstack(
            rx.text(
                "¿Te resultó útil este artículo?",
                font_size="0.75rem",
                font_weight="700",
                color=COLOR_ACENTO_TEXTO,
                letter_spacing="0.1em",
                text_transform="uppercase",
            ),
            rx.heading(
                "Hablemos de tu futuro profesional",
                size="6",
                font_weight="800",
                color=COLOR_TEXTO_PRINCIPAL,
                text_align="center",
                line_height="1.2",
            ),
            rx.text(
                "Nuestro equipo de admisiones está disponible para "
                "resolver tus dudas y ayudarte a elegir la carrera "
                "adecuada.",
                font_size="0.9375rem",
                color=COLOR_TEXTO_SECUNDARIO,
                text_align="center",
                max_width="36rem",
                line_height="1.6",
            ),
            rx.flex(
                # --- CTA primario ---
                enlace_navegacion(
                    "/contacto",
                    rx.icon("message-circle", size=18),
                    rx.text("Consultar", as_="span", font_weight="700"),
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
                ),
                # --- CTA secundario ---
                enlace_navegacion(
                    "/blog",
                    rx.icon("arrow-left", size=18),
                    rx.text("Ver más artículos", as_="span", font_weight="600"),
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
                ),
                gap="0.75rem",
                flex_direction=["column", "row"],
                align="center",
                justify="center",
                margin_top="1.5rem",
                width="100%",
            ),
            align="center",
            spacing="3",
            width="100%",
        ),
        padding="2.5rem 1.5rem",
        border_radius=RADIO_EXTRA_GRANDE,
        background=COLOR_ACENTO_FONDO,
        border=f"1px solid {COLOR_ACENTO_TEXTO}",
        width="100%",
        margin_top="3rem",
    )


# ======================================================================
# Vista completa
# ======================================================================


@rx.page(
    route="/blog/[post_id]",
    title=f"Artículo | {NOMBRE_INSTITUTO}",
    on_load=EstadoBlog.redirigir_si_post_invalido,  # ← VALIDACIÓN DE POST_ID
)
def vista_post() -> rx.Component:
    """
    Página de detalle del artículo.

    Estructura:
    1. Barra de navegación.
    2. Hero editorial con imagen + título + meta.
    3. Contenedor con:
       - Botón "Volver al blog".
       - Cuerpo del artículo.
       - Navegación al post anterior / siguiente.
       - CTA final hacia /contacto.
    4. Pie de página.

    El `on_load` (`redirigir_si_post_invalido`) se ejecuta al cargar
    la página. Si el `post_id` de la URL no corresponde a ningún post
    real, redirige automáticamente a `/404`.

    El scroll es natural de la página (no hay flexbox que pelear).
    """
    return rx.vstack(
        # --- Barra de navegación ---
        barra_navegacion_superior(),
        # --- Hero ---
        _hero_post(),
        # --- Cuerpo ---
        rx.box(
            rx.vstack(
                # Botón volver
                _boton_volver(),
                # Cuerpo del artículo
                _cuerpo_post(),
                # Navegación entre posts
                _navegacion_posts(),
                # CTA final
                _cta_final_post(),
                spacing="6",
                width="100%",
                align="start",
            ),
            max_width=ANCHO_CONTENIDO,
            margin="0 auto",
            padding=f"2.5rem {PADDING_LATERAL} 4rem {PADDING_LATERAL}",
            width="100%",
        ),
        # --- Pie de página ---
        pie_pagina_institucional(),
        align="center",
        min_height="100vh",
        width="100%",
        spacing="0",
    )


__all__ = ["vista_post"]