"""
Hero para la página de carreras, estilo Google Play Store:
- Carrusel de banners destacados con flechas de navegación.
- Indicadores de posición (dots).
- Barra de progreso del auto-avance (feedback UX).
- Grid de perspectiva sutil de fondo.
- Auto-avance del carrusel con `rx.moment(interval=...)` (FIX de
  la fuga de memoria).

Sistema de color (UX)
---------------------
- Colores de carrera: mediante los helpers globales
  `color_carrera_adaptativo()` y `color_suave_carrera_adaptativo()`.
- Elementos institucionales (grid perspectiva, flechas, dots inactivos):
  tokens Radix.
- Overlay sobre imagen del banner: `rgba` intencionales para legibilidad.
- Barra de progreso: color de la carrera activa.

Nota técnica: AUTO-AVANCE CON `rx.moment`
-----------------------------------------
El auto-avance del carrusel se implementa con el componente
`rx.moment(interval=5000)`, que internamente es un `<Moment>` de
Moment.js con un `setInterval` de JS.

Cada 5000 ms (5 s) dispara el evento `siguiente_carrusel`. Al
desmontar el componente (salir de `/carreras`), el navegador cancela
el intervalo automáticamente.

Ventajas sobre el `while True` en Python:
- **Cero fugas de memoria**: 1 intervalo por página activa.
- **Cero CPU del servidor**: el timer vive en el navegador.
- **Cancelación automática**: al desmontar el componente.
- **Sin `on_unmount` manual**: el navegador lo maneja.

Nota técnica: BARRA DE PROGRESO
-------------------------------
La barra de progreso del auto-avance se implementa con CSS puro
usando un `@keyframes` global que anima `width` de 0% a 100% durante
5 segundos.

Se reinicia automáticamente al cambiar el índice del carrusel porque
la barra es un componente nuevo (React lo remonta al cambiar la
`key`).

El color de la barra coincide con el color de la carrera activa,
reforzando la identidad visual del banner.
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

# Intervalo del auto-avance en milisegundos (5 segundos).
INTERVALO_AUTO_AVANCE_MS = 5000

# Segundos del auto-avance (para la animación CSS de la barra).
INTERVALO_AUTO_AVANCE_SEG = INTERVALO_AUTO_AVANCE_MS / 1000

# Nombre del keyframe CSS de la barra de progreso.
KEYFRAME_BARRA_PROGRESO = "progreso_carrusel"

# Altura de la barra de progreso.
ALTURA_BARRA_PROGRESO = "0.25rem"


# ======================================================================
# Keyframe CSS de la barra de progreso
# ======================================================================


def keyframes_progreso_carrusel() -> dict:
    """
    Devuelve el `@keyframes` para la barra de progreso del carrusel.

    La animación va de `width: 0%` a `width: 100%` en
    `INTERVALO_AUTO_AVANCE_SEG` segundos con timing lineal, para que
    la barra se llene a velocidad constante.

    Se debe inyectar en los estilos globales de la app (en
    `app_portada_instein.py`).

    Returns:
        Dict compatible con el `style=` de `rx.App(...)`.
    """
    return {
        f"@keyframes {KEYFRAME_BARRA_PROGRESO}": {
            "0%": {"width": "0%"},
            "100%": {"width": "100%"},
        },
    }


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
# Barra de progreso del auto-avance
# ======================================================================


def _barra_progreso_auto_avance() -> rx.Component:
    """
    Barra de progreso animada que se llena durante el intervalo de
    auto-avance.

    La barra se reinicia automáticamente al cambiar de banner porque
    React remonta el componente cuando su `key` cambia. Usamos
    `key=EstadoInstitucional.indice_carrusel` para forzar el remount.

    La barra:
    - Tiene el color de la carrera activa.
    - Se llena de 0% a 100% en `INTERVALO_AUTO_AVANCE_SEG` segundos.
    - Está posicionada al fondo del banner, superpuesta.

    Returns:
        Componente con la barra animada.
    """
    return rx.box(
        rx.box(
            height="100%",
            background=_color_carrera(EstadoInstitucional.item_carrusel_actual["carrera"]),
            border_radius=RADIO_PASTILLA,
            # Animación CSS: la barra se llena linealmente durante 5s.
            animation=(
                f"{KEYFRAME_BARRA_PROGRESO} "
                f"{INTERVALO_AUTO_AVANCE_SEG}s linear infinite"
            ),
            # `transform-origin: left` para que crezca desde la izquierda.
            transform_origin="left center",
        ),
        position="absolute",
        bottom="0",
        left="0",
        right="0",
        height=ALTURA_BARRA_PROGRESO,
        background="rgba(0,0,0,0.3)",
        backdrop_filter="blur(4px)",
        overflow="hidden",
        z_index="3",
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

    Nota: los `rgba(0,0,0,X)` y `rgba(255,255,255,X)` se mantienen
    porque se aplican SOBRE la imagen del banner (para garantizar
    legibilidad del texto blanco), no sobre el fondo del tema.
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
            # --- Barra de progreso del auto-avance ---
            _barra_progreso_auto_avance(),
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
                padding_bottom="1.5rem",  # Deja espacio para la barra
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
# Auto-avance con rx.moment (FIX FUGA DE MEMORIA)
# ======================================================================


def _auto_avance_moment() -> rx.Component:
    """
    Componente invisible que dispara `siguiente_carrusel` cada 5 s.

    Usa `rx.moment(interval=INTERVALO_AUTO_AVANCE_MS)`, que inyecta un
    `setInterval` de JS en el cliente. Al desmontar el componente
    (salir de `/carreras`), el navegador cancela el intervalo
    automáticamente.

    Esto reemplaza al antiguo `@rx.event(background=True)` con
    `while True`, que causaba una fuga de memoria porque la tarea
    nunca se detenía al salir de la página.
    """
    return rx.moment(
        interval=INTERVALO_AUTO_AVANCE_MS,
        on_change=EstadoInstitucional.siguiente_carrusel,
        display="none",
    )


# ======================================================================
# Carrusel completo
# ======================================================================


def _carrusel_carreras() -> rx.Component:
    """
    Carrusel de banners + barra de progreso + indicadores + miniaturas +
    auto-avance.

    La barra de progreso se reinicia automáticamente cuando cambia el
    índice del carrusel porque el componente se remonta gracias a la
    `key` ligada a `indice_carrusel`.
    """
    return rx.box(
        # --- Auto-avance con rx.moment (FIX) ---
        _auto_avance_moment(),
        # --- Contenedor con flechas + banner ---
        rx.box(
            # La `key` ligada al índice fuerza el remount del banner
            # (y con él, de la barra de progreso) al cambiar de item.
            rx.box(
                _banner_carrera(EstadoInstitucional.item_carrusel_actual),
                key=EstadoInstitucional.indice_carrusel,
                width="100%",
            ),
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

    El auto-avance vive en `_auto_avance_moment()`, que usa
    `rx.moment(interval=...)` para disparar `siguiente_carrusel` cada
    5 segundos sin mantener una tarea de Python corriendo.

    La barra de progreso (dentro del banner) se reinicia
    automáticamente al cambiar de banner gracias a la `key`.
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


__all__ = [
    "hero_carreras",
    "keyframes_progreso_carrusel",
]