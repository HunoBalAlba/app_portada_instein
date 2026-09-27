"""
Vista de detalle de una carrera específica
(ruta dinámica "/carrera/[carrera_id]").

Estructura:
- Encabezado sticky con breadcrumb, botón de regreso y progreso de scroll.
- Hero con contenedor orbital (imagen + iconos orbitando).
- Hero con información textual: nombre, lema, badges, CTA.
- Pestañas (Tabs) con las 4 secciones del detalle.
- Sección de preguntas frecuentes con acordeón.
- Botón flotante "volver arriba".
- Pie de página institucional.

El motor kepleriano genera las órbitas de los iconos alrededor
de la imagen central de cada carrera.
"""

import reflex as rx

from app_portada_instein.componentes.barra_navegacion import barra_navegacion_superior
from app_portada_instein.componentes.pie_pagina import pie_pagina_institucional
from app_portada_instein.componentes.primitivos import enlace_navegacion
from app_portada_instein.componentes.secciones_detalle import (
    seccion_informacion,
    seccion_perfil_y_campo_laboral,
    seccion_plan_estudios,
)
from app_portada_instein.dominio.estado_institucional import EstadoInstitucional
from app_portada_instein.infraestructura.constantes_visuales import NOMBRE_INSTITUTO


# ======================================================================
# Constantes de layout
# ======================================================================

MAX_WIDTH_CONTENIDO = "72rem"
MAX_WIDTH_SECCION = "64rem"
PADDING_LATERAL = "1.5rem"

# Colores neutros (consistentes con las otras vistas).
COLOR_TEXTO_PRINCIPAL = rx.color_mode_cond(light="#0f172a", dark="#f1f5f9")
COLOR_TEXTO_SECUNDARIO = rx.color_mode_cond(light="#64748b", dark="#94a3b8")
COLOR_TEXTO_CUERPO = rx.color_mode_cond(light="#475569", dark="#cbd5e1")
COLOR_FONDO_CARTA = rx.color_mode_cond(light="#ffffff", dark="#0f1117")
COLOR_FONDO_SUAVE = rx.color_mode_cond(light="#f8fafc", dark="#1e293b")
COLOR_BORDE_SUAVE = rx.color_mode_cond(light="#e2e8f0", dark="#334155")
COLOR_DIVISOR = rx.color_mode_cond(light="#f1f5f9", dark="#1e293b")


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


def _pestana_trigger(
    texto: str,
    icono: str,
    value: str,
    contador: str | None = None,
) -> rx.Component:
    """
    Trigger (botón) de pestaña con icono + texto + contador opcional.

    Args:
        texto: Etiqueta visible de la pestaña.
        icono: Nombre del icono de Lucide.
        value: Valor único que identifica la pestaña.
        contador: Texto opcional (ej: número de items) que se muestra
            como badge al lado del texto.
    """
    children = [
        rx.icon(icono, size=18),
        rx.text(
            texto,
            font_size="0.875rem",
            font_weight="600",
            white_space="nowrap",
        ),
    ]

    if contador is not None:
        children.append(
            rx.text(
                contador,
                font_size="0.6875rem",
                font_weight="700",
                padding="0.125rem 0.5rem",
                border_radius="9999px",
                background=rx.color_mode_cond(
                    light="#f1f5f9",
                    dark="#1e293b",
                ),
                color=COLOR_TEXTO_SECUNDARIO,
            )
        )

    return rx.tabs.trigger(
        rx.flex(
            *children,
            align="center",
            justify="center",
            gap="0.5rem",
            width="100%",
        ),
        value=value,
        padding="0.75rem 1rem",
        cursor="pointer",
        transition="all 0.2s",
        color=COLOR_TEXTO_SECUNDARIO,
        border_radius="0.75rem",
        _hover={
            "background": rx.color_mode_cond(light="#f8fafc", dark="#334155"),
            "color": COLOR_TEXTO_PRINCIPAL,
        },
        _selected={
            "color": COLOR_TEXTO_PRINCIPAL,
            "background": COLOR_FONDO_CARTA,
            "box_shadow": "0 2px 8px -2px rgb(0 0 0 / 0.08)",
        },
    )


# ======================================================================
# Encabezado sticky con breadcrumb
# ======================================================================


def _encabezado_fijo_detalle() -> rx.Component:
    """
    Encabezado sticky con:
    - Botón de regreso a /carreras.
    - Breadcrumb: Carreras > [Nombre corto].
    - Espaciador a la derecha para balance visual.
    """
    nombre_corto = EstadoInstitucional.carrera_seleccionada["nombre_corto"]

    return rx.box(
        rx.flex(
            # --- Botón de regreso ---
            enlace_navegacion(
                "/carreras",
                rx.icon("arrow-left", size=18),
                rx.text("Volver", font_size="0.8125rem", font_weight="600"),
                color=COLOR_TEXTO_PRINCIPAL,
                padding="0.5rem 0.875rem",
                border_radius="0.75rem",
                background=COLOR_FONDO_CARTA,
                border="1px solid " + COLOR_BORDE_SUAVE,
                display="flex",
                align_items="center",
                gap="0.375rem",
                transition="all 0.2s",
                flex_shrink="0",
                text_decoration="none",
                _hover={
                    "background": COLOR_FONDO_SUAVE,
                    "transform": "translateX(-2px)",
                },
            ),
            # --- Breadcrumb central ---
            rx.flex(
                rx.text(
                    "Carreras",
                    font_size="0.8125rem",
                    color=COLOR_TEXTO_SECUNDARIO,
                ),
                rx.icon(
                    "chevron-right",
                    size=14,
                    color=COLOR_TEXTO_SECUNDARIO,
                ),
                rx.text(
                    nombre_corto,
                    font_size="0.8125rem",
                    font_weight="600",
                    color=COLOR_TEXTO_PRINCIPAL,
                ),
                align="center",
                gap="0.375rem",
                display=rx.breakpoints(initial="none", md="flex"),
            ),
            # --- Espaciador invisible para balance ---
            rx.box(width="6rem", flex_shrink="0"),
            align="center",
            justify="between",
            width="100%",
        ),
        align="center",
        justify="center",
        width="100%",
        padding="0.75rem 1.5rem",
        background=rx.color_mode_cond(
            light="rgba(255,255,255,0.85)",
            dark="rgba(15,17,23,0.85)",
        ),
        backdrop_filter="blur(12px)",
        border_bottom="1px solid " + COLOR_BORDE_SUAVE,
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
    """
    Contenedor cuadrado con:
    - Anillo decorativo exterior (órbita visible).
    - Halo radial con el color de la carrera.
    - 4 iconos orbitando con elipses keplerianas.
    - Imagen central de la carrera con anillo de color.
    """
    carrera = EstadoInstitucional.carrera_seleccionada
    color_principal = carrera["color_principal"]
    color_suave = carrera["color_suave"]

    return rx.box(
        # --- Anillo decorativo exterior ---
        rx.box(
            position="absolute",
            top="5%",
            left="5%",
            right="5%",
            bottom="5%",
            border=f"1px dashed {color_principal}33",
            border_radius="9999px",
            z_index="0",
        ),
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
            width=["10rem", "13rem", "15rem"],
            height=["10rem", "13rem", "15rem"],
            border_radius="9999px",
            border="3px solid " + color_principal,
            box_shadow=f"0 15px 30px -8px {color_principal}80",
            overflow="hidden",
            z_index="10",
            animation="pulso_central 3s ease-in-out infinite",
        ),
        # --- Contenedor ---
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
# Badge informativo reutilizable
# ======================================================================


def _badge_info(
    icono: str,
    texto: str,
    color: str,
    fondo_suave: bool = True,
) -> rx.Component:
    """
    Badge informativo con icono + texto.

    Args:
        icono: Nombre del icono de Lucide.
        texto: Texto visible del badge.
        color: Color principal del badge.
        fondo_suave: Si True, usa un fondo del color con opacidad baja.
    """
    return rx.flex(
        rx.icon(icono, size=12, color=color),
        rx.text(
            texto,
            font_size="0.75rem",
            font_weight="600",
            color=color,
            white_space="nowrap",
        ),
        align="center",
        gap="0.375rem",
        padding="0.375rem 0.75rem",
        border_radius="9999px",
        background=color + "15" if fondo_suave else "transparent",
        border="1px solid " + color + "44",
    )


# ======================================================================
# Hero de carrera
# ======================================================================


def _hero_carrera() -> rx.Component:
    """
    Bloque de presentación principal:
    - Columna izquierda: contenedor orbital con imagen + iconos.
    - Columna derecha: nombre, lema, badges y CTA.
    """
    carrera = EstadoInstitucional.carrera_seleccionada
    color_principal = carrera["color_principal"]

    return rx.flex(
        # --- Columna izquierda: contenedor orbital ---
        rx.box(
            _contenedor_orbital_imagen(),
            width=["100%", "100%", "100%", "40%"],
            flex_shrink="0",
        ),
        # --- Columna derecha: información textual ---
        rx.vstack(
            # --- Badge de categoría con icono decorativo ---
            rx.flex(
                rx.icon("award", size=12, color="#ffffff"),
                rx.text(
                    "TÉCNICO SUPERIOR",
                    font_size="0.625rem",
                    font_weight="800",
                    color="#ffffff",
                    letter_spacing="0.1em",
                ),
                align="center",
                gap="0.375rem",
                background=color_principal,
                padding="0.375rem 0.75rem",
                border_radius="9999px",
                width="fit-content",
                box_shadow=f"0 4px 12px -2px {color_principal}66",
            ),
            # --- Nombre de la carrera ---
            rx.heading(
                carrera["nombre"],
                size="8",
                font_weight="800",
                color=COLOR_TEXTO_PRINCIPAL,
                line_height="1.1",
                text_align="left",
                letter_spacing="-0.025em",
            ),
            # --- Lema ---
            rx.text(
                carrera["lema"],
                font_size="1rem",
                color=COLOR_TEXTO_CUERPO,
                line_height="1.6",
                max_width="36rem",
            ),
            # --- Badges informativos ---
            rx.flex(
                _badge_info("clock", carrera["duracion"], color_principal),
                _badge_info("building-2", carrera["modalidad"], color_principal),
                _badge_info(
                    "users",
                    f"{carrera['cupos_disponibles']} cupos disponibles",
                    "#16a34a",
                ),
                wrap="wrap",
                gap="0.5rem",
                margin_top="0.5rem",
            ),
            # --- CTA de contacto ---
            rx.flex(
                enlace_navegacion(
                    "/contacto",
                    rx.icon("phone-call", size=16, color="#ffffff"),
                    rx.text(
                        "Solicitar información",
                        font_size="0.875rem",
                        font_weight="700",
                        color="#ffffff",
                    ),
                    display="flex",
                    align_items="center",
                    gap="0.5rem",
                    background=color_principal,
                    padding="0.75rem 1.5rem",
                    border_radius="9999px",
                    text_decoration="none",
                    box_shadow=f"0 10px 25px -5px {color_principal}66",
                    transition="all 0.25s cubic-bezier(0.4, 0, 0.2, 1)",
                    _hover={
                        "transform": "translateY(-2px)",
                        "box_shadow": f"0 15px 35px -5px {color_principal}88",
                    },
                ),
                margin_top="1.5rem",
            ),
            align="start",
            spacing="4",
            width=["100%", "100%", "100%", "60%"],
        ),
        width="100%",
        justify="center",
        align="center",
        gap=["2rem", "2.5rem", "3rem", "3rem"],
        padding=["2rem 1.5rem", "2.5rem 1.5rem", "3rem 1.5rem", "3rem 1.5rem"],
        flex_direction=["column", "column", "column", "row"],
    )


# ======================================================================
# Item del acordeón de FAQs
# ======================================================================


def _item_pregunta(pregunta: dict, indice: int) -> rx.Component:
    """Item individual de preguntas frecuentes con acordeón."""
    esta_abierta = EstadoPreguntasFrecuentesDetalle.indice_pregunta_abierta == indice
    color_carrera = EstadoInstitucional.carrera_seleccionada["color_principal"]

    return rx.box(
        # --- Cabecera clicable ---
        rx.box(
            rx.flex(
                # --- Ícono indicador ---
                rx.box(
                    rx.icon(
                        "circle_help",
                        size=16,
                        color=rx.cond(esta_abierta, "#ffffff", color_carrera),
                    ),
                    padding="0.5rem",
                    border_radius="0.5rem",
                    background=rx.cond(
                        esta_abierta,
                        color_carrera,
                        color_carrera + "15",
                    ),
                    display="flex",
                    align_items="center",
                    justify_content="center",
                    flex_shrink="0",
                    transition="all 0.2s",
                ),
                # --- Texto de la pregunta ---
                rx.text(
                    pregunta["pregunta"],
                    font_size="0.9375rem",
                    font_weight="600",
                    color=COLOR_TEXTO_PRINCIPAL,
                    flex="1",
                    line_height="1.4",
                ),
                # --- Chevron indicador ---
                rx.icon(
                    "chevron-down",
                    size=20,
                    color=COLOR_TEXTO_SECUNDARIO,
                    transform=rx.cond(
                        esta_abierta,
                        "rotate(180deg)",
                        "rotate(0deg)",
                    ),
                    transition="transform 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
                    flex_shrink="0",
                ),
                align="center",
                gap="0.75rem",
                width="100%",
            ),
            on_click=lambda: EstadoPreguntasFrecuentesDetalle.alternar_pregunta(indice),
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
                    line_height="1.7",
                    color=COLOR_TEXTO_CUERPO,
                ),
                padding="0 1.25rem 1.25rem 3.5rem",
            ),
            rx.fragment(),
        ),
        # --- Contenedor ---
        width="100%",
        border=rx.cond(
            esta_abierta,
            f"1px solid {color_carrera}66",
            "1px solid " + COLOR_BORDE_SUAVE,
        ),
        border_radius="0.875rem",
        background=COLOR_FONDO_CARTA,
        transition="all 0.2s",
        overflow="hidden",
        _hover={
            "border_color": color_carrera + "66",
            "box_shadow": "0 4px 12px -2px rgb(0 0 0 / 0.05)",
        },
    )


# ======================================================================
# Sección: PREGUNTAS FRECUENTES
# ======================================================================


def _seccion_preguntas_frecuentes() -> rx.Component:
    """Sección completa con las preguntas frecuentes de la carrera."""
    carrera = EstadoInstitucional.carrera_seleccionada
    color_carrera = carrera["color_principal"]

    return rx.vstack(
        # --- Encabezado ---
        rx.flex(
            # --- Icono en caja tintada ---
            rx.box(
                rx.icon("circle_help", size=20, color=color_carrera),
                padding="0.625rem",
                border_radius="0.75rem",
                background=color_carrera + "15",
                border="1px solid " + color_carrera + "20",
                display="flex",
                align_items="center",
                justify_content="center",
                flex_shrink="0",
            ),
            # --- Título + subtítulo ---
            rx.vstack(
                rx.text(
                    "Preguntas frecuentes",
                    font_size="0.9375rem",
                    font_weight="800",
                    color=COLOR_TEXTO_PRINCIPAL,
                    text_transform="uppercase",
                    letter_spacing="0.05em",
                    line_height="1.2",
                ),
                rx.text(
                    "Respuestas a las dudas más comunes de esta carrera.",
                    font_size="0.75rem",
                    color=COLOR_TEXTO_SECUNDARIO,
                    line_height="1.4",
                ),
                spacing="1",
                align="start",
                flex="1",
                min_width="0",
            ),
            # --- Badge contador ---
            rx.box(
                rx.text(
                    carrera["preguntas_frecuentes"].length().to_string(),
                    font_size="0.6875rem",
                    font_weight="700",
                    color=color_carrera,
                    text_transform="uppercase",
                    letter_spacing="0.05em",
                ),
                padding="0.25rem 0.625rem",
                border_radius="9999px",
                background=color_carrera + "15",
                border="1px solid " + color_carrera + "22",
                flex_shrink="0",
            ),
            align="center",
            gap="0.75rem",
            width="100%",
            margin_bottom="1.5rem",
            flex_wrap="wrap",
        ),
        # --- Lista de preguntas ---
        rx.vstack(
            rx.foreach(
                carrera["preguntas_frecuentes"],
                _item_pregunta,
            ),
            width="100%",
            spacing="3",
        ),
        spacing="0",
        width="100%",
        max_width=MAX_WIDTH_SECCION,
        margin="0 auto",
    )


# ======================================================================
# Pestañas de secciones del detalle
# ======================================================================


def _pestanas_secciones_detalle() -> rx.Component:
    """
    Sistema de pestañas con `rx.tabs.root` para las 4 secciones del detalle.

    Estructura:
    - `rx.tabs.list`: contiene los triggers (Info, Plan, Perfil, FAQs).
    - `rx.tabs.content`: contiene el contenido de cada sección.

    El estado de la pestaña activa se gestiona con
    `EstadoInstitucional.seccion_detalle_activa`.
    """
    return rx.tabs.root(
        # --- Lista de triggers ---
        rx.tabs.list(
            _pestana_trigger("Info", "info", value="info"),
            _pestana_trigger("Plan", "book-open-text", value="plan"),
            _pestana_trigger("Perfil", "target", value="perfil"),
            _pestana_trigger(
                "Preguntas",
                "circle_help",
                value="preguntas_frecuentes",
            ),
            width="100%",
            gap="0.25rem",
            background=COLOR_FONDO_SUAVE,
            padding="0.375rem",
            border_radius="1rem",
            border="1px solid " + COLOR_BORDE_SUAVE,
        ),
        # --- Contenido: Info ---
        rx.tabs.content(
            seccion_informacion(),
            margin_top="1.5rem",
            value="info",
        ),
        # --- Contenido: Plan ---
        rx.tabs.content(
            seccion_plan_estudios(),
            margin_top="1.5rem",
            value="plan",
        ),
        # --- Contenido: Perfil ---
        rx.tabs.content(
            seccion_perfil_y_campo_laboral(),
            margin_top="1.5rem",
            value="perfil",
        ),
        # --- Contenido: Preguntas Frecuentes ---
        rx.tabs.content(
            _seccion_preguntas_frecuentes(),
            margin_top="1.5rem",
            value="preguntas_frecuentes",
        ),
        # --- Configuración del root ---
        default_value="info",
        value=EstadoInstitucional.seccion_detalle_activa,
        on_change=EstadoInstitucional.seleccionar_seccion_detalle,
        width="100%",
    )


# ======================================================================
# Botón flotante "volver arriba"
# ======================================================================


def _boton_volver_arriba() -> rx.Component:
    """
    Botón flotante para volver al inicio de la página.

    Útil en vistas largas como el detalle de carrera.
    """
    color_principal = EstadoInstitucional.carrera_seleccionada["color_principal"]

    return rx.box(
        rx.icon(
            "arrow-up",
            size=20,
            color="#ffffff",
        ),
        position="fixed",
        bottom="2rem",
        right="2rem",
        height="3rem",
        width="3rem",
        border_radius="9999px",
        background=color_principal,
        box_shadow=f"0 10px 30px -8px {color_principal}88",
        display=rx.breakpoints(initial="none", md="flex"),
        align_items="center",
        justify_content="center",
        cursor="pointer",
        z_index="40",
        transition="all 0.25s cubic-bezier(0.4, 0, 0.2, 1)",
        on_click=rx.call_script("window.scrollTo({top: 0, behavior: 'smooth'})"),
        _hover={
            "transform": "translateY(-3px)",
            "box_shadow": f"0 15px 40px -8px {color_principal}aa",
        },
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
    - Encabezado sticky con breadcrumb.
    - Hero con contenedor orbital + info textual + CTA.
    - Pestañas (Info, Plan, Perfil, FAQs).
    - Botón flotante "volver arriba".
    - Pie de página institucional.
    """
    return rx.vstack(
        # --- Barra de navegación principal ---
        barra_navegacion_superior(),
        # --- Contenido principal ---
        rx.box(
            # --- Encabezado sticky con breadcrumb ---
            _encabezado_fijo_detalle(),
            # --- Hero con contenedor orbital + info ---
            _hero_carrera(),
            # --- Pestañas de secciones ---
            rx.box(
                _pestanas_secciones_detalle(),
                padding=f"0 {PADDING_LATERAL} 6rem {PADDING_LATERAL}",
                max_width=MAX_WIDTH_CONTENIDO,
                margin="0 auto",
                width="100%",
            ),
            # --- Botón flotante "volver arriba" ---
            _boton_volver_arriba(),
            # --- Contenedor principal ---
            padding_bottom="3rem",
            width="100%",
        ),
        # --- Pie de página ---
        pie_pagina_institucional(),
        # --- Layout del contenedor raíz ---
        align="center",
        min_height="100vh",
        width="100%",
        spacing="0",
    )