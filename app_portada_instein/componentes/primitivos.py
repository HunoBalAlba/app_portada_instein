"""
Componentes primitivos reutilizables en toda la aplicación.

Usa las constantes de `styles.py` para mantener consistencia visual
(bordes, radios, sombras, colores de acento, etc.).
"""

import reflex as rx

from app_portada_instein.styles import (
    BORDE_PREDETERMINADO,
    COLOR_FONDO_ACENTO,
    RADIO_BORDE,
    SOMBRA_CAJA,
)


# ======================================================================
# Contenedor clicable (botón semántico)
# ======================================================================


def contenedor_clicable(*hijos, al_hacer_clic=None, **propiedades) -> rx.Component:
    """
    Contenedor que actúa como botón para eventos internos.

    Aplica `cursor="pointer"`, `role="button"` y `tab_index=0` por defecto,
    pero permite sobrescribir cualquier propiedad sin duplicar kwargs.
    """
    propiedades.setdefault("cursor", "pointer")
    propiedades.setdefault("role", "button")
    propiedades.setdefault("tab_index", 0)

    return rx.box(
        *hijos,
        on_click=al_hacer_clic,
        **propiedades,
    )


# ======================================================================
# Enlace de navegación
# ======================================================================


def enlace_navegacion(destino: str, *hijos, **propiedades) -> rx.Component:
    """
    Enlace de navegación entre páginas (URLs reales).

    Aplica `text_decoration="none"` y `cursor="pointer"` por defecto,
    pero permite sobrescribirlos sin duplicar kwargs.
    """
    propiedades.setdefault("text_decoration", "none")
    propiedades.setdefault("cursor", "pointer")

    return rx.link(
        *hijos,
        href=destino,
        **propiedades,
    )


# ======================================================================
# Tarjeta estilizada
# ======================================================================


def tarjeta_estilizada(*hijos, **propiedades) -> rx.Component:
    """
    Tarjeta con estilo institucional estándar.

    Usa las constantes de `styles.py` para mantener consistencia:
    - Padding de 1.25rem.
    - Radio de borde.
    - Borde gris suave.
    - Sombra de caja estándar.
    """
    propiedades.setdefault("padding", "1.25rem")
    propiedades.setdefault("border_radius", RADIO_BORDE)
    propiedades.setdefault("border", BORDE_PREDETERMINADO)
    propiedades.setdefault("box_shadow", SOMBRA_CAJA)

    return rx.box(*hijos, **propiedades)


# ======================================================================
# Tarjeta de información pequeña
# ======================================================================


def tarjeta_informacion_pequena(
    icono: str,
    titulo: str,
    valor: str,
    color_icono: str,
) -> rx.Component:
    """
    Tarjeta compacta con icono + título + valor.

    Usada en la vista de detalle de carrera para mostrar datos rápidos
    (duración, título, certificación, etc.).
    """
    return rx.card(
        rx.hstack(
            rx.box(
                # --- Icono con fondo de acento ---
                rx.box(
                    rx.icon(icono, size=16, color=color_icono),
                    padding="0.5rem",
                    background=COLOR_FONDO_ACENTO,
                    border_radius="0.5rem",
                    width="fit-content",
                    margin_bottom="0.5rem",
                    display="flex",
                ),
                # --- Título y valor ---
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
