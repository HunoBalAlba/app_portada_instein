"""
Ensamblador del explorador completo de carrera destacada.

Importa los submódulos y los apila en el orden correcto:
1. Panel flotante (oculto por defecto).
2. Buscador.
3. Grid de imágenes de carreras.

Todos los imports son RELATIVOS al paquete `explorador` para evitar
imports circulares.
"""

import reflex as rx

from app_portada_instein.infraestructura.constantes_visuales import (
    ANCHO_CONTENIDO,
)

# ✅ Imports relativos (NO absolutos desde el propio paquete)
from .buscador import _buscador_carreras, _grid_imagenes_carreras
from .constantes import PADDING_EXPLORADOR
from .panel_flotante import _panel_flotante_selector


def explorador_carrera_destacada() -> rx.Component:
    """
    Explorador completo estilo Leonardo AI con navegación al detalle.

    Estructura:
    - Panel flotante de acceso rápido (oculto por defecto).
    - Buscador de carreras.
    - Grid de imágenes que navegan a `/carrera/{id}`.
    - Estado vacío cuando no hay resultados.
    """
    return rx.box(
        # ==========================================================
        # Panel flotante (botón + overlay + panel desplegable)
        # ==========================================================
        _panel_flotante_selector(),
        # ==========================================================
        # Contenido principal
        # ==========================================================
        rx.vstack(
            _buscador_carreras(),
            _grid_imagenes_carreras(),
            width="100%",
            align="center",
            spacing="4",
            padding=PADDING_EXPLORADOR,
            max_width=ANCHO_CONTENIDO,
            margin="0 auto",
        ),
        width="100%",
        position="relative",
    )


__all__ = ["explorador_carrera_destacada"]