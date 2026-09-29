"""
Componentes visuales relacionados con la presentación de carreras
y su plan de estudios.

Estilo inspirado en Google Play Store:
- Item horizontal con ranking a la izquierda.
- Icono circular + nombre + categoría + rating.
- Hover con fondo sutil.

Sistema de color (UX)
---------------------
Los elementos interactivos que representan la carrera (pastilla de año
activa, número de materia, hover de fila) usan el COLOR DE MARCA de
la carrera. Los textos largos son NEUTROS (`gray-11`) para mantener
legibilidad.

Elementos con color de carrera:
- Pastilla de año activa (fondo y borde).
- Número de materia (fondo sólido).
- Borde hover de fila de materia.

Elementos con accent (institucional):
- No se usa accent en este módulo.

Elementos con color neutro:
- Textos de nombre, descripción, duración.
- Rating (texto).
- Iconos decorativos.
- Bordes base.
"""

import reflex as rx

from app_portada_instein.componentes.primitivos import (
    contenedor_clicable,
    enlace_navegacion,
)
from app_portada_instein.datos.modelos_carrera import Carrera, PlanAnual
from app_portada_instein.dominio.estado_institucional import EstadoInstitucional
from app_portada_instein.infraestructura.constantes_visuales import (
    COLOR_BORDE_SUAVE,
    COLOR_FONDO_CARTA,
    COLOR_FONDO_SUAVE,
    COLOR_TEXTO_CUERPO,
    COLOR_TEXTO_PRINCIPAL,
    COLOR_TEXTO_SECUNDARIO,
    RADIO_MEDIO,
    RADIO_PASTILLA,
    # Helpers de color adaptativo
    color_carrera_adaptativo,
    color_suave_carrera_adaptativo,
)


# ======================================================================
# Constantes locales
# ======================================================================

# Color de la estrella de puntuación (amarillo).
COLOR_ESTRELLA = rx.color("amber", 9)

# Tamaño del icono circular de la carrera.
TAMANO_ICONO_CARRERA = "4rem"


# ======================================================================
# Helpers de color de carrera
# ======================================================================


def _color_carrera_actual() -> rx.Var:
    """Color principal de la carrera seleccionada, adaptado al modo."""
    return color_carrera_adaptativo(EstadoInstitucional.carrera_seleccionada)


def _color_suave_carrera_actual() -> rx.Var:
    """Color suave de la carrera seleccionada, adaptado al modo."""
    return color_suave_carrera_adaptativo(EstadoInstitucional.carrera_seleccionada)


# ======================================================================
# Helpers internos
# ======================================================================


def _icono_carrera_circular(carrera: Carrera) -> rx.Component:
    """Icono circular de la carrera (imagen redondeada)."""
    return rx.box(
        rx.image(
            src="/" + carrera["imagen_archivo"],
            alt=carrera["nombre"],
            width="100%",
            height="100%",
            object_fit="cover",
            border_radius=RADIO_MEDIO,
        ),
        width=TAMANO_ICONO_CARRERA,
        height=TAMANO_ICONO_CARRERA,
        flex_shrink="0",
        border_radius=RADIO_MEDIO,
        overflow="hidden",
    )


def _rating_compacto(puntuacion: str = "4.8") -> rx.Component:
    """
    Fila compacta con puntuación + estrella.

    Args:
        puntuacion: Valor de puntuación a mostrar (ej: "4.8").
    """
    return rx.flex(
        rx.text(
            puntuacion,
            font_size="0.75rem",
            font_weight="600",
            color=COLOR_TEXTO_PRINCIPAL,
        ),
        rx.icon(
            "star",
            size=10,
            color=COLOR_ESTRELLA,
            fill=COLOR_ESTRELLA,
        ),
        align="center",
        gap="0.25rem",
        margin_top="0.125rem",
    )


def _info_carrera_compacta(
    carrera: Carrera,
    descripcion_corta: str | None = None,
) -> rx.Component:
    """
    Bloque de información textual de la carrera.

    Args:
        carrera: Datos de la carrera.
        descripcion_corta: Si se pasa, se usa como segunda línea
            (ej: lema truncado). Si no, se usa "duracion · Técnico Superior".
    """
    texto_secundario = (
        descripcion_corta
        if descripcion_corta is not None
        else carrera["duracion"] + " · Técnico Superior"
    )

    return rx.vstack(
        rx.text(
            carrera["nombre_corto"],
            font_size="0.9375rem",
            font_weight="600",
            color=COLOR_TEXTO_PRINCIPAL,
            line_height="1.3",
        ),
        rx.text(
            texto_secundario,
            font_size="0.75rem",
            color=COLOR_TEXTO_SECUNDARIO,
            line_height="1.3",
        ),
        _rating_compacto(),
        align="start",
        spacing="1",
        flex="1",
        min_width="0",
    )


# ======================================================================
# Item de carrera con ranking (estilo Google Play)
# ======================================================================


def tarjeta_carrera(carrera: Carrera) -> rx.Component:
    """
    Item de carrera estilo Google Play Store.

    Estructura horizontal:
    - Icono circular de la carrera.
    - Nombre + duración + rating.
    """
    return enlace_navegacion(
        f"/carrera/{carrera['id']}",
        rx.flex(
            _icono_carrera_circular(carrera),
            _info_carrera_compacta(carrera),
            align="center",
            gap="1rem",
            width="100%",
        ),
        padding="0.75rem",
        border_radius=RADIO_MEDIO,
        background="transparent",
        width="100%",
        text_align="left",
        transition="all 0.15s ease-out",
        cursor="pointer",
        _hover={"background": COLOR_FONDO_SUAVE},
    )


# ======================================================================
# Item de carrera con ranking explícito (número a la izquierda)
# ======================================================================


def item_carrera_con_ranking(carrera: Carrera, indice: int) -> rx.Component:
    """
    Item de carrera con número de ranking a la izquierda.
    Estilo "Listas de éxitos" de Google Play.
    """
    return enlace_navegacion(
        f"/carrera/{carrera['id']}",
        rx.flex(
            # --- Número de ranking ---
            rx.box(
                rx.text(
                    (indice + 1).to_string(),
                    font_size="1rem",
                    font_weight="600",
                    color=COLOR_TEXTO_SECUNDARIO,
                ),
                width="1.5rem",
                text_align="center",
                flex_shrink="0",
            ),
            _icono_carrera_circular(carrera),
            _info_carrera_compacta(
                carrera,
                descripcion_corta=carrera["lema"][:40] + "...",
            ),
            align="center",
            gap="1rem",
            width="100%",
        ),
        padding="0.75rem",
        border_radius=RADIO_MEDIO,
        background="transparent",
        width="100%",
        text_align="left",
        transition="all 0.15s ease-out",
        cursor="pointer",
        _hover={"background": COLOR_FONDO_SUAVE},
    )


# ======================================================================
# Pastilla de año del plan de estudios
# ======================================================================


def pastilla_anio(plan_anual: PlanAnual, indice: int) -> rx.Component:
    """
    Pastilla seleccionable que representa un año del plan de estudios.

    Usa el COLOR DE LA CARRERA cuando está activa para reforzar la
    identidad visual.
    """
    esta_activo = EstadoInstitucional.indice_anio_seleccionado == indice
    color_carrera = _color_carrera_actual()
    color_suave_carrera = _color_suave_carrera_actual()

    return contenedor_clicable(
        rx.text(plan_anual["anio"], size="2"),
        al_hacer_clic=lambda: EstadoInstitucional.seleccionar_anio(indice),
        padding="0.625rem 1.125rem",
        border_radius=RADIO_MEDIO,
        background=rx.cond(
            esta_activo,
            color_carrera,          # ← color de carrera cuando activa
            color_suave_carrera,    # ← color suave de carrera cuando inactiva
        ),
        color=rx.cond(
            esta_activo,
            "white",                # ← blanco sobre fondo sólido de carrera
            COLOR_TEXTO_CUERPO,
        ),
        border=rx.cond(
            esta_activo,
            f"1px solid {color_carrera}",
            f"1px solid {color_carrera}",
        ),
        box_shadow=rx.cond(
            esta_activo,
            f"0 4px 12px -2px {color_carrera}",
            "none",
        ),
        font_weight="600",
        white_space="nowrap",
        display="inline-flex",
        align_items="center",
        transition="all 0.2s",
    )


# ======================================================================
# Fila de materia
# ======================================================================


def fila_materia(materia: str, indice: int) -> rx.Component:
    """
    Fila individual de una materia dentro del plan de estudios.

    El número de la materia usa el color de la carrera como fondo.
    El hover de la fila usa borde con color de carrera.
    """
    color_carrera = _color_carrera_actual()

    return rx.box(
        rx.flex(
            # --- Número de materia (con color de carrera) ---
            rx.flex(
                rx.text(
                    (indice + 1).to_string(),
                    font_size="0.875rem",
                    font_weight="700",
                    color="white",
                ),
                height="2rem",
                width="2rem",
                border_radius=RADIO_MEDIO,
                background=color_carrera,   # ← color de carrera
                align="center",
                justify="center",
                flex_shrink="0",
            ),
            # --- Nombre de la materia ---
            rx.text(
                materia,
                font_size="0.9375rem",
                color=COLOR_TEXTO_CUERPO,
                flex="1",
            ),
            # --- Icono decorativo ---
            rx.icon("book-open", size=16, color=COLOR_TEXTO_SECUNDARIO),
            align="center",
            gap="0.875rem",
            width="100%",
        ),
        padding="0.875rem 1rem",
        border_radius=RADIO_MEDIO,
        background=COLOR_FONDO_CARTA,
        border=f"1px solid {COLOR_BORDE_SUAVE}",
        transition="all 0.2s",
        _hover={
            "background": COLOR_FONDO_SUAVE,
            "border_color": color_carrera,   # ← borde con color de carrera
            "transform": "translateX(4px)",
        },
    )


__all__ = [
    "fila_materia",
    "item_carrera_con_ranking",
    "pastilla_anio",
    "tarjeta_carrera",
]