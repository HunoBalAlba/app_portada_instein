"""
Vista de detalle de una carrera específica
(ruta dinámica "/carrera/[carrera_id]").

Muestra:
- La imagen de la carrera rodeada de iconos orbitando (órbita kepleriana).
- Información, plan de estudios, perfil/campo laboral y preguntas frecuentes.

Usa `rx.tabs.root` (pestañas) para gestionar las secciones.
"""

import reflex as rx

from ..componentes.barra_navegacion import barra_navegacion_superior
from ..componentes.pie_pagina import pie_pagina_institucional
from ..componentes.primitivos import contenedor_clicable, enlace_navegacion
from ..componentes.secciones_detalle import (
    seccion_informacion,
    seccion_perfil_y_campo_laboral,
    seccion_plan_estudios,
)
from ..dominio.estado_institucional import EstadoInstitucional
from ..infraestructura.constantes_visuales import NOMBRE_INSTITUTO


# ======================================================================
# Estado del acordeón de preguntas frecuentes
# ======================================================================

class EstadoPreguntasFrecuentesDetalle(rx.State):
    """Estado del acordeón de preguntas frecuentes en la vista de detalle."""

    indice_pregunta_abierta: int = -1

    @rx.event
    def alternar_pregunta(self, indice: int):
        """Abre o cierra una pregunta frecuente."""
        if self.indice_pregunta_abierta == indice:
            self.indice_pregunta_abierta = -1
        else:
            self.indice_pregunta_abierta = indice


# ======================================================================
# Trigger de pestaña (plantilla reutilizable)
# ======================================================================

def _pestana_trigger(texto: str, icono: str, value: str) -> rx.Component:
    """
    Trigger (botón) de pestaña con icono + texto.

    Cada pestaña tiene un `value` único que la identifica.
    """
    return rx.tabs.trigger(
        rx.hstack(
            rx.icon(icono, size=20),
            rx.heading(texto, size="4"),
            spacing="2",
            align="center",
            width="100%",
        ),
        value=value,
    )


# ======================================================================
# Encabezado fijo
# ======================================================================

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


# ======================================================================
# Icono orbital
# ======================================================================

def _icono_orbital(icono_animado: dict) -> rx.Component:
    """Renderiza un icono orbitando alrededor de la imagen de la carrera."""
    periodo = icono_animado["periodo"]
    keyframe_orbita = icono_animado["keyframe_orbita"]
    desfase = icono_animado["desfase_temporal"]
    color_icono = icono_animado["color"]
    tiene_anillos = icono_animado["tiene_anillos"]

    return rx.box(
        rx.box(
            rx.cond(
                tiene_anillos,
                _anillos_saturno(color_icono),
                rx.fragment(),
            ),
            rx.icon(
                icono_animado["nombre"],
                size=18,
                color="#ffffff",
            ),
            padding="0.5rem",
            border_radius="0.625rem",
            background=color_icono,
            box_shadow=f"0 6px 16px -4px {color_icono}88",
            display="flex",
            align_items="center",
            justify_content="center",
            position="relative",
        ),
        position="absolute",
        top="50%",
        left="50%",
        transform_origin="center center",
        animation=f"{keyframe_orbita} {periodo}s linear {desfase}s infinite",
        z_index="20",
    )


def _anillos_saturno(color: str) -> rx.Component:
    """Dibuja los anillos característicos de Saturno alrededor del icono."""
    return rx.box(
        rx.box(
            position="absolute",
            top="50%",
            left="50%",
            width="1.8rem",
            height="0.45rem",
            border=f"2px solid {color}cc",
            border_radius="9999px",
            transform="translate(-50%, -50%)",
        ),
        rx.box(
            position="absolute",
            top="50%",
            left="50%",
            width="2.2rem",
            height="0.65rem",
            border=f"1.5px solid {color}66",
            border_radius="9999px",
            transform="translate(-50%, -50%)",
        ),
        position="absolute",
        top="50%",
        left="50%",
        width="0",
        height="0",
        z_index="5",
        pointer_events="none",
    )


# ======================================================================
# Contenedor orbital con imagen central + iconos orbitando
# ======================================================================

def _contenedor_orbital_imagen() -> rx.Component:
    """Contenedor cuadrado con halo, iconos orbitando e imagen central."""
    carrera = EstadoInstitucional.carrera_seleccionada
    color_principal = carrera["color_principal"]
    color_suave = carrera["color_suave"]

    return rx.box(
        # --- Halo radial ---
        rx.box(
            position="absolute",
            top="0",
            left="0",
            right="0",
            bottom="0",
            background=(
                "radial-gradient(circle at 50% 50%, "
                + color_principal
                + "33 0%, "
                + color_suave
                + "00 60%)"
            ),
            border_radius="9999px",
            filter="blur(20px)",
            z_index="1",
        ),

        # --- Iconos orbitales ---
        rx.box(
            rx.foreach(
                carrera["iconos_animados"],
                _icono_orbital,
            ),
            position="absolute",
            top="0",
            left="0",
            right="0",
            bottom="0",
            z_index="5",
        ),

        # --- Imagen central ---
        rx.box(
            rx.image(
                src="/" + carrera["imagen_archivo"],
                alt=carrera["nombre"],
                width="100%",
                height="100%",
                object_fit="cover",
                border_radius="9999px",
            ),
            position="absolute",
            top="50%",
            left="50%",
            transform="translate(-50%, -50%)",
            width="15rem",
            height="15rem",
            border_radius="9999px",
            border="3px solid " + color_principal,
            box_shadow=f"0 15px 30px -8px {color_principal}80",
            overflow="hidden",
            z_index="10",
            animation="pulso_central 3s ease-in-out infinite",
        ),

        position="relative",
        width="100%",
        max_width="20rem",
        aspect_ratio="1",
        margin="0 auto",
        display="flex",
        align_items="center",
        justify_content="center",
        overflow="visible",
    )


# ======================================================================
# Hero de carrera
# ======================================================================

def _hero_carrera() -> rx.Component:
    """Bloque de presentación principal con la imagen orbital + texto."""
    carrera = EstadoInstitucional.carrera_seleccionada

    return rx.flex(
        # --- Columna izquierda: contenedor orbital ---
        rx.box(
            _contenedor_orbital_imagen(),
            width=["100%", "100%", "100%", "40%"],
        ),
        # --- Columna derecha: información textual ---
        rx.vstack(
            rx.heading(carrera["nombre"], size="7"),
            rx.heading(
                carrera["lema"],
                size="3",
                color=carrera["color_principal"],
            ),
            rx.flex(
                rx.flex(
                    rx.icon("clock", size=12),
                    rx.text(carrera["duracion"]),
                    align="center",
                    gap="0.375rem",
                    font_size="0.75rem",
                    font_weight="600",
                    border="1px solid " + carrera["color_principal"],
                    padding="0.375rem 0.75rem",
                    border_radius="0.5rem",
                ),
                rx.flex(
                    rx.icon(
                        "shield-check",
                        size=12,
                        color=rx.color_mode_cond(
                            light=carrera["color_principal"],
                            dark=carrera["color_suave"],
                        ),
                    ),
                    rx.text(
                        "Técnico Superior",
                        color=rx.color_mode_cond(
                            light=carrera["color_principal"],
                            dark=carrera["color_suave"],
                        ),
                    ),
                    background=rx.color_mode_cond(
                        light=carrera["color_suave"],
                        dark=carrera["color_principal"],
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
                margin_top="0.5rem",
            ),
            align="start",
            spacing="3",
            width=["100%", "100%", "100%", "60%"],
        ),
        width="100%",
        justify="center",
        align="center",
        gap="2rem",
        padding="1.5rem 1.5rem 1rem 1.5rem",
        flex_direction=["column", "column", "column", "row"],
    )


# ======================================================================
# Sección: PREGUNTAS FRECUENTES
# ======================================================================

def _item_pregunta(pregunta: dict, indice: int) -> rx.Component:
    """Item individual de preguntas frecuentes con acordeón."""
    esta_abierta = (
        EstadoPreguntasFrecuentesDetalle.indice_pregunta_abierta == indice
    )
    color_carrera = EstadoInstitucional.carrera_seleccionada["color_principal"]

    return rx.box(
        # --- Cabecera clicable ---
        rx.box(
            rx.flex(
                rx.icon(
                    "help-circle",
                    size=18,
                    color=color_carrera,
                    flex_shrink="0",
                ),
                rx.text(
                    pregunta["pregunta"],
                    font_size="0.9375rem",
                    font_weight="600",
                    color=rx.color_mode_cond(light="#1e293b", dark="#f1f5f9"),
                    flex="1",
                ),
                rx.icon(
                    "chevron-down",
                    size=18,
                    color=rx.color_mode_cond(light="#64748b", dark="#94a3b8"),
                    transform=rx.cond(
                        esta_abierta,
                        "rotate(180deg)",
                        "rotate(0deg)",
                    ),
                    transition="transform 0.3s",
                    flex_shrink="0",
                ),
                align="center",
                gap="0.75rem",
                width="100%",
            ),
            on_click=lambda: EstadoPreguntasFrecuentesDetalle.alternar_pregunta(
                indice
            ),
            cursor="pointer",
            padding="1.125rem 1.25rem",
            role="button",
            tab_index=0,
            width="100%",
        ),
        # --- Respuesta colapsable ---
        rx.cond(
            esta_abierta,
            rx.box(
                rx.text(
                    pregunta["respuesta"],
                    font_size="0.875rem",
                    line_height="1.6",
                    color=rx.color_mode_cond(light="#475569", dark="#cbd5e1"),
                ),
                padding="0 1.25rem 1.25rem 3.25rem",
            ),
            rx.fragment(),
        ),
        width="100%",
        border=rx.cond(
            esta_abierta,
            f"1px solid {color_carrera}66",
            "1px solid "
            + rx.color_mode_cond(light="#e2e8f0", dark="#1e293b"),
        ),
        border_radius="0.875rem",
        background=rx.color_mode_cond(light="#ffffff", dark="#0f1117"),
        transition="all 0.2s",
        _hover={"border_color": color_carrera + "44"},
    )


def _seccion_preguntas_frecuentes() -> rx.Component:
    """Sección completa con las preguntas frecuentes de la carrera."""
    carrera = EstadoInstitucional.carrera_seleccionada
    color_carrera = carrera["color_principal"]

    return rx.vstack(
        # --- Encabezado ---
        rx.flex(
            rx.icon("help-circle", size=22, color=color_carrera),
            rx.heading(
                "Preguntas Frecuentes",
                size="4",
                color=rx.color_mode_cond(light="#0f172a", dark="#f1f5f9"),
            ),
            rx.text(
                carrera["preguntas_frecuentes"].length().to_string(),
                font_size="0.75rem",
                font_weight="700",
                color=color_carrera,
                padding="0.125rem 0.5rem",
                background=color_carrera + "15",
                border_radius="9999px",
            ),
            align="center",
            gap="0.5rem",
            margin_bottom="1.5rem",
        ),

        # --- Lista de preguntas ---
        rx.vstack(
            rx.foreach(
                carrera["preguntas_frecuentes"],
                lambda pregunta, idx: _item_pregunta(pregunta, idx),
            ),
            width="100%",
            spacing="3",
        ),

        spacing="0",
        width="100%",
        max_width="64rem",
        margin="0 auto",
    )


# ======================================================================
# Pestañas de secciones del detalle
# ======================================================================

def _pestanas_secciones_detalle() -> rx.Component:
    """
    Sistema de pestañas con `rx.tabs.root` para las 4 secciones del detalle.

    Estructura:
    - `rx.tabs.list`: contiene los triggers (Info, Plan, Perfil, Preguntas Frecuentes).
    - `rx.tabs.content`: contiene el contenido de cada sección.

    El estado de la pestaña activa se gestiona con
    `EstadoInstitucional.seccion_detalle_activa` mediante `value` y `on_change`.
    """
    return rx.tabs.root(
        # --- Lista de triggers ---
        rx.tabs.list(
            _pestana_trigger("Info", "info", value="info"),
            _pestana_trigger("Plan", "book-open-text", value="plan"),
            _pestana_trigger("Perfil", "target", value="perfil"),
            _pestana_trigger(
                "Preguntas Frecuentes",
                "help-circle",
                value="preguntas_frecuentes",
            ),
            width="100%",
        ),

        # --- Contenido: Info ---
        rx.tabs.content(
            seccion_informacion(),
            margin_top="1em",
            value="info",
        ),

        # --- Contenido: Plan ---
        rx.tabs.content(
            seccion_plan_estudios(),
            margin_top="1em",
            value="plan",
        ),

        # --- Contenido: Perfil ---
        rx.tabs.content(
            seccion_perfil_y_campo_laboral(),
            margin_top="1em",
            value="perfil",
        ),

        # --- Contenido: Preguntas Frecuentes ---
        rx.tabs.content(
            _seccion_preguntas_frecuentes(),
            margin_top="1em",
            value="preguntas_frecuentes",
        ),

        # --- Configuración del root ---
        default_value="info",
        value=EstadoInstitucional.seccion_detalle_activa,
        on_change=EstadoInstitucional.seleccionar_seccion_detalle,
        width="100%",
    )


# ======================================================================
# Vista completa
# ======================================================================

@rx.page(
    route="/carrera/[carrera_id]",
    title=f"Detalle de Carrera | {NOMBRE_INSTITUTO}",
)
def vista_detalle_carrera() -> rx.Component:
    """
    Página de detalle con:
    - Encabezado fijo.
    - Hero con imagen orbital.
    - Pestañas (Info, Plan, Perfil, Preguntas Frecuentes).
    - Pie de página.
    """
    return rx.vstack(
        barra_navegacion_superior(),
        rx.box(
            _encabezado_fijo_detalle(),
            _hero_carrera(),

            # --- Pestañas de secciones ---
            rx.box(
                _pestanas_secciones_detalle(),
                padding="0 1rem 6rem 1rem",
            ),

            padding_bottom="3rem",
            max_width="72rem",
            width="100%",
        ),
        pie_pagina_institucional(),
        align="center",
        min_height="100vh",
        width="100%",
    )