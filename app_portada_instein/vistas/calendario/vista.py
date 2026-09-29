"""
Vista completa del Calendario Académico (ruta "/calendario").
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

from .cta import cta_calendario
from .hero import grid_info_rapida, hero_calendario
from .tabs import tabs_calendario


# ======================================================================
# Constantes locales
# ======================================================================

PADDING_LATERAL = "1.5rem"


# ======================================================================
# Vista
# ======================================================================


@rx.page(
    route="/calendario",
    title=f"Calendario académico | {NOMBRE_INSTITUTO}",
)
def vista_calendario() -> rx.Component:
    """Página del calendario académico del instituto."""
    return rx.vstack(
        barra_navegacion_superior(),
        hero_calendario(),
        grid_info_rapida(),
        # --- Tabs: Actividades + Fechas importantes ---
        rx.box(
            tabs_calendario(),
            max_width="64rem",
            margin="0 auto",
            padding=f"2rem {PADDING_LATERAL} 4rem {PADDING_LATERAL}",
            width="100%",
        ),
        cta_calendario(),
        pie_pagina_institucional(),
        align="center",
        min_height="100vh",
        width="100%",
        spacing="0",
    )


__all__ = ["vista_calendario"]