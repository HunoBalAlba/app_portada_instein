"""
Buscador de carreras + card de imagen + grid de imágenes + estado vacío.

Estructura:
- `_buscador_carreras`: input con iconos decorativos.
- `_card_imagen_carrera`: card con imagen destacada (patrón rx.card + rx.inset).
- `_grid_imagenes_carreras`: grid + contador + estado vacío condicional.
- `_estado_vacio_busqueda`: mensaje cuando la búsqueda no devuelve resultados.

Sistema de color (UX)
---------------------
- Card de carrera: usa el color de marca de cada carrera para borde,
  gradiente y hover.
- Textos: neutros (`gray-11`/`gray-12`) para máxima legibilidad.
- Estado vacío: botón "Restablecer búsqueda" con accent institucional.
"""

import reflex as rx

from app_portada_instein.componentes.primitivos import enlace_navegacion
from app_portada_instein.dominio.estado_institucional import EstadoInstitucional
from app_portada_instein.infraestructura.constantes_visuales import (
    ANCHO_CONTENIDO,
    COLOR_BORDE_SUAVE,
    COLOR_FONDO_CARTA,
    COLOR_FONDO_SUAVE,
    COLOR_TEXTO_PRINCIPAL,
    COLOR_TEXTO_SECUNDARIO,
    RADIO_EXTRA_GRANDE,
    RADIO_GRANDE,
    RADIO_MEDIO,
    RADIO_PASTILLA,
)

from .constantes import (
    ANCHO_MAXIMO_BUSCADOR,
    PADDING_INFERIOR_GRID,
    TAMANO_ICONO_ESTADO_VACIO,
)
from .helpers import color_carrera


# ======================================================================
# Constantes locales
# ======================================================================

# Altura del banner (imagen) de la card de carrera.
ALTURA_BANNER_CARD = "7rem"


# ======================================================================
# BUSCADOR
# ======================================================================


def _buscador_carreras() -> rx.Component:
    """
    Buscador central estilo Leonardo AI.

    UX:
    - Icono de búsqueda a la izquierda.
    - Input con placeholder.
    - Icono de "sparkles" a la derecha (decorativo).
    - El estado vacío se muestra en `_grid_imagenes_carreras` cuando
      no hay resultados.
    """
    return rx.box(
        rx.flex(
            rx.box(
                rx.icon("search", size=20, color=COLOR_TEXTO_SECUNDARIO),
                padding="0.5rem",
                display="flex",
                align_items="center",
                justify_content="center",
            ),
            rx.input(
                placeholder=(
                    "Busca una carrera: Sistemas, Contaduría, Electrónica..."
                ),
                value=EstadoInstitucional.texto_busqueda_carrera,
                on_change=EstadoInstitucional.actualizar_busqueda_carrera,
                variant="soft",
                size="3",
                width="100%",
                border="none",
                background="transparent",
                _focus={"box_shadow": "none", "outline": "none"},
            ),
            rx.box(
                rx.icon("sparkles", size=18, color=COLOR_TEXTO_SECUNDARIO),
                padding="0.5rem",
                display="flex",
                align_items="center",
                justify_content="center",
            ),
            align="center",
            width="100%",
            gap="0.5rem",
        ),
        width="100%",
        max_width=ANCHO_MAXIMO_BUSCADOR,
        margin="0 auto 1.5rem auto",
        padding="0.75rem 1rem",
        border_radius=RADIO_GRANDE,
        background=COLOR_FONDO_CARTA,
        border=f"1px solid {COLOR_BORDE_SUAVE}",
        backdrop_filter="blur(12px)",
        box_shadow="0 10px 30px -10px rgba(0,0,0,0.15)",
        transition="all 0.2s",
    )


# ======================================================================
# ESTADO VACÍO (sin resultados)
# ======================================================================


def _estado_vacio_busqueda() -> rx.Component:
    """
    Estado vacío cuando la búsqueda no devuelve resultados.

    UX:
    - Icono grande de "search-x" en gris.
    - Título destacado.
    - Texto explicativo con el término buscado.
    - Botón "Restablecer búsqueda" con accent institucional.

    El botón dispara `actualizar_busqueda_carrera("")` para limpiar
    el input y volver a mostrar todas las carreras.
    """
    return rx.vstack(
        # ==========================================================
        # Icono en caja tintada
        # ==========================================================
        rx.box(
            rx.icon(
                "search-x",
                size=TAMANO_ICONO_ESTADO_VACIO,
                color=COLOR_TEXTO_SECUNDARIO,
            ),
            padding="1.5rem",
            border_radius=RADIO_EXTRA_GRANDE,
            background=COLOR_FONDO_SUAVE,
            border=f"1px solid {COLOR_BORDE_SUAVE}",
            display="flex",
            align_items="center",
            justify_content="center",
        ),
        # ==========================================================
        # Título + descripción
        # ==========================================================
        rx.vstack(
            rx.heading(
                "No se encontraron carreras",
                size="5",
                font_weight="700",
                color=COLOR_TEXTO_PRINCIPAL,
                text_align="center",
            ),
            rx.text(
                "No hay resultados para ",
                rx.text.span(
                    f'"{EstadoInstitucional.texto_busqueda_carrera}"',
                    font_weight="700",
                    color=COLOR_TEXTO_PRINCIPAL,
                ),
                ". Intenta con otro término o explora todas las carreras "
                "disponibles.",
                font_size="0.875rem",
                color=COLOR_TEXTO_SECUNDARIO,
                text_align="center",
                max_width="32rem",
                line_height="1.6",
            ),
            spacing="2",
            align="center",
        ),
        # ==========================================================
        # Botón "Restablecer búsqueda"
        # ==========================================================
        rx.button(
            rx.icon("rotate-ccw", size=16),
            rx.text("Restablecer búsqueda", as_="span", font_weight="700"),
            on_click=lambda: EstadoInstitucional.actualizar_busqueda_carrera(""),
            size="3",
            variant="solid",
            color_scheme="crimson",
            cursor="pointer",
            margin_top="0.5rem",
        ),
        direction="column",
        align="center",
        justify="center",
        gap="1.5rem",
        padding="4rem 1.5rem",
        width="100%",
    )


# ======================================================================
# CARD DE IMAGEN DE CARRERA (patrón rx.card + rx.inset)
# ======================================================================


def _card_imagen_carrera(carrera: dict) -> rx.Component:
    """
    Card con la imagen de la carrera destacada arriba.

    Al hacer clic, navega al detalle (`/carrera/{id}`).

    Patrón aplicado (`rx.card` + `rx.inset`):
    - Inset top: imagen horizontal (banner) edge-to-edge.
    - Contenido: nombre corto + duración + indicador de navegación.

    UX:
    - Gradiente tintado con el color de la carrera sobre la imagen.
    - Icono de la carrera con fondo suave del color de la carrera.
    - Hover: borde + sombra del color de la carrera + elevación.
    - Click: navega al detalle.
    """
    color = color_carrera(carrera)

    return enlace_navegacion(
        f"/carrera/{carrera['id']}",
        rx.card(
            # ==========================================================
            # Inset top: imagen de la carrera (edge-to-edge)
            # ==========================================================
            rx.inset(
                rx.box(
                    rx.image(
                        src="/" + carrera["imagen_archivo"],
                        alt=carrera["nombre"],
                        width="100%",
                        height="100%",
                        object_fit="cover",
                    ),
                    # Overlay con gradiente del color de la carrera
                    rx.box(
                        position="absolute",
                        top="0",
                        left="0",
                        right="0",
                        bottom="0",
                        background=rx.color_mode_cond(
                            light=(
                                f"linear-gradient(180deg, "
                                f"transparent 40%, "
                                f"{carrera['color_principal']}44 100%)"
                            ),
                            dark=(
                                f"linear-gradient(180deg, "
                                f"transparent 40%, "
                                f"{carrera['color_principal_dark']}55 100%)"
                            ),
                        ),
                        pointer_events="none",
                    ),
                    position="relative",
                    width="100%",
                    height=ALTURA_BANNER_CARD,
                    overflow="hidden",
                    border_radius=RADIO_MEDIO,
                ),
                side="top",
                pb="current",
            ),
            # ==========================================================
            # Contenido: icono + nombre + duración
            # ==========================================================
            rx.flex(
                # Icono de la carrera con fondo suave del color
                rx.flex(
                    rx.icon(
                        carrera["icono"],
                        size=14,
                        color=color,
                    ),
                    height="1.75rem",
                    width="1.75rem",
                    border_radius=RADIO_MEDIO,
                    background=rx.color_mode_cond(
                        light=f"{carrera['color_principal']}15",
                        dark=f"{carrera['color_principal_dark']}20",
                    ),
                    border=f"1px solid {color}",
                    align="center",
                    justify="center",
                    flex_shrink="0",
                ),
                # Nombre + duración
                rx.vstack(
                    rx.text(
                        carrera["nombre_corto"],
                        font_size="0.875rem",
                        font_weight="700",
                        color=COLOR_TEXTO_PRINCIPAL,
                        line_height="1.2",
                    ),
                    rx.text(
                        carrera["duracion"],
                        font_size="0.6875rem",
                        color=COLOR_TEXTO_SECUNDARIO,
                        line_height="1.2",
                    ),
                    spacing="0",
                    align="start",
                    flex="1",
                    min_width="0",
                ),
                # Indicador de navegación
                rx.icon(
                    "arrow-up-right",
                    size=14,
                    color=COLOR_TEXTO_SECUNDARIO,
                    flex_shrink="0",
                ),
                align="center",
                gap="0.5rem",
                width="100%",
            ),
            # ==========================================================
            # Estilos de la card
            # ==========================================================
            padding="0.5rem",
            width="100%",
            cursor="pointer",
            transition="all 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
            _hover={
                "transform": "translateY(-4px)",
                "border_color": color,
                "box_shadow": f"0 20px 40px -12px {color}",
            },
        ),
        text_decoration="none",
        width="100%",
    )


# ======================================================================
# GRID DE IMÁGENES DE CARRERAS
# ======================================================================


def _grid_imagenes_carreras() -> rx.Component:
    """
    Grid con las imágenes de todas las carreras.

    UX:
    - Muestra el contador de resultados.
    - Si hay resultados, muestra el grid.
    - Si NO hay resultados, muestra `_estado_vacio_busqueda()`.
    """
    return rx.box(
        # ==========================================================
        # Contador de carreras
        # ==========================================================
        rx.flex(
            rx.text(
                "Carreras disponibles",
                font_size="0.75rem",
                font_weight="700",
                letter_spacing="0.1em",
                text_transform="uppercase",
                color=COLOR_TEXTO_SECUNDARIO,
            ),
            rx.text(
                EstadoInstitucional.carreras_filtradas.length().to_string(),
                font_size="0.75rem",
                font_weight="700",
                color=COLOR_TEXTO_PRINCIPAL,
                padding="0.125rem 0.5rem",
                background=COLOR_FONDO_SUAVE,
                border_radius=RADIO_PASTILLA,
            ),
            align="center",
            gap="0.5rem",
            margin_bottom="1rem",
        ),
        # ==========================================================
        # Condicional: grid o estado vacío
        # ==========================================================
        rx.cond(
            EstadoInstitucional.carreras_filtradas.length() > 0,
            rx.grid(
                rx.foreach(
                    EstadoInstitucional.carreras_filtradas,
                    _card_imagen_carrera,
                ),
                columns=rx.breakpoints(initial="2", sm="2", md="3", lg="5"),
                spacing="3",
                width="100%",
            ),
            _estado_vacio_busqueda(),
        ),
        width="100%",
        max_width=ANCHO_CONTENIDO,
        margin=PADDING_INFERIOR_GRID,
    )


__all__ = [
    "_buscador_carreras",
    "_card_imagen_carrera",
    "_estado_vacio_busqueda",
    "_grid_imagenes_carreras",
]