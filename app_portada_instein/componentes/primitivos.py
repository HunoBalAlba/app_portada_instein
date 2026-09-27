"""
Componentes primitivos reutilizables en toda la aplicación.
"""

import reflex as rx

from ..infraestructura.constantes_visuales import (
    RADIO_EXTRA_GRANDE,
    SOMBRA_SUAVE,
)


def contenedor_clicable(*hijos, al_hacer_clic=None, **propiedades) -> rx.Component:
    """Contenedor que actúa como botón para eventos internos."""
    return rx.box(
        *hijos,
        on_click=al_hacer_clic,
        cursor="pointer",
        role="button",
        **propiedades,
    )


def enlace_navegacion(destino: str, *hijos, **propiedades) -> rx.Component:
    """
    Enlace de navegación entre páginas (URLs reales).

    Aplica `text_decoration="none"` y `cursor="pointer"` por defecto,
    pero permite sobrescribirlos sin duplicar kwargs.
    """
    # Valores por defecto que el llamador puede sobrescribir
    propiedades.setdefault("text_decoration", "none")
    propiedades.setdefault("cursor", "pointer")

    return rx.link(
        *hijos,
        href=destino,
        **propiedades,
    )


def tarjeta_estilizada(*hijos, **propiedades) -> rx.Component:
    """Tarjeta con estilo institucional estándar."""
    propiedades.setdefault("padding", "1.25rem")
    propiedades.setdefault("border_radius", RADIO_EXTRA_GRANDE)
    propiedades.setdefault("border", f"1px solid {rx.color('accent', 8)}")
    propiedades.setdefault("box_shadow", SOMBRA_SUAVE)

    return rx.box(*hijos, **propiedades)


def tarjeta_informacion_pequena(
    icono: str,
    titulo: str,
    valor: str,
    color_icono: str,
) -> rx.Component:
    """Tarjeta compacta con icono + título + valor (usada en detalle)."""
    return rx.card(
        rx.hstack(
            rx.box(
                rx.box(
                    rx.icon(icono, size=16, color=color_icono),
                    padding="0.5rem",
                    background=rx.color("accent", 3),
                    border_radius="0.5rem",
                    width="fit-content",
                    margin_bottom="0.5rem",
                    display="flex",
                ),
                rx.heading(
                    titulo,
                    size="1",
                    color_scheme="gray",
                    text_transform="uppercase",
                ),
                rx.heading(valor, size="1"),
            ),
        ),
        width="100%",
    )