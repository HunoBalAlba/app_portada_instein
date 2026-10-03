"""
Meta info del post: autor · fecha · minutos de lectura.

Usado en:
- `post_destacado.py` → card destacada del blog.
- `card_post.py`      → cards del grid de posts.
- `vista_post.py`     → hero editorial del detalle.

Nota técnica: TIPADO ESTRICTO CON `Post`
----------------------------------------
`meta_info_post(post: Post)` recibe un `Post` (el `TypedDict` de
`datos_blog`), NO un `dict` genérico.

Esto es CRÍTICO porque Reflex necesita tipos precisos para props
tipadas. Si el tipo es `dict`, los campos internos se infieren como
`str | int | bool` y `rx.text(...)` puede fallar.

Además, `post["minutos_lectura"]` es `int` y se usa dentro de un
f-string (`f"{post['minutos_lectura']} min"`), lo cual requiere que
Reflex sepa que es un `int` para formatearlo correctamente.
"""

from __future__ import annotations

import reflex as rx

from app_portada_instein.infraestructura.constantes_visuales import (
    COLOR_TEXTO_SECUNDARIO,
)

from .datos_blog import Post


# ======================================================================
# Constantes locales
# ======================================================================

TAMANO_ICONO_META: int = 12
"""Tamaño (en px) de los iconos de la meta info."""

TAMANO_TEXTO_META: str = "0.75rem"
"""Tamaño de fuente de los textos de la meta info."""


# ======================================================================
# Helpers internos
# ======================================================================


def _separador() -> rx.Component:
    """
    Separador visual entre los items de la meta info (un `·`).

    Se usa entre autor ↔ fecha ↔ minutos de lectura.
    """
    return rx.text(
        "·",
        font_size=TAMANO_TEXTO_META,
        color=COLOR_TEXTO_SECUNDARIO,
    )


def _item_meta(icono: str, texto: str | rx.Var) -> rx.Component:
    """
    Item individual de la meta info (icono + texto).

    Args:
        icono: Nombre del icono de Lucide.
        texto: Texto del item (str o Var reactiva).
    """
    return rx.flex(
        rx.icon(
            icono,
            size=TAMANO_ICONO_META,
            color=COLOR_TEXTO_SECUNDARIO,
        ),
        rx.text(
            texto,
            font_size=TAMANO_TEXTO_META,
            color=COLOR_TEXTO_SECUNDARIO,
        ),
        align="center",
        gap="0.375rem",
    )


# ======================================================================
# Meta info completa
# ======================================================================


def meta_info_post(post: Post) -> rx.Component:
    """
    Meta info del post: autor · fecha · minutos de lectura.

    Args:
        post: `Post` (TypedDict). Tipado estricto para que Reflex
            sepa que:
            - `post["autor"]` es `str`
            - `post["fecha"]` es `str`
            - `post["minutos_lectura"]` es `int`

    Returns:
        Fila horizontal con los 3 items separados por `·`.
    """
    return rx.flex(
        # --- Autor ---
        _item_meta("user", post["autor"]),
        _separador(),
        # --- Fecha ---
        _item_meta("calendar", post["fecha"]),
        _separador(),
        # --- Minutos de lectura ---
        _item_meta("clock", f"{post['minutos_lectura']} min"),
        align="center",
        gap="0.375rem",
        flex_wrap="wrap",
    )


__all__ = ["meta_info_post"]