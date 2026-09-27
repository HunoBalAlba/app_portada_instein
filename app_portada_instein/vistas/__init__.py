"""
Capa de presentación: vistas (páginas).

Cada vista está decorada con @rx.page y se registra automáticamente
en la aplicación al importar este paquete.

Rutas registradas:
- "/"                        → vista_inicio
- "/carreras"                → vista_carreras
- "/carrera/[carrera_id]"    → vista_detalle_carrera
- "/contacto"                → vista_contacto
"""

from .vista_carreras import vista_carreras
from .vista_contacto import vista_contacto
from .vista_detalle_carrera import vista_detalle_carrera
from .vista_inicio import vista_inicio


__all__ = [
    "vista_carreras",
    "vista_contacto",
    "vista_detalle_carrera",
    "vista_inicio",
]
