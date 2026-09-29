"""
Componentes primitivos reutilizables en toda la aplicación.

Usa los tokens de `constantes_visuales.py` para mantener consistencia
visual (bordes, radios, sombras, colores, fuentes).

Componentes:
- `contenedor_clicable`: caja con role="button" para eventos internos.
- `enlace_navegacion`: enlace estilizado para navegación entre páginas.
- `tarjeta_estilizada`: tarjeta con estilo institucional estándar.
- `tarjeta_informacion_pequena`: tarjeta compacta con icono + título + valor.
"""

import reflex as rx

from app_portada_instein.infraestructura.constantes_visuales import (
    BORDE_PREDETERMINADO,
    COLOR_BORDE_SUAVE,
    COLOR_FONDO_CARTA,
    COLOR_FONDO_SUAVE,
    COLOR_TEXTO_CUERPO,
    COLOR_TEXTO_SECUNDARIO,
    RADIO_BORDE,
    RADIO_MEDIO,
    SOMBRA_CAJA,
)


# ======================================================================
# Constantes locales (para tarjetas)
# ======================================================================

# Padding por defecto de las tarjetas.
PADDING_TARJETA = "1.25rem"

# Espaciado entre icono y contenido en la tarjeta pequeña.
GAP_ICONO_CONTENIDO = "0.75rem"

# Tamaño del icono en la tarjeta de información pequeña.
TAMANO_ICONO_TARJETA = 18


# ======================================================================
# Contenedor clicable (botón semántico)
# ======================================================================


def contenedor_clicable(*hijos, al_hacer_clic=None, **propiedades) -> rx.Component:
    """
    Contenedor que actúa como botón para eventos internos.

    Aplica `cursor="pointer"`, `role="button"` y `tab_index=0` por
    defecto, pero permite sobrescribir cualquier propiedad sin duplicar
    kwargs.

    Args:
        *hijos: Elementos hijos del contenedor.
        al_hacer_clic: Evento a disparar en click (o Var de evento).
        **propiedades: Props adicionales de Reflex (styles, etc.).
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

    Args:
        destino: URL de destino (ej: "/carreras", "/carrera/0").
        *hijos: Contenido visible del enlace.
        **propiedades: Props adicionales de Reflex.
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

    Usa tokens de `constantes_visuales.py`:
    - Padding: 1.25rem.
    - Radio de borde: `RADIO_BORDE`.
    - Borde: `BORDE_PREDETERMINADO` (gris suave).
    - Fondo: `COLOR_FONDO_CARTA` (adaptativo al modo).
    - Sombra: `SOMBRA_CAJA`.

    Args:
        *hijos: Contenido de la tarjeta.
        **propiedades: Props adicionales de Reflex.
    """
    propiedades.setdefault("padding", PADDING_TARJETA)
    propiedades.setdefault("border_radius", RADIO_BORDE)
    propiedades.setdefault("border", BORDE_PREDETERMINADO)
    propiedades.setdefault("background", COLOR_FONDO_CARTA)
    propiedades.setdefault("box_shadow", SOMBRA_CAJA)

    return rx.box(*hijos, **propiedades)


# ======================================================================
# Tarjeta de información pequeña
# ======================================================================


def tarjeta_informacion_pequena(
    icono: str,
    titulo: str,
    valor: str,
    color_icono: str = "",
    color_fondo_icono: str = "",
) -> rx.Component:
    """
    Tarjeta compacta con icono + título + valor.

    Usada en la vista de detalle de carrera para mostrar datos rápidos
    (duración, título, modalidad, cupos).

    Diseño UX:
    - Icono con fondo tintado (color de marca o neutro).
    - Título en mayúsculas, tamaño pequeño, color secundario.
    - Valor en tamaño destacado, color principal.
    - Hover: borde del color del icono y sombra suave.

    Args:
        icono: Nombre del icono de Lucide.
        titulo: Texto del título (ej: "DURACIÓN").
        valor: Valor a mostrar (ej: "3 Años").
        color_icono: Color del icono. Puede ser un Var de color de
            carrera o un token neutro. Si no se pasa, usa neutro.
        color_fondo_icono: Color de fondo del icono. Si no se pasa,
            usa `COLOR_FONDO_SUAVE` (neutro). Para tinte de marca,
            pasar el color suave de la carrera.

    Returns:
        Componente `rx.card` con la estructura completa.
    """
    # --- Valores por defecto si no se pasan ---
    color_icono_final = color_icono or COLOR_TEXTO_SECUNDARIO
    color_fondo_final = color_fondo_icono or COLOR_FONDO_SUAVE

    return rx.card(
        rx.flex(
            # ==========================================================
            # Icono en caja tintada
            # ==========================================================
            rx.box(
                rx.icon(
                    icono,
                    size=TAMANO_ICONO_TARJETA,
                    color=color_icono_final,
                ),
                padding="0.5rem",
                border_radius=RADIO_MEDIO,
                background=color_fondo_final,
                display="flex",
                align_items="center",
                justify_content="center",
                flex_shrink="0",
            ),
            # ==========================================================
            # Título + Valor
            # ==========================================================
            rx.vstack(
                rx.text(
                    titulo,
                    font_size="0.6875rem",
                    font_weight="700",
                    color=COLOR_TEXTO_SECUNDARIO,
                    text_transform="uppercase",
                    letter_spacing="0.05em",
                    line_height="1.1",
                ),
                rx.text(
                    valor,
                    font_size="0.9375rem",
                    font_weight="700",
                    color=COLOR_TEXTO_CUERPO,
                    line_height="1.3",
                ),
                spacing="1",
                align="start",
                flex="1",
                min_width="0",
            ),
            align="start",
            gap=GAP_ICONO_CONTENIDO,
            width="100%",
        ),
        width="100%",
        padding="1rem",
        transition="all 0.2s",
        _hover={
            "border_color": color_icono_final,
            "transform": "translateY(-2px)",
            "box_shadow": f"0 8px 20px -8px {color_icono_final}",
        },
    )


__all__ = [
    "contenedor_clicable",
    "enlace_navegacion",
    "tarjeta_estilizada",
    "tarjeta_informacion_pequena",
]