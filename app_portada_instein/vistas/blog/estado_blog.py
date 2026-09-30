"""
Estado del Blog Institucional.

... (docstring existente) ...
"""

import reflex as rx

from .datos_blog import POSTS


# ======================================================================
# Constantes del módulo
# ======================================================================

POSTS_POR_PAGINA = 6


# ======================================================================
# Estado
# ======================================================================


class EstadoBlog(rx.State):
    """Estado de filtros y paginación del blog."""

    # ==================================================================
    # ESTADO PERSISTENTE
    # ==================================================================

    categoria_activa: str = "todas"
    texto_busqueda: str = ""
    posts_visibles: int = POSTS_POR_PAGINA

    # ==================================================================
    # VARS COMPUTADAS: LISTAS FILTRADAS
    # ==================================================================

    @rx.var
    def posts_filtrados(self) -> list[dict]:
        """Posts filtrados por categoría y búsqueda (sin el destacado)."""
        posts = [p for p in POSTS if not p["destacado"]]

        if self.categoria_activa != "todas":
            posts = [
                p for p in posts
                if p["categoria"] == self.categoria_activa
            ]

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
    def posts_paginados(self) -> list[dict]:
        """Posts filtrados, limitados por la paginación actual."""
        return self.posts_filtrados[: self.posts_visibles]

    @rx.var
    def post_destacado(self) -> dict:
        """Post destacado (siempre el primero con `destacado=True`)."""
        for post in POSTS:
            if post["destacado"]:
                return post
        return POSTS[0]

    # ==================================================================
    # VARS COMPUTADAS: CONTADORES Y FLAGS
    # ==================================================================

    @rx.var
    def hay_resultados(self) -> bool:
        """Indica si hay posts que coincidan con los filtros."""
        return len(self.posts_filtrados) > 0

    @rx.var
    def contador_resultados(self) -> str:
        """Texto con el número de resultados."""
        return str(len(self.posts_filtrados))

    @rx.var
    def hay_mas_posts(self) -> bool:
        """Indica si hay más posts por cargar."""
        return len(self.posts_filtrados) > self.posts_visibles

    @rx.var
    def hay_filtros_activos(self) -> bool:
        """Indica si hay algún filtro activo."""
        return (
            self.categoria_activa != "todas"
            or self.texto_busqueda != ""
        )

    # ==================================================================
    # VARS COMPUTADAS: POST SELECCIONADO (ruta /blog/[post_id])
    # ==================================================================
    # ⚠️ CAMBIO IMPORTANTE: `post_seleccionado` YA NO TIENE FALLBACK.
    # Si el post no existe, devuelve `{}` (dict vacío). Esto permite
    # detectar IDs inválidos y redirigir a 404.
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
    def post_seleccionado(self) -> dict:
        """
        Devuelve el post correspondiente al `post_id` de la URL.

        ⚠️ Ya NO tiene fallback a POSTS[0]. Si el post no existe,
        devuelve `{}` (dict vacío). Esto permite detectar IDs inválidos
        y redirigir a la página 404.
        """
        post_id = self.post_id_desde_url
        if post_id < 0:
            return {}

        for post in POSTS:
            if post["id"] == post_id:
                return post
        return {}

    @rx.var
    def post_es_valido(self) -> bool:
        """Indica si el `post_id` de la URL corresponde a un post real."""
        return bool(self.post_seleccionado)

    # ==================================================================
    # VARS COMPUTADAS: NAVEGACIÓN ENTRE POSTS
    # ==================================================================

    @rx.var
    def post_anterior(self) -> dict:
        """
        Post inmediatamente anterior al actual (por id).

        Devuelve `{}` si no hay post anterior o si el actual no existe.
        """
        actual = self.post_seleccionado
        if not actual:
            return {}
        actual_id = actual["id"]
        for post in POSTS:
            if post["id"] == actual_id - 1:
                return post
        return {}

    @rx.var
    def post_siguiente(self) -> dict:
        """
        Post inmediatamente siguiente al actual (por id).

        Devuelve `{}` si no hay post siguiente o si el actual no existe.
        """
        actual = self.post_seleccionado
        if not actual:
            return {}
        actual_id = actual["id"]
        for post in POSTS:
            if post["id"] == actual_id + 1:
                return post
        return {}

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
        """Restablece todos los filtros."""
        self.categoria_activa = "todas"
        self.texto_busqueda = ""
        self.posts_visibles = POSTS_POR_PAGINA

    @rx.event
    def cargar_mas_posts(self):
        """Incrementa el número de posts visibles."""
        self.posts_visibles += POSTS_POR_PAGINA

    # ==================================================================
    # EVENT HANDLERS: VALIDACIÓN DE RUTA
    # ==================================================================

    @rx.event
    def redirigir_si_post_invalido(self):
        """
        Redirige a la página 404 si el `post_id` de la URL no existe.

        Este evento se dispara desde `on_load` de la vista `/blog/[post_id]`.
        Si el post es válido, no hace nada y la vista se renderiza normal.

        Returns:
            `rx.redirect` si el post no existe, `None` si existe.
        """
        if not self.post_seleccionado:
            return rx.redirect("/404")
        return None




    @rx.event
    def redirigir_si_post_invalido(self):
        """
        Redirige a la página 404 si el `post_id` de la URL no existe.

        Añade `?origen=blog` al query param para que la 404 muestre
        CTAs contextuales ("Ver blog").
        """
        if not self.post_seleccionado:
            return rx.redirect("/404?origen=blog")  # ← AÑADIR ?origen=blog
        return None


    
# ======================================================================
# EXPORTS
# ======================================================================

__all__ = ["EstadoBlog", "POSTS_POR_PAGINA"]