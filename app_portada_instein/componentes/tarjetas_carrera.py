"""
Componentes visuales relacionados con la presentación de carreras
y su plan de estudios.

Estilo inspirado en Google Play Store:
- Item horizontal con ranking a la izquierda.
- Icono circular + nombre + categoría + rating.
- Hover con fondo sutil.
"""

import reflex as rx

from ..componentes.primitivos import contenedor_clicable, enlace_navegacion
from ..datos.modelos_carrera import Carrera, PlanAnual
from ..dominio.estado_institucional import EstadoInstitucional


# ======================================================================
# Item de carrera con ranking (estilo Google Play)
# ======================================================================

def tarjeta_carrera(carrera: Carrera) -> rx.Component:
    """
    Item de carrera estilo Google Play Store.

    Estructura horizontal:
    - Número de ranking (1, 2, 3...) a la izquierda.
    - Icono circular de la carrera.
    - Nombre + categoría + duración.
    """
    return enlace_navegacion(
        f"/carrera/{carrera['id']}",

        rx.flex(
            # --- Icono circular de la carrera ---
            rx.box(
                rx.image(
                    src="/" + carrera["imagen_archivo"],
                    alt=carrera["nombre"],
                    width="100%",
                    height="100%",
                    object_fit="cover",
                    border_radius="0.875rem",
                ),
                width="4rem",
                height="4rem",
                flex_shrink="0",
                border_radius="0.875rem",
                overflow="hidden",
            ),

            # --- Información ---
            rx.vstack(
                rx.text(
                    carrera["nombre_corto"],
                    font_size="0.9375rem",
                    font_weight="600",
                    color=rx.color_mode_cond(light="#0f172a", dark="#f1f5f9"),
                    line_height="1.3",
                ),
                rx.text(
                    carrera["duracion"] + " · Técnico Superior",
                    font_size="0.75rem",
                    color=rx.color_mode_cond(light="#64748b", dark="#94a3b8"),
                ),
                rx.flex(
                    rx.text(
                        "4.8",
                        font_size="0.75rem",
                        font_weight="600",
                        color=rx.color_mode_cond(light="#0f172a", dark="#f1f5f9"),
                    ),
                    rx.icon("star", size=10, color="#fbbf24", fill="#fbbf24"),
                    align="center",
                    gap="0.25rem",
                    margin_top="0.125rem",
                ),
                align="start",
                spacing="1",
                flex="1",
                min_width="0",
            ),

            align="center",
            gap="1rem",
            width="100%",
        ),

        # --- Estilos base ---
        padding="0.75rem",
        border_radius="0.75rem",
        background="transparent",
        width="100%",
        text_align="left",
        transition="all 0.15s ease-out",
        cursor="pointer",
        _hover={
            "background": rx.color_mode_cond(light="#f1f5f9", dark="#1e293b"),
        },
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
                    color=rx.color_mode_cond(light="#64748b", dark="#94a3b8"),
                ),
                width="1.5rem",
                text_align="center",
                flex_shrink="0",
            ),

            # --- Icono circular ---
            rx.box(
                rx.image(
                    src="/" + carrera["imagen_archivo"],
                    alt=carrera["nombre"],
                    width="100%",
                    height="100%",
                    object_fit="cover",
                    border_radius="0.875rem",
                ),
                width="4rem",
                height="4rem",
                flex_shrink="0",
                border_radius="0.875rem",
                overflow="hidden",
            ),

            # --- Información ---
            rx.vstack(
                rx.text(
                    carrera["nombre_corto"],
                    font_size="0.9375rem",
                    font_weight="600",
                    color=rx.color_mode_cond(light="#0f172a", dark="#f1f5f9"),
                    line_height="1.3",
                ),
                rx.text(
                    carrera["lema"][:40] + "...",
                    font_size="0.75rem",
                    color=rx.color_mode_cond(light="#64748b", dark="#94a3b8"),
                    line_height="1.3",
                ),
                rx.flex(
                    rx.text(
                        "4.8",
                        font_size="0.75rem",
                        font_weight="600",
                        color=rx.color_mode_cond(light="#0f172a", dark="#f1f5f9"),
                    ),
                    rx.icon("star", size=10, color="#fbbf24", fill="#fbbf24"),
                    align="center",
                    gap="0.25rem",
                    margin_top="0.125rem",
                ),
                align="start",
                spacing="1",
                flex="1",
                min_width="0",
            ),

            align="center",
            gap="1rem",
            width="100%",
        ),

        padding="0.75rem",
        border_radius="0.75rem",
        background="transparent",
        width="100%",
        text_align="left",
        transition="all 0.15s ease-out",
        cursor="pointer",
        _hover={
            "background": rx.color_mode_cond(light="#f1f5f9", dark="#1e293b"),
        },
    )


# ======================================================================
# Pastilla de año del plan de estudios
# ======================================================================

def pastilla_anio(plan_anual: PlanAnual, indice: int) -> rx.Component:
    """Pastilla seleccionable que representa un año del plan de estudios."""
    esta_activo = EstadoInstitucional.indice_anio_seleccionado == indice

    return contenedor_clicable(
        rx.text(plan_anual["anio"], size="2"),
        al_hacer_clic=lambda: EstadoInstitucional.seleccionar_anio(indice),
        padding="0.625rem 1.125rem",
        border_radius="0.75rem",
        background=rx.cond(
            esta_activo,
            EstadoInstitucional.carrera_seleccionada["color_principal"],
            rx.color("accent", 1),
        ),
        color=rx.cond(esta_activo, "#ffffff", "gray"),
        border=f"1px solid {rx.cond(esta_activo, 'none', EstadoInstitucional.carrera_seleccionada['color_principal'] + '44')}",
        box_shadow=rx.cond(
            esta_activo,
            "0 4px 12px -2px rgb(37 99 235 / 0.25)",
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
    """Fila individual de una materia dentro del plan de estudios."""
    color_carrera = EstadoInstitucional.carrera_seleccionada["color_principal"]

    return rx.box(
        rx.flex(
            rx.flex(
                rx.text(
                    (indice + 1).to_string(),
                    font_size="0.875rem",
                    font_weight="700",
                    color="#ffffff",
                ),
                height="2rem",
                width="2rem",
                border_radius="0.625rem",
                background=color_carrera,
                align="center",
                justify="center",
                flex_shrink="0",
            ),
            rx.text(
                materia,
                font_size="0.9375rem",
                color=rx.color_mode_cond(light="#334155", dark="#cbd5e1"),
                flex="1",
            ),
            rx.icon("book-open", size=16, color="#94a3b8"),
            align="center",
            gap="0.875rem",
            width="100%",
        ),
        padding="0.875rem 1rem",
        border_radius="0.75rem",
        background=rx.color_mode_cond(light="#f8fafc", dark="#0f1117"),
        border=(
            "1px solid "
            + rx.color_mode_cond(light="#e2e8f0", dark="#1e293b")
        ),
        transition="all 0.2s",
        _hover={
            "background": rx.color_mode_cond(light="#f1f5f9", dark="#1e293b"),
            "border_color": color_carrera + "55",
            "transform": "translateX(4px)",
        },
    )