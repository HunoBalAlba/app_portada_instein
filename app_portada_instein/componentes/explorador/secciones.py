"""
Grids de contenido dinámico del explorador:
- Info: descripción + datos rápidos.
- Plan: años + materias.
- Perfil: habilidades.
- Campo: salidas laborales.
- FAQ: acordeón de preguntas frecuentes.
"""

import reflex as rx

from app_portada_instein.componentes.primitivos import contenedor_clicable
from app_portada_instein.dominio.estado_institucional import EstadoInstitucional
from app_portada_instein.infraestructura.constantes_visuales import (
    ANCHO_SECCION,
    COLOR_ACENTO_BORDE,
    COLOR_ACENTO_FONDO,
    COLOR_ACENTO_TEXTO,
    COLOR_BORDE_SUAVE,
    COLOR_FONDO_CARTA,
    COLOR_FONDO_SUAVE,
    COLOR_TEXTO_CUERPO,
    COLOR_TEXTO_PRINCIPAL,
    COLOR_TEXTO_SECUNDARIO,
    RADIO_GRANDE,
    RADIO_MEDIO,
    RADIO_PASTILLA,
)

from .helpers import (
    color_carrera,
    color_carrera_destacada,
    color_suave_carrera_destacada,
)


# ======================================================================
# CARD GENÉRICA DE CONTENIDO
# ======================================================================


def _card_explorador(
    titulo: str,
    descripcion: str,
    icono: str = "circle-dot",
) -> rx.Component:
    """
    Card individual estilo "Featured".

    UX:
    - Icono con fondo suave del color de carrera.
    - Hover: borde + sombra del color de carrera.
    """
    color = color_carrera_destacada()
    color_suave = color_suave_carrera_destacada()

    return rx.box(
        rx.vstack(
            rx.flex(
                rx.icon(icono, size=20, color=color),
                height="2.5rem",
                width="2.5rem",
                border_radius=RADIO_MEDIO,
                background=color_suave,
                border=f"1px solid {color}",
                align="center",
                justify="center",
                margin_bottom="0.75rem",
            ),
            rx.heading(
                titulo,
                size="3",
                font_weight="700",
                color=COLOR_TEXTO_PRINCIPAL,
                line_height="1.3",
            ),
            rx.text(
                descripcion,
                font_size="0.8125rem",
                color=COLOR_TEXTO_SECUNDARIO,
                line_height="1.5",
            ),
            align="start",
            spacing="1",
            width="100%",
        ),
        padding="1.25rem",
        border_radius=RADIO_GRANDE,
        background=COLOR_FONDO_CARTA,
        border=f"1px solid {COLOR_BORDE_SUAVE}",
        width="100%",
        transition="all 0.2s",
        _hover={
            "transform": "translateY(-4px)",
            "border_color": color,
            "box_shadow": f"0 15px 30px -10px {color}",
        },
    )


# ======================================================================
# CONTADOR DE ITEMS
# ======================================================================


def _contador_items(texto: str, cantidad) -> rx.Component:
    """
    Contador con etiqueta y badge numérico en accent.

    Args:
        texto: Texto descriptivo (ej: "Materias del año:").
        cantidad: Var de cantidad (con .length() o .to_string()).
    """
    return rx.flex(
        rx.text(
            texto,
            font_size="0.875rem",
            color=COLOR_TEXTO_SECUNDARIO,
        ),
        rx.text(
            cantidad,
            font_size="0.875rem",
            font_weight="700",
            color=COLOR_ACENTO_TEXTO,
            padding="0.125rem 0.5rem",
            background=COLOR_ACENTO_FONDO,
            border=f"1px solid {COLOR_ACENTO_BORDE}",
            border_radius=RADIO_PASTILLA,
        ),
        align="center",
        gap="0.5rem",
        margin_bottom="1.5rem",
    )


# ======================================================================
# SECCIÓN: INFORMACIÓN
# ======================================================================


def _grid_info() -> rx.Component:
    """Grid con la información completa de la carrera."""
    carrera = EstadoInstitucional.carrera_destacada
    color = color_carrera(carrera)

    return rx.vstack(
        # --- Descripción ---
        rx.box(
            rx.vstack(
                rx.flex(
                    rx.icon("file-text", size=22, color=color),
                    rx.heading(
                        "Descripción de la Carrera",
                        size="4",
                        color=COLOR_TEXTO_PRINCIPAL,
                    ),
                    align="center",
                    gap="0.5rem",
                    margin_bottom="0.75rem",
                ),
                rx.text(
                    carrera["descripcion"],
                    font_size="0.9375rem",
                    line_height="1.7",
                    color=COLOR_TEXTO_CUERPO,
                ),
                align="start",
                spacing="2",
                width="100%",
            ),
            padding="1.5rem",
            border_radius=RADIO_GRANDE,
            background=COLOR_FONDO_CARTA,
            border=f"1px solid {color}",
            width="100%",
            margin_bottom="1rem",
        ),
        # --- Grid de datos rápidos ---
        rx.grid(
            _card_explorador(
                "Duración",
                f"{carrera['duracion']} · 6 semestres",
                "clock",
            ),
            _card_explorador(
                "Título",
                "Técnico Superior en Provisión Nacional",
                "award",
            ),
            _card_explorador(
                "Certificación",
                "Resolución Ministerial R.M. 0871/2016",
                "shield-check",
            ),
            _card_explorador(
                "Modalidad",
                "Presencial · Turnos mañana, tarde y noche",
                "building-2",
            ),
            _card_explorador(
                "Ubicación",
                "Galería FLOR DE ORO - 1er piso",
                "map-pin",
            ),
            _card_explorador(
                "Contacto",
                "WhatsApp: 71282993 · Tel: 79104232",
                "phone",
            ),
            columns=rx.breakpoints(initial="1", sm="2", lg="2"),
            spacing="4",
            width="100%",
        ),
        spacing="0",
        width="100%",
        max_width=ANCHO_SECCION,
        margin="0 auto",
    )


# ======================================================================
# SECCIÓN: PLAN DE ESTUDIOS
# ======================================================================


def _pastilla_anio_explorador(anio: dict, indice: int) -> rx.Component:
    """
    Pastilla seleccionable para elegir el año del plan.

    UX:
    - Activa: fondo sólido del color de carrera + texto blanco.
    - Inactiva: fondo neutro + borde sutil.
    """
    esta_activo = EstadoInstitucional.indice_anio_explorador == indice
    color = color_carrera_destacada()

    return contenedor_clicable(
        rx.text(anio["anio"], size="2"),
        al_hacer_clic=lambda: EstadoInstitucional.seleccionar_anio_explorador(
            indice
        ),
        padding="0.625rem 1.125rem",
        border_radius=RADIO_MEDIO,
        background=rx.cond(esta_activo, color, COLOR_FONDO_SUAVE),
        color=rx.cond(esta_activo, "white", COLOR_TEXTO_CUERPO),
        border=rx.cond(
            esta_activo,
            f"1px solid {color}",
            f"1px solid {COLOR_BORDE_SUAVE}",
        ),
        box_shadow=rx.cond(
            esta_activo,
            f"0 4px 12px -2px {color}",
            "none",
        ),
        font_weight="600",
        white_space="nowrap",
        display="inline-flex",
        align_items="center",
        transition="all 0.2s",
    )


def _grid_plan() -> rx.Component:
    """Grid con el plan de estudios agrupado por año."""
    carrera = EstadoInstitucional.carrera_destacada
    color = color_carrera(carrera)

    return rx.vstack(
        # --- Encabezado + selector de año ---
        rx.box(
            rx.flex(
                rx.icon("book-open", size=20, color=color),
                rx.heading(
                    "Plan de Estudios",
                    size="4",
                    color=COLOR_TEXTO_PRINCIPAL,
                ),
                align="center",
                gap="0.5rem",
                margin_bottom="1rem",
            ),
            rx.flex(
                rx.foreach(
                    carrera["plan_estudios"],
                    _pastilla_anio_explorador,
                ),
                gap="0.5rem",
                flex_wrap="wrap",
                margin_bottom="1rem",
            ),
            width="100%",
        ),
        # --- Contador de materias ---
        _contador_items(
            "Materias del año: ",
            EstadoInstitucional.materias_anio_explorador.length().to_string(),
        ),
        # --- Grid de materias ---
        rx.grid(
            rx.foreach(
                EstadoInstitucional.materias_anio_explorador,
                lambda materia, idx: _card_explorador(
                    f"Materia {idx + 1}",
                    materia,
                    "book-open",
                ),
            ),
            columns=rx.breakpoints(initial="1", sm="2", lg="3"),
            spacing="3",
            width="100%",
        ),
        spacing="0",
        width="100%",
        max_width=ANCHO_SECCION,
        margin="0 auto",
    )


# ======================================================================
# SECCIÓN: PERFIL PROFESIONAL
# ======================================================================


def _grid_perfil() -> rx.Component:
    """Grid con el perfil profesional."""
    return rx.grid(
        rx.foreach(
            EstadoInstitucional.perfil_carrera_destacada,
            lambda item, idx: _card_explorador(
                f"Habilidad {idx + 1}",
                item,
                "check-circle",
            ),
        ),
        columns=rx.breakpoints(initial="1", sm="2", lg="2"),
        spacing="3",
        width="100%",
        max_width=ANCHO_SECCION,
        margin="0 auto",
    )


# ======================================================================
# SECCIÓN: CAMPO LABORAL
# ======================================================================


def _grid_campo() -> rx.Component:
    """Grid con el campo laboral."""
    return rx.grid(
        rx.foreach(
            EstadoInstitucional.campo_carrera_destacada,
            lambda item, idx: _card_explorador(
                f"Salida {idx + 1}",
                item,
                "briefcase",
            ),
        ),
        columns=rx.breakpoints(initial="1", sm="2", lg="2"),
        spacing="3",
        width="100%",
        max_width=ANCHO_SECCION,
        margin="0 auto",
    )


# ======================================================================
# SECCIÓN: FAQ
# ======================================================================


class EstadoFAQ(rx.State):
    """Estado del acordeón de FAQ del explorador."""

    indice_faq_abierto: int = -1

    @rx.event
    def alternar_faq(self, indice: int):
        """Abre o cierra una pregunta del FAQ."""
        if self.indice_faq_abierto == indice:
            self.indice_faq_abierto = -1
        else:
            self.indice_faq_abierto = indice


def _item_faq_explorador(pregunta: dict, indice: int) -> rx.Component:
    """
    Item individual del FAQ con acordeón.

    UX:
    - Icono del chevron: neutro (no cambia de color).
    - Borde: color de carrera cuando abierto.
    - Hover: borde del color de carrera.
    """
    esta_abierta = EstadoFAQ.indice_faq_abierto == indice
    color = color_carrera_destacada()

    return rx.box(
        # --- Cabecera clicable ---
        rx.box(
            rx.flex(
                rx.icon(
                    "help-circle",
                    size=18,
                    color=color,
                    flex_shrink="0",
                ),
                rx.text(
                    pregunta["pregunta"],
                    font_size="0.9375rem",
                    font_weight="600",
                    color=COLOR_TEXTO_PRINCIPAL,
                    flex="1",
                ),
                rx.icon(
                    "chevron-down",
                    size=18,
                    color=COLOR_TEXTO_SECUNDARIO,
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
            on_click=lambda: EstadoFAQ.alternar_faq(indice),
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
                    color=COLOR_TEXTO_CUERPO,
                ),
                padding="0 1.25rem 1.25rem 3.25rem",
            ),
            rx.fragment(),
        ),
        # --- Contenedor ---
        width="100%",
        border=rx.cond(
            esta_abierta,
            f"1px solid {color}",
            f"1px solid {COLOR_BORDE_SUAVE}",
        ),
        border_radius=RADIO_MEDIO,
        background=COLOR_FONDO_CARTA,
        transition="all 0.2s",
        _hover={"border_color": color},
    )


def _grid_faq() -> rx.Component:
    """Grid con preguntas frecuentes específicas de la carrera."""
    return rx.vstack(
        # --- Contador de preguntas ---
        _contador_items(
            "Preguntas frecuentes de esta carrera",
            EstadoInstitucional.preguntas_frecuentes_carrera_destacada.length().to_string(),
        ),
        # --- Lista de preguntas ---
        rx.vstack(
            rx.foreach(
                EstadoInstitucional.preguntas_frecuentes_carrera_destacada,
                _item_faq_explorador,
            ),
            width="100%",
            spacing="3",
        ),
        spacing="0",
        width="100%",
        max_width=ANCHO_SECCION,
        margin="0 auto",
    )


# ======================================================================
# CONTENIDO DINÁMICO
# ======================================================================


def _contenido_explorador() -> rx.Component:
    """Renderiza el contenido dinámico según la sección activa."""
    return rx.box(
        rx.match(
            EstadoInstitucional.seccion_explorador_activa,
            ("info", _grid_info()),
            ("plan", _grid_plan()),
            ("perfil", _grid_perfil()),
            ("campo", _grid_campo()),
            ("faq", _grid_faq()),
            _grid_info(),
        ),
        width="100%",
        min_height="20rem",
    )


__all__ = [
    "EstadoFAQ",
    "_contenido_explorador",
    "_grid_campo",
    "_grid_faq",
    "_grid_info",
    "_grid_perfil",
    "_grid_plan",
]