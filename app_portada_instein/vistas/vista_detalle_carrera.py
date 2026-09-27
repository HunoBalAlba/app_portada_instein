"""
Vista de detalle de una carrera específica
(ruta dinámica "/carrera/[carrera_id]").
"""

import reflex as rx

from ..componentes.barra_navegacion import barra_navegacion_superior
from ..componentes.primitivos import contenedor_clicable, enlace_navegacion
from ..componentes.secciones_detalle import (
    seccion_informacion,
    seccion_perfil_y_campo_laboral,
    seccion_plan_estudios,
)
from ..dominio.estado_institucional import EstadoInstitucional
from ..infraestructura.constantes_visuales import NOMBRE_INSTITUTO


def _pestana_seccion(etiqueta: str, icono: str, id_seccion: str) -> rx.Component:
    """Pestaña seleccionable dentro de la vista de detalle."""
    esta_activa = EstadoInstitucional.seccion_detalle_activa == id_seccion

    return contenedor_clicable(
        rx.icon(
            icono,
            size=26,
            color=rx.cond(esta_activa, "#f3f4f7", "gray"),
        ),
        rx.text(
            etiqueta,
            as_="span",
            color=rx.cond(esta_activa, "#f3f4f7", "gray"),
        ),
        al_hacer_clic=lambda: EstadoInstitucional.seleccionar_seccion_detalle(
            id_seccion
        ),
        display="flex",
        align_items="center",
        justify_content="center",
        gap="0.5rem",
        flex="1",
        padding="0.625rem 0",
        border_radius="0.75rem",
        background=rx.cond(
            esta_activa,
            EstadoInstitucional.carrera_seleccionada["color_principal"],
            "transparent",
        ),
        box_shadow=rx.cond(esta_activa, "0 1px 2px 0 rgb(0 0 0 / 0.05)", "none"),
        transition="all 0.2s",
        border=f"0.5px solid {rx.cond(esta_activa, 'transparent', EstadoInstitucional.carrera_seleccionada['color_principal'])}",
    )


def _encabezado_fijo_detalle() -> rx.Component:
    """Encabezado fijo con botón de regreso y nombre corto de la carrera."""
    return rx.box(
        rx.flex(
            enlace_navegacion(
                "/carreras",
                rx.icon("layout-grid", size=26),
                color=rx.color("accent", 11),
                padding="0.5rem",
                margin_left="-0.5rem",
                border_radius="0.75rem",
                border=f"1px solid {rx.color('accent', 8)}",
                display="flex",
            ),
            rx.heading(
                EstadoInstitucional.carrera_seleccionada["nombre_corto"],
                size="6",
            ),
            rx.box(width="2.25rem"),
            justify="between",
            padding="0.525rem 1rem",
            border_radius="1rem",
            width="100%",
            align="center",
            background=rx.color("accent", 1),
            flex_shrink="0",
        ),
        align="center",
        justify="between",
        width="100%",
        padding="0.625rem 1rem",
        background=rx.color("accent", 1),
        position="sticky",
        top="0",
        z_index="50",
    )


def _hero_carrera() -> rx.Component:
    """Bloque de presentación principal de la carrera seleccionada."""
    return rx.box(
        rx.box(
            rx.icon(
                EstadoInstitucional.carrera_seleccionada["icono"],
                size=32,
                color="#ffffff",
            ),
            padding="1rem",
            background=EstadoInstitucional.carrera_seleccionada["color_principal"],
            border_radius="1rem",
            border="3px solid "
            + EstadoInstitucional.carrera_seleccionada["color_principal"],
            box_shadow="0 10px 25px -5px rgb(37 99 235 / 0.25)",
            width="fit-content",
            margin_bottom="1.25rem",
            display="flex",
        ),
        rx.heading(EstadoInstitucional.carrera_seleccionada["nombre"], size="7"),
        rx.heading(
            EstadoInstitucional.carrera_seleccionada["lema"],
            size="3",
            color=EstadoInstitucional.carrera_seleccionada["color_principal"],
        ),
        rx.flex(
            rx.flex(
                rx.icon("clock", size=12),
                rx.text(EstadoInstitucional.carrera_seleccionada["duracion"]),
                align="center",
                gap="0.375rem",
                font_size="0.75rem",
                font_weight="600",
                border="1px solid "
                + EstadoInstitucional.carrera_seleccionada["color_principal"],
                padding="0.375rem 0.75rem",
                border_radius="0.5rem",
            ),
            rx.flex(
                rx.icon(
                    "shield-check",
                    size=12,
                    color=rx.color_mode_cond(
                        light=EstadoInstitucional.carrera_seleccionada[
                            "color_principal"
                        ],
                        dark=EstadoInstitucional.carrera_seleccionada["color_suave"],
                    ),
                ),
                rx.text(
                    "Técnico Superior",
                    color=rx.color_mode_cond(
                        light=EstadoInstitucional.carrera_seleccionada[
                            "color_principal"
                        ],
                        dark=EstadoInstitucional.carrera_seleccionada["color_suave"],
                    ),
                ),
                background=rx.color_mode_cond(
                    light=EstadoInstitucional.carrera_seleccionada["color_suave"],
                    dark=EstadoInstitucional.carrera_seleccionada["color_principal"],
                ),
                align="center",
                gap="0.375rem",
                font_size="0.75rem",
                font_weight="600",
                padding="0.375rem 0.75rem",
                border_radius="0.5rem",
            ),
            wrap="wrap",
            gap="0.5rem",
            margin_top="1rem",
        ),
        padding="1.5rem 1.5rem 1rem 1.5rem",
    )


@rx.page(
    route="/carrera/[carrera_id]",
    title=f"Detalle de Carrera | {NOMBRE_INSTITUTO}",
)
def vista_detalle_carrera() -> rx.Component:
    """Página de detalle con información, plan y perfil de la carrera."""
    return rx.vstack(
        barra_navegacion_superior(),
        rx.box(
            _encabezado_fijo_detalle(),
            _hero_carrera(),
            rx.box(
                rx.flex(
                    _pestana_seccion("Info", "info", "info"),
                    _pestana_seccion("Plan", "book-open-text", "plan"),
                    _pestana_seccion("Perfil", "target", "perfil"),
                    gap="0.25rem",
                    padding="0.25rem",
                ),
                padding="0.5rem 0rem 1rem 0rem",
                position="sticky",
                top="69px",
                z_index="40",
                background=rx.color("accent", 1),
                backdrop_filter="blur(12px)",
            ),
            rx.box(
                rx.match(
                    EstadoInstitucional.seccion_detalle_activa,
                    ("info", seccion_informacion()),
                    ("plan", seccion_plan_estudios()),
                    ("perfil", seccion_perfil_y_campo_laboral()),
                    seccion_informacion(),
                ),
                padding="0 1rem 6rem 1rem",
            ),
            padding_bottom="3rem",
            max_width="72rem",
            width="100%",
        ),
        align="center",
        min_height="100vh",
        width="100%",
    )