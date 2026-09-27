"""
Secciones que componen la vista de detalle de una carrera:
- Información general
- Plan de estudios (con selector segmentado de años)
- Perfil profesional y campo laboral
"""

import reflex as rx

from app_portada_instein.componentes.primitivos import (
    enlace_navegacion,
    tarjeta_informacion_pequena,
)
from app_portada_instein.componentes.tarjetas_carrera import fila_materia
from app_portada_instein.componentes.vinetas import vineta_campo_laboral, vineta_perfil_profesional
from app_portada_instein.dominio.estado_institucional import EstadoInstitucional
from app_portada_instein.infraestructura.constantes_visuales import SOMBRA_SUAVE


# ======================================================================
# Estilos auxiliares
# ======================================================================


def _estilo_tarjeta_detalle() -> dict:
    """Devuelve el estilo común para tarjetas de detalle."""
    return {
        "padding": "1.5rem",
        "border_radius": "1rem",
        "border": "1px solid " + EstadoInstitucional.carrera_seleccionada["color_principal"],
        "box_shadow": SOMBRA_SUAVE,
    }


# ======================================================================
# Estado del selector segmentado del plan de estudios
# ======================================================================


class EstadoPlanEstudios(rx.State):
    """Estado del selector segmentado para seleccionar el año del plan."""

    anio_seleccionado: str = "0"
    """Valor del año seleccionado como string (ej: "0", "1", "2")."""

    @rx.event
    def cambiar_anio(self, valor: str | list[str]):
        """
        Cambia el año seleccionado desde el selector segmentado.

        El `on_change` de `rx.segmented_control.root` envía el valor
        como `str` o `list[str]` según el modo. Normalizamos ambos
        casos a un string simple.

        Args:
            valor: Valor del item seleccionado. Puede ser "1" o ["1"].
        """
        if isinstance(valor, list):
            self.anio_seleccionado = valor[0] if valor else "0"
        else:
            self.anio_seleccionado = str(valor)

    @rx.var
    def indice_anio_actual(self) -> int:
        """Devuelve el índice del año seleccionado como int."""
        try:
            return int(self.anio_seleccionado)
        except (ValueError, TypeError):
            return 0


# ======================================================================
# Sección: INFORMACIÓN
# ======================================================================


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
                rx.icon("arrow-right", size=30, color="#ffffff", margin_left="auto"),
                align="center",
                gap="0.75rem",
            ),
            background=EstadoInstitucional.carrera_seleccionada["color_principal"],
            padding="1.25rem",
            border_radius="1rem",
            box_shadow="0 10px 25px -5px rgb(37 99 235 / 0.25)",
            transition="all 0.2s",
        ),
        gap="1rem",
        direction="column",
        width="100%",
    )


# ======================================================================
# Sección: PLAN DE ESTUDIOS (con selector segmentado)
# ======================================================================


def _opcion_anio_segmento(opcion: dict) -> rx.Component:
    """
    Renderiza un item del selector segmentado de años.

    Recibe un dict con `etiqueta` y `valor` precalculados en el State,
    por lo que no necesita el índice adicional.
    """
    return rx.segmented_control.item(
        opcion["etiqueta"],
        value=opcion["valor"],
    )


def seccion_plan_estudios() -> rx.Component:
    """
    Sección con el plan de estudios dividido por años.

    Usa `rx.segmented_control.root` (selector segmentado) con items
    precalculados en el State (`opciones_anio_plan`).
    """
    return rx.box(
        # --- Encabezado ---
        rx.box(
            rx.heading(
                "Plan de Estudios",
                size="2",
                color="gray",
                text_transform="uppercase",
                margin_bottom="0.75rem",
            ),
            # --- Selector segmentado de años ---
            rx.segmented_control.root(
                rx.foreach(
                    EstadoInstitucional.opciones_anio_plan,
                    _opcion_anio_segmento,
                ),
                on_change=EstadoPlanEstudios.cambiar_anio,
                value=EstadoPlanEstudios.anio_seleccionado,
                width="100%",
                size="3",
                variant="surface",
                radius="large",
            ),
            margin_bottom="1rem",
        ),
        # --- Contenido del año seleccionado ---
        rx.card(
            rx.flex(
                rx.box(
                    rx.text(
                        EstadoInstitucional.carrera_seleccionada["plan_estudios"][
                            EstadoPlanEstudios.indice_anio_actual
                        ]["anio"],
                        size="3",
                        font_weight="700",
                    ),
                    rx.text(
                        EstadoInstitucional.carrera_seleccionada["plan_estudios"][
                            EstadoPlanEstudios.indice_anio_actual
                        ]["materias"]
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
                    EstadoInstitucional.carrera_seleccionada["plan_estudios"][
                        EstadoPlanEstudios.indice_anio_actual
                    ]["materias"],
                    fila_materia,
                ),
                gap="0.5rem",
                width="100%",
            ),
        ),
    )


# ======================================================================
# Sección: PERFIL Y CAMPO LABORAL
# ======================================================================


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
