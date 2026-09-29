"""
Ensamblador de los tabs del Calendario Académico.
"""

import reflex as rx

from app_portada_instein.infraestructura.constantes_visuales import (
    RADIO_EXTRA_GRANDE,
)

from .tabs_fechas import tab_fechas_importantes
from .tabs_instituto import tab_actividades_instituto


def tabs_calendario() -> rx.Component:
    """
    Tabs con dos pestañas:
    - "Actividades del instituto": timeline con eventos.
    - "Fechas importantes": feriados y días especiales de Bolivia.
    """
    return rx.tabs.root(
        # ==========================================================
        # Lista de triggers
        # ==========================================================
        rx.tabs.list(
            rx.tabs.trigger(
                rx.icon("calendar-check", size=16),
                rx.text("Actividades del instituto"),
                value="actividades",
                font_size="0.875rem",
                font_weight="600",
            ),
            rx.tabs.trigger(
                rx.icon("flag", size=16),
                rx.text("Fechas importantes"),
                value="fechas",
                font_size="0.875rem",
                font_weight="600",
            ),
            width="100%",
            gap="0.25rem",
            padding="0.375rem",
            border_radius=RADIO_EXTRA_GRANDE,
        ),
        # ==========================================================
        # Contenido: Actividades del instituto
        # ==========================================================
        rx.tabs.content(
            tab_actividades_instituto(),
            margin_top="2rem",
            value="actividades",
        ),
        # ==========================================================
        # Contenido: Fechas importantes
        # ==========================================================
        rx.tabs.content(
            tab_fechas_importantes(),
            margin_top="2rem",
            value="fechas",
        ),
        default_value="actividades",
        width="100%",
    )


__all__ = ["tabs_calendario"]