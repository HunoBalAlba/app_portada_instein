"""
Card individual de post + grid de posts + estado vacío + botón
"Cargar más".

Estructura:
- `_card_post`: card con imagen real + badge + título + extracto + meta.
  Es un enlace a `/blog/{id}` (ya NO un trigger de diálogo).
- `_imagen_post`: capa de imagen con fallback de icono por categoría.
- `grid_posts`: grid responsive de cards.
- `estado_vacio`: estado vacío cuando los filtros no devuelven nada.
- `boton_cargar_mas`: botón de paginación simple.

Sistema de color (UX)
---------------------
- Cada card respira el color de su categoría (borde hover + sombra).
- La imagen tiene un overlay sutil con el color de la categoría.
- Los textos son neutros (`gray-11`/`gray-12`).

Nota técnica: navegación
------------------------
Las cards ya NO abren un diálogo modal. Ahora son enlaces a la página
de detalle `/blog/{id}`, donde el post se muestra completo con scroll
natural de página (patrón Medium/Substack/NYT).

Ventajas:
- URL compartible del post.
- SEO indexable.
- Botón atrás del navegador funciona.
- Sin problemas de scroll en móvil.

Nota técnica: imágenes
----------------------
- `post["imagen"]` es el nombre del archivo en `assets/blog/`.
- El fallback usa `icono_categoria` como fondo detrás de la imagen.
"""

import reflex as rx

from app_portada_instein.infraestructura.constantes_visuales import (
    COLOR_ACENTO_SOLIDO,
    COLOR_ACENTO_TEXTO,
    COLOR_BORDE_SUAVE,
    COLOR_FONDO_CARTA,
    COLOR_FONDO_SUAVE,
    COLOR_TEXTO_CUERPO,
    COLOR_TEXTO_PRINCIPAL,
    COLOR_TEXTO_SECUNDARIO,
    RADIO_EXTRA_GRANDE,
    RADIO_MEDIO,
)

from .estado_blog import EstadoBlog
from .helpers_categoria import (
    badge_categoria,
    fondo_categoria,
    icono_categoria,
)
from .meta_info import meta_info_post


# ======================================================================
# Constantes locales
# ======================================================================

# Altura del bloque de imagen en la card.
ALTURA_IMAGEN_CARD = "11rem"

# Ruta base de las imágenes del blog.
RUTA_IMAGENES_BLOG = "/blog/"


# ======================================================================
# Bloque de imagen con overlay de categoría
# ======================================================================


def _imagen_post(post) -> rx.Component:
    """
    Bloque de imagen del post con:
    - Fallback de icono de categoría como fondo.
    - Imagen real encima.
    - Overlay sutil con el color de la categoría.
    - Zoom sutil en hover (delegado a la card padre).

    Args:
        post: Dict del post (puede ser estático o Var).
    """
    return rx.box(
        # --- Capa 1: fondo con icono de categoría (fallback) ---
        rx.box(
            rx.flex(
                icono_categoria(post["categoria"]),
                align="center",
                justify="center",
                width="100%",
                height="100%",
            ),
            position="absolute",
            top="0",
            left="0",
            right="0",
            bottom="0",
            background=fondo_categoria(post["categoria"]),
            display="flex",
            align_items="center",
            justify_content="center",
            z_index="0",
        ),
        # --- Capa 2: imagen real ---
        rx.image(
            src=f"{RUTA_IMAGENES_BLOG}{post['imagen']}",
            alt=post["titulo"],
            width="100%",
            height="100%",
            object_fit="cover",
            position="absolute",
            top="0",
            left="0",
            z_index="1",
            transition="transform 0.4s cubic-bezier(0.4, 0, 0.2, 1)",
            _group_hover={
                "transform": "scale(1.05)",
            },
        ),
        # --- Capa 3: overlay sutil con el color de la categoría ---
        rx.box(
            position="absolute",
            top="0",
            left="0",
            right="0",
            bottom="0",
            background=rx.match(
                post["categoria"],
                (
                    "tecnologia",
                    "linear-gradient(180deg, transparent 60%, rgba(37, 99, 235, 0.15) 100%)",
                ),
                (
                    "contaduria",
                    "linear-gradient(180deg, transparent 60%, rgba(124, 58, 237, 0.15) 100%)",
                ),
                (
                    "empleabilidad",
                    "linear-gradient(180deg, transparent 60%, rgba(22, 163, 74, 0.15) 100%)",
                ),
                (
                    "institucional",
                    "linear-gradient(180deg, transparent 60%, rgba(196, 30, 58, 0.15) 100%)",
                ),
                (
                    "estudiantes",
                    "linear-gradient(180deg, transparent 60%, rgba(234, 88, 12, 0.15) 100%)",
                ),
                (
                    "tutoriales",
                    "linear-gradient(180deg, transparent 60%, rgba(8, 145, 178, 0.15) 100%)",
                ),
                "transparent",
            ),
            z_index="2",
            pointer_events="none",
        ),
        # --- Contenedor ---
        position="relative",
        width="100%",
        height=ALTURA_IMAGEN_CARD,
        border_radius=RADIO_EXTRA_GRANDE,
        overflow="hidden",
        background=COLOR_FONDO_SUAVE,
    )


# ======================================================================
# Card individual de post (enlace a la página de detalle)
# ======================================================================


def _card_post(post) -> rx.Component:
    """
    Card individual de post que enlaza a la página de detalle.

    A diferencia de la versión anterior, ya NO envuelve la card en
    un `rx.dialog`. En su lugar, es un `rx.link` a `/blog/{id}`.

    UX:
    - Imagen con zoom sutil en hover (vía `_group_hover`).
    - Borde de acento en hover.
    - Elevación + sombra tintada con el color de acento.
    - CTA "Leer artículo" con flecha que se anima en hover.
    - Al hacer clic en cualquier parte de la card → navega al detalle.

    Args:
        post: Dict del post (puede ser estático o Var en `rx.foreach`).
    """
    # ==========================================================
    # Card interna (contenido visual)
    # ==========================================================
    card = rx.box(
        rx.vstack(
            # --- Imagen del post ---
            _imagen_post(post),
            # --- Badge de categoría ---
            badge_categoria(post["categoria"]),
            # --- Título ---
            rx.heading(
                post["titulo"],
                size="4",
                font_weight="700",
                color=COLOR_TEXTO_PRINCIPAL,
                line_height="1.3",
            ),
            # --- Extracto ---
            rx.text(
                post["extracto"],
                font_size="0.875rem",
                color=COLOR_TEXTO_CUERPO,
                line_height="1.6",
            ),
            # --- Meta info (autor · fecha · minutos) ---
            meta_info_post(post),
            # --- CTA "Leer artículo" con flecha animada ---
            rx.flex(
                rx.text("Leer artículo", as_="span", font_weight="700"),
                rx.icon(
                    "arrow-right",
                    size=14,
                    class_name="arrow-leer",
                    transition="transform 0.2s",
                ),
                align="center",
                gap="0.375rem",
                color=COLOR_ACENTO_TEXTO,
                font_size="0.8125rem",
                margin_top="0.5rem",
                transition="all 0.2s",
            ),
            align="start",
            spacing="2",
            width="100%",
            height="100%",
        ),
        # ==========================================================
        # Estilos de la card
        # ==========================================================
        padding="1.25rem",
        border_radius=RADIO_EXTRA_GRANDE,
        background=COLOR_FONDO_CARTA,
        border=f"1px solid {COLOR_BORDE_SUAVE}",
        width="100%",
        height="100%",
        transition="all 0.25s cubic-bezier(0.4, 0, 0.2, 1)",
        cursor="pointer",
        _hover={
            "transform": "translateY(-4px)",
            "border_color": COLOR_ACENTO_TEXTO,
            "box_shadow": f"0 16px 40px -12px {COLOR_ACENTO_SOLIDO}",
            "& .arrow-leer": {"transform": "translateX(4px)"},
        },
        # Marcamos el grupo para que la imagen pueda reaccionar al hover
        class_name="card-post",
    )

    # ==========================================================
    # Enlace a la página de detalle (ya no diálogo)
    # ==========================================================
    return rx.link(
        card,
        href=f"/blog/{post['id']}",
        text_decoration="none",
        width="100%",
        height="100%",
        # `display: block` evita comportamientos raros del inline
        display="block",
    )


# ======================================================================
# Grid de posts
# ======================================================================


def grid_posts() -> rx.Component:
    """Grid responsive con los posts paginados."""
    return rx.grid(
        rx.foreach(
            EstadoBlog.posts_paginados,
            _card_post,
        ),
        columns=rx.breakpoints(initial="1", sm="2", md="2", lg="3"),
        spacing="4",
        width="100%",
        align_items="stretch",
    )


# ======================================================================
# Estado vacío
# ======================================================================


def estado_vacio() -> rx.Component:
    """Estado vacío cuando los filtros no devuelven resultados."""
    return rx.vstack(
        # ==========================================================
        # Icono en caja tintada
        # ==========================================================
        rx.box(
            rx.icon("search-x", size=48, color=COLOR_TEXTO_SECUNDARIO),
            padding="1.5rem",
            border_radius=RADIO_EXTRA_GRANDE,
            background=COLOR_FONDO_SUAVE,
            border=f"1px solid {COLOR_BORDE_SUAVE}",
            display="flex",
            align_items="center",
            justify_content="center",
        ),
        # ==========================================================
        # Título + mensaje
        # ==========================================================
        rx.vstack(
            rx.heading(
                "No hay artículos con esos filtros",
                size="5",
                font_weight="700",
                color=COLOR_TEXTO_PRINCIPAL,
                text_align="center",
            ),
            rx.text(
                "Prueba ajustando la búsqueda o seleccionando otra categoría.",
                font_size="0.875rem",
                color=COLOR_TEXTO_SECUNDARIO,
                text_align="center",
                max_width="32rem",
                line_height="1.6",
            ),
            spacing="2",
            align="center",
        ),
        # ==========================================================
        # Botón "Limpiar filtros"
        # ==========================================================
        rx.button(
            rx.icon("rotate-ccw", size=16),
            rx.text("Limpiar filtros", as_="span", font_weight="700"),
            on_click=EstadoBlog.limpiar_filtros,
            size="3",
            variant="solid",
            color_scheme="crimson",
            cursor="pointer",
            margin_top="0.5rem",
        ),
        direction="column",
        align="center",
        justify="center",
        gap="1.5rem",
        padding="4rem 1.5rem",
        width="100%",
    )


# ======================================================================
# Botón "Cargar más"
# ======================================================================


def boton_cargar_mas() -> rx.Component:
    """Botón 'Cargar más' (solo se muestra si hay más posts)."""
    return rx.cond(
        EstadoBlog.hay_mas_posts,
        rx.flex(
            rx.button(
                rx.icon("plus", size=16),
                rx.text(
                    "Cargar más artículos",
                    as_="span",
                    font_weight="700",
                ),
                on_click=EstadoBlog.cargar_mas_posts,
                size="3",
                variant="outline",
                color_scheme="crimson",
                cursor="pointer",
                transition="all 0.2s",
                _hover={
                    "transform": "translateY(-2px)",
                    "box_shadow": f"0 10px 25px -5px {COLOR_ACENTO_SOLIDO}",
                },
            ),
            justify="center",
            width="100%",
            margin_top="2rem",
        ),
        rx.fragment(),
    )


__all__ = [
    "boton_cargar_mas",
    "estado_vacio",
    "grid_posts",
]