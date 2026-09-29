"""
Widgets que componen la sección de "carrera destacada" del home:
- Estrellas de fondo.
- Líneas de fuga radiales.
- Iconos orbitando elípticamente.
- Imagen central (el "Sol").
- Selector de carrera.

Sistema de color (UX)
---------------------
- Colores de carrera: mediante helpers globales
  `color_carrera_adaptativo()` y `color_suave_carrera_adaptativo()`.
- Estrellas y líneas de fuga: neutros (adaptativos al modo).
- Fondos orbitales: gradientes adaptativos.
- Overlays sobre imágenes: `rgba` intencionales para legibilidad.
"""

import random

import reflex as rx

from app_portada_instein.componentes.primitivos import (
    contenedor_clicable,
    enlace_navegacion,
)
from app_portada_instein.dominio.estado_institucional import EstadoInstitucional
from app_portada_instein.infraestructura.constantes_visuales import (
    COLOR_BORDE_SUAVE,
    COLOR_FONDO_CARTA,
    COLOR_TEXTO_CUERPO,
    COLOR_TEXTO_PRINCIPAL,
    COLOR_TEXTO_SECUNDARIO,
    RADIO_EXTRA_GRANDE,
    RADIO_GRANDE,
    RADIO_MEDIO,
    RADIO_PASTILLA,
    color_carrera_adaptativo,
    color_suave_carrera_adaptativo,
)


# ======================================================================
# Constantes locales
# ======================================================================

# Cantidad de estrellas decorativas del fondo orbital.
CANTIDAD_ESTRELLAS = 80
SEMILLA_ESTRELLAS = 42

# Ángulos de las líneas de fuga radiales.
ANGULOS_LINEAS_FUGA = [i * 22.5 for i in range(16)]

# Anchos de las líneas de fuga.
ANCHO_LINEA_FUGA = "150%"


# ======================================================================
# Helpers de color adaptativo
# ======================================================================


def _color_carrera(carrera: dict) -> rx.Var:
    """Color principal de la carrera adaptado al color_mode."""
    return color_carrera_adaptativo(carrera)


def _color_suave_carrera(carrera: dict) -> rx.Var:
    """Color suave de la carrera adaptado al color_mode."""
    return color_suave_carrera_adaptativo(carrera)


# ======================================================================
# Estrellas de fondo
# ======================================================================


def _generar_estrellas(
    cantidad: int = CANTIDAD_ESTRELLAS,
    semilla: int = SEMILLA_ESTRELLAS,
) -> list[dict]:
    """
    Genera posiciones aleatorias pero reproducibles para las estrellas.

    Args:
        cantidad: Número de estrellas a generar.
        semilla: Semilla para reproducibilidad.

    Returns:
        Lista de dicts con la configuración de cada estrella.
    """
    rng = random.Random(semilla)
    return [
        {
            "x": rng.uniform(0, 100),
            "y": rng.uniform(0, 100),
            "tamano": rng.uniform(1, 3),
            "opacidad": rng.uniform(0.3, 0.9),
            "delay": rng.uniform(0, 3),
        }
        for _ in range(cantidad)
    ]


ESTRELLAS_FONDO = _generar_estrellas()


def _estrella_fondo(estrella: dict) -> rx.Component:
    """
    Renderiza una estrella individual del fondo.

    Usa `COLOR_TEXTO_PRINCIPAL` (gray-12) para que sea visible en
    ambos modos (oscuro en light, claro en dark).

    Args:
        estrella: Dict con `x`, `y`, `tamano`, `opacidad`, `delay`.
    """
    return rx.box(
        position="absolute",
        left=f"{estrella['x']}%",
        top=f"{estrella['y']}%",
        width=f"{estrella['tamano']}px",
        height=f"{estrella['tamano']}px",
        background=COLOR_TEXTO_PRINCIPAL,
        border_radius=RADIO_PASTILLA,
        opacity=f"{estrella['opacidad']}",
        animation=(
            f"flotar_estrella {2 + estrella['delay']}s "
            f"ease-in-out {estrella['delay']}s infinite"
        ),
        z_index="0",
        pointer_events="none",
    )


# ======================================================================
# Líneas de fuga radiales
# ======================================================================


def _linea_fuga(angulo: int, color_carrera: rx.Var) -> rx.Component:
    """
    Renderiza una línea de fuga radial desde el centro del contenedor.

    Args:
        angulo: Ángulo de rotación en grados.
        color_carrera: Color de la carrera (Var adaptativo).
    """
    return rx.box(
        position="absolute",
        top="50%",
        left="50%",
        width=ANCHO_LINEA_FUGA,
        height="1px",
        background=rx.color_mode_cond(
            light=COLOR_TEXTO_SECUNDARIO,
            dark=color_carrera,
        ),
        opacity=rx.color_mode_cond(light="0.15", dark="0.25"),
        transform_origin="0 50%",
        transform=f"translate(0, -50%) rotate({angulo}deg)",
        z_index="1",
        pointer_events="none",
    )


# ======================================================================
# Icono orbital (con anillos opcionales estilo Saturno)
# ======================================================================


def _anillos_saturno(color: rx.Var | str) -> rx.Component:
    """
    Dibuja los anillos característicos de Saturno alrededor del icono.

    Args:
        color: Color de la carrera (Var adaptativo) o hex fijo.
    """
    return rx.box(
        rx.box(
            position="absolute",
            top="50%",
            left="50%",
            width="2.4rem",
            height="0.6rem",
            border=f"2px solid {color}",
            border_radius=RADIO_PASTILLA,
            transform="translate(-50%, -50%)",
            opacity="0.8",
        ),
        rx.box(
            position="absolute",
            top="50%",
            left="50%",
            width="3.0rem",
            height="0.9rem",
            border=f"1.5px solid {color}",
            border_radius=RADIO_PASTILLA,
            transform="translate(-50%, -50%)",
            opacity="0.4",
        ),
        position="absolute",
        top="50%",
        left="50%",
        width="0",
        height="0",
        z_index="5",
        pointer_events="none",
    )


def _icono_orbital(icono_animado: dict) -> rx.Component:
    """
    Renderiza un icono con su propia trayectoria elíptica kepleriana
    alrededor de la imagen central (como un planeta alrededor del Sol).

    Args:
        icono_animado: Dict con datos del icono (periodo, keyframe,
            desfase, color, tiene_anillos, nombre).
    """
    periodo = icono_animado["periodo"]
    keyframe_orbita = icono_animado["keyframe_orbita"]
    desfase = icono_animado["desfase_temporal"]
    color_icono = icono_animado["color"]
    tiene_anillos = icono_animado["tiene_anillos"]

    return rx.box(
        rx.box(
            rx.cond(
                tiene_anillos,
                _anillos_saturno(color_icono),
                rx.fragment(),
            ),
            rx.icon(icono_animado["nombre"], size=24, color="white"),
            padding="0.75rem",
            border_radius=RADIO_GRANDE,
            background=color_icono,
            box_shadow=f"0 8px 20px -5px {color_icono}",
            display="flex",
            align_items="center",
            justify_content="center",
            position="relative",
        ),
        position="absolute",
        top="50%",
        left="50%",
        transform_origin="center center",
        animation=f"{keyframe_orbita} {periodo}s linear {desfase}s infinite",
        z_index="20",
    )


# ======================================================================
# Contenedor orbital completo
# ======================================================================


def contenedor_animacion_orbital(carrera: dict) -> rx.Component:
    """
    Contenedor que ocupa TODO el espacio de la tarjeta con:
    - Fondo espacial adaptativo (estrellas + líneas de fuga).
    - Iconos orbitando con elipses keplerianas.
    - Imagen central (el "Sol").

    Capas (de fondo a frente):
    - z_index=-1: Fondo base (gradiente adaptativo).
    - z_index=0: Estrellas.
    - z_index=1: Líneas de fuga.
    - z_index=2: Halo radial.
    - z_index=10: Imagen central.
    - z_index=20: Iconos orbitando.

    Args:
        carrera: Dict con `color_principal`, `color_principal_dark`,
            `color_suave`, `color_suave_dark`, `iconos_animados`,
            `imagen_archivo`, `nombre`.
    """
    color_principal = _color_carrera(carrera)
    color_suave = _color_suave_carrera(carrera)

    return rx.box(
        # ==============================================================
        # CAPA 1: Fondo espacial
        # ==============================================================
        rx.box(
            # --- Estrellas ---
            rx.box(
                *[_estrella_fondo(estrella) for estrella in ESTRELLAS_FONDO],
                position="absolute",
                top="0",
                left="0",
                right="0",
                bottom="0",
                z_index="0",
                pointer_events="none",
            ),
            # --- Líneas de fuga ---
            rx.box(
                *[
                    _linea_fuga(angulo, color_principal)
                    for angulo in ANGULOS_LINEAS_FUGA
                ],
                position="absolute",
                top="0",
                left="0",
                right="0",
                bottom="0",
                z_index="1",
                pointer_events="none",
            ),
            # --- Halo radial ---
            rx.box(
                position="absolute",
                top="0",
                left="0",
                right="0",
                bottom="0",
                background=(
                    f"radial-gradient(circle at 50% 50%, "
                    f"{carrera['color_principal']}33 0%, "
                    f"{carrera['color_suave']}00 70%)"
                ),
                z_index="2",
                pointer_events="none",
            ),
            # --- Fondo base ---
            position="absolute",
            top="0",
            left="0",
            right="0",
            bottom="0",
            background=rx.color_mode_cond(
                light="linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%)",
                dark="linear-gradient(135deg, #0b0914 0%, #05040a 100%)",
            ),
            z_index="-1",
        ),
        # ==============================================================
        # CAPA 2: Iconos orbitales
        # ==============================================================
        rx.box(
            rx.foreach(carrera["iconos_animados"], _icono_orbital),
            position="absolute",
            top="0",
            left="0",
            right="0",
            bottom="0",
            z_index="20",
        ),
        # ==============================================================
        # CAPA 3: Imagen central
        # ==============================================================
        rx.box(
            rx.image(
                src="/" + carrera["imagen_archivo"],
                alt=carrera["nombre"],
                width="100%",
                height="100%",
                object_fit="cover",
                border_radius=RADIO_PASTILLA,
            ),
            position="absolute",
            top="50%",
            left="50%",
            transform="translate(-50%, -50%)",
            width="8rem",
            height="8rem",
            border_radius=RADIO_PASTILLA,
            border=f"4px solid {color_principal}",
            box_shadow=f"0 20px 40px -10px {color_principal}",
            overflow="hidden",
            z_index="10",
            animation="pulso_central 3s ease-in-out infinite",
        ),
        # ==============================================================
        # CONTENEDOR PRINCIPAL
        # ==============================================================
        position="relative",
        width="100%",
        height="100%",
        display="flex",
        align_items="center",
        justify_content="center",
        overflow="hidden",
    )


# ======================================================================
# Cuadro principal de resumen multimedia
# ======================================================================


def _etiqueta_superpuesta(
    contenido: rx.Component,
    posicion: dict,
) -> rx.Component:
    """
    Etiqueta flotante sobre la imagen del hero orbital.

    Usa `rgba(0,0,0,0.3)` intencional para garantizar legibilidad
    sobre cualquier imagen de fondo, independientemente del modo.

    Args:
        contenido: Contenido interno de la etiqueta.
        posicion: Dict con `top`/`left` o `top`/`right`.
    """
    return rx.box(
        contenido,
        position="absolute",
        z_index="30",
        background="rgba(0,0,0,0.4)",
        backdrop_filter="blur(12px)",
        border_radius=RADIO_PASTILLA,
        padding="0.25rem 0.625rem",
        border="1px solid rgba(255,255,255,0.15)",
        **posicion,
    )


def cuadro_resumen_multimedia() -> rx.Component:
    """
    Tarjeta principal con:
    - Contenedor orbital (imagen central + iconos).
    - Etiquetas superpuestas (RESUMEN, duración).
    - CTA al detalle.

    UX:
    - Etiqueta "RESUMEN" con punto rojo (semántico).
    - Etiqueta de duración con fondo translúcido.
    - CTA "abrir detalle" con fondo blanco y sombra.
    """
    carrera = EstadoInstitucional.carrera_destacada
    color_principal = _color_carrera(carrera)

    return rx.box(
        # --- Contenedor orbital de fondo ---
        contenedor_animacion_orbital(carrera),
        # ==========================================================
        # Etiqueta superior izquierda: RESUMEN
        # ==========================================================
        _etiqueta_superpuesta(
            rx.flex(
                rx.box(
                    height="0.375rem",
                    width="0.375rem",
                    border_radius=RADIO_PASTILLA,
                    background=rx.color("red", 9),
                ),
                rx.text("RESUMEN", size="1", color="white"),
                align="center",
                gap="0.375rem",
            ),
            posicion={"top": "1rem", "left": "1rem"},
        ),
        # ==========================================================
        # Etiqueta superior derecha: duración
        # ==========================================================
        _etiqueta_superpuesta(
            rx.text(carrera["duracion"], size="1", color="white"),
            posicion={"top": "1rem", "right": "1rem"},
        ),
        # ==========================================================
        # Pie con nombre corto + botón de detalle
        # ==========================================================
        rx.flex(
            rx.box(
                rx.text(
                    "TÉCNICO SUPERIOR EN",
                    size="1",
                    color="rgba(255,255,255,0.75)",
                ),
                rx.heading(carrera["nombre_corto"], size="6", color="white"),
            ),
            enlace_navegacion(
                EstadoInstitucional.url_detalle_carrera_destacada,
                rx.icon(
                    "image_upscale",
                    size=20,
                    color=color_principal,
                    margin_left="0.125rem",
                ),
                height="2.75rem",
                width="2.75rem",
                border_radius=RADIO_PASTILLA,
                background="white",
                display="flex",
                align_items="center",
                justify_content="center",
                box_shadow="0 10px 25px -5px rgba(0,0,0,0.4)",
                flex_shrink="0",
            ),
            position="absolute",
            bottom="0",
            left="0",
            right="0",
            z_index="30",
            align="end",
            justify="between",
            padding="1rem",
            background="linear-gradient(to top, rgba(0,0,0,0.7), transparent)",
        ),
        # ==========================================================
        # Contenedor principal
        # ==========================================================
        position="relative",
        width="100%",
        height="18rem",
        border_radius=RADIO_EXTRA_GRANDE,
        overflow="hidden",
        border=f"2px solid {color_principal}",
        box_shadow=f"0 20px 40px -10px {color_principal}",
    )


# ======================================================================
# Pastilla selector de carrera destacada
# ======================================================================


def pastilla_carrera_destacada(carrera: dict) -> rx.Component:
    """
    Pastilla seleccionable para elegir la carrera destacada en el home.

    UX:
    - Estado activo: fondo sólido del color de carrera + icono blanco.
    - Estado inactivo: fondo transparente + icono color de carrera.
    - Nombre corto debajo del icono.
    """
    esta_activa = EstadoInstitucional.id_carrera_destacada == carrera["id"]
    color_carrera = _color_carrera(carrera)

    return contenedor_clicable(
        rx.box(
            rx.icon(
                carrera["icono"],
                size=26,
                color=rx.cond(esta_activa, "white", color_carrera),
            ),
            padding="0.75rem",
            background=rx.cond(esta_activa, color_carrera, "transparent"),
            border=f"1px solid {color_carrera}",
            border_radius=RADIO_GRANDE,
            box_shadow=rx.cond(
                esta_activa,
                f"0 10px 25px -5px {color_carrera}",
                "none",
            ),
            transition="all 0.2s",
            display="flex",
        ),
        rx.text(
            carrera["nombre_corto"],
            size="1",
            color=rx.cond(esta_activa, color_carrera, COLOR_TEXTO_SECUNDARIO),
            margin_top="0.375rem",
        ),
        al_hacer_clic=lambda: EstadoInstitucional.seleccionar_carrera_destacada(
            carrera["id"]
        ),
        display="flex",
        flex_direction="column",
        align_items="center",
        justify_content="center",
        flex_shrink="0",
    )


# ======================================================================
# Bloque de texto descriptivo de la carrera destacada
# ======================================================================


def bloque_texto_carrera_destacada() -> rx.Component:
    """
    Texto descriptivo de la carrera destacada con badge "CARRERA DESTACADA".

    UX:
    - Badge con fondo sólido del color de carrera.
    - Título y lema en neutros.
    - CTA "Explorar Carreras" con fondo del color de carrera.
    """
    carrera = EstadoInstitucional.carrera_destacada
    color_principal = _color_carrera(carrera)

    return rx.box(
        # ==========================================================
        # Badge "CARRERA DESTACADA"
        # ==========================================================
        rx.flex(
            rx.icon("star", size=12, color="white"),
            rx.text(
                "CARRERA DESTACADA",
                font_size="0.625rem",
                font_weight="800",
                color="white",
                letter_spacing="0.1em",
            ),
            align="center",
            gap="0.375rem",
            background=color_principal,
            padding="0.375rem 0.75rem",
            border_radius=RADIO_PASTILLA,
            width="fit-content",
            box_shadow=f"0 4px 12px -2px {color_principal}",
            margin_bottom="1rem",
        ),
        # ==========================================================
        # Título grande
        # ==========================================================
        rx.heading(
            carrera["nombre"],
            size="8",
            color=COLOR_TEXTO_PRINCIPAL,
        ),
        # ==========================================================
        # Lema
        # ==========================================================
        rx.text(
            carrera["lema"],
            font_size="1rem",
            color=COLOR_TEXTO_CUERPO,
            margin_top="0.5rem",
        ),
        # ==========================================================
        # CTA "Explorar Carreras"
        # ==========================================================
        enlace_navegacion(
            "/carreras",
            rx.text(
                "Explorar Carreras",
                as_="span",
                font_size="0.875rem",
                font_weight="700",
            ),
            rx.icon("layout-grid", size=16),
            display="flex",
            align_items="center",
            gap="0.5rem",
            margin_top="1.5rem",
            background=color_principal,
            color="white",
            padding="0.75rem 1.5rem",
            border_radius=RADIO_PASTILLA,
            width="fit-content",
            box_shadow=f"0 10px 25px -5px {color_principal}",
            transition="all 0.2s",
            _hover={
                "transform": "translateY(-2px)",
                "filter": "brightness(1.1)",
            },
        ),
        padding="1.5rem 1.5rem 1rem 1.5rem",
    )


# ======================================================================
# Selector completo de carrera destacada
# ======================================================================


def selector_carrera_destacada() -> rx.Component:
    """
    Bloque con:
    - Encabezado "Elige una carrera" + contador.
    - Fila de pastillas selectoras.
    """
    return rx.box(
        # ==========================================================
        # Encabezado
        # ==========================================================
        rx.flex(
            rx.text(
                "Elige una carrera",
                color_scheme="gray",
                size="1",
                text_transform="uppercase",
                font_weight="600",
                letter_spacing="0.05em",
            ),
            rx.text(
                (EstadoInstitucional.id_carrera_destacada + 1).to_string()
                + " / "
                + EstadoInstitucional.carreras.length().to_string(),
                color_scheme="gray",
                size="1",
                font_weight="600",
            ),
            align="center",
            justify="between",
            padding="0 1.5rem",
            margin_bottom="1.75rem",
        ),
        # ==========================================================
        # Fila de pastillas
        # ==========================================================
        rx.vstack(
            rx.box(
                rx.flex(
                    rx.foreach(
                        EstadoInstitucional.carreras,
                        pastilla_carrera_destacada,
                    ),
                    justify="between",
                    align="center",
                    width="100%",
                    direction="row",
                ),
                width="100%",
                max_width="30em",
            ),
            align="center",
            justify="center",
        ),
        align="center",
        justify="center",
        padding_top="1rem",
        padding_bottom="1rem",
    )


__all__ = [
    "bloque_texto_carrera_destacada",
    "contenedor_animacion_orbital",
    "cuadro_resumen_multimedia",
    "pastilla_carrera_destacada",
    "selector_carrera_destacada",
]