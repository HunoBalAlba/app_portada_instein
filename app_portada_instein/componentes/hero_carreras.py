"""
Hero para la página de carreras, estilo Google Play Store:
- Carrusel de banners destacados con flechas de navegación.
- Indicadores de posición (dots).
- Grid de perspectiva sutil de fondo.
- Usa la imagen horizontal (`imagen_banner`) para el fondo del banner.

Sistema de color (UX)
---------------------
- Colores de carrera: mediante los helpers globales
  `color_carrera_adaptativo()` y `color_suave_carrera_adaptativo()`.
- Elementos institucionales (grid perspectiva, flechas, dots inactivos):
  tokens Radix.
- Overlay sobre imagen del banner: `rgba` intencionales para legibilidad.
"""

import reflex as rx

from app_portada_instein.dominio.estado_institucional import EstadoInstitucional
from app_portada_instein.infraestructura.constantes_visuales import (
    ANCHO_CONTENIDO,
    ANCHO_SECCION,
    COLOR_ACENTO_BORDE,
    COLOR_BORDE_HOVER,
    COLOR_BORDE_SUAVE,
    COLOR_FONDO_CARTA,
    COLOR_FONDO_SUAVE,
    COLOR_TEXTO_PRINCIPAL,
    COLOR_TEXTO_SECUNDARIO,
    RADIO_GRANDE,
    RADIO_MEDIO,
    RADIO_PASTILLA,
    SOMBRA_CAJA,
    color_carrera_adaptativo,
    color_suave_carrera_adaptativo,
)


# ======================================================================
# Constantes locales
# ======================================================================

# Ancho del grid de fondo (más ancho que el contenedor para cubrir todo).
ANCHO_GRID_PERSPECTIVA = "200%"

# Ángulos de las líneas radiales del grid.
ANGULOS_GRID = [i * 45 for i in range(8)]

# Tamaño de los iconos de las flechas.
TAMANO_ICONO_FLECHA = 22

# Padding del contenedor del hero.
PADDING_HERO = "3rem 3rem 2rem 3rem"


# ======================================================================
# Helpers de color adaptativo (alias de los globales)
# ======================================================================


def _color_carrera(carrera: dict) -> rx.Var:
    """Alias local para `color_carrera_adaptativo`."""
    return color_carrera_adaptativo(carrera)


def _color_suave_carrera(carrera: dict) -> rx.Var:
    """Alias local para `color_suave_carrera_adaptativo`."""
    return color_suave_carrera_adaptativo(carrera)


# ======================================================================
# Grid de perspectiva de fondo
# ======================================================================


def _grid_perspectiva() -> rx.Component:
    """
    Grid de líneas radiales que simulan perspectiva.

    Usa `accent-6` con baja opacidad (más marcada en dark mode) para
    no competir con el carrusel.
    """
    return rx.box(
        *[
            rx.box(
                position="absolute",
                top="50%",
                left="50%",
                width=ANCHO_GRID_PERSPECTIVA,
                height="1px",
                background=rx.color("accent", 6),
                opacity=rx.color_mode_cond(light="0.06", dark="0.12"),
                transform_origin="0 50%",
                transform=f"translate(0, -50%) rotate({angulo}deg)",
            )
            for angulo in ANGULOS_GRID
        ],
        position="absolute",
        top="0",
        left="0",
        right="0",
        bottom="0",
        overflow="hidden",
        z_index="0",
        pointer_events="none",
    )


# ======================================================================
# Banner individual destacado (estilo Google Play)
# ======================================================================


def _banner_carrera(item: dict) -> rx.Component:
    """
    Banner horizontal grande, estilo Google Play Store.

    Recibe un dict con la estructura:
    {
        "carrera": { ...datos de la carrera... },
        "etiqueta": "Inscripciones abiertas",
    }

    Usa:
    - `imagen_banner` (16:9) como fondo del banner.
    - `imagen_archivo` (1:1) para el icono circular.

    Nota: los `rgba(0,0,0,X)` y `rgba(255,255,255,X)` se mantienen
    porque se aplican SOBRE la imagen del banner (para garantizar
    legibilidad del texto blanco), no sobre el fondo del tema. Estos
    valores funcionan igual en light y dark mode.
    """
    carrera = item["carrera"]
    etiqueta = item["etiqueta"]
    color_carrera = _color_carrera(carrera)

    return rx.link(
        rx.box(
            # --- Imagen de fondo con overlay ---
            rx.box(
                rx.image(
                    src="/" + carrera["imagen_banner"],
                    alt=carrera["nombre"],
                    width="100%",
                    height="100%",
                    object_fit="cover",
                    position="absolute",
                    top="0",
                    left="0",
                    z_index="0",
                ),
                position="absolute",
                top="0",
                left="0",
                right="0",
                bottom="0",
                background=(
                    "linear-gradient(to top, rgba(0,0,0,0.85) 0%, "
                    "rgba(0,0,0,0.2) 60%, rgba(0,0,0,0.4) 100%)"
                ),
                z_index="1",
            ),
            # --- Contenido sobre la imagen ---
            rx.vstack(
                # --- Etiqueta superior ---
                rx.box(
                    rx.text(
                        etiqueta,
                        font_size="0.75rem",
                        font_weight="600",
                        color="white",
                    ),
                    padding="0.375rem 0.75rem",
                    background="rgba(0,0,0,0.6)",
                    backdrop_filter="blur(8px)",
                    border_radius=RADIO_MEDIO,
                    width="fit-content",
                ),
                # --- Espaciador ---
                rx.box(flex="1"),
                # --- Título grande ---
                rx.heading(
                    carrera["nombre"],
                    font_size=["1.25rem", "1.5rem", "1.75rem"],
                    font_weight="800",
                    color="white",
                    line_height="1.2",
                    max_width="90%",
                ),
                # --- Footer: icono + subtítulo + CTA ---
                rx.flex(
                    # Icono circular
                    rx.box(
                        rx.image(
                            src="/" + carrera["imagen_archivo"],
                            alt=carrera["nombre"],
                            width="100%",
                            height="100%",
                            object_fit="cover",
                            border_radius=RADIO_PASTILLA,
                        ),
                        width="3rem",
                        height="3rem",
                        border_radius=RADIO_PASTILLA,
                        overflow="hidden",
                        border="2px solid rgba(255,255,255,0.4)",
                        flex_shrink="0",
                    ),
                    # Subtítulo
                    rx.vstack(
                        rx.text(
                            carrera["nombre_corto"],
                            font_size="0.875rem",
                            font_weight="600",
                            color="white",
                        ),
                        rx.text(
                            carrera["duracion"] + " · Técnico Superior",
                            font_size="0.75rem",
                            color="rgba(255,255,255,0.75)",
                        ),
                        align="start",
                        spacing="0",
                        flex="1",
                    ),
                    # Botón CTA
                    rx.box(
                        rx.text(
                            "Ver detalle",
                            font_size="0.75rem",
                            font_weight="600",
                            color="white",
                        ),
                        padding="0.5rem 0.875rem",
                        border_radius=RADIO_MEDIO,
                        background="rgba(0,0,0,0.6)",
                        backdrop_filter="blur(8px)",
                        border="1px solid rgba(255,255,255,0.25)",
                        flex_shrink="0",
                    ),
                    align="center",
                    gap="0.75rem",
                    width="100%",
                    margin_top="1rem",
                ),
                align="start",
                justify="between",
                spacing="2",
                width="100%",
                height="100%",
                padding="1.25rem",
                position="relative",
                z_index="2",
            ),
            position="relative",
            height="20rem",
            border_radius=RADIO_GRANDE,
            overflow="hidden",
            transition="all 0.3s",
            _hover={
                "transform": "translateY(-4px)",
                "box_shadow": f"0 20px 40px -10px {color_carrera}",
            },
        ),
        href=f"/carrera/{carrera['id']}",
        text_decoration="none",
        width="100%",
    )


# ======================================================================
# Flecha de navegación (izquierda / derecha)
# ======================================================================


def _flecha_navegacion(direccion: str) -> rx.Component:
    """
    Flecha circular para navegar el carrusel.

    Args:
        direccion: "izquierda" o "derecha".
    """
    if direccion == "izquierda":
        icono = "chevron-left"
        evento = EstadoInstitucional.anterior_carrusel
        posicion = {"left": "-1.5rem"}
    else:
        icono = "chevron-right"
        evento = EstadoInstitucional.siguiente_carrusel
        posicion = {"right": "-1.5rem"}

    return rx.box(
        rx.icon(
            icono,
            size=TAMANO_ICONO_FLECHA,
            color=COLOR_TEXTO_PRINCIPAL,
        ),
        position="absolute",
        top="50%",
        transform="translateY(-50%)",
        height="2.75rem",
        width="2.75rem",
        border_radius=RADIO_PASTILLA,
        background=COLOR_FONDO_CARTA,
        border=f"1px solid {COLOR_BORDE_SUAVE}",
        box_shadow=SOMBRA_CAJA,
        display="flex",
        align_items="center",
        justify_content="center",
        cursor="pointer",
        z_index="10",
        transition="all 0.2s",
        on_click=evento,
        _hover={
            "transform": "translateY(-50%) scale(1.1)",
            "box_shadow": "0 8px 20px -4px rgba(0,0,0,0.2)",
            "border_color": COLOR_ACENTO_BORDE,
        },
        **posicion,
    )


# ======================================================================
# Indicadores de posición (dots)
# ======================================================================


def _dot_indicador(item: dict, idx: int) -> rx.Component:
    """
    Dot individual del carrusel.

    El dot activo se alarga (pill) y usa el color de la carrera;
    los inactivos usan `COLOR_BORDE_SUAVE`.

    Args:
        item: Dict con `carrera` y `etiqueta`.
        idx: Índice del dot en el carrusel.
    """
    esta_activo = EstadoInstitucional.indice_carrusel == idx

    return rx.box(
        height="0.5rem",
        width=rx.cond(esta_activo, "1.5rem", "0.5rem"),
        border_radius=RADIO_PASTILLA,
        background=rx.cond(
            esta_activo,
            _color_carrera(item["carrera"]),
            COLOR_BORDE_SUAVE,
        ),
        cursor="pointer",
        transition="all 0.3s",
        on_click=lambda: EstadoInstitucional.ir_a_banner(idx),
    )


def _indicadores_dots() -> rx.Component:
    """Fila de dots que indican la posición actual del carrusel."""
    return rx.flex(
        rx.foreach(
            EstadoInstitucional.carreras_destacadas_con_etiquetas,
            _dot_indicador,
        ),
        gap="0.375rem",
        justify="center",
        align="center",
        margin_top="1.5rem",
        width="100%",
    )


# ======================================================================
# Miniaturas de carreras
# ======================================================================


def _miniatura_carrera(item: dict, idx: int) -> rx.Component:
    """
    Miniatura individual de carrera en el carrusel.

    La miniatura activa usa borde y texto con el color de la carrera.

    Args:
        item: Dict con `carrera` y `etiqueta`.
        idx: Índice de la miniatura en el carrusel.
    """
    esta_activa = EstadoInstitucional.indice_carrusel == idx
    carrera = item["carrera"]
    color_carrera = _color_carrera(carrera)

    return rx.box(
        rx.text(
            carrera["nombre_corto"],
            font_size="0.75rem",
            font_weight="600",
            color=rx.cond(
                esta_activa,
                color_carrera,
                COLOR_TEXTO_SECUNDARIO,
            ),
            white_space="nowrap",
        ),
        padding="0.5rem 0.875rem",
        border_radius=RADIO_PASTILLA,
        background=rx.cond(
            esta_activa,
            COLOR_FONDO_SUAVE,
            COLOR_FONDO_CARTA,
        ),
        border=rx.cond(
            esta_activa,
            f"1px solid {color_carrera}",
            f"1px solid {COLOR_BORDE_SUAVE}",
        ),
        cursor="pointer",
        transition="all 0.2s",
        on_click=lambda: EstadoInstitucional.ir_a_banner(idx),
        _hover={
            "transform": "translateY(-2px)",
            "border_color": color_carrera,
            "box_shadow": "0 8px 20px -8px rgba(0, 0, 0, 0.15)",
        },
    )


def _miniaturas_carreras() -> rx.Component:
    """
    Fila de miniaturas clicables debajo del carrusel.

    Cada miniatura muestra el nombre corto de la carrera y al hacer
    clic navega al banner correspondiente.
    """
    return rx.flex(
        rx.foreach(
            EstadoInstitucional.carreras_destacadas_con_etiquetas,
            _miniatura_carrera,
        ),
        gap="0.5rem",
        justify="center",
        align="center",
        flex_wrap="wrap",
        margin_top="1.5rem",
        width="100%",
    )


# ======================================================================
# Carrusel completo
# ======================================================================


def _carrusel_carreras() -> rx.Component:
    """Carrusel de banners + indicadores + miniaturas."""
    return rx.box(
        # --- Contenedor con flechas + banner ---
        rx.box(
            _banner_carrera(EstadoInstitucional.item_carrusel_actual),
            _flecha_navegacion("izquierda"),
            _flecha_navegacion("derecha"),
            position="relative",
            width="100%",
            max_width=ANCHO_SECCION,
            margin="0 auto",
        ),
        # --- Indicadores de posición (dots) ---
        _indicadores_dots(),
        # --- Miniaturas clicables ---
        _miniaturas_carreras(),
        width="100%",
    )


# ======================================================================
# Hero completo
# ======================================================================


def hero_carreras() -> rx.Component:
    """
    Hero de la página de carreras estilo Google Play Store con carrusel.
    """
    return rx.box(
        # --- Grid de perspectiva de fondo ---
        _grid_perspectiva(),
        # --- Carrusel ---
        rx.box(
            _carrusel_carreras(),
            max_width=ANCHO_CONTENIDO,
            margin="0 auto",
            padding=PADDING_HERO,
            position="relative",
            z_index="1",
            width="100%",
        ),
        # --- Contenedor principal ---
        position="relative",
        width="100%",
        overflow="hidden",
    )


__all__ = ["hero_carreras"]