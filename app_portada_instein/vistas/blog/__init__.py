"""
Paquete de la vista Blog Institucional.

API pública:
- `vista_blog()`: la página completa registrada con `@rx.page`.
- `vista_post()`: la página de detalle del artículo.

Uso desde `app_portada_instein.py`:
    from app_portada_instein.vistas.blog import vista_blog, vista_post
"""

from .vista_blog import vista_blog
from .vista_post import vista_post

__all__ = ["vista_blog", "vista_post"]