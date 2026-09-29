"""
Barra de opciones del explorador (tabs circulares).
"""

import reflex as rx

from app_portada_instein.componentes.primitivos import contenedor_clicable
from app_portada_instein.dominio.estado_institucional import EstadoInstitucional
from app_portada_instein.infraestructura.constantes_visuales import (
    COLOR_BORDE_SUAVE,
    COLOR_FONDO_CARTA,
    COLOR_TEXTO_CUERPO,
    COLOR_TEXTO_SECUNDARIO,
    RADIO_PASTILLA,
)

from .constantes import OPCIONES_EXPLORADOR, TAMANO_ICONO_OPCION
from .helpers import color_carrera_destacada


def _boton_opcion_explorador(
    icono: str,
    etiqueta: str,
    id_seccion: str,
) -> rx.Component:
    """
    Botón circular con icono y etiqueta debajo.

    UX:
    - Estado activo: fondo sólido del color de carrera + icono blanco.
    - Estado inactivo: fondo neutro + icono neutro.
    - Hover: elevación sutil.
    """
    esta_activa = EstadoInstitucional.seccion_explorador_activa == id_seccion
    color = color_carrera_destacada()

    return contenedor_clicable(
        rx.vstack(
            rx.flex(
                rx.icon(
                    icono,
                    size=TAMANO_ICONO_OPCION,
                    color=rx.cond(esta_activa, "white", COLOR_TEXTO_CUERPO),
                ),
                height="3rem",
                width="3rem",
                border_radius=RADIO_PASTILLA,
                background=rx.cond(
                    esta_activa,
                    color,
                    COLOR_FONDO_CARTA,
                ),
                border=rx.cond(
                    esta_activa,
                    f"1px solid {color}",
                    f"1px solid {COLOR_BORDE_SUAVE}",
                ),
                align="center",
                justify="center",
                box_shadow=rx.cond(
                    esta_activa,
                    f"0 8px 20px -4px {color}",
                    "0 2px 6px -2px rgba(0,0,0,0.08)",
                ),
                transition="all 0.2s",
                backdrop_filter="blur(12px)",
            ),
            rx.text(
                etiqueta,
                font_size="0.75rem",
                font_weight=rx.cond(esta_activa, "700", "600"),
                color=rx.cond(
                    esta_activa,
                    color,
                    COLOR_TEXTO_SECUNDARIO,
                ),
                white_space="nowrap",
            ),
            align="center",
            spacing="2",
        ),
        al_hacer_clic=lambda: EstadoInstitucional.seleccionar_seccion_explorador(
            id_seccion
        ),
        transition="all 0.2s",
        _hover={"transform": "translateY(-2px)"},
    )


def _barra_opciones_explorador() -> rx.Component:
    """Barra horizontal con las opciones del explorador."""
    return rx.flex(
        *[
            _boton_opcion_explorador(icono, etiqueta, id_seccion)
            for icono, etiqueta, id_seccion in OPCIONES_EXPLORADOR
        ],
        gap="1.25rem",
        justify="center",
        align="start",
        flex_wrap="wrap",
        width="100%",
        margin_bottom="2.5rem",
    )


__all__ = [
    "_barra_opciones_explorador",
    "_boton_opcion_explorador",
]