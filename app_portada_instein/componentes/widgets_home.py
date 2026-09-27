"""
Widgets que componen la página de inicio (hero, carrera destacada,
tarjeta de resumen multimedia con iconos orbitando elípticamente,
fondo estrellado y líneas de fuga radiales, CTA, etc.).
"""

import random

import reflex as rx

from app_portada_instein.componentes.primitivos import (
    contenedor_clicable,
    enlace_navegacion,
)
from app_portada_instein.dominio.estado_institucional import EstadoInstitucional


# ======================================================================
# Estrellas de fondo (posiciones precalculadas, reproducibles)
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
    """
    Renderiza una estrella individual del fondo.

    En modo claro usa color oscuro (para contraste con fondo claro);
    en modo oscuro usa color blanco.
    """
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
# Líneas de fuga radiales (16 rayos desde el centro)
# ======================================================================

def _linea_fuga(angulo: int, color_claro: str) -> rx.Component:
    """
    Renderiza una línea de fuga radial desde el centro del contenedor.

    En modo claro usa un color tenue oscuro; en modo oscuro usa el
    color principal de la carrera con opacidad media.
    """
    return rx.box(
        position="absolute",
        top="50%",
        left="50%",
        width="150%",
        height="1px",
        background=rx.color_mode_cond(
            light="#94a3b8",
            dark=color_claro,
        ),
        opacity=rx.color_mode_cond(light="0.15", dark="0.25"),
        transform_origin="0 50%",
        transform=f"translate(0, -50%) rotate({angulo}deg)",
        z_index="1",
        pointer_events="none",
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
                "0 10px 25px -5px rgb(37 99 235 / 0.25)",
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
    """Texto descriptivo (nombre, lema y CTA) de la carrera destacada."""
    return rx.box(
        rx.heading(EstadoInstitucional.carrera_destacada["nombre"], size="8"),
        rx.text(
            EstadoInstitucional.carrera_destacada["lema"],
            color_scheme="gray",
        ),
        enlace_navegacion(
            "/carreras",
            rx.text(
                "Explorar Carreras",
                as_="span",
                font_size="0.875rem",
                font_weight="700",
            ),
            rx.icon("layout-grid", size=16, color=rx.color("accent", 11)),
            display="flex",
            align_items="center",
            gap="0.5rem",
            margin_top="1rem",
            background=rx.color("accent", 1),
            color=rx.color("accent", 11),
            padding="0.625rem 1.25rem",
            border_radius="9999px",
            width="fit-content",
            box_shadow="0 10px 25px -5px rgb(37 99 235 / 0.25)",
            transition="transform 0.2s",
        ),
        padding="1.25rem 1.5rem 1rem 1.5rem",
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

    - NO rota sobre su propio eje.
    - Sigue su propia órbita con excentricidad y perspectiva únicas.
    - Puede tener anillos (si `tiene_anillos=True`) mediante rx.cond.
    - NO tiene efecto wobble: orbita suavemente.
    """
    periodo = icono_animado["periodo"]
    keyframe_orbita = icono_animado["keyframe_orbita"]
    desfase = icono_animado["desfase_temporal"]
    color_icono = icono_animado["color"]
    tiene_anillos = icono_animado["tiene_anillos"]

    return rx.box(
        # --- Icono con decoración condicional de anillos ---
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
        # --- Contenedor con la animación orbital elíptica ---
        position="absolute",
        top="50%",
        left="50%",
        transform_origin="center center",
        animation=f"{keyframe_orbita} {periodo}s linear {desfase}s infinite",
        z_index="20",
    )


# ======================================================================
# Contenedor orbital completo (fondo espacial + iconos + imagen central)
# ======================================================================

def _contenedor_animacion_orbital(carrera: dict) -> rx.Component:
    """
    Contenedor que ocupa TODO el espacio de la tarjeta con:
    - Fondo espacial adaptativo al modo claro/oscuro (estrellas + líneas).
    - Iconos orbitando libremente.
    - Imagen central (el "Sol").

    El fondo espacial YA NO es circular, se extiende por toda la tarjeta.
    """
    color_principal = carrera["color_principal"]
    color_suave = carrera["color_suave"]

    # Precalculamos los ángulos de las líneas de fuga (16 rayos)
    angulos_lineas = [i * 22.5 for i in range(16)]

    return rx.box(
        # ==============================================================
        # CAPA 1: Fondo espacial (ocupa toda la tarjeta)
        # ==============================================================
        rx.box(
            # --- Estrellas de fondo ---
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

            # --- Líneas de fuga radiales ---
            rx.box(
                *[
                    _linea_fuga(angulo, color_principal)
                    for angulo in angulos_lineas
                ],
                position="absolute",
                top="0",
                left="0",
                right="0",
                bottom="0",
                z_index="1",
                pointer_events="none",
            ),

            # --- Halo radial del color de la carrera ---
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

            # --- Fondo base: adaptativo al modo claro/oscuro ---
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
        # CAPA 3: Imagen central (el "Sol")
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
        # CONTENEDOR PRINCIPAL (ocupa todo, fondo completo)
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
    Tarjeta principal del home.

    Ahora el fondo espacial ocupa TODO el contenedor rectangular
    de la tarjeta (no solo un círculo interior).
    """
    carrera = EstadoInstitucional.carrera_destacada

    return rx.box(
        # --- Contenedor orbital que ocupa todo el espacio ---
        _contenedor_animacion_orbital(carrera),

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
                    color=rx.color_mode_cond(
                        light=carrera["color_principal"],
                        dark=carrera["color_principal"],
                    ),
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

        # --- Contenedor de la tarjeta: ocupa TODO el ancho disponible ---
        position="relative",
        width="100%",
        height="28rem",
        border_radius="1.5rem",
        overflow="hidden",
        border="1px solid " + carrera["color_principal"] + "44",
        box_shadow="0 20px 40px -10px " + carrera["color_principal"] + "55",
    )


# ======================================================================
# Hero completo del home
# ======================================================================

def hero_bienvenida() -> rx.Component:
    """Sección hero del home con carrera destacada y selector."""
    return rx.box(
        rx.flex(
            rx.flex(
                rx.box(
                    height="0.5rem",
                    width="0.5rem",
                    border_radius="9999px",
                    background="#22c55e",
                ),
                rx.text("INSCRIPCIONES ABIERTAS", size="1"),
                align="center",
                gap="0.5rem",
                border=f"1px solid {rx.color('accent', 8)}",
                border_radius="9999px",
                padding="0.375rem 0.75rem",
                width="fit-content",
                box_shadow="0 1px 2px 0 rgb(0 0 0 / 0.05)",
            ),
            rx.text("Gestión 2026", size="1", color_scheme="gray"),
            align="center",
            justify="between",
            padding="1.5rem 1.5rem 1rem 1.5rem",
        ),
        rx.flex(
            rx.box(
                bloque_texto_carrera_destacada(),
                width=["100%", "100%", "100%", "40%"],
            ),
            rx.box(
                cuadro_resumen_multimedia(),
                width=["100%", "100%", "100%", "60%"],
            ),
            width="100%",
            justify="center",
            align="center",
            flex_direction=[
                "column-reverse",
                "column-reverse",
                "column-reverse",
                "row",
            ],
        ),
        rx.box(
            rx.flex(
                rx.text(
                    "Elige una carrera",
                    color_scheme="gray",
                    size="1",
                    text_transform="uppercase",
                ),
                rx.text(
                    (EstadoInstitucional.id_carrera_destacada + 1).to_string()
                    + " / "
                    + EstadoInstitucional.carreras.length().to_string(),
                    color_scheme="gray",
                    size="1",
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
        ),
    )