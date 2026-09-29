"""
Sección de preguntas frecuentes con estilo acordeón (inspirado en Discord).

Este componente se usa en el HOME. La vista de detalle de carrera tiene
su propio acordeón (en `vista_detalle_carrera.py`) porque las preguntas
son específicas por carrera.

Sistema de color (UX)
---------------------
- Fondo de pregunta abierta: tinte suave de accent.
- Icono del chevron: color accent cuando está abierto.
- Textos: neutros (`gray-11`/`gray-12`) para máxima legibilidad.

Diseño:
- Acordeón vertical con una sola pregunta abierta a la vez.
- Cabecera clicable con hover sutil.
- Respuesta colapsable con animación de transición.
"""

import reflex as rx

from app_portada_instein.infraestructura.constantes_visuales import (
    COLOR_ACENTO_BORDE,
    COLOR_ACENTO_FONDO,
    COLOR_ACENTO_TEXTO,
    COLOR_BORDE_HOVER,
    COLOR_BORDE_SUAVE,
    COLOR_FONDO_CARTA,
    COLOR_TEXTO_CUERPO,
    COLOR_TEXTO_PRINCIPAL,
    COLOR_TEXTO_SECUNDARIO,
    RADIO_EXTRA_GRANDE,
    RADIO_MEDIO,
)


# ======================================================================
# Estructura de preguntas frecuentes
# ======================================================================

PREGUNTAS_FRECUENTES: list[dict] = [
    {
        "pregunta": "¿Qué es el INSTEIN?",
        "respuesta": (
            "El Instituto Técnico Integrado San Antonio de Padua (INSTEIN) "
            "es una institución educativa de nivel técnico superior "
            "autorizada por Resolución Ministerial R.M. 0871/2016. "
            "Ofrecemos formación técnica de excelencia en 5 carreras."
        ),
    },
    {
        "pregunta": "¿Cómo puedo inscribirme a una carrera?",
        "respuesta": (
            "Puedes inscribirte presencialmente en nuestras oficinas "
            "ubicadas en la Galería FLOR DE ORO (1er piso), o contactarnos "
            "por WhatsApp al 71282993. El proceso incluye la presentación "
            "de documentos personales y el pago de la matrícula."
        ),
    },
    {
        "pregunta": "¿Cuánto duran las carreras?",
        "respuesta": (
            "Todas nuestras carreras tienen una duración de 3 años "
            "(6 semestres). Al finalizar, los estudiantes obtienen el "
            "título de Técnico Superior en Provisión Nacional."
        ),
    },
    {
        "pregunta": "¿Cuáles son los requisitos de admisión?",
        "respuesta": (
            "Los requisitos son: fotocopia del diploma de bachiller, "
            "fotocopia del carnet de identidad, 2 fotografías tamaño carnet, "
            "y el pago de la matrícula y primera mensualidad."
        ),
    },
    {
        "pregunta": "¿Qué horarios ofrecen?",
        "respuesta": (
            "Ofrecemos turnos de mañana (08:30 - 12:30) y tarde "
            "(14:30 - 18:30). Algunas carreras también tienen turno "
            "nocturno (19:00 - 22:00) para estudiantes que trabajan."
        ),
    },
    {
        "pregunta": "¿Los títulos son válidos para trabajar?",
        "respuesta": (
            "Sí, nuestros títulos son emitidos por el Ministerio de "
            "Educación con validez nacional. Están registrados en el "
            "sistema educativo boliviano y son reconocidos por empleadores."
        ),
    },
]


# ======================================================================
# Estado del acordeón
# ======================================================================


class EstadoPreguntasFrecuentes(rx.State):
    """Estado del acordeón de preguntas frecuentes del home."""

    indice_abierto: int = -1
    """-1 significa que ninguno está abierto."""

    @rx.event
    def alternar_pregunta(self, indice: int):
        """Abre o cierra una pregunta del acordeón."""
        if self.indice_abierto == indice:
            self.indice_abierto = -1
        else:
            self.indice_abierto = indice


# ======================================================================
# Elemento de pregunta individual (acordeón)
# ======================================================================


def _pregunta_frecuente(pregunta: dict, indice: int) -> rx.Component:
    """
    Renderiza una pregunta del acordeón con su respuesta colapsable.

    UX:
    - Icono del chevron gira 180° cuando está abierta.
    - El color del chevron cambia a accent cuando está abierta.
    - La tarjeta completa resalta con borde accent cuando está abierta.
    - Hover: borde gris más marcado.
    """
    esta_abierta = EstadoPreguntasFrecuentes.indice_abierto == indice

    return rx.box(
        # --- Cabecera clicable ---
        rx.box(
            rx.flex(
                # --- Texto de la pregunta ---
                rx.text(
                    pregunta["pregunta"],
                    font_size="0.9375rem",
                    font_weight="600",
                    color=COLOR_TEXTO_PRINCIPAL,
                    flex="1",
                    line_height="1.4",
                ),
                # --- Chevron indicador (color accent cuando abierto) ---
                rx.icon(
                    "chevron-down",
                    size=18,
                    color=rx.cond(
                        esta_abierta,
                        COLOR_ACENTO_TEXTO,
                        COLOR_TEXTO_SECUNDARIO,
                    ),
                    transform=rx.cond(
                        esta_abierta,
                        "rotate(180deg)",
                        "rotate(0deg)",
                    ),
                    transition="transform 0.3s cubic-bezier(0.4, 0, 0.2, 1), color 0.2s",
                    flex_shrink="0",
                ),
                align="center",
                gap="1rem",
                width="100%",
            ),
            on_click=lambda: EstadoPreguntasFrecuentes.alternar_pregunta(indice),
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
                padding="0 1.25rem 1.25rem 1.25rem",
            ),
            rx.fragment(),
        ),
        # --- Estilos base ---
        width="100%",
        border=rx.cond(
            esta_abierta,
            f"1px solid {COLOR_ACENTO_BORDE}",
            f"1px solid {COLOR_BORDE_SUAVE}",
        ),
        border_radius=RADIO_MEDIO,
        background=rx.cond(
            esta_abierta,
            COLOR_ACENTO_FONDO,
            COLOR_FONDO_CARTA,
        ),
        transition="all 0.2s",
        overflow="hidden",
        _hover={
            "border_color": rx.cond(
                esta_abierta,
                COLOR_ACENTO_BORDE,
                COLOR_BORDE_HOVER,
            ),
        },
    )


# ======================================================================
# Sección completa de preguntas frecuentes
# ======================================================================


def seccion_preguntas_frecuentes() -> rx.Component:
    """
    Sección completa con título + lista de preguntas frecuentes.

    Usa tokens Radix adaptativos al color_mode. Los textos son neutros
    y el accent solo se usa como acento en los elementos activos.
    """
    return rx.box(
        rx.vstack(
            # ==========================================================
            # Encabezado
            # ==========================================================
            rx.vstack(
                rx.text(
                    "PREGUNTAS FRECUENTES",
                    font_size="0.75rem",
                    font_weight="700",
                    letter_spacing="0.15em",
                    color=COLOR_ACENTO_TEXTO,  # ← accent para la etiqueta
                ),
                rx.heading(
                    "¿Tienes dudas?",
                    size="6",
                    color=COLOR_TEXTO_PRINCIPAL,
                ),
                rx.text(
                    "Aquí respondemos las preguntas más comunes de nuestros estudiantes.",
                    font_size="0.875rem",
                    color=COLOR_TEXTO_SECUNDARIO,
                    text_align="center",
                    max_width="42rem",
                ),
                align="center",
                spacing="2",
                margin_bottom="2rem",
            ),
            # ==========================================================
            # Lista de preguntas
            # ==========================================================
            rx.vstack(
                *[
                    _pregunta_frecuente(p, i)
                    for i, p in enumerate(PREGUNTAS_FRECUENTES)
                ],
                width="100%",
                max_width="48rem",
                spacing="3",
            ),
            align="center",
            width="100%",
        ),
        width="100%",
        padding="3rem 1.5rem",
    )


__all__ = [
    "EstadoPreguntasFrecuentes",
    "PREGUNTAS_FRECUENTES",
    "seccion_preguntas_frecuentes",
]