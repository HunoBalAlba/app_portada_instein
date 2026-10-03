"""
Estado del Blog Institucional.

Gestiona:
- Filtros por categoría y búsqueda de texto.
- Paginación progresiva (botón "Cargar más").
- Resolución del post seleccionado a partir del `post_id` de la URL.
- Navegación al post anterior / siguiente.
- Validación de ruta (redirección a `/404?origen=blog` si el post no existe).

Nota técnica: TIPADO ESTRICTO CON `Post`
----------------------------------------
Las `@rx.var` que devuelven un post (destacado, seleccionado, anterior,
siguiente) están tipadas como `Post` (el `TypedDict` de `datos_blog`),
NO como `dict` genérico.

Esto es CRÍTICO porque Reflex necesita tipos precisos para props
tipadas como `rx.image(alt=str)`:

    ❌ dict genérico → post["titulo"] se infiere como str | int | bool
    ✅ Post          → post["titulo"] se infiere como str

Sin esto, Reflex lanza:

    TypeError: Invalid var passed for prop Img.alt, expected type
    <class 'str'>, got value ... of type str | int | bool.

Nota técnica: FALLBACK DE `post_seleccionado`
---------------------------------------------
`post_seleccionado` SIEMPRE devuelve un `Post` válido (fallback al
destacado) para garantizar el tipado que `rx.image`/`rx.foreach`
necesitan. La validez real del id se comprueba con `post_es_valido`.

El `on_load` de `vista_post.py` usa `post_es_valido` (no
`post_seleccionado`) para decidir si redirige a `/404`.

Nota técnica: FLAGS `hay_post_anterior` / `hay_post_siguiente`
-------------------------------------------------------------
Como `post_anterior` y `post_siguiente` NUNCA son falsy (siempre
devuelven un `Post` con al menos el destacado como fallback), NO se
pueden usar en `rx.cond(post_anterior, ...)` porque el condicional
siempre evaluaría a True.

Para decidir si mostrar u ocultar las tarjetas de navegación, se usan
los flags `hay_post_anterior` y `hay_post_siguiente` (bool), que SÍ
detectan si existe un post vecino real.
"""

from __future__ import annotations

import reflex as rx

from .datos_blog import (
    POSTS,
    Post,
    obtener_post,
    obtener_post_destacado,
)


# ======================================================================
# Constantes del módulo
# ======================================================================

POSTS_POR_PAGINA: int = 6
"""Cantidad de posts visibles en cada "página" (botón Cargar más)."""


# ======================================================================
# Estado
# ======================================================================


class EstadoBlog(rx.State):
    """Estado de filtros y paginación del blog."""

    # ==================================================================
    # ESTADO PERSISTENTE
    # ==================================================================

    categoria_activa: str = "todas"
    """Categoría activa del filtro (clave de `CATEGORIAS`, o "todas")."""

    texto_busqueda: str = ""
    """Texto de búsqueda por título, extracto o autor."""

    posts_visibles: int = POSTS_POR_PAGINA
    """Cantidad de posts visibles actualmente (paginación progresiva)."""

    # ==================================================================
    # VARS COMPUTADAS: LISTAS FILTRADAS
    # ==================================================================

    @rx.var
    def posts_filtrados(self) -> list[Post]:
        """
        Posts filtrados por categoría y búsqueda (sin el destacado).

        El post destacado se excluye porque se renderiza aparte con
        el componente `post_destacado`.
        """
        posts: list[Post] = [
            p for p in POSTS if not p["destacado"]
        ]

        # --- Filtro por categoría ---
        if self.categoria_activa != "todas":
            posts = [
                p for p in posts
                if p["categoria"] == self.categoria_activa
            ]

        # --- Filtro por búsqueda de texto ---
        if self.texto_busqueda:
            busqueda = self.texto_busqueda.lower()
            posts = [
                p for p in posts
                if busqueda in p["titulo"].lower()
                or busqueda in p["extracto"].lower()
                or busqueda in p["autor"].lower()
            ]

        return posts

    @rx.var
    def posts_paginados(self) -> list[Post]:
        """Posts filtrados, limitados por la paginación actual."""
        return self.posts_filtrados[: self.posts_visibles]

    @rx.var
    def post_destacado(self) -> Post:
        """
        Post destacado (el primero con `destacado=True`).

        ✅ Devuelve `Post` (no dict genérico) para que Reflex sepa que
        `post["titulo"]` es `str` y lo acepte en `rx.image(alt=...)`.
        """
        return obtener_post_destacado()

    # ==================================================================
    # VARS COMPUTADAS: CONTADORES Y FLAGS
    # ==================================================================

    @rx.var
    def hay_resultados(self) -> bool:
        """Indica si hay posts que coincidan con los filtros."""
        return len(self.posts_filtrados) > 0

    @rx.var
    def contador_resultados(self) -> str:
        """Texto con el número de resultados (para mostrar en la UI)."""
        return str(len(self.posts_filtrados))

    @rx.var
    def hay_mas_posts(self) -> bool:
        """Indica si hay más posts por cargar (botón "Cargar más")."""
        return len(self.posts_filtrados) > self.posts_visibles

    @rx.var
    def hay_filtros_activos(self) -> bool:
        """Indica si hay algún filtro activo (categoría o búsqueda)."""
        return (
            self.categoria_activa != "todas"
            or self.texto_busqueda != ""
        )

    # ==================================================================
    # VARS COMPUTADAS: POST SELECCIONADO (ruta /blog/[post_id])
    # ==================================================================

    @rx.var
    def post_id_desde_url(self) -> int:
        """
        Extrae el `post_id` de la URL como int.

        Devuelve -1 si el valor no es convertible a int (por ejemplo,
        `/blog/abc`), lo que se interpreta como inválido.
        """
        valor_crudo = self.router.page.params.get("post_id", "")
        try:
            return int(valor_crudo)
        except (ValueError, TypeError):
            return -1

    @rx.var
    def post_seleccionado(self) -> Post:
        """
        Devuelve el post correspondiente al `post_id` de la URL.

        ⚠️ SIEMPRE devuelve un `Post` válido (fallback al destacado)
        para garantizar el tipado que `rx.image`/`rx.foreach` necesitan.

        La validez real del id se comprueba con `post_es_valido`, que
        se usa en `redirigir_si_post_invalido`.
        """
        post = obtener_post(self.post_id_desde_url)
        return post if post else obtener_post_destacado()

    @rx.var
    def post_es_valido(self) -> bool:
        """Indica si el `post_id` de la URL corresponde a un post real."""
        return obtener_post(self.post_id_desde_url) is not None

    # ==================================================================
    # VARS COMPUTADAS: NAVEGACIÓN ENTRE POSTS
    # ==================================================================

    @rx.var
    def hay_post_anterior(self) -> bool:
        """
        Indica si existe un post anterior al actual (por id).

        ✅ Se usa en `vista_post.py` para decidir si mostrar la tarjeta
        de navegación al post anterior. NO se puede usar
        `rx.cond(post_anterior, ...)` directamente porque `post_anterior`
        siempre devuelve un `Post` (nunca es falsy).
        """
        actual = obtener_post(self.post_id_desde_url)
        if actual is None:
            return False
        return obtener_post(actual["id"] - 1) is not None

    @rx.var
    def hay_post_siguiente(self) -> bool:
        """
        Indica si existe un post siguiente al actual (por id).

        ✅ Se usa en `vista_post.py` para decidir si mostrar la tarjeta
        de navegación al post siguiente. NO se puede usar
        `rx.cond(post_siguiente, ...)` directamente porque `post_siguiente`
        siempre devuelve un `Post` (nunca es falsy).
        """
        actual = obtener_post(self.post_id_desde_url)
        if actual is None:
            return False
        return obtener_post(actual["id"] + 1) is not None

    @rx.var
    def post_anterior(self) -> Post:
        """
        Post inmediatamente anterior al actual (por id).

        ✅ Devuelve `Post` (no dict) por el mismo motivo que
        `post_seleccionado`. Si no hay anterior, devuelve el destacado.

        ⚠️ Para saber si HAY un post anterior real, usa el flag
        `hay_post_anterior` (bool).
        """
        actual = obtener_post(self.post_id_desde_url)
        if actual is None:
            return obtener_post_destacado()
        anterior = obtener_post(actual["id"] - 1)
        return anterior if anterior else obtener_post_destacado()

    @rx.var
    def post_siguiente(self) -> Post:
        """
        Post inmediatamente siguiente al actual (por id).

        ✅ Devuelve `Post` (no dict) por el mismo motivo que
        `post_seleccionado`. Si no hay siguiente, devuelve el destacado.

        ⚠️ Para saber si HAY un post siguiente real, usa el flag
        `hay_post_siguiente` (bool).
        """
        actual = obtener_post(self.post_id_desde_url)
        if actual is None:
            return obtener_post_destacado()
        siguiente = obtener_post(actual["id"] + 1)
        return siguiente if siguiente else obtener_post_destacado()

    # ==================================================================
    # EVENT HANDLERS: FILTROS Y PAGINACIÓN
    # ==================================================================

    @rx.event
    def seleccionar_categoria(self, categoria: str):
        """Cambia la categoría activa y resetea la paginación."""
        self.categoria_activa = categoria
        self.posts_visibles = POSTS_POR_PAGINA

    @rx.event
    def actualizar_busqueda(self, texto: str):
        """Actualiza el texto de búsqueda y resetea la paginación."""
        self.texto_busqueda = texto
        self.posts_visibles = POSTS_POR_PAGINA

    @rx.event
    def limpiar_filtros(self):
        """Restablece todos los filtros a sus valores por defecto."""
        self.categoria_activa = "todas"
        self.texto_busqueda = ""
        self.posts_visibles = POSTS_POR_PAGINA

    @rx.event
    def cargar_mas_posts(self):
        """Incrementa el número de posts visibles en una página más."""
        self.posts_visibles += POSTS_POR_PAGINA

    # ==================================================================
    # EVENT HANDLERS: VALIDACIÓN DE RUTA
    # ==================================================================

    @rx.event
    def redirigir_si_post_invalido(self):
        """
        Redirige a `/404?origen=blog` si el `post_id` de la URL no existe.

        Este evento se dispara desde `on_load` de la vista
        `/blog/[post_id]`. Si el post es válido, no hace nada.

        El query param `?origen=blog` permite que la página 404 muestre
        CTAs contextuales ("Ver blog") en lugar de los genéricos.

        Returns:
            `rx.redirect("/404?origen=blog")` si el post no existe,
            `None` si existe (no hace nada).
        """
        if not self.post_es_valido:
            return rx.redirect("/404?origen=blog")
        return None


# ======================================================================
# EXPORTS
# ======================================================================

__all__ = [
    "EstadoBlog",
    "POSTS_POR_PAGINA",
]