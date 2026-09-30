"""
Vista Blog Institucional (ruta "/blog").

Este módulo SOLO ensambla los componentes. Toda la lógica vive en
módulos separados:

- `datos_blog.py`         → CATEGORIAS + POSTS.
- `estado_blog.py`        → EstadoBlog (filtros + paginación).
- `helpers_categoria.py`  → helpers de rx.match para categorías.
- `meta_info.py`          → meta info del post.
- `dialogos.py`           → rx.dialog con el contenido completo.
- `hero.py`               → hero con badge + título + subtítulo.
- `post_destacado.py`     → post destacado (featured).
- `filtros_blog.py`       → barra de filtros + pills.
- `card_post.py`          → cards + grid + estado vacío.
- `newsletter_blog.py`    → newsletter inline.
- `cta_blog.py`           → CTA final.
"""

import reflex as rx

from app_portada_instein.componentes.barra_navegacion import (
    barra_navegacion_superior,
)
from app_portada_instein.componentes.pie_pagina import (
    pie_pagina_institucional,
)
from app_portada_instein.infraestructura.constantes_visuales import (
    NOMBRE_INSTITUTO,
)

from .card_post import boton_cargar_mas, estado_vacio, grid_posts
from .cta_blog import cta_blog
from .estado_blog import EstadoBlog
from .filtros_blog import barra_filtros
from .hero import hero_blog
from .newsletter_blog import newsletter_blog
from .post_destacado import post_destacado


# ======================================================================
# Constantes locales
# ======================================================================

ANCHO_CONTENIDO = "64rem"
PADDING_LATERAL = "1.5rem"


# ======================================================================
# Vista
# ======================================================================


@rx.page(route="/blog", title=f"Blog | {NOMBRE_INSTITUTO}")
def vista_blog() -> rx.Component:
    """Página del blog institucional del instituto."""
    return rx.vstack(
        barra_navegacion_superior(),
        hero_blog(),
        rx.box(
            rx.vstack(
                # --- Post destacado ---
                post_destacado(),
                # --- Filtros ---
                barra_filtros(),
                # --- Grid o estado vacío ---
                rx.cond(
                    EstadoBlog.hay_resultados,
                    rx.vstack(
                        grid_posts(),
                        boton_cargar_mas(),
                        spacing="0",
                        width="100%",
                    ),
                    estado_vacio(),
                ),
                # --- Newsletter ---
                newsletter_blog(),
                spacing="6",
                width="100%",
            ),
            max_width=ANCHO_CONTENIDO,
            margin="0 auto",
            padding=f"2rem {PADDING_LATERAL} 4rem {PADDING_LATERAL}",
            width="100%",
        ),
        cta_blog(),
        pie_pagina_institucional(),
        align="center",
        min_height="100vh",
        width="100%",
        spacing="0",
    )


__all__ = ["vista_blog"]