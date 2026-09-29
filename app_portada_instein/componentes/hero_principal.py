"""
Hero principal del home con sistema completo de capas.

Capas (de fondo a frente):
- CAPA -1: Imagen de fondo (fondo_hero.png).
- CAPA 0: Overlay de gradiente para legibilidad.
- CAPA 1: Líneas luminosas diagonales.
- CAPA 2: Iconos flotantes (partículas).
- CAPA 3: Contenido principal (título, CTA, explorador).

Sistema de color (UX)
---------------------
- Fondo: imagen + overlay con `rgba` intencionales para legibilidad.
- Acentos (badge "INSCRIPCIONES", span del título, CTA primario,
  trust badges, líneas luminosas): accent institucional (crimson).
- Textos: neutros (`gray-11`/`gray-12`).
- Partículas decorativas: `gray-11` con baja opacidad.
- Punto de "inscripciones abiertas": `green-8` (semántico).
"""

import random

import reflex as rx

from app_portada_instein.componentes.explorador.explorador import (
    explorador_carrera_destacada,
)
from app_portada_instein.componentes.primitivos import enlace_navegacion
from app_portada_instein.infraestructura.constantes_visuales import (
    COLOR_ACENTO_BORDE,
    COLOR_ACENTO_SOLIDO,
    COLOR_ACENTO_TEXTO,
    COLOR_BORDE_SUAVE,
    COLOR_FONDO_CARTA,
    COLOR_TEXTO_PRINCIPAL,
    COLOR_TEXTO_SECUNDARIO,
    RADIO_PASTILLA,
    SOMBRA_CAJA,
    SOMBRA_FUERTE,
)


# ======================================================================
# Catálogo de iconos para las partículas
# ======================================================================

ICONOS_PARTICULAS: list[str] = [
    # Sistemas Informáticos
    "cpu", "code-2", "database", "wifi", "terminal", "binary", "hard-drive",
    # Contaduría General
    "calculator", "receipt", "coins", "chart-line", "wallet", "trending-up",
    # Secretariado Ejecutivo
    "briefcase", "calendar-clock", "mail", "users", "file-text", "clipboard-list",
    # Comercio Internacional
    "globe", "ship", "package", "truck", "plane",
    # Electrónica
    "zap", "circuit-board", "radio", "plug-zap", "settings",
    # Académicos generales
    "graduation-cap", "book-open", "award", "lightbulb", "target", "rocket",
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

# Opacidad de las partículas decorativas.
OPACIDAD_PARTICULAS = "0.4"

# Anchos de las líneas luminosas.
ANCHO_LINEA_1 = "50rem"
ANCHO_LINEA_2 = "40rem"
ANCHO_LINEA_3 = "60rem"


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

    Args:
        particula: Dict con `icono`, `x`, `y`, `tamano`, `opacidad`,
            `delay`, `duracion`, `rotacion`.
    """
    return rx.box(
        rx.icon(
            particula["icono"],
            size=particula["tamano"],
            color=COLOR_TEXTO_SECUNDARIO,
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

    Usa accent crimson. Los `rgba` internos del gradiente son
    intencionales y usan el accent sólido del tema.

    Args:
        angulo: Ángulo de rotación en grados.
        x: Posición izquierda (ej: "-10%").
        y: Posición superior (ej: "25%").
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
        background=rx.color_mode_cond(
            light=(
                f"linear-gradient(90deg, transparent, "
                f"{COLOR_ACENTO_TEXTO}, transparent)"
            ),
            dark=(
                f"linear-gradient(90deg, transparent, "
                f"{COLOR_ACENTO_SOLIDO}, transparent)"
            ),
        ),
        opacity=OPACIDAD_PARTICULAS,
        transform=f"rotate({angulo}deg)",
        filter="blur(1px)",
        box_shadow=f"0 0 10px {COLOR_ACENTO_TEXTO}",
        animation=f"deslizar_linea {duracion}s linear {delay}s infinite",
        pointer_events="none",
    )


def _capa_lineas_luminosas() -> rx.Component:
    """Capa con 3 líneas luminosas diagonales distribuidas."""
    return rx.box(
        _linea_luminosa(-30, "-10%", "25%", ANCHO_LINEA_1, 0.0, 8.0),
        _linea_luminosa(45, "60%", "10%", ANCHO_LINEA_2, 2.0, 10.0),
        _linea_luminosa(-60, "30%", "80%", ANCHO_LINEA_3, 4.0, 12.0),
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

    Los `rgba` son intencionales: el overlay se aplica SOBRE la imagen
    del hero, no sobre el fondo del tema. Los valores están calibrados
    para máxima legibilidad del texto en ambos modos.
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
            dark=(
                "linear-gradient(180deg, "
                "rgba(5, 4, 10, 0.5) 0%, "
                "rgba(5, 4, 10, 0.9) 100%)"
            ),
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
    como fallback. Los colores son hex intencionales porque el fondo
    está pensado para combinarse con el overlay.
    """
    return rx.box(
        background_image="url('/fondo_hero.png')",
        background_size="cover",
        background_position="center",
        background_repeat="repeat",
        background_color=rx.color_mode_cond(
            light="#f8fafc",
            dark="#05040a",
        ),
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

    Args:
        icono: Nombre del icono de Lucide.
        etiqueta: Texto visible del badge.
    """
    return rx.flex(
        rx.icon(icono, size=14, color=COLOR_ACENTO_TEXTO),
        rx.text(
            etiqueta,
            font_size="0.75rem",
            font_weight="600",
            color=COLOR_TEXTO_SECUNDARIO,
        ),
        align="center",
        gap="0.4rem",
        padding="0.5rem 0.875rem",
        border_radius=RADIO_PASTILLA,
        background=COLOR_FONDO_CARTA,
        border=f"1px solid {COLOR_BORDE_SUAVE}",
        backdrop_filter="blur(12px)",
    )


# ======================================================================
# Contenido principal: Badge de inscripciones
# ======================================================================


def _badge_inscripciones_abiertas() -> rx.Component:
    """
    Badge con punto verde pulsante + texto "INSCRIPCIONES ABIERTAS".

    Usa `green-8` para el punto (semántico de éxito/activo) y
    fondo neutro para el resto.
    """
    return rx.flex(
        rx.box(
            height="0.5rem",
            width="0.5rem",
            border_radius=RADIO_PASTILLA,
            background=rx.color("green", 8),
            animation="pulse 2s ease-in-out infinite",
        ),
        rx.text(
            "INSCRIPCIONES ABIERTAS · GESTIÓN 2026",
            font_size="0.75rem",
            font_weight="700",
            color=COLOR_TEXTO_PRINCIPAL,
            letter_spacing="0.05em",
        ),
        align="center",
        gap="0.5rem",
        padding="0.5rem 1rem",
        border_radius=RADIO_PASTILLA,
        background=COLOR_FONDO_CARTA,
        border=f"1px solid {COLOR_BORDE_SUAVE}",
        backdrop_filter="blur(12px)",
        box_shadow=SOMBRA_CAJA,
    )


# ======================================================================
# Contenido principal: CTA dual
# ======================================================================


def _cta_primario() -> rx.Component:
    """CTA primario 'Ver Carreras' con accent sólido."""
    return enlace_navegacion(
        "/carreras",
        rx.icon("graduation-cap", size=18),
        rx.text("Ver Carreras", as_="span", font_weight="700"),
        display="flex",
        align_items="center",
        gap="0.5rem",
        background=COLOR_ACENTO_SOLIDO,
        color="white",
        padding="0.875rem 1.75rem",
        border_radius=RADIO_PASTILLA,
        font_size="0.9375rem",
        box_shadow=SOMBRA_FUERTE,
        transition="all 0.2s",
        _hover={
            "transform": "translateY(-2px)",
            "filter": "brightness(1.1)",
        },
    )


def _cta_secundario() -> rx.Component:
    """CTA secundario 'Conocer más' con fondo neutro y borde sutil."""
    return enlace_navegacion(
        "/contacto",
        rx.icon("message_circle", size=18),
        rx.text("Conocer más", as_="span", font_weight="600"),
        display="flex",
        align_items="center",
        gap="0.5rem",
        background=COLOR_FONDO_CARTA,
        color=COLOR_TEXTO_PRINCIPAL,
        padding="0.875rem 1.75rem",
        border_radius=RADIO_PASTILLA,
        font_size="0.9375rem",
        border=f"1px solid {COLOR_BORDE_SUAVE}",
        backdrop_filter="blur(12px)",
        transition="all 0.2s",
        _hover={
            "transform": "translateY(-2px)",
            "border_color": COLOR_ACENTO_BORDE,
        },
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
        rx.box(
            _badge_inscripciones_abiertas(),
            margin_bottom="1.5rem",
        ),
        # --- Título principal (con span en accent) ---
        rx.heading(
            "Forja tu futuro como ",
            rx.text.span(
                "Técnico Superior",
                color=COLOR_ACENTO_TEXTO,
            ),
            "",
            size="9",
            text_align="center",
            font_weight="900",
            letter_spacing="-0.03em",
            line_height="1.1",
            color=COLOR_TEXTO_PRINCIPAL,
            max_width="48rem",
        ),
        # --- Subtítulo ---
        rx.text(
            "Formación técnica de excelencia con títulos de Provisión "
            "Nacional. 5 carreras, equipamiento moderno y docentes "
            "especializados.",
            font_size=["1rem", "1.125rem", "1.25rem"],
            text_align="center",
            color=COLOR_TEXTO_SECUNDARIO,
            max_width="42rem",
            line_height="1.6",
            margin_top="1rem",
        ),
        # --- CTA dual ---
        rx.flex(
            _cta_primario(),
            _cta_secundario(),
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
        # CAPA -1: Imagen de fondo
        _capa_imagen_fondo(),
        # CAPA 0: Overlay de gradiente
        _capa_overlay_gradiente(),
        # CAPA 1: Líneas luminosas diagonales
        _capa_lineas_luminosas(),
        # CAPA 2: Iconos flotantes (partículas)
        _capa_iconos_particulas(),
        # CAPA 3: Contenido principal
        rx.vstack(
            _hero_titulo_y_cta(),
            explorador_carrera_destacada(),
            width="100%",
            align="center",
            spacing="0",
            position="relative",
            z_index="2",
        ),
        # Contenedor principal
        position="relative",
        width="100%",
        overflow="hidden",
        min_height="100vh",
    )


__all__ = ["hero_principal"]