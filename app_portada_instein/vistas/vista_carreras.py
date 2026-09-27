"""
Vista con la lista completa de carreras (ruta "/carreras").

Estilo Google Play Store:
- Banner destacado con 3 carreras.
- Listas de éxitos con ranking numerado.
- Filtros tipo pill arriba.
"""

import reflex as rx

from app_portada_instein.componentes.barra_navegacion import barra_navegacion_superior
from app_portada_instein.componentes.hero_carreras import hero_carreras
from app_portada_instein.componentes.pie_pagina import pie_pagina_institucional
from app_portada_instein.componentes.tarjetas_carrera import item_carrera_con_ranking
from app_portada_instein.dominio.estado_institucional import EstadoInstitucional
from app_portada_instein.infraestructura.constantes_visuales import NOMBRE_INSTITUTO


# ======================================================================
# Filtros tipo pill (estilo Google Play)
# ======================================================================


def _filtro_pill(etiqueta: str, activo: bool = False) -> rx.Component:
    """Botón pill de filtro, estilo Google Play Store."""
    return rx.box(
        rx.text(
            etiqueta,
            font_size="0.8125rem",
            font_weight="600",
            color=rx.cond(
                activo,
                "#0f172a",
                rx.color_mode_cond(light="#334155", dark="#cbd5e1"),
            ),
        ),
        padding="0.5rem 1rem",
        border_radius="9999px",
        background=rx.cond(
            activo,
            "#a7f3d0",
            rx.color_mode_cond(light="#f1f5f9", dark="#1e293b"),
        ),
        border="1px solid " + rx.color_mode_cond(light="#e2e8f0", dark="#334155"),
        cursor="pointer",
        transition="all 0.2s",
        _hover={
            "background": rx.cond(
                activo,
                "#6ee7b7",
                rx.color_mode_cond(light="#e2e8f0", dark="#334155"),
            ),
        },
    )


def _barra_filtros() -> rx.Component:
    """Barra con los filtros tipo pill."""
    return rx.flex(
        _filtro_pill("Más exitosas (gratuitas)", activo=True),
        _filtro_pill("De mayor recaudación"),
        _filtro_pill("Top ventas"),
        gap="0.5rem",
        flex_wrap="wrap",
        width="100%",
        margin_bottom="1.5rem",
    )


# ======================================================================
# Grid de listas de éxitos (3 columnas)
# ======================================================================


def _grid_listas_exitos() -> rx.Component:
    """
    Grid con 3 columnas, cada una con items de ranking.

    La primera columna muestra las carreras 1, 2, 3.
    La segunda las carreras 4, 5, 6.
    La tercera las carreras 7, 8, 9.

    En este caso tenemos 5 carreras, así que se distribuyen:
    - Columna 1: 1, 2
    - Columna 2: 3, 4
    - Columna 3: 5
    """
    return rx.grid(
        # Columna 1: carreras 0, 1
        rx.vstack(
            rx.foreach(
                EstadoInstitucional.carreras,
                lambda carrera, idx: rx.cond(
                    idx < 2,
                    item_carrera_con_ranking(carrera, idx),
                    rx.fragment(),
                ),
            ),
            spacing="2",
            width="100%",
        ),
        # Columna 2: carreras 2, 3
        rx.vstack(
            rx.foreach(
                EstadoInstitucional.carreras,
                lambda carrera, idx: rx.cond(
                    (idx >= 2) & (idx < 4),
                    item_carrera_con_ranking(carrera, idx),
                    rx.fragment(),
                ),
            ),
            spacing="2",
            width="100%",
        ),
        # Columna 3: carreras 4+
        rx.vstack(
            rx.foreach(
                EstadoInstitucional.carreras,
                lambda carrera, idx: rx.cond(
                    idx >= 4,
                    item_carrera_con_ranking(carrera, idx),
                    rx.fragment(),
                ),
            ),
            spacing="2",
            width="100%",
        ),
        columns=rx.breakpoints(
            initial="1",
            sm="1",
            md="2",
            lg="3",
        ),
        spacing="6",
        width="100%",
    )


# ======================================================================
# Vista completa
# ======================================================================


@rx.page(
    route="/carreras",
    title=f"Carreras | {NOMBRE_INSTITUTO}",
    on_load=EstadoInstitucional.auto_avanzar_carrusel,
)
def vista_carreras() -> rx.Component:
    """
    Página con la oferta académica completa estilo Google Play Store.

    Estructura:
    1. Barra de navegación.
    2. Hero con 3 banners destacados.
    3. Sección "Listas de éxitos" con filtros + grid.
    4. Pie de página.
    """
    return rx.vstack(
        # --- Barra de navegación ---
        barra_navegacion_superior(),
        # --- Contenido principal ---
        rx.box(
            # Hero con banners destacados
            hero_carreras(),
            # Sección "Listas de éxitos"
            rx.box(
                # --- Encabezado de sección ---
                rx.heading(
                    "Listas de éxitos",
                    size="6",
                    font_weight="700",
                    color=rx.color_mode_cond(light="#0f172a", dark="#f1f5f9"),
                    margin_bottom="1.5rem",
                ),
                # --- Filtros ---
                _barra_filtros(),
                # --- Grid de listas ---
                _grid_listas_exitos(),
                max_width="72rem",
                margin="0 auto",
                padding="2rem 1.5rem 4rem 1.5rem",
                width="100%",
            ),
            width="100%",
        ),
        # --- Pie de página ---
        pie_pagina_institucional(),
        align="center",
        min_height="100vh",
        width="100%",
    )
