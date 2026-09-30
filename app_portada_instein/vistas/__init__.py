"""
Capa de presentación: vistas (páginas).

Rutas registradas:
- "/"                        → vista_inicio
- "/carreras"                → vista_carreras
- "/carrera/[carrera_id]"    → vista_detalle_carrera
- "/contacto"                → vista_contacto
- "/sobre-nosotros"          → vista_sobre_nosotros
- "/faq"                     → vista_faq
- "/calendario"              → vista_calendario
- "/admision"                → vista_admision
- "/becas"                   → vista_becas
- "/blog"                    → vista_blog
- "/blog/[post_id]"          → vista_post
- "/404"                     → vista_404
"""

from .blog import vista_blog, vista_post
from .calendario import vista_calendario
from .vista_404 import vista_404
from .vista_admision import vista_admision
from .vista_becas import vista_becas
from .vista_carreras import vista_carreras
from .vista_contacto import vista_contacto
from .vista_detalle_carrera import vista_detalle_carrera
from .vista_faq import vista_faq
from .vista_inicio import vista_inicio
from .vista_sobre_nosotros import vista_sobre_nosotros


__all__ = [
    "vista_404",
    "vista_admision",
    "vista_becas",
    "vista_blog",
    "vista_calendario",
    "vista_carreras",
    "vista_contacto",
    "vista_detalle_carrera",
    "vista_faq",
    "vista_inicio",
    "vista_post",
    "vista_sobre_nosotros",
]