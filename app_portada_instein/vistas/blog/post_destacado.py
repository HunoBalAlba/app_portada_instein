"""
Post destacado (featured) del blog con imagen real.

Estructura:
- `_imagen_destacada`: bloque de imagen grande con overlay y badge
  "DESTACADO".
- `post_destacado`: card completa con layout de dos columnas (imagen +
  contenido) que enlaza a la página de detalle del post.

Sistema de color (UX)
---------------------
- La imagen tiene un overlay con el color de la categoría.
- El borde hover y la sombra usan el accent institucional (crimson).
- El badge "DESTACADO" va sobre la imagen, esquina superior izquierda.

Nota técnica: navegación
------------------------
La card destacada ya NO abre un diálogo modal. Ahora es un enlace
directo a la página de detalle `/blog/{id}`, donde el post se muestra
completo con scroll natural de página (patrón Medium/Substack/NYT).

Ventajas:
- URL compartible del post destacado.
- SEO indexable.
- Botón atrás del navegador funciona.
- Sin problemas de scroll en móvil.

Nota técnica: imágenes
----------------------
- `post["imagen"]` es el nombre del archivo en `assets/blog/`.
- La ruta se construye como `/blog/{post['imagen']}`.
- El zoom de la imagen se logra con el selector `& img` en el hover
  de la card.
"""

import reflex as rx

from app_portada_instein.infraestructura.constantes_visuales import (
    COLOR_ACENTO_FONDO,
    COLOR_ACENTO_SOLIDO,
    COLOR_ACENTO_TEXTO,
    COLOR_BORDE_SUAVE,
    COLOR_FONDO_CARTA,
    COLOR_FONDO_SUAVE,
    COLOR_TEXTO_CUERPO,
    COLOR_TEXTO_PRINCIPAL,
    RADIO_EXTRA_GRANDE,
    RADIO_MEDIO,
    RADIO_PASTILLA,
)

from .estado_blog import EstadoBlog
from .helpers_categoria import badge_categoria, fondo_categoria
from .meta_info import meta_info_post


# ======================================================================
# Constantes locales
# ======================================================================

# Altura responsive del bloque de imagen destacada.
ALTURA_IMAGEN_DESTACADA = ["14rem", "16rem", "18rem"]

# Ancho responsive del bloque de imagen.
ANCHO_IMAGEN_DESTACADA = ["100%", "100%", "40%"]

# Ruta base de las imágenes del blog.
RUTA_IMAGENES_BLOG = "/blog/"


# ======================================================================
# Bloque de imagen destacada
# ======================================================================


def _imagen_destacada(post) -> rx.Component:
    """
    Bloque de imagen grande del post destacado con:
    - Fallback de color de categoría como fondo.
    - Imagen real encima.
    - Overlay sutil con gradiente del color de la categoría.
    - Badge "DESTACADO" en la esquina superior izquierda.
    - Zoom sutil en hover (vía `& img` en la card padre).

    Args:
        post: Dict del post destacado (Var reactivo).
    """
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
            src=f"{RUTA_IMAGENES_BLOG}{post['imagen']}",
            alt=post["titulo"],
            width="100%",
            height="100%",
            object_fit="cover",
            position="absolute",
            top="0",
            left="0",
            z_index="1",
            transition="transform 0.5s cubic-bezier(0.4, 0, 0.2, 1)",
        ),
        # ==========================================================
        # CAPA 3: Overlay sutil con gradiente
        # ==========================================================
        rx.box(
            position="absolute",
            top="0",
            left="0",
            right="0",
            bottom="0",
            background=(
                "linear-gradient(180deg, "
                "rgba(0,0,0,0.25) 0%, "
                "rgba(0,0,0,0.05) 40%, "
                "rgba(0,0,0,0.4) 100%)"
            ),
            z_index="2",
            pointer_events="none",
        ),
        # ==========================================================
        # CAPA 4: Badge "DESTACADO" en la esquina superior izquierda
        # ==========================================================
        rx.flex(
            rx.icon("star", size=12, color="white", fill="white"),
            rx.text(
                "DESTACADO",
                font_size="0.625rem",
                font_weight="800",
                color="white",
                letter_spacing="0.15em",
            ),
            align="center",
            gap="0.375rem",
            padding="0.375rem 0.75rem",
            border_radius=RADIO_PASTILLA,
            background="rgba(0,0,0,0.5)",
            backdrop_filter="blur(8px)",
            border="1px solid rgba(255,255,255,0.2)",
            position="absolute",
            top="1rem",
            left="1rem",
            z_index="3",
            width="fit-content",
        ),
        # ==========================================================
        # Contenedor principal
        # ==========================================================
        position="relative",
        height=ALTURA_IMAGEN_DESTACADA,
        width=ANCHO_IMAGEN_DESTACADA,
        border_radius=RADIO_EXTRA_GRANDE,
        overflow="hidden",
        background=COLOR_FONDO_SUAVE,
        flex_shrink="0",
    )


# ======================================================================
# Post destacado completo
# ======================================================================


def post_destacado() -> rx.Component:
    """
    Post destacado con layout de dos columnas que enlaza al detalle.

    Estructura:
    - Columna izquierda (40%): imagen grande con overlay y badge.
    - Columna derecha (60%): badge de categoría + título + extracto
      + meta + CTA "Leer artículo".

    La card completa es un enlace a `/blog/{id}` (ya no un diálogo).

    UX:
    - Imagen con zoom sutil en hover (`& img`).
    - Borde hover con accent + sombra elevada.
    - CTA "Leer artículo" con flecha que se desplaza en hover.
    - En móvil/tablet se apila verticalmente (imagen arriba, texto abajo).
    """
    post = EstadoBlog.post_destacado

    # ==========================================================
    # Card destacada (contenido visual)
    # ==========================================================
    card_destacada = rx.box(
        rx.flex(
            # ==========================================================
            # Columna izquierda: imagen destacada
            # ==========================================================
            _imagen_destacada(post),
            # ==========================================================
            # Columna derecha: contenido
            # ==========================================================
            rx.vstack(
                # --- Badge de categoría ---
                badge_categoria(post["categoria"]),
                # --- Título ---
                rx.heading(
                    post["titulo"],
                    size="7",
                    font_weight="800",
                    color=COLOR_TEXTO_PRINCIPAL,
                    line_height="1.2",
                    letter_spacing="-0.02em",
                ),
                # --- Extracto ---
                rx.text(
                    post["extracto"],
                    font_size="0.9375rem",
                    color=COLOR_TEXTO_CUERPO,
                    line_height="1.7",
                ),
                # --- Meta info ---
                meta_info_post(post),
                # --- CTA "Leer artículo" ---
                rx.flex(
                    rx.text("Leer artículo", as_="span", font_weight="700"),
                    rx.icon(
                        "arrow-right",
                        size=16,
                        class_name="arrow-destacado",
                        transition="transform 0.2s",
                    ),
                    align="center",
                    gap="0.5rem",
                    background=COLOR_ACENTO_SOLIDO,
                    color="white",
                    padding="0.75rem 1.5rem",
                    border_radius=RADIO_PASTILLA,
                    font_size="0.875rem",
                    margin_top="0.5rem",
                    box_shadow=f"0 10px 25px -5px {COLOR_ACENTO_SOLIDO}",
                    transition="all 0.2s",
                    cursor="pointer",
                ),
                align="start",
                spacing="3",
                flex="1",
                min_width="0",
            ),
            # --- Dirección responsive ---
            direction=rx.breakpoints(
                initial="column",
                sm="column",
                md="row",
                lg="row",
            ),
            gap="2rem",
            align="center",
            width="100%",
        ),
        # ==========================================================
        # Estilos de la card
        # ==========================================================
        padding="1.5rem",
        border_radius=RADIO_EXTRA_GRANDE,
        background=COLOR_FONDO_CARTA,
        border=f"1px solid {COLOR_BORDE_SUAVE}",
        width="100%",
        transition="all 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
        cursor="pointer",
        _hover={
            "border_color": COLOR_ACENTO_TEXTO,
            "box_shadow": f"0 20px 40px -10px {COLOR_ACENTO_SOLIDO}",
            # Zoom sutil de la imagen (afecta a cualquier <img> dentro)
            "& img": {"transform": "scale(1.05)"},
            # Flecha se desliza
            "& .arrow-destacado": {"transform": "translateX(4px)"},
        },
    )

    # ==========================================================
    # Enlace directo a la página de detalle
    # ==========================================================
    return rx.link(
        card_destacada,
        href=f"/blog/{post['id']}",
        text_decoration="none",
        width="100%",
        display="block",
    )


__all__ = ["post_destacado"]