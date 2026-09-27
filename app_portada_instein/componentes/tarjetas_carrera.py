"""
Componentes visuales relacionados con la presentación de carreras
y su plan de estudios.
"""

import reflex as rx

from ..componentes.primitivos import contenedor_clicable, enlace_navegacion
from ..datos.modelos_carrera import Carrera, PlanAnual
from ..dominio.estado_institucional import EstadoInstitucional


def tarjeta_carrera(carrera: Carrera) -> rx.Component:
    """Tarjeta clicable que enlaza al detalle de una carrera."""
    return enlace_navegacion(
        f"/carrera/{carrera['id']}",
        rx.flex(
            rx.flex(
                rx.box(
                    rx.icon(
                        carrera["icono"],
                        size=30,
                        color=rx.color_mode_cond(
                            light=carrera["color_principal"],
                            dark=carrera["color_suave"],
                        ),
                    ),
                    padding="0.5rem",
                    background=rx.color_mode_cond(
                        light=carrera["color_suave"],
                        dark=carrera["color_principal"],
                    ),
                    border_radius="0.75rem",
                    width="fit-content",
                    display="flex",
                ),
                rx.icon(
                    "arrow-up-right",
                    size=16,
                    color=rx.color_mode_cond(
                        light=carrera["color_principal"],
                        dark=carrera["color_suave"],
                    ),
                ),
                align="start",
                justify="between",
                margin_bottom="0.75rem",
                width="100%",
            ),
            align="start",
            justify="between",
            margin_bottom="0.75rem",
            width="100%",
        ),
        rx.vstack(
            rx.heading(carrera["nombre"], size="4"),
            rx.heading(
                carrera["lema"],
                size="1",
                color=carrera["color_principal"],
                text_transform="uppercase",
            ),
            rx.flex(
                rx.badge(
                    carrera["duracion"],
                    variant="outline",
                    radius="large",
                    color="gray",
                    padding="0.125rem 0.5rem",
                ),
                rx.badge(
                    "Técnico Superior",
                    background=rx.color_mode_cond(
                        light=carrera["color_suave"],
                        dark=carrera["color_principal"],
                    ),
                    color=rx.color_mode_cond(
                        light=carrera["color_principal"],
                        dark=carrera["color_suave"],
                    ),
                    variant="solid",
                    padding="0.125rem 0.5rem",
                ),
                wrap="wrap",
                gap="0.5rem",
                margin_bottom="0.75rem",
            ),
            spacing="2",
        ),
        rx.flex(
            rx.text(
                "Explorar programa",
                size="2",
                color=rx.color_mode_cond(
                    light=carrera["color_principal"],
                    dark=carrera["color_suave"],
                ),
            ),
            rx.icon(
                "chevron-right",
                size=12,
                color=rx.color_mode_cond(
                    light=carrera["color_principal"],
                    dark=carrera["color_suave"],
                ),
            ),
            align="center",
            gap="0.25rem",
            margin_top="0.25rem",
        ),
        padding="1.25rem",
        border_radius="1rem",
        border=f"1px solid {carrera['color_principal']}",
        box_shadow="0 1px 2px 0 rgb(0 0 0 / 0.05)",
        width="100%",
        text_align="left",
        transition="all 0.3s",
        display="flex",
        flex_direction="column",
    )


def pastilla_anio(plan_anual: PlanAnual, indice: int) -> rx.Component:
    """Pastilla seleccionable que representa un año del plan de estudios."""
    esta_activo = EstadoInstitucional.indice_anio_seleccionado == indice

    return contenedor_clicable(
        rx.text(plan_anual["anio"], size="2"),
        al_hacer_clic=lambda: EstadoInstitucional.seleccionar_anio(indice),
        padding="0.5rem 1rem",
        border_radius="0.5rem",
        background=rx.cond(
            esta_activo,
            EstadoInstitucional.carrera_seleccionada["color_principal"],
            rx.color("accent", 1),
        ),
        color=rx.cond(esta_activo, "#ffffff", "gray"),
        border=f"1px solid {rx.cond(esta_activo, 'none', EstadoInstitucional.carrera_seleccionada['color_principal'])}",
        box_shadow=rx.cond(
            esta_activo,
            "0 4px 6px -1px rgb(0 0 0 / 0.08), 0 2px 4px -2px rgb(0 0 0 / 0.05)",
            "none",
        ),
        white_space="nowrap",
        display="inline-flex",
        align_items="center",
    )


def fila_materia(materia: str, indice: int) -> rx.Component:
    """Fila individual de una materia dentro del plan de estudios."""
    return rx.card(
        rx.flex(
            rx.flex(
                rx.text(
                    (indice + 1).to_string(),
                    size="3",
                    color=rx.color_mode_cond(
                        light=EstadoInstitucional.carrera_seleccionada["color_principal"],
                        dark=EstadoInstitucional.carrera_seleccionada["color_suave"],
                    ),
                ),
                height="1.75rem",
                width="1.75rem",
                border_radius="0.5rem",
                background=rx.color_mode_cond(
                    light=EstadoInstitucional.carrera_seleccionada["color_suave"],
                    dark=EstadoInstitucional.carrera_seleccionada["color_principal"],
                ),
                align="center",
                justify="center",
                flex_shrink="0",
            ),
            rx.heading(materia, size="2"),
            rx.icon("book-open", size=16, color="#d1d5db"),
            align="center",
            gap="0.75rem",
            transition="all 0.2s",
        ),
    )