"""
Secciones que componen la vista de detalle de una carrera:
- Información general
- Plan de estudios
- Perfil profesional y campo laboral
"""

import reflex as rx

from ..componentes.primitivos import (
    contenedor_clicable,
    enlace_navegacion,
    tarjeta_informacion_pequena,
)
from ..componentes.tarjetas_carrera import fila_materia, pastilla_anio
from ..componentes.vinetas import (
    vineta_campo_laboral,
    vineta_perfil_profesional,
)
from ..dominio.estado_institucional import EstadoInstitucional
from ..infraestructura.constantes_visuales import SOMBRA_SUAVE


def _estilo_tarjeta_detalle() -> dict:
    """Devuelve el estilo común para tarjetas de detalle."""
    return dict(
        padding="1.5rem",
        border_radius="1rem",
        border="1px solid " + EstadoInstitucional.carrera_seleccionada["color_principal"],
        box_shadow=SOMBRA_SUAVE,
    )


def seccion_informacion() -> rx.Component:
    """Sección de información general de la carrera."""
    return rx.flex(
        rx.box(
            rx.heading(
                "Descripción de la Carrera",
                size="2",
                color_scheme="gray",
                text_transform="uppercase",
                margin_bottom="0.75rem",
            ),
            rx.text(EstadoInstitucional.carrera_seleccionada["descripcion"]),
            **_estilo_tarjeta_detalle(),
        ),
        rx.flex(
            tarjeta_informacion_pequena(
                icono="clock",
                titulo="Duración",
                valor=EstadoInstitucional.carrera_seleccionada["duracion"],
                color_icono=rx.color_mode_cond(
                    light=EstadoInstitucional.carrera_seleccionada["color_principal"],
                    dark=EstadoInstitucional.carrera_seleccionada["color_suave"],
                ),
            ),
            tarjeta_informacion_pequena(
                icono="award",
                titulo="Título",
                valor="Técnico Superior",
                color_icono=rx.color_mode_cond(
                    light=EstadoInstitucional.carrera_seleccionada["color_principal"],
                    dark=EstadoInstitucional.carrera_seleccionada["color_suave"],
                ),
            ),
            flex_direction=["column", "column", "row"],
            spacing="4",
            padding="1em",
            width="100%",
        ),
        enlace_navegacion(
            "/contacto",
            rx.flex(
                rx.icon("phone-call", size=20, color="#ffffff"),
                rx.box(
                    rx.text("¿Interesado en esta carrera?", color="#ffffff"),
                    rx.text("Contáctanos para más información", color="#ffffff"),
                ),
                rx.icon(
                    "arrow-right", size=30, color="#ffffff", margin_left="auto"
                ),
                align="center",
                gap="0.75rem",
            ),
            background=EstadoInstitucional.carrera_seleccionada["color_principal"],
            padding="1.25rem",
            border_radius="1rem",
            box_shadow="0 10px 25px -5px rgb(37 99 235 / 0.25)",
            transition="all 0.2s",
            # Ya no es necesario text_decoration="none"; el helper lo aplica.
        ),
        gap="1rem",
        direction="column",
        width="100%",
    )


def seccion_plan_estudios() -> rx.Component:
    """Sección con el plan de estudios dividido por años."""
    return rx.box(
        rx.box(
            rx.heading(
                "Plan de Estudios",
                size="2",
                color="gray",
                text_transform="uppercase",
                margin_bottom="0.75rem",
            ),
            rx.box(
                rx.foreach(
                    EstadoInstitucional.carrera_seleccionada["plan_estudios"],
                    lambda plan_anual, indice: pastilla_anio(plan_anual, indice),
                ),
                display="flex",
                gap="0.5rem",
                overflow_x="auto",
                padding_bottom="0.5rem",
                padding_left="0.25rem",
                padding_right="0.25rem",
                margin_left="-0.25rem",
                margin_right="-0.25rem",
            ),
            margin_bottom="1rem",
        ),
        rx.card(
            rx.flex(
                rx.box(
                    rx.text(EstadoInstitucional.plan_anual_seleccionado["anio"]),
                    rx.text(
                        EstadoInstitucional.plan_anual_seleccionado["materias"]
                        .length()
                        .to_string()
                        + " materias",
                        size="1",
                        color_scheme="gray",
                    ),
                ),
                rx.box(
                    rx.icon(
                        "graduation-cap",
                        size=40,
                        color=EstadoInstitucional.carrera_seleccionada["color_principal"],
                    ),
                ),
                align="center",
                justify="between",
                margin_bottom="1rem",
            ),
            rx.vstack(
                rx.foreach(
                    EstadoInstitucional.plan_anual_seleccionado["materias"],
                    lambda materia, indice: fila_materia(materia, indice),
                ),
                gap="0.5rem",
                width="100%",
            ),
        ),
    )


def seccion_perfil_y_campo_laboral() -> rx.Component:
    """Sección con perfil profesional y campo laboral."""
    return rx.flex(
        rx.box(
            rx.flex(
                rx.icon(
                    "user-check",
                    size=26,
                    color=EstadoInstitucional.carrera_seleccionada["color_principal"],
                ),
                rx.heading("Perfil Profesional", size="2"),
                align="center",
                gap="0.5rem",
                margin_bottom="1rem",
            ),
            rx.vstack(
                rx.foreach(
                    EstadoInstitucional.carrera_seleccionada["perfil_profesional"],
                    vineta_perfil_profesional,
                ),
                gap="0.75rem",
                width="100%",
            ),
            **_estilo_tarjeta_detalle(),
            width="100%",
        ),
        rx.box(
            rx.flex(
                rx.icon(
                    "building-2",
                    size=26,
                    color=EstadoInstitucional.carrera_seleccionada["color_principal"],
                ),
                rx.heading("Campo Laboral", size="2"),
                align="center",
                gap="0.5rem",
                margin_bottom="1rem",
            ),
            rx.vstack(
                rx.foreach(
                    EstadoInstitucional.carrera_seleccionada["campo_laboral"],
                    vineta_campo_laboral,
                ),
                gap="0.75rem",
                width="100%",
            ),
            **_estilo_tarjeta_detalle(),
            width="100%",
        ),
        spacing="4",
        flex_direction=["column", "column", "row"],
        width="100%",
    )