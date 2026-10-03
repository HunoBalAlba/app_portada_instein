# app_portada_instein/componentes/explorador/buscador.py

"""
Buscador de carreras + card de imagen + grid + estado vacío.
Estilo Neon adaptativo (dark/light).

Estructura:
- `_buscador_carreras`: input con iconos decorativos.
- `_card_imagen_carrera`: card con imagen destacada.
- `_grid_imagenes_carreras`: grid + contador + estado vacío.
- `_estado_vacio_busqueda`: estado vacío cuando no hay resultados
  (delegado al componente unificado).

Sistema de color (UX)
---------------------
✅ ADAPTATIVO: todos los colores respetan el color_mode del usuario.

- Fondo del buscador: `FONDO_HOME_CARD_ADAPTATIVO`.
- Acentos: azul marino neon (`AZUL_MARINO_NEON` = `#3b5bdb`) en AMBOS modos.
- Texto: `TEXTO_HOME_PRINCIPAL` / `TEXTO_HOME_SUAVE` / `TEXTO_HOME_MAS_SUAVE`.
- Bordes: `BORDE_HOME_AZUL` / `BORDE_HOME_MEDIO` / `BORDE_HOME_SUAVE`.
- Fondo tintado del icono: `FONDO_AZUL_SUAVE`.

Nota técnica: ESTADO VACÍO UNIFICADO
------------------------------------
✅ REFACTORIZADO: el estado vacío ya NO tiene su propia implementación
local. Ahora delega en el componente genérico
`componentes/estado_vacio.py`, que centraliza el estilo y permite
personalizar icono, título, mensaje y botones.

⚠️ IMPORTANTE: como queremos mostrar el término buscado con estilo
(azul marino neon + negrita), pasamos el `mensaje` como un
`rx.Component` (no un `str`). El componente unificado acepta ambos.
"""

from __future__ import annotations

import reflex as rx

from app_portada_instein.componentes.estado_vacio import (
    estado_vacio as _estado_vacio_unificado,
)
from app_portada_instein.componentes.primitivos import enlace_navegacion
from app_portada_instein.dominio.estado_institucional import (
    EstadoInstitucional,
)
from app_portada_instein.infraestructura.constantes_visuales import (
    ANCHO_CONTENIDO,
    AZUL_MARINO_NEON,
    BORDE_HOME_AZUL,
    BORDE_HOME_MEDIO,
    BORDE_HOME_SUAVE,
    FONDO_AZUL_SUAVE,
    FONDO_HOME_CARD_ADAPTATIVO,
    RADIO_EXTRA_GRANDE,
    RADIO_GRANDE,
    RADIO_MEDIO,
    RADIO_PASTILLA,
    SOMBRA_HOVER_CARD_HOME,
    TEXTO_HOME_MAS_SUAVE,
    TEXTO_HOME_PRINCIPAL,
    TEXTO_HOME_SUAVE,
)

from .constantes import (
    ANCHO_MAXIMO_BUSCADOR,
    PADDING_INFERIOR_GRID,
    TAMANO_ICONO_ESTADO_VACIO,
)


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
    Buscador central estilo Neon adaptativo.

    UX:
    - Icono de búsqueda a la izquierda (azul marino neon).
    - Input con placeholder adaptativo.
    - Icono de "sparkles" a la derecha (decorativo, azul marino neon).
    - Fondo adaptativo con glassmorphism.
    - Hover: borde azul marino.

    ✅ ADAPTATIVO: fondo, texto, borde y sombra cambian según el modo.

    El estado vacío se muestra en `_grid_imagenes_carreras` cuando
    no hay resultados.
    """
    return rx.box(
        rx.flex(
            rx.box(
                rx.icon("search", size=20, color=AZUL_MARINO_NEON),
                padding="0.5rem",
                display="flex",
                align_items="center",
                justify_content="center",
            ),
            rx.input(
                placeholder=(
                    "Busca una carrera: Sistemas, Contaduría, "
                    "Electrónica..."
                ),
                value=EstadoInstitucional.texto_busqueda_carrera,
                on_change=EstadoInstitucional.actualizar_busqueda_carrera,
                variant="soft",
                size="3",
                width="100%",
                border="none",
                background="transparent",
                color=TEXTO_HOME_PRINCIPAL,
                _placeholder={"color": TEXTO_HOME_MAS_SUAVE},
                _focus={"box_shadow": "none", "outline": "none"},
            ),
            rx.box(
                rx.icon("sparkles", size=18, color=AZUL_MARINO_NEON),
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
        background=FONDO_HOME_CARD_ADAPTATIVO,
        border=f"1px solid {BORDE_HOME_SUAVE}",
        backdrop_filter="blur(12px)",
        box_shadow=rx.color_mode_cond(
            light=f"0 10px 30px -10px {AZUL_MARINO_NEON}20",
            dark=f"0 10px 30px -10px {AZUL_MARINO_NEON}40",
        ),
        transition="all 0.2s",
        _hover={
            "border_color": BORDE_HOME_AZUL,
        },
    )


# ======================================================================
# ESTADO VACÍO (delegado al componente unificado)
# ======================================================================


def _estado_vacio_busqueda() -> rx.Component:
    """
    Estado vacío cuando la búsqueda no devuelve resultados.

    ✅ REFACTORIZADO: delega en `componentes/estado_vacio.py`.

    UX:
    - Icono grande de "search-x" en azul marino con glow.
    - Título: "No se encontraron carreras".
    - Mensaje enriquecido con el término buscado entre comillas
      (azul marino neon + negrita).
    - Botón "Restablecer búsqueda" con azul marino neon + glow.

    El botón dispara `actualizar_busqueda_carrera("")` para limpiar
    el input y volver a mostrar todas las carreras.
    """
    # Mensaje enriquecido con el término buscado
    mensaje_enriquecido = rx.text(
        "No hay resultados para ",
        rx.text.span(
            f'"{EstadoInstitucional.texto_busqueda_carrera}"',
            font_weight="700",
            color=AZUL_MARINO_NEON,
        ),
        ". Intenta con otro término o explora todas las carreras "
        "disponibles.",
        font_size="0.875rem",
        color=TEXTO_HOME_MAS_SUAVE,
        text_align="center",
        max_width="32rem",
        line_height="1.6",
    )

    return _estado_vacio_unificado(
        titulo="No se encontraron carreras",
        mensaje=mensaje_enriquecido,
        icono="search-x",
        variante="neon",
        tamano_icono=TAMANO_ICONO_ESTADO_VACIO,
        icono_acento=True,
        boton_accion_etiqueta="Restablecer búsqueda",
        boton_accion_icono="rotate-ccw",
        boton_accion_on_click=(
            EstadoInstitucional.actualizar_busqueda_carrera("")
        ),
        boton_accion_color_scheme="blue",
    )


# ======================================================================
# CARD DE IMAGEN DE CARRERA
# ======================================================================


def _card_imagen_carrera(carrera: dict) -> rx.Component:
    """
    Card con la imagen de la carrera destacada arriba.

    Al hacer clic, navega al detalle (`/carrera/{id}`).

    Patrón aplicado (`rx.card` + `rx.inset`):
    - Inset top: imagen horizontal (banner) edge-to-edge.
    - Contenido: nombre corto + duración + indicador de navegación.

    ✅ ADAPTATIVO: fondo, textos y borde cambian según el modo.

    Estilo Neon:
    - Fondo con glassmorphism adaptativo.
    - Icono azul marino con fondo tintado.
    - Hover: borde azul + glow azul + elevación.
    """
    return enlace_navegacion(
        f"/carrera/{carrera['id']}",
        rx.card(
            # ==========================================================
            # Inset top: imagen de la carrera
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
                    # Overlay con gradiente azul marino
                    rx.box(
                        position="absolute",
                        top="0",
                        left="0",
                        right="0",
                        bottom="0",
                        background=(
                            f"linear-gradient(180deg, "
                            f"transparent 40%, "
                            f"rgba(59, 91, 219, 0.4) 100%)"
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
                # Icono de la carrera con fondo tintado azul
                rx.flex(
                    rx.icon(
                        carrera["icono"],
                        size=14,
                        color=AZUL_MARINO_NEON,
                    ),
                    height="1.75rem",
                    width="1.75rem",
                    border_radius=RADIO_MEDIO,
                    background=FONDO_AZUL_SUAVE,
                    border=f"1px solid {BORDE_HOME_AZUL}",
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
                        color=TEXTO_HOME_PRINCIPAL,
                        line_height="1.2",
                    ),
                    rx.text(
                        carrera["duracion"],
                        font_size="0.6875rem",
                        color=TEXTO_HOME_MAS_SUAVE,
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
                    color=TEXTO_HOME_MAS_SUAVE,
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
            background=FONDO_HOME_CARD_ADAPTATIVO,
            backdrop_filter="blur(12px)",
            border=f"1px solid {BORDE_HOME_SUAVE}",
            transition="all 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
            _hover={
                "transform": "translateY(-4px)",
                "border_color": BORDE_HOME_AZUL,
                "box_shadow": SOMBRA_HOVER_CARD_HOME,
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

    ✅ ADAPTATIVO: contador, texto y borde cambian según el modo.
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
                color=TEXTO_HOME_MAS_SUAVE,
            ),
            rx.text(
                EstadoInstitucional.carreras_filtradas
                .length()
                .to_string(),
                font_size="0.75rem",
                font_weight="700",
                color=TEXTO_HOME_PRINCIPAL,
                padding="0.125rem 0.5rem",
                background=FONDO_AZUL_SUAVE,
                border=f"1px solid {BORDE_HOME_AZUL}",
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
                columns=rx.breakpoints(
                    initial="2",
                    sm="2",
                    md="3",
                    lg="5",
                ),
                spacing="3",
                width="100%",
            ),
            _estado_vacio_busqueda(),
        ),
        width="100%",
        max_width=ANCHO_CONTENIDO,
        margin=PADDING_INFERIOR_GRID,
    )


# ======================================================================
# EXPORTS
# ======================================================================

__all__ = [
    "_buscador_carreras",
    "_card_imagen_carrera",
    "_estado_vacio_busqueda",
    "_grid_imagenes_carreras",
]