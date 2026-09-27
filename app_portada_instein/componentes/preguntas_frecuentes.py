"""
Sección de preguntas frecuentes con estilo acordeón (inspirado en Discord).
"""

import reflex as rx


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
    """Estado del acordeón de preguntas frecuentes."""

    indice_abierto: int = -1  # -1 significa que ninguno está abierto

    @rx.event
    def alternar_pregunta(self, indice: int):
        """Abre o cierra una pregunta."""
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

    Estilo inspirado en Discord: fondo oscuro con bordes sutiles.
    """
    esta_abierta = EstadoPreguntasFrecuentes.indice_abierto == indice

    return rx.box(
        # --- Cabecera clicable ---
        rx.box(
            rx.flex(
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
                    transform=rx.cond(esta_abierta, "rotate(180deg)", "rotate(0deg)"),
                    transition="transform 0.3s",
                ),
                align="center",
                gap="1rem",
                width="100%",
            ),
            on_click=lambda: EstadoPreguntasFrecuentes.alternar_pregunta(indice),
            cursor="pointer",
            padding="1.125rem 1.25rem",
            role="button",
            tab_index=0,  # ⚠️ CORREGIDO: int, no str
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
                padding="0 1.25rem 1.25rem 1.25rem",
            ),
            rx.fragment(),
        ),
        # --- Estilos base ---
        width="100%",
        border=("1px solid " + rx.color_mode_cond(light="#e2e8f0", dark="#1e293b")),
        border_radius="0.875rem",
        background=rx.color_mode_cond(light="#ffffff", dark="#0f1117"),
        transition="all 0.2s",
        _hover={
            "border_color": rx.color_mode_cond(light="#cbd5e1", dark="#334155"),
        },
    )


# ======================================================================
# Sección completa de preguntas frecuentes
# ======================================================================


def seccion_preguntas_frecuentes() -> rx.Component:
    """Sección completa con título + lista de preguntas frecuentes."""
    return rx.box(
        rx.vstack(
            # --- Encabezado ---
            rx.vstack(
                rx.text(
                    "PREGUNTAS FRECUENTES",
                    font_size="0.75rem",
                    font_weight="700",
                    letter_spacing="0.15em",
                    color=rx.color_mode_cond(light="#64748b", dark="#94a3b8"),
                ),
                rx.heading(
                    "¿Tienes dudas?",
                    size="6",
                    color=rx.color_mode_cond(light="#0f172a", dark="#f1f5f9"),
                ),
                rx.text(
                    "Aquí respondemos las preguntas más comunes de nuestros estudiantes.",
                    font_size="0.875rem",
                    color=rx.color_mode_cond(light="#475569", dark="#94a3b8"),
                    text_align="center",
                ),
                align="center",
                spacing="2",
                margin_bottom="2rem",
            ),
            # --- Lista de preguntas ---
            rx.vstack(
                *[_pregunta_frecuente(p, i) for i, p in enumerate(PREGUNTAS_FRECUENTES)],
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
