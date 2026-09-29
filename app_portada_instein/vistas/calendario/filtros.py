"""
Barra de filtros y ordenamiento del tab 'Actividades del instituto'.
"""

import reflex as rx

from app_portada_instein.infraestructura.constantes_visuales import (
    COLOR_ACENTO_FONDO,
    COLOR_ACENTO_SOLIDO,
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

from .datos import OPCIONES_CARRERA, OPCIONES_ORDEN, OPCIONES_TIPO_EVENTO
from .estado import EstadoCalendario


# ======================================================================
# Etiqueta de grupo
# ======================================================================


def _etiqueta_grupo(texto: str) -> rx.Component:
    """Etiqueta en mayúsculas para encabezar un grupo de filtros."""
    return rx.text(
        texto,
        font_size="0.6875rem",
        font_weight="700",
        color=COLOR_TEXTO_SECUNDARIO,
        text_transform="uppercase",
        letter_spacing="0.075em",
        margin_bottom="0.5rem",
    )


# ======================================================================
# Pill de filtro genérico
# ======================================================================


def _pill_filtro(
    etiqueta: str,
    icono: str,
    activo,
    on_click,
) -> rx.Component:
    """
    Pill de filtro reutilizable.

    Args:
        etiqueta: Texto visible del pill.
        icono: Nombre del icono Lucide.
        activo: Condición (Var o bool) que indica si está activo.
        on_click: Evento a disparar (ya construido con sus argumentos).
    """
    return rx.box(
        rx.flex(
            rx.icon(
                icono,
                size=14,
                color=rx.cond(activo, "white", COLOR_TEXTO_SECUNDARIO),
            ),
            rx.text(
                etiqueta,
                font_size="0.8125rem",
                font_weight="600",
                color=rx.cond(activo, "white", COLOR_TEXTO_CUERPO),
                white_space="nowrap",
            ),
            align="center",
            gap="0.375rem",
        ),
        padding="0.5rem 1rem",
        border_radius=RADIO_PASTILLA,
        background=rx.cond(
            activo,
            COLOR_ACENTO_SOLIDO,
            COLOR_FONDO_SUAVE,
        ),
        border=rx.cond(
            activo,
            f"1px solid {COLOR_ACENTO_SOLIDO}",
            f"1px solid {COLOR_BORDE_SUAVE}",
        ),
        cursor="pointer",
        transition="all 0.2s cubic-bezier(0.4, 0, 0.2, 1)",
        on_click=on_click,
        box_shadow=rx.cond(
            activo,
            f"0 4px 12px -2px {COLOR_ACENTO_SOLIDO}",
            "none",
        ),
        _hover={
            "transform": "translateY(-1px)",
            "background": rx.cond(
                activo,
                COLOR_ACENTO_SOLIDO,
                COLOR_FONDO_CARTA,
            ),
        },
    )


# ======================================================================
# Buscador
# ======================================================================


def _buscador_eventos() -> rx.Component:
    """Input de búsqueda por título, descripción o lugar."""
    return rx.box(
        rx.flex(
            rx.icon(
                "search",
                size=16,
                color=COLOR_TEXTO_SECUNDARIO,
            ),
            rx.input(
                placeholder="Buscar evento por nombre o lugar...",
                value=EstadoCalendario.texto_busqueda,
                on_change=EstadoCalendario.actualizar_busqueda,
                variant="soft",
                size="2",
                width="100%",
                border="none",
                background="transparent",
                _focus={"box_shadow": "none", "outline": "none"},
            ),
            rx.cond(
                EstadoCalendario.texto_busqueda != "",
                rx.box(
                    rx.icon(
                        "x",
                        size=16,
                        color=COLOR_TEXTO_SECUNDARIO,
                    ),
                    padding="0.25rem",
                    border_radius=RADIO_MEDIO,
                    cursor="pointer",
                    on_click=EstadoCalendario.actualizar_busqueda(""),
                    _hover={"background": COLOR_FONDO_SUAVE},
                ),
                rx.fragment(),
            ),
            align="center",
            gap="0.5rem",
            width="100%",
        ),
        width="100%",
        padding="0.5rem 0.875rem",
        border_radius=RADIO_GRANDE,
        background=COLOR_FONDO_CARTA,
        border=f"1px solid {COLOR_BORDE_SUAVE}",
        transition="all 0.2s",
    )


# ======================================================================
# Selector de ordenamiento
# ======================================================================


def _selector_orden() -> rx.Component:
    """
    Selector de ordenamiento con `rx.select`.

    `rx.select` de Radix Themes requiere `rx.select.item` como hijos
    explícitos (NO acepta listas de dicts).
    """
    return rx.box(
        rx.flex(
            rx.icon(
                "arrow-up-down",
                size=14,
                color=COLOR_TEXTO_SECUNDARIO,
            ),
            rx.select.root(
                rx.select.trigger(
                    width="100%",
                    variant="soft",
                    radius="large",
                ),
                rx.select.content(
                    *[
                        rx.select.item(
                            opcion["etiqueta"],
                            value=opcion["valor"],
                        )
                        for opcion in OPCIONES_ORDEN
                    ],
                ),
                value=EstadoCalendario.orden_activo,
                on_change=EstadoCalendario.cambiar_orden,
                width="100%",
            ),
            align="center",
            gap="0.5rem",
            width="100%",
        ),
        width="100%",
        padding="0.25rem 0.5rem",
        border_radius=RADIO_GRANDE,
        background=COLOR_FONDO_CARTA,
        border=f"1px solid {COLOR_BORDE_SUAVE}",
    )


# ======================================================================
# Barra de filtros completa
# ======================================================================


def _barra_filtros() -> rx.Component:
    """
    Barra de filtros completa:
    - Búsqueda por texto.
    - Filtro por carrera (pills).
    - Filtro por tipo de evento (pills).
    - Ordenamiento (selector).
    - Botón "Limpiar filtros" (si hay filtros activos).

    ⚠️ Nota sobre los event handlers:
    En Reflex, cuando quieres pasar argumentos a un evento, se escribe
    directamente `Estado.handler(valor)` en `on_click=`. Reflex lo
    interpreta como "construir este evento con estos argumentos", NO
    como una llamada a función.

    ❌ INCORRECTO:
        on_click=lambda v=opcion["valor"]: Estado.handler(v)
    ✅ CORRECTO:
        on_click=Estado.handler(opcion["valor"])
    """
    return rx.vstack(
        # ==========================================================
        # Búsqueda + orden
        # ==========================================================
        rx.grid(
            _buscador_eventos(),
            _selector_orden(),
            columns=rx.breakpoints(initial="1", md="2"),
            spacing="3",
            width="100%",
        ),
        # ==========================================================
        # Filtro por carrera
        # ==========================================================
        rx.vstack(
            _etiqueta_grupo("Filtrar por carrera"),
            rx.flex(
                *[
                    _pill_filtro(
                        opcion["etiqueta"],
                        opcion["icono"],
                        EstadoCalendario.filtro_carrera == opcion["valor"],
                        # ✅ Pasar el evento construido con argumentos
                        EstadoCalendario.cambiar_filtro_carrera(opcion["valor"]),
                    )
                    for opcion in OPCIONES_CARRERA
                ],
                gap="0.5rem",
                flex_wrap="wrap",
                width="100%",
            ),
            align="start",
            spacing="0",
            width="100%",
        ),
        # ==========================================================
        # Filtro por tipo de evento
        # ==========================================================
        rx.vstack(
            _etiqueta_grupo("Filtrar por tipo"),
            rx.flex(
                *[
                    _pill_filtro(
                        opcion["etiqueta"],
                        opcion["icono"],
                        EstadoCalendario.filtro_tipo == opcion["valor"],
                        # ✅ Pasar el evento construido con argumentos
                        EstadoCalendario.cambiar_filtro_tipo(opcion["valor"]),
                    )
                    for opcion in OPCIONES_TIPO_EVENTO
                ],
                gap="0.5rem",
                flex_wrap="wrap",
                width="100%",
            ),
            align="start",
            spacing="0",
            width="100%",
        ),
        # ==========================================================
        # Resultado + limpiar filtros
        # ==========================================================
        rx.flex(
            rx.flex(
                rx.text(
                    "Resultados:",
                    font_size="0.8125rem",
                    color=COLOR_TEXTO_SECUNDARIO,
                ),
                rx.text(
                    EstadoCalendario.contador_resultados,
                    font_size="0.8125rem",
                    font_weight="700",
                    color=COLOR_ACENTO_TEXTO,
                    padding="0.125rem 0.5rem",
                    background=COLOR_ACENTO_FONDO,
                    border=f"1px solid {COLOR_ACENTO_TEXTO}",
                    border_radius=RADIO_PASTILLA,
                ),
                align="center",
                gap="0.375rem",
            ),
            rx.cond(
                EstadoCalendario.hay_filtros_activos,
                rx.box(
                    rx.flex(
                        rx.icon(
                            "rotate-ccw",
                            size=14,
                            color=COLOR_TEXTO_SECUNDARIO,
                        ),
                        rx.text(
                            "Limpiar filtros",
                            font_size="0.75rem",
                            font_weight="600",
                            color=COLOR_TEXTO_CUERPO,
                        ),
                        align="center",
                        gap="0.375rem",
                    ),
                    padding="0.375rem 0.75rem",
                    border_radius=RADIO_MEDIO,
                    background=COLOR_FONDO_SUAVE,
                    border=f"1px solid {COLOR_BORDE_SUAVE}",
                    cursor="pointer",
                    transition="all 0.2s",
                    on_click=EstadoCalendario.limpiar_filtros,
                    _hover={
                        "background": COLOR_FONDO_CARTA,
                        "border_color": COLOR_ACENTO_TEXTO,
                    },
                ),
                rx.fragment(),
            ),
            align="center",
            justify="between",
            width="100%",
            flex_wrap="wrap",
            gap="0.5rem",
        ),
        spacing="4",
        width="100%",
        margin_bottom="2rem",
    )


__all__ = ["_barra_filtros"]