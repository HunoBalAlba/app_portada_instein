# app_portada_instein/componentes/tarjetas_carrera.py

"""
Componentes visuales relacionados con la presentación de carreras
y su plan de estudios — estilo Neon dark.

Estilo inspirado en Google Play Store (dark mode):
- Item horizontal con ranking a la izquierda.
- Icono circular + nombre + categoría + rating.
- Hover con fondo azul marino translúcido.

Sistema de color (UX)
---------------------
✅ REFACTORIZADO: TODAS las carreras usan azul marino (`AZUL_MARINO_NEON`).
   Ya no hay colores de marca individuales porque el home es dark con un
   único acento.

- Textos: blanco puro y blanco suave (`TEXTO_OSCURO_*`).
- Acentos: azul marino neon (`AZUL_MARINO_NEON` = `#3b5bdb`).
- Bordes: oscuros translúcidos (`BORDE_OSCURO_*`).
- Rating: estrella amarilla (`#fbbf24`).
"""

import reflex as rx

from app_portada_instein.componentes.primitivos import (
    contenedor_clicable,
    enlace_navegacion,
)
from app_portada_instein.datos.modelos_carrera import Carrera, PlanAnual
from app_portada_instein.dominio.estado_institucional import EstadoInstitucional
from app_portada_instein.infraestructura.constantes_visuales import (
    AZUL_MARINO_NEON,
    BORDE_OSCURO_AZUL,
    BORDE_OSCURO_SUAVE,
    FONDO_HOME_CARD,
    RADIO_MEDIO,
    TEXTO_OSCURO_MAS_SUAVE,
    TEXTO_OSCURO_PRINCIPAL,
    TEXTO_OSCURO_SUAVE,
)


# ======================================================================
# Constantes locales
# ======================================================================

# Color de la estrella de puntuación (amarillo semántico).
COLOR_ESTRELLA = "#fbbf24"

# Tamaño del icono circular de la carrera.
TAMANO_ICONO_CARRERA = "4rem"

# Color suave azul marino (para fondos tintados).
COLOR_AZUL_MARINO_SUAVE = "rgba(59, 91, 219, 0.15)"


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
        border=f"1px solid {BORDE_OSCURO_SUAVE}",
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
            color=TEXTO_OSCURO_PRINCIPAL,
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
            font_weight="700",
            color=TEXTO_OSCURO_PRINCIPAL,
            line_height="1.3",
        ),
        rx.text(
            texto_secundario,
            font_size="0.75rem",
            color=TEXTO_OSCURO_MAS_SUAVE,
            line_height="1.3",
        ),
        _rating_compacto(),
        align="start",
        spacing="1",
        flex="1",
        min_width="0",
    )


# ======================================================================
# Item de carrera con ranking (estilo Google Play dark)
# ======================================================================


def tarjeta_carrera(carrera: Carrera) -> rx.Component:
    """
    Item de carrera estilo Google Play Store (dark).

    Estructura horizontal:
    - Icono circular de la carrera.
    - Nombre + duración + rating.

    Estilo Neon:
    - Fondo transparente por defecto.
    - Hover: fondo azul marino translúcido.
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
        _hover={"background": COLOR_AZUL_MARINO_SUAVE},
    )


# ======================================================================
# Item de carrera con ranking explícito (número a la izquierda)
# ======================================================================


def item_carrera_con_ranking(carrera: Carrera, indice: int) -> rx.Component:
    """
    Item de carrera con número de ranking a la izquierda.
    Estilo "Listas de éxitos" de Google Play (dark).
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
                    color=TEXTO_OSCURO_MAS_SUAVE,
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
        _hover={"background": COLOR_AZUL_MARINO_SUAVE},
    )


# ======================================================================
# Pastilla de año del plan de estudios
# ======================================================================


def pastilla_anio(plan_anual: PlanAnual, indice: int) -> rx.Component:
    """
    Pastilla seleccionable que representa un año del plan de estudios.

    ✅ REFACTORIZADO: usa azul marino neon en lugar del color de la
    carrera.

    Estilo Neon:
    - Activa: fondo azul marino neon + texto blanco + glow azul.
    - Inactiva: fondo dark translúcido + borde oscuro.
    """
    esta_activo = EstadoInstitucional.indice_anio_seleccionado == indice

    return contenedor_clicable(
        rx.text(plan_anual["anio"], size="2"),
        al_hacer_clic=lambda: EstadoInstitucional.seleccionar_anio(indice),
        padding="0.625rem 1.125rem",
        border_radius=RADIO_MEDIO,
        background=rx.cond(
            esta_activo,
            AZUL_MARINO_NEON,
            "rgba(255, 255, 255, 0.05)",
        ),
        color=rx.cond(
            esta_activo,
            "white",
            TEXTO_OSCURO_SUAVE,
        ),
        border=rx.cond(
            esta_activo,
            f"1px solid {AZUL_MARINO_NEON}",
            f"1px solid {BORDE_OSCURO_SUAVE}",
        ),
        box_shadow=rx.cond(
            esta_activo,
            f"0 0 20px {AZUL_MARINO_NEON}60",
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

    ✅ REFACTORIZADO: usa azul marino neon en lugar del color de la
    carrera.

    Estilo Neon:
    - Número de materia: fondo azul marino neon con glow.
    - Hover: borde azul marino + fondo translúcido + desplazamiento.
    """
    return rx.box(
        rx.flex(
            # --- Número de materia (azul marino neon) ---
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
                background=AZUL_MARINO_NEON,
                box_shadow=f"0 0 12px {AZUL_MARINO_NEON}60",
                align="center",
                justify="center",
                flex_shrink="0",
            ),
            # --- Nombre de la materia ---
            rx.text(
                materia,
                font_size="0.9375rem",
                color=TEXTO_OSCURO_SUAVE,
                flex="1",
            ),
            # --- Icono decorativo ---
            rx.icon(
                "book-open",
                size=16,
                color=TEXTO_OSCURO_MAS_SUAVE,
            ),
            align="center",
            gap="0.875rem",
            width="100%",
        ),
        padding="0.875rem 1rem",
        border_radius=RADIO_MEDIO,
        background=FONDO_HOME_CARD,
        backdrop_filter="blur(12px)",
        border=f"1px solid {BORDE_OSCURO_SUAVE}",
        transition="all 0.2s",
        _hover={
            "background": COLOR_AZUL_MARINO_SUAVE,
            "border_color": BORDE_OSCURO_AZUL,
            "transform": "translateX(4px)",
        },
    )


__all__ = [
    "fila_materia",
    "item_carrera_con_ranking",
    "pastilla_anio",
    "tarjeta_carrera",
]