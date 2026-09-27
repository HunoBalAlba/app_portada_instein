"""
Widgets que componen la sección de "carrera destacada" del home:
- Estrellas de fondo.
- Líneas de fuga radiales.
- Iconos orbitando elípticamente.
- Imagen central (el "Sol").
- Selector de carrera.
"""

import random

import reflex as rx

from app_portada_instein.componentes.primitivos import (
    contenedor_clicable,
    enlace_navegacion,
)
from app_portada_instein.dominio.estado_institucional import EstadoInstitucional


# ======================================================================
# Estrellas de fondo
# ======================================================================

def _generar_estrellas(cantidad: int = 80, semilla: int = 42) -> list[dict]:
    """Genera posiciones aleatorias pero reproducibles para las estrellas."""
    rng = random.Random(semilla)
    estrellas: list[dict] = []
    for _ in range(cantidad):
        estrellas.append(
            {
                "x": rng.uniform(0, 100),
                "y": rng.uniform(0, 100),
                "tamano": rng.uniform(1, 3),
                "opacidad": rng.uniform(0.3, 0.9),
                "delay": rng.uniform(0, 3),
            }
        )
    return estrellas


ESTRELLAS_FONDO = _generar_estrellas()


def _estrella_fondo(estrella: dict) -> rx.Component:
    """Renderiza una estrella individual del fondo."""
    return rx.box(
        position="absolute",
        left=f"{estrella['x']}%",
        top=f"{estrella['y']}%",
        width=f"{estrella['tamano']}px",
        height=f"{estrella['tamano']}px",
        background=rx.color_mode_cond(light="#1e293b", dark="#ffffff"),
        border_radius="9999px",
        opacity=f"{estrella['opacidad']}",
        animation=(
            f"flotar_estrella {2 + estrella['delay']}s ease-in-out "
            f"{estrella['delay']}s infinite"
        ),
        z_index="0",
        pointer_events="none",
    )


# ======================================================================
# Líneas de fuga radiales
# ======================================================================

def _linea_fuga(angulo: int, color_claro: str) -> rx.Component:
    """Renderiza una línea de fuga radial desde el centro del contenedor."""
    return rx.box(
        position="absolute",
        top="50%",
        left="50%",
        width="150%",
        height="1px",
        background=rx.color_mode_cond(light="#94a3b8", dark=color_claro),
        opacity=rx.color_mode_cond(light="0.15", dark="0.25"),
        transform_origin="0 50%",
        transform=f"translate(0, -50%) rotate({angulo}deg)",
        z_index="1",
        pointer_events="none",
    )


# ======================================================================
# Icono orbital (con anillos opcionales estilo Saturno)
# ======================================================================

def _anillos_saturno(color: str) -> rx.Component:
    """Dibuja los anillos característicos de Saturno alrededor del icono."""
    return rx.box(
        rx.box(
            position="absolute",
            top="50%",
            left="50%",
            width="2.4rem",
            height="0.6rem",
            border=f"2px solid {color}cc",
            border_radius="9999px",
            transform="translate(-50%, -50%)",
        ),
        rx.box(
            position="absolute",
            top="50%",
            left="50%",
            width="3.0rem",
            height="0.9rem",
            border=f"1.5px solid {color}66",
            border_radius="9999px",
            transform="translate(-50%, -50%)",
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
            rx.icon(icono_animado["nombre"], size=24, color="#ffffff"),
            padding="0.75rem",
            border_radius="1rem",
            background=color_icono,
            box_shadow=f"0 8px 20px -5px {color_icono}88",
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
    """
    color_principal = carrera["color_principal"]
    color_suave = carrera["color_suave"]
    angulos_lineas = [i * 22.5 for i in range(16)]

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
                *[_linea_fuga(angulo, color_principal) for angulo in angulos_lineas],
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
                    "radial-gradient(circle at 50% 50%, "
                    + color_principal
                    + "33 0%, "
                    + color_suave
                    + "00 70%)"
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
                border_radius="9999px",
            ),
            position="absolute",
            top="50%",
            left="50%",
            transform="translate(-50%, -50%)",
            width="8rem",
            height="8rem",
            border_radius="9999px",
            border="4px solid " + color_principal,
            box_shadow="0 20px 40px -10px " + color_principal + "80",
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

def cuadro_resumen_multimedia() -> rx.Component:
    """
    Tarjeta principal con:
    - Contenedor orbital (imagen central + iconos).
    - Etiquetas superpuestas (RESUMEN, duración).
    - CTA al detalle.
    """
    carrera = EstadoInstitucional.carrera_destacada

    return rx.box(
        contenedor_animacion_orbital(carrera),

        # --- Etiqueta superior izquierda: RESUMEN ---
        rx.flex(
            rx.box(
                height="0.375rem",
                width="0.375rem",
                border_radius="9999px",
                background="#ef4444",
            ),
            rx.text("RESUMEN", size="1", color="#ffffff"),
            align="center",
            gap="0.375rem",
            background="rgba(0,0,0,0.3)",
            backdrop_filter="blur(12px)",
            border_radius="9999px",
            padding="0.25rem 0.625rem",
            border="1px solid rgba(255,255,255,0.1)",
            position="absolute",
            top="1rem",
            left="1rem",
            z_index="30",
        ),

        # --- Etiqueta superior derecha: duración ---
        rx.box(
            rx.text(carrera["duracion"], size="1", color="#ffffff"),
            position="absolute",
            top="1rem",
            right="1rem",
            z_index="30",
            background="rgba(0,0,0,0.3)",
            backdrop_filter="blur(12px)",
            border_radius="9999px",
            padding="0.25rem 0.625rem",
            border="1px solid rgba(255,255,255,0.1)",
        ),

        # --- Pie con nombre corto + botón de detalle ---
        rx.flex(
            rx.box(
                rx.text(
                    "TÉCNICO SUPERIOR EN",
                    size="1",
                    color="rgba(255,255,255,0.7)",
                ),
                rx.heading(carrera["nombre_corto"], size="6", color="#ffffff"),
            ),
            enlace_navegacion(
                EstadoInstitucional.url_detalle_carrera_destacada,
                rx.icon(
                    "image_upscale",
                    size=20,
                    color=carrera["color_principal"],
                    margin_left="0.125rem",
                ),
                height="2.75rem",
                width="2.75rem",
                border_radius="9999px",
                background="#ffffff",
                display="flex",
                align_items="center",
                justify_content="center",
                box_shadow="0 10px 25px -5px rgb(37 99 235 / 0.25)",
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
            background="linear-gradient(to top, rgba(0,0,0,0.6), transparent)",
        ),

        position="relative",
        width="100%",
        height="18rem",
        border_radius="1.5rem",
        overflow="hidden",
        border="2px solid " + carrera["color_principal"] + "44",
        box_shadow="0 20px 40px -10px " + carrera["color_principal"] + "55",
    )


# ======================================================================
# Pastilla selector de carrera destacada
# ======================================================================

def pastilla_carrera_destacada(carrera: dict) -> rx.Component:
    """Pastilla seleccionable para elegir la carrera destacada en el home."""
    esta_activa = EstadoInstitucional.id_carrera_destacada == carrera["id"]

    return contenedor_clicable(
        rx.box(
            rx.icon(
                carrera["icono"],
                size=26,
                color=rx.cond(esta_activa, "#ffffff", carrera["color_principal"]),
            ),
            padding="0.75rem",
            background=rx.cond(esta_activa, carrera["color_principal"], "transparent"),
            border=f"1px solid {carrera['color_principal']}",
            border_radius="1rem",
            box_shadow=rx.cond(
                esta_activa,
                f"0 10px 25px -5px {carrera['color_principal']}66",
                "none",
            ),
            transition="all 0.2s",
            display="flex",
        ),
        rx.text(
            carrera["nombre_corto"],
            size="1",
            color=rx.cond(esta_activa, carrera["color_principal"], "gray"),
            margin_top="0.375rem",
        ),
        al_hacer_clic=lambda: EstadoInstitucional.seleccionar_carrera_destacada(carrera["id"]),
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
    """
    carrera = EstadoInstitucional.carrera_destacada
    color_principal = carrera["color_principal"]

    return rx.box(
        # --- Badge "CARRERA DESTACADA" ---
        rx.flex(
            rx.icon("star", size=12, color="#ffffff"),
            rx.text(
                "CARRERA DESTACADA",
                font_size="0.625rem",
                font_weight="800",
                color="#ffffff",
                letter_spacing="0.1em",
            ),
            align="center",
            gap="0.375rem",
            background=color_principal,
            padding="0.375rem 0.75rem",
            border_radius="9999px",
            width="fit-content",
            box_shadow=f"0 4px 12px -2px {color_principal}66",
            margin_bottom="1rem",
        ),
        # --- Título grande ---
        rx.heading(
            carrera["nombre"],
            size="8",
            color=rx.color_mode_cond(light="#0f172a", dark="#f1f5f9"),
        ),
        # --- Lema ---
        rx.text(
            carrera["lema"],
            font_size="1rem",
            color=rx.color_mode_cond(light="#475569", dark="#94a3b8"),
            margin_top="0.5rem",
        ),
        # --- CTA ---
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
            color="#ffffff",
            padding="0.75rem 1.5rem",
            border_radius="9999px",
            width="fit-content",
            box_shadow=f"0 10px 25px -5px {color_principal}66",
            transition="all 0.2s",
            _hover={
                "transform": "translateY(-2px)",
                "box_shadow": f"0 15px 35px -5px {color_principal}88",
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