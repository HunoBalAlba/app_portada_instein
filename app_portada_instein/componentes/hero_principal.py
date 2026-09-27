"""
Hero principal del home con sistema completo de capas.

Capas (de fondo a frente):
- CAPA -1: Imagen de fondo (fondo_hero.png).
- CAPA 0: Overlay de gradiente para legibilidad.
- CAPA 1: Líneas luminosas diagonales + iconos flotantes.
- CAPA 2: Contenido principal (título, CTA, explorador de carrera).

Usa constantes de `styles.py` para mantener consistencia visual.
"""

import random

import reflex as rx

from app_portada_instein.componentes.explorador_carrera import (
    explorador_carrera_destacada,
)
from app_portada_instein.componentes.primitivos import enlace_navegacion
from app_portada_instein.styles import (
    SOMBRA_CAJA,
    SOMBRA_FUERTE,
)


# ======================================================================
# Catálogo de iconos para las partículas
# ======================================================================

ICONOS_PARTICULAS: list[str] = [
    # Sistemas Informáticos
    "cpu",
    "code-2",
    "database",
    "wifi",
    "terminal",
    "binary",
    "hard-drive",
    # Contaduría General
    "calculator",
    "receipt",
    "coins",
    "chart-line",
    "wallet",
    "trending-up",
    # Secretariado Ejecutivo
    "briefcase",
    "calendar-clock",
    "mail",
    "users",
    "file-text",
    "clipboard-list",
    # Comercio Internacional
    "globe",
    "ship",
    "package",
    "truck",
    "plane",
    # Electrónica
    "zap",
    "circuit-board",
    "radio",
    "plug-zap",
    "settings",
    # Académicos generales
    "graduation-cap",
    "book-open",
    "award",
    "lightbulb",
    "target",
    "rocket",
]


# ======================================================================
# Configuración de las partículas
# ======================================================================

CANTIDAD_PARTICULAS = 45
SEMILLA_PARTICULAS = 42
TAMANOS_PARTICULAS = [14, 18, 20, 24, 28, 32]
OPACIDAD_MINIMA = 0.15
OPACIDAD_MAXIMA = 0.35
DURACION_MINIMA = 4.0
DURACION_MAXIMA = 8.0
ROTACION_MINIMA = -25
ROTACION_MAXIMA = 25


def _generar_iconos_particulas(
    cantidad: int = CANTIDAD_PARTICULAS,
    semilla: int = SEMILLA_PARTICULAS,
) -> list[dict]:
    """
    Genera partículas basadas en iconos de carreras.

    Cada partícula es un icono de Lucide con posición, tamaño, opacidad,
    duración y rotación aleatorias pero reproducibles (semilla fija).

    Args:
        cantidad: Número de partículas a generar.
        semilla: Semilla para reproducibilidad.

    Returns:
        Lista de dicts con la configuración de cada partícula.
    """
    rng = random.Random(semilla)
    return [
        {
            "icono": rng.choice(ICONOS_PARTICULAS),
            "x": rng.uniform(0, 100),
            "y": rng.uniform(0, 100),
            "tamano": rng.choice(TAMANOS_PARTICULAS),
            "opacidad": rng.uniform(OPACIDAD_MINIMA, OPACIDAD_MAXIMA),
            "delay": rng.uniform(0, 5),
            "duracion": rng.uniform(DURACION_MINIMA, DURACION_MAXIMA),
            "rotacion": rng.uniform(ROTACION_MINIMA, ROTACION_MAXIMA),
        }
        for _ in range(cantidad)
    ]


ICONOS_PARTICULAS_FONDO = _generar_iconos_particulas()


# ======================================================================
# CAPA 2: Partículas (iconos flotantes)
# ======================================================================


def _icono_particula(particula: dict) -> rx.Component:
    """
    Renderiza un icono de carrera como partícula flotante en gris.

    El icono tiene:
    - Color gris adaptativo al modo claro/oscuro.
    - Opacidad baja para no competir con el contenido.
    - Animación de flotación + titileo.
    - Rotación inicial sutil.
    """
    return rx.box(
        rx.icon(
            particula["icono"],
            size=particula["tamano"],
            color=rx.color_mode_cond(light="#64748b", dark="#94a3b8"),
        ),
        position="absolute",
        left=f"{particula['x']}%",
        top=f"{particula['y']}%",
        opacity=f"{particula['opacidad']}",
        style={"--rotacion": f"{particula['rotacion']}deg"},
        animation=(
            f"flotar_icono_particula {particula['duracion']}s ease-in-out "
            f"{particula['delay']}s infinite"
        ),
        pointer_events="none",
    )


def _capa_iconos_particulas() -> rx.Component:
    """
    Capa con todos los iconos flotando como partículas.

    Se posiciona absolutamente sobre el contenedor principal con
    z_index=1 (debajo del contenido principal que tiene z_index=2).
    """
    return rx.box(
        *[_icono_particula(p) for p in ICONOS_PARTICULAS_FONDO],
        position="absolute",
        top="0",
        left="0",
        right="0",
        bottom="0",
        overflow="hidden",
        pointer_events="none",
        z_index="1",
    )


# ======================================================================
# CAPA 1: Líneas luminosas diagonales
# ======================================================================


def _linea_luminosa(
    angulo: int,
    x: str,
    y: str,
    ancho: str,
    delay: float = 0.0,
    duracion: float = 6.0,
) -> rx.Component:
    """
    Línea luminosa diagonal sutil.

    Args:
        angulo: Ángulo de rotación en grados.
        x, y: Posición absoluta.
        ancho: Ancho de la línea (ej: "50rem").
        delay: Retraso de la animación.
        duracion: Duración de una vuelta completa.
    """
    return rx.box(
        position="absolute",
        left=x,
        top=y,
        width=ancho,
        height="1px",
        background="linear-gradient(90deg, transparent, #a855f7, transparent)",
        opacity="0.4",
        transform=f"rotate({angulo}deg)",
        filter="blur(1px)",
        box_shadow="0 0 10px #a855f7",
        animation=f"deslizar_linea {duracion}s linear {delay}s infinite",
        pointer_events="none",
    )


def _capa_lineas_luminosas() -> rx.Component:
    """Capa con líneas luminosas diagonales distribuidas."""
    return rx.box(
        _linea_luminosa(-30, "-10%", "25%", "50rem", 0.0, 8.0),
        _linea_luminosa(45, "60%", "10%", "40rem", 2.0, 10.0),
        _linea_luminosa(-60, "30%", "80%", "60rem", 4.0, 12.0),
        position="absolute",
        top="0",
        left="0",
        right="0",
        bottom="0",
        overflow="hidden",
        pointer_events="none",
        z_index="1",
    )


# ======================================================================
# CAPA 0: Overlay de gradiente
# ======================================================================


def _capa_overlay_gradiente() -> rx.Component:
    """
    Overlay de gradiente para garantizar legibilidad del contenido
    sobre la imagen de fondo, adaptativo al modo claro/oscuro.
    """
    return rx.box(
        position="absolute",
        top="0",
        left="0",
        right="0",
        bottom="0",
        background=rx.color_mode_cond(
            light=(
                "linear-gradient(180deg, "
                "rgba(248, 250, 252, 0.75) 0%, "
                "rgba(248, 250, 252, 0.9) 100%)"
            ),
            dark=("linear-gradient(180deg, rgba(5, 4, 10, 0.5) 0%, rgba(5, 4, 10, 0.9) 100%)"),
        ),
        pointer_events="none",
        z_index="0",
    )


# ======================================================================
# CAPA -1: Imagen de fondo
# ======================================================================


def _capa_imagen_fondo() -> rx.Component:
    """
    Imagen de fondo del hero (assets/fondo_hero.png).

    Si la imagen no existe, se muestra el color de fondo adaptativo
    como fallback.
    """
    return rx.box(
        background_image="url('/fondo_hero.png')",
        background_size="cover",
        background_position="center",
        background_repeat="no-repeat",
        background_color=rx.color_mode_cond(light="#f8fafc", dark="#05040a"),
        position="absolute",
        top="0",
        left="0",
        right="0",
        bottom="0",
        z_index="-1",
    )


# ======================================================================
# Contenido principal: Trust badges
# ======================================================================


def _trust_badge(icono: str, etiqueta: str) -> rx.Component:
    """
    Badge individual con icono + texto para mostrar credenciales.

    Usado para comunicar:
    - Resolución ministerial vigente.
    - Título de Provisión Nacional.
    - Cantidad de egresados.
    - Empleabilidad.
    """
    return rx.flex(
        rx.icon(icono, size=14, color=rx.color("accent", 11)),
        rx.text(
            etiqueta,
            font_size="0.75rem",
            font_weight="600",
            color=rx.color_mode_cond(light="#334155", dark="#cbd5e1"),
        ),
        align="center",
        gap="0.4rem",
        padding="0.5rem 0.875rem",
        border_radius="9999px",
        background=rx.color_mode_cond(
            light="rgba(255,255,255,0.75)",
            dark="rgba(15,17,23,0.75)",
        ),
        border="1px solid " + rx.color_mode_cond(light="#e2e8f0", dark="#1e293b"),
        backdrop_filter="blur(12px)",
    )


# ======================================================================
# Contenido principal: Título + CTA
# ======================================================================


def _hero_titulo_y_cta() -> rx.Component:
    """
    Bloque superior del hero con:
    - Badge de inscripciones abiertas.
    - Título principal grande.
    - Subtítulo.
    - CTA dual (primario + secundario).
    - Trust badges con credenciales.
    """
    return rx.vstack(
        # --- Badge de inscripciones abiertas ---
        rx.flex(
            rx.box(
                height="0.5rem",
                width="0.5rem",
                border_radius="9999px",
                background="#22c55e",
                animation="pulse 2s ease-in-out infinite",
            ),
            rx.text(
                "INSCRIPCIONES ABIERTAS · GESTIÓN 2026",
                font_size="0.75rem",
                font_weight="700",
                color=rx.color_mode_cond(light="#0f172a", dark="#f1f5f9"),
                letter_spacing="0.05em",
            ),
            align="center",
            gap="0.5rem",
            padding="0.5rem 1rem",
            border_radius="9999px",
            background=rx.color_mode_cond(
                light="rgba(255,255,255,0.9)",
                dark="rgba(15,17,23,0.9)",
            ),
            border="1px solid " + rx.color_mode_cond(light="#e2e8f0", dark="#1e293b"),
            backdrop_filter="blur(12px)",
            box_shadow=SOMBRA_CAJA,
            margin_bottom="1.5rem",
        ),
        # --- Título principal ---
        rx.heading(
            "Forja tu futuro como ",
            rx.text.span("Técnico Superior", color=rx.color("accent", 11)),
            "",
            size="9",
            text_align="center",
            font_weight="900",
            letter_spacing="-0.03em",
            line_height="1.1",
            color=rx.color_mode_cond(light="#0f172a", dark="#f1f5f9"),
            max_width="48rem",
        ),
        # --- Subtítulo ---
        rx.text(
            "Formación técnica de excelencia con títulos de Provisión Nacional. "
            "5 carreras, equipamiento moderno y docentes especializados.",
            font_size=["1rem", "1.125rem", "1.25rem"],
            text_align="center",
            color=rx.color_mode_cond(light="#475569", dark="#cbd5e1"),
            max_width="42rem",
            line_height="1.6",
            margin_top="1rem",
        ),
        # --- CTA dual ---
        rx.flex(
            # CTA primario: Ver Carreras
            enlace_navegacion(
                "/carreras",
                rx.icon("graduation-cap", size=18),
                rx.text("Ver Carreras", as_="span", font_weight="700"),
                display="flex",
                align_items="center",
                gap="0.5rem",
                background=rx.color("accent", 11),
                color="#ffffff",
                padding="0.875rem 1.75rem",
                border_radius="9999px",
                font_size="0.9375rem",
                box_shadow=SOMBRA_FUERTE,
                transition="all 0.2s",
                _hover={
                    "transform": "translateY(-2px)",
                    "box_shadow": "0 15px 35px -5px rgba(37, 99, 235, 0.5)",
                },
            ),
            # CTA secundario: Conocer más
            enlace_navegacion(
                "/contacto",
                rx.icon("message-circle", size=18),
                rx.text("Conocer más", as_="span", font_weight="600"),
                display="flex",
                align_items="center",
                gap="0.5rem",
                background=rx.color_mode_cond(
                    light="rgba(255,255,255,0.9)",
                    dark="rgba(15,17,23,0.9)",
                ),
                color=rx.color_mode_cond(light="#0f172a", dark="#f1f5f9"),
                padding="0.875rem 1.75rem",
                border_radius="9999px",
                font_size="0.9375rem",
                border="1px solid " + rx.color_mode_cond(light="#e2e8f0", dark="#334155"),
                backdrop_filter="blur(12px)",
                transition="all 0.2s",
                _hover={
                    "transform": "translateY(-2px)",
                    "border_color": rx.color("accent", 8),
                },
            ),
            gap="0.75rem",
            margin_top="2rem",
            flex_direction=["column", "row", "row"],
            align="center",
            justify="center",
        ),
        # --- Trust badges ---
        rx.flex(
            _trust_badge("award", "R.M. 0871/2016"),
            _trust_badge("shield-check", "Título Nacional"),
            _trust_badge("users", "500+ Egresados"),
            _trust_badge("trending-up", "100% Empleabilidad"),
            gap="0.5rem",
            margin_top="2.5rem",
            flex_wrap="wrap",
            justify="center",
            max_width="48rem",
        ),
        align="center",
        text_align="center",
        padding="4rem 1.5rem 2rem 1.5rem",
        position="relative",
        z_index="2",
    )


# ======================================================================
# Hero principal completo
# ======================================================================


def hero_principal() -> rx.Component:
    """
    Hero completo del home con sistema de capas apiladas.

    Orden de renderizado (de atrás hacia adelante):
    1. Imagen de fondo.
    2. Overlay de gradiente.
    3. Líneas luminosas diagonales.
    4. Iconos flotantes (partículas).
    5. Contenido principal (título + CTA + explorador).
    """
    return rx.box(
        # ==============================================================
        # CAPA -1: Imagen de fondo
        # ==============================================================
        _capa_imagen_fondo(),
        # ==============================================================
        # CAPA 0: Overlay de gradiente
        # ==============================================================
        _capa_overlay_gradiente(),
        # ==============================================================
        # CAPA 1: Líneas luminosas diagonales
        # ==============================================================
        _capa_lineas_luminosas(),
        # ==============================================================
        # CAPA 2: Iconos flotantes (partículas)
        # ==============================================================
        _capa_iconos_particulas(),
        # ==============================================================
        # CAPA 3: Contenido principal
        # ==============================================================
        rx.vstack(
            _hero_titulo_y_cta(),
            explorador_carrera_destacada(),
            width="100%",
            align="center",
            spacing="0",
            position="relative",
            z_index="2",
        ),
        # ==============================================================
        # Contenedor principal
        # ==============================================================
        position="relative",
        width="100%",
        overflow="hidden",
        min_height="100vh",
    )
