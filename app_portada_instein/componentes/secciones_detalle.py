"""
Secciones que componen la vista de detalle de una carrera.

Componentes:
- `seccion_informacion`: descripción + datos rápidos + CTA.
- `seccion_plan_estudios`: selector de año + progreso + materias.
- `seccion_perfil_y_campo_laboral`: perfil profesional + campo laboral.

Sistema de color (UX)
---------------------
El ACENTO VISUAL es ÚNICO para todas las carreras: azul marino neon
(`AZUL_MARINO_NEON` = `#3b5bdb`). Se usa de forma SUTIL para decorar:

- Bordes de tarjetas.
- Borde superior grueso de cada tarjeta.
- Hover de tarjetas.
- Barra de progreso del plan de estudios.

TODOS los textos e iconos son NEUTROS (`gray-11`/`gray-12`) para
garantizar legibilidad y elegancia visual.

Sistema de diseño:
- Padding consistente: `PADDING_TARJETA`.
- Border-radius: `RADIO_TARJETA`.
- Hover states: borde tintado + sombra elevada.
- Tipografía: Inter (heredada del tema).

Nota técnica: acento único
--------------------------
El proyecto unificó el acento visual bajo un único azul marino. Los
helpers `color_carrera_adaptativo` y `color_suave_carrera_adaptativo`
fueron eliminados de `constantes_visuales.py`. Este módulo usa
directamente las constantes `AZUL_MARINO_NEON` y `FONDO_AZUL_SUAVE`.
"""

from __future__ import annotations

import reflex as rx

from app_portada_instein.componentes.primitivos import (
    enlace_navegacion,
    tarjeta_informacion_pequena,
)
from app_portada_instein.componentes.tarjetas_carrera import fila_materia
from app_portada_instein.componentes.vinetas import (
    vineta_campo_laboral,
    vineta_perfil_profesional,
)
from app_portada_instein.dominio.estado_institucional import (
    EstadoInstitucional,
    OpcionAnio,
)
from app_portada_instein.infraestructura.constantes_visuales import (
    # Acento único del proyecto
    AZUL_MARINO_NEON,
    FONDO_AZUL_SUAVE,
    # Colores neutros
    COLOR_ACENTO_FONDO,
    COLOR_ACENTO_TEXTO,
    COLOR_BORDE_SUAVE,
    COLOR_DIVISOR,
    COLOR_FONDO_CARTA,
    COLOR_FONDO_SUAVE,
    COLOR_TEXTO_CUERPO,
    COLOR_TEXTO_PRINCIPAL,
    COLOR_TEXTO_SECUNDARIO,
    # Sistema de diseño
    RADIO_EXTRA_GRANDE,
    RADIO_GRANDE,
    RADIO_MEDIO,
    RADIO_PASTILLA,
    SOMBRA_SUAVE,
)


# ======================================================================
# Constantes de diseño
# ======================================================================

PADDING_TARJETA = "1.5rem"
RADIO_TARJETA = "1.25rem"


# ======================================================================
# Helpers de color (delegan en constantes del acento único)
# ======================================================================


def _color_principal() -> str:
    """
    Color principal del acento global (azul marino neon).

    ✅ REFACTORIZADO: ya no depende de la carrera seleccionada. El
    proyecto unificó el acento visual bajo un único azul marino.

    Usado SOLO para bordes, hover y barra de progreso. NO se usa en
    textos ni iconos para mantener legibilidad neutra.

    Returns:
        Hex del azul marino neon (`#3b5bdb`).
    """
    return AZUL_MARINO_NEON


def _color_suave() -> rx.Var:
    """
    Color suave de fondo del acento global.

    ✅ REFACTORIZADO: usa `FONDO_AZUL_SUAVE` (adaptativo light/dark)
    en lugar del color suave de la carrera.

    Returns:
        Var reactiva con el fondo azul marino translúcido, adaptado
        al color_mode actual.
    """
    return FONDO_AZUL_SUAVE


# ======================================================================
# Helpers de estilo (DRY)
# ======================================================================


def _estilo_tarjeta_detalle() -> dict:
    """
    Estilo común para tarjetas de detalle.

    Fondo neutro (`gray-1`), borde neutro sutil (`gray-6`), borde
    superior grueso del acento azul marino, y hover con borde y
    sombra tintados con el acento.

    El borde superior tintado es el toque distintivo que comunica
    "esta tarjeta pertenece al detalle de la carrera" sin recargar
    los textos.
    """
    acento = _color_principal()

    return {
        "padding": PADDING_TARJETA,
        "border_radius": RADIO_TARJETA,
        "background": COLOR_FONDO_CARTA,
        "border": f"1px solid {COLOR_BORDE_SUAVE}",
        "border_top": f"4px solid {acento}",
        "box_shadow": SOMBRA_SUAVE,
        "width": "100%",
        "height": "100%",
        "transition": "all 0.25s cubic-bezier(0.4, 0, 0.2, 1)",
        "_hover": {
            "border_color": acento,
            "box_shadow": f"0 12px 32px -8px {acento}",
            "transform": "translateY(-2px)",
        },
    }


def _badge_contador(texto: str) -> rx.Component:
    """
    Badge pill con el contador de items de una sección.

    Textos e iconos NEUTROS. El borde usa el acento como acento sutil.
    """
    acento = _color_principal()

    return rx.box(
        rx.text(
            texto,
            font_size="0.6875rem",
            font_weight="700",
            color=COLOR_TEXTO_SECUNDARIO,
            text_transform="uppercase",
            letter_spacing="0.05em",
            white_space="nowrap",
        ),
        padding="0.25rem 0.625rem",
        border_radius=RADIO_PASTILLA,
        background=COLOR_FONDO_SUAVE,
        border=f"1px solid {acento}",
        flex_shrink="0",
    )


def _encabezado_seccion(
    icono: str,
    titulo: str,
    subtitulo: str | None = None,
    badge: str | None = None,
) -> rx.Component:
    """
    Encabezado consistente para las secciones del detalle.

    Estructura:
    - Icono en caja neutra (izquierda).
    - Título + subtítulo (centro).
    - Badge opcional (derecha).

    Args:
        icono: Nombre del icono de Lucide.
        titulo: Título principal de la sección.
        subtitulo: Texto opcional debajo del título.
        badge: Texto opcional para un badge a la derecha.
    """
    hijos = [
        # --- Icono en caja neutra ---
        rx.box(
            rx.icon(icono, size=20, color=COLOR_TEXTO_SECUNDARIO),
            padding="0.625rem",
            border_radius=RADIO_MEDIO,
            background=COLOR_FONDO_SUAVE,
            border=f"1px solid {COLOR_BORDE_SUAVE}",
            display="flex",
            align_items="center",
            justify_content="center",
            flex_shrink="0",
        ),
        # --- Título + subtítulo ---
        rx.vstack(
            rx.text(
                titulo,
                font_size="0.9375rem",
                font_weight="800",
                color=COLOR_TEXTO_PRINCIPAL,
                text_transform="uppercase",
                letter_spacing="0.05em",
                line_height="1.2",
            ),
            *(
                [
                    rx.text(
                        subtitulo,
                        font_size="0.75rem",
                        color=COLOR_TEXTO_SECUNDARIO,
                        line_height="1.4",
                    )
                ]
                if subtitulo
                else []
            ),
            spacing="1",
            align="start",
            flex="1",
            min_width="0",
        ),
    ]

    if badge is not None:
        hijos.append(_badge_contador(badge))

    return rx.flex(
        *hijos,
        align="center",
        gap="0.75rem",
        width="100%",
        margin_bottom="1.25rem",
        flex_wrap="wrap",
    )


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


def _cta_contacto(color_principal: str) -> rx.Component:
    """
    Bloque CTA de contacto con icono, texto y flecha.

    El fondo usa el COLOR DEL ACENTO (decorativo, texto blanco
    garantiza contraste WCAG en ambos modos).

    Args:
        color_principal: Color hex del fondo del CTA.
    """
    return enlace_navegacion(
        "/contacto",
        rx.flex(
            # --- Icono grande ---
            rx.box(
                rx.icon("phone-call", size=26, color="white"),
                padding="1rem",
                border_radius=RADIO_GRANDE,
                background="rgba(255,255,255,0.15)",
                border="1px solid rgba(255,255,255,0.2)",
                display="flex",
                align_items="center",
                justify_content="center",
                flex_shrink="0",
            ),
            # --- Texto ---
            rx.vstack(
                rx.flex(
                    rx.text(
                        "¿Interesado en esta carrera?",
                        font_size="1rem",
                        font_weight="800",
                        color="white",
                        line_height="1.3",
                    ),
                    rx.box(
                        rx.flex(
                            rx.box(
                                width="0.375rem",
                                height="0.375rem",
                                border_radius=RADIO_PASTILLA,
                                background=rx.color("green", 8),
                                animation="pulse 2s ease-in-out infinite",
                            ),
                            rx.text(
                                "Inscripciones abiertas",
                                font_size="0.625rem",
                                font_weight="800",
                                color="white",
                                letter_spacing="0.075em",
                            ),
                            align="center",
                            gap="0.375rem",
                        ),
                        padding="0.25rem 0.625rem",
                        border_radius=RADIO_PASTILLA,
                        background="rgba(255,255,255,0.2)",
                    ),
                    align="center",
                    gap="0.5rem",
                    flex_wrap="wrap",
                ),
                rx.text(
                    "Contáctanos para recibir más información y conocer el "
                    "proceso de inscripción.",
                    font_size="0.8125rem",
                    color="rgba(255,255,255,0.9)",
                    line_height="1.5",
                ),
                spacing="2",
                align="start",
                flex="1",
            ),
            # --- Flecha ---
            rx.box(
                rx.icon("arrow-right", size=20, color="white"),
                padding="0.5rem",
                border_radius=RADIO_PASTILLA,
                background="rgba(255,255,255,0.15)",
                display="flex",
                align_items="center",
                justify_content="center",
                flex_shrink="0",
                transition="transform 0.2s",
            ),
            align="center",
            gap="1rem",
            width="100%",
        ),
        background=color_principal,
        padding="1.25rem 1.5rem",
        border_radius=RADIO_TARJETA,
        box_shadow=f"0 10px 25px -5px {color_principal}",
        transition="all 0.25s cubic-bezier(0.4, 0, 0.2, 1)",
        text_decoration="none",
        width="100%",
        _hover={
            "transform": "translateY(-3px)",
            "box_shadow": f"0 20px 45px -8px {color_principal}",
        },
    )


def seccion_informacion() -> rx.Component:
    """
    Sección de información general de la carrera:

    1. Descripción larga con encabezado.
    2. Grid de 4 datos rápidos (duración, título, modalidad, cupos).
    3. CTA grande de contacto (comentado por defecto).
    """
    return rx.vstack(
        # =============================================================
        # 1. Descripción
        # =============================================================
        rx.box(
            _encabezado_seccion(
                "info",
                "Descripción de la carrera",
                "Información general y objetivos del programa.",
            ),
            rx.text(
                EstadoInstitucional.carrera_seleccionada["descripcion"],
                font_size="0.9375rem",
                line_height="1.75",
                color=COLOR_TEXTO_CUERPO,
            ),
            **_estilo_tarjeta_detalle(),
        ),
        # =============================================================
        # 2. Grid de datos rápidos (iconos NEUTROS)
        # =============================================================
        rx.grid(
            tarjeta_informacion_pequena(
                icono="clock",
                titulo="Duración",
                valor=EstadoInstitucional.carrera_seleccionada["duracion"],
                color_icono=COLOR_TEXTO_SECUNDARIO,
            ),
            tarjeta_informacion_pequena(
                icono="award",
                titulo="Título",
                valor="Técnico Superior",
                color_icono=COLOR_TEXTO_SECUNDARIO,
            ),
            tarjeta_informacion_pequena(
                icono="building-2",
                titulo="Modalidad",
                valor=EstadoInstitucional.carrera_seleccionada["modalidad"],
                color_icono=COLOR_TEXTO_SECUNDARIO,
            ),
            tarjeta_informacion_pequena(
                icono="users",
                titulo="Cupos",
                valor=(
                    f"{EstadoInstitucional.carrera_seleccionada['cupos_disponibles']} "
                    f"disponibles"
                ),
                color_icono=COLOR_TEXTO_SECUNDARIO,
            ),
            columns=rx.breakpoints(initial="1", sm="2", lg="4"),
            spacing="3",
            width="100%",
        ),
        # =============================================================
        # 3. CTA de contacto (descomentar si se quiere mostrar)
        # =============================================================
        # _cta_contacto(_color_principal()),
        spacing="4",
        width="100%",
    )


# ======================================================================
# Sección: PLAN DE ESTUDIOS
# ======================================================================


def _opcion_anio_segmento(opcion: OpcionAnio) -> rx.Component:
    """
    Renderiza un item del selector segmentado de años.

    Args:
        opcion: Dict con `etiqueta` y `valor` del año.
    """
    return rx.segmented_control.item(
        opcion["etiqueta"],
        value=opcion["valor"],
    )


def _barra_progreso_plan() -> rx.Component:
    """
    Barra de progreso del plan de estudios.

    Usa el COLOR DEL ACENTO para el relleno de la barra. Es el único
    elemento decorativo con color dentro del header del año.
    """
    total_anios = (
        EstadoInstitucional.carrera_seleccionada["plan_estudios"].length()
    )
    anio_actual = EstadoPlanEstudios.indice_anio_actual + 1

    # Cálculo del porcentaje como Var compatible.
    porcentaje = (anio_actual * 100 / total_anios).to_string() + "%"

    return rx.flex(
        # --- Texto de progreso ---
        rx.text(
            "Año "
            + anio_actual.to_string()
            + " de "
            + total_anios.to_string(),
            font_size="0.75rem",
            font_weight="700",
            color=COLOR_TEXTO_SECUNDARIO,
            flex_shrink="0",
            white_space="nowrap",
        ),
        # --- Barra con acento ---
        rx.box(
            rx.box(
                width=porcentaje,
                height="100%",
                background=_color_principal(),
                border_radius=RADIO_PASTILLA,
                transition="width 0.35s cubic-bezier(0.4, 0, 0.2, 1)",
            ),
            height="0.375rem",
            flex="1",
            background=COLOR_DIVISOR,
            border_radius=RADIO_PASTILLA,
            overflow="hidden",
        ),
        align="center",
        gap="0.75rem",
        width="100%",
        margin_bottom="1.5rem",
    )


def seccion_plan_estudios() -> rx.Component:
    """
    Sección con el plan de estudios dividido por años.

    Estructura:
    1. Encabezado + Selector segmentado.
    2. Contenido del año: barra de progreso + header + materias.
    """
    plan_actual = EstadoInstitucional.carrera_seleccionada["plan_estudios"][
        EstadoPlanEstudios.indice_anio_actual
    ]

    return rx.vstack(
        # =============================================================
        # 1. Encabezado + Selector
        # =============================================================
        rx.box(
            _encabezado_seccion(
                "book-open-text",
                "Plan de estudios",
                "Selecciona el año para ver las materias correspondientes.",
            ),
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
            width="100%",
        ),
        # =============================================================
        # 2. Contenido del año seleccionado
        # =============================================================
        rx.box(
            # --- Barra de progreso (con acento) ---
            _barra_progreso_plan(),
            # --- Header del año (icono NEUTRO) ---
            rx.flex(
                rx.vstack(
                    rx.text(
                        plan_actual["anio"],
                        font_size="1.5rem",
                        font_weight="800",
                        color=COLOR_TEXTO_PRINCIPAL,
                        line_height="1.15",
                        letter_spacing="-0.02em",
                    ),
                    rx.flex(
                        rx.icon(
                            "book-open",
                            size=12,
                            color=COLOR_TEXTO_SECUNDARIO,
                        ),
                        rx.text(
                            plan_actual["materias"].length().to_string()
                            + " materias",
                            font_size="0.8125rem",
                            font_weight="500",
                            color=COLOR_TEXTO_SECUNDARIO,
                        ),
                        align="center",
                        gap="0.375rem",
                    ),
                    spacing="1",
                    align="start",
                ),
                rx.box(
                    rx.icon(
                        "graduation-cap",
                        size=36,
                        color=COLOR_TEXTO_SECUNDARIO,
                    ),
                    padding="0.875rem",
                    border_radius=RADIO_GRANDE,
                    background=COLOR_FONDO_SUAVE,
                    border=f"1px solid {COLOR_BORDE_SUAVE}",
                    display="flex",
                    align_items="center",
                    justify_content="center",
                    flex_shrink="0",
                ),
                align="center",
                justify="between",
                width="100%",
                margin_bottom="1.5rem",
                padding_bottom="1.5rem",
                border_bottom=f"1px solid {COLOR_DIVISOR}",
                flex_wrap="wrap",
                gap="1rem",
            ),
            # --- Lista de materias ---
            rx.vstack(
                rx.foreach(
                    plan_actual["materias"],
                    fila_materia,
                ),
                gap="0.5rem",
                width="100%",
            ),
            **_estilo_tarjeta_detalle(),
        ),
        spacing="4",
        width="100%",
    )


# ======================================================================
# Sección: PERFIL Y CAMPO LABORAL
# ======================================================================


def _tarjeta_lista(
    icono: str,
    titulo: str,
    subtitulo: str,
    items,
    render_item,
    badge: str | None = None,
) -> rx.Component:
    """
    Tarjeta genérica para listas (perfil, campo laboral).

    Args:
        icono: Nombre del icono de Lucide.
        titulo: Título de la sección.
        subtitulo: Subtítulo descriptivo.
        items: Lista del estado con los items a renderizar.
        render_item: Función que renderiza cada item.
        badge: Texto opcional para un badge a la derecha.
    """
    return rx.box(
        _encabezado_seccion(icono, titulo, subtitulo, badge),
        rx.vstack(
            rx.foreach(items, render_item),
            gap="0.75rem",
            width="100%",
        ),
        **_estilo_tarjeta_detalle(),
    )


def seccion_perfil_y_campo_laboral() -> rx.Component:
    """
    Sección con dos columnas:

    - **Perfil Profesional**: habilidades y competencias.
    - **Campo Laboral**: dónde puede trabajar el egresado.

    Usa un grid responsive que colapsa a 1 columna en móvil.
    """
    carrera = EstadoInstitucional.carrera_seleccionada

    return rx.grid(
        # =============================================================
        # Columna 1: Perfil Profesional
        # =============================================================
        _tarjeta_lista(
            icono="user-check",
            titulo="Perfil profesional",
            subtitulo="Competencias que desarrollarás durante la carrera.",
            badge=f"{carrera['perfil_profesional'].length()} habilidades",
            items=carrera["perfil_profesional"],
            render_item=vineta_perfil_profesional,
        ),
        # =============================================================
        # Columna 2: Campo Laboral
        # =============================================================
        _tarjeta_lista(
            icono="building-2",
            titulo="Campo laboral",
            subtitulo="Dónde podrás trabajar al egresar.",
            badge=f"{carrera['campo_laboral'].length()} opciones",
            items=carrera["campo_laboral"],
            render_item=vineta_campo_laboral,
        ),
        columns=rx.breakpoints(initial="1", md="2"),
        spacing="4",
        width="100%",
        align_items="stretch",
    )


__all__ = [
    "seccion_informacion",
    "seccion_perfil_y_campo_laboral",
    "seccion_plan_estudios",
]