# app_portada_instein/componentes/hero_principal.py

"""
Hero principal del home — estilo Neon adaptativo (dark/light).

Capas (de fondo a frente):
- CAPA 0: Gradiente adaptativo (light: claro, dark: oscuro).
- CAPA 1: Orbes de glow azul marino en esquinas.
- CAPA 2: Partículas (iconos flotantes) en azul marino.
- CAPA 3: Contenido principal (título, CTA, trust badges, explorador).

Sistema de color (UX)
---------------------
✅ ADAPTATIVO: todos los colores respetan el color_mode del usuario.

- Fondo: `FONDO_HOME_HERO` (light: claro, dark: oscuro).
- Acentos: azul marino neon (`AZUL_MARINO_NEON` = `#3b5bdb`) en AMBOS modos.
- Texto: `TEXTO_HOME_PRINCIPAL` / `TEXTO_HOME_MAS_SUAVE`.
- Bordes: `BORDE_HOME_AZUL` / `BORDE_HOME_MEDIO` / `BORDE_HOME_SUAVE`.
- Badges: glassmorphism con borde azul marino translúcido.
- Punto de "inscripciones abiertas": verde semántico (`#22c55e`).
- Título: gradiente adaptativo (`GRADIENTE_TEXTO_HOME`).

Estilo Neon:
- Tipografía masiva (`size="9"`, `font_weight="900"`).
- Espaciado generoso (`padding="6rem 1.5rem 4rem 1.5rem"`).
- Glassmorphism (blur + bordes translúcidos).
- Orbes de glow en las esquinas para dar profundidad.
- Partículas decorativas de baja opacidad.

Notas técnicas:
- `rx.icon(size=...)` NO acepta `rx.breakpoints(...)` — solo int fijo.
- Las opacidades de partículas y orbes son mayores en dark (más
  contraste) y menores en light (evitar saturación).
"""

import random

import reflex as rx

from app_portada_instein.componentes.explorador.explorador import (
    explorador_carrera_destacada,
)
from app_portada_instein.componentes.primitivos import enlace_navegacion
from app_portada_instein.infraestructura.constantes_visuales import (
    AZUL_MARINO_NEON,
    BORDE_HOME_AZUL,
    BORDE_HOME_MEDIO,
    BORDE_HOME_SUAVE,
    FONDO_AZUL_MUY_SUAVE,
    FONDO_AZUL_SUAVE,
    FONDO_HOME_HERO,
    GRADIENTE_TEXTO_HOME,
    RADIO_PASTILLA,
    TEXTO_HOME_MAS_SUAVE,
    TEXTO_HOME_PRINCIPAL,
    TEXTO_HOME_SUAVE,
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
    "briefcase", "calendar-clock", "mail", "users", "file-text",
    "clipboard-list",
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

CANTIDAD_PARTICULAS = 50
SEMILLA_PARTICULAS = 42
TAMANOS_PARTICULAS = [14, 18, 20, 24, 28, 32]

# Opacidades (más sutiles que antes para no saturar sobre fondo claro)
OPACIDAD_MINIMA = 0.08
OPACIDAD_MAXIMA = 0.20

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
    Renderiza un icono de carrera como partícula flotante en azul marino.

    El icono tiene:
    - Color azul marino neon (`AZUL_MARINO_NEON`).
    - Opacidad baja para no competir con el contenido.
    - Animación de flotación + titileo.
    - Rotación inicial sutil.

    ✅ ADAPTATIVO: en light mode la opacidad es menor (0.5x) para
    evitar saturación sobre fondo claro.

    Args:
        particula: Dict con `icono`, `x`, `y`, `tamano`, `opacidad`,
            `delay`, `duracion`, `rotacion`.
    """
    return rx.box(
        rx.icon(
            particula["icono"],
            size=particula["tamano"],
            color=AZUL_MARINO_NEON,
        ),
        position="absolute",
        left=f"{particula['x']}%",
        top=f"{particula['y']}%",
        opacity=rx.color_mode_cond(
            light=f"{particula['opacidad'] * 0.5}",   # 50% en light
            dark=f"{particula['opacidad']}",
        ),
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
# CAPA 1: Orbes de glow azul marino
# ======================================================================


def _orbes_glow() -> rx.Component:
    """
    Orbes de glow azul marino en las esquinas del hero.

    Estilo Neon: dos orbes radiales grandes con blur profundo en las
    esquinas opuestas (superior derecha e inferior izquierda) para
    dar profundidad visual y sensación de "luz ambiental".

    ✅ ADAPTATIVO: en light mode la opacidad es menor (evita que el
    fondo claro se sature de azul).

    Los orbes no son interactivos (`pointer_events="none"`) y están
    por debajo del contenido principal (`z_index="0"`).
    """
    return rx.fragment(
        # Orbe superior derecha (azul marino neon)
        rx.box(
            position="absolute",
            top="-30%",
            right="-15%",
            width="60%",
            height="100%",
            background=(
                f"radial-gradient(circle, {AZUL_MARINO_NEON} 0%, "
                f"transparent 60%)"
            ),
            opacity=rx.color_mode_cond(
                light="0.12",   # sutil en light
                dark="0.25",
            ),
            filter="blur(80px)",
            z_index="0",
            pointer_events="none",
        ),
        # Orbe inferior izquierda (azul marino profundo)
        rx.box(
            position="absolute",
            bottom="-30%",
            left="-15%",
            width="60%",
            height="100%",
            background=(
                "radial-gradient(circle, #1a237e 0%, transparent 60%)"
            ),
            opacity=rx.color_mode_cond(
                light="0.15",
                dark="0.30",
            ),
            filter="blur(80px)",
            z_index="0",
            pointer_events="none",
        ),
    )


# ======================================================================
# Contenido principal: Badge de inscripciones
# ======================================================================


def _badge_inscripciones_abiertas() -> rx.Component:
    """
    Badge con punto verde pulsante + texto "INSCRIPCIONES ABIERTAS".

    Usa `#22c55e` (verde semántico) para el punto y glassmorphism
    con borde azul marino translúcido para el contenedor.

    ✅ ADAPTATIVO: fondo azul más suave en light mode.
    """
    return rx.flex(
        rx.box(
            height="0.5rem",
            width="0.5rem",
            border_radius=RADIO_PASTILLA,
            background="#22c55e",
            animation="pulse 2s ease-in-out infinite",
            box_shadow="0 0 12px #22c55e",
            flex_shrink="0",
        ),
        rx.text(
            "INSCRIPCIONES ABIERTAS · GESTIÓN 2026",
            font_size="0.75rem",
            font_weight="700",
            color=TEXTO_HOME_PRINCIPAL,
            letter_spacing="0.1em",
        ),
        align="center",
        gap="0.5rem",
        padding="0.5rem 1rem",
        border_radius=RADIO_PASTILLA,
        background=FONDO_AZUL_SUAVE,
        border=f"1px solid {BORDE_HOME_AZUL}",
        backdrop_filter="blur(12px)",
        width="fit-content",
    )


# ======================================================================
# Contenido principal: CTA dual
# ======================================================================


def _cta_primario() -> rx.Component:
    """
    CTA primario "Explorar Carreras" con azul marino neon + glow.

    Estilo Neon:
    - Fondo azul marino neon sólido.
    - Glow intenso (`box_shadow`).
    - Flecha que se desplaza en hover.

    ✅ El azul marino es el mismo en ambos modos (color de marca).
    """
    return enlace_navegacion(
        "/carreras",
        rx.text("Explorar Carreras", as_="span", font_weight="700"),
        rx.icon(
            "arrow-right",
            size=18,
            class_name="arrow-icon",
            transition="transform 0.2s",
        ),
        display="flex",
        align_items="center",
        gap="0.5rem",
        background=AZUL_MARINO_NEON,
        color="white",
        padding="1rem 2rem",
        border_radius=RADIO_PASTILLA,
        font_size="1rem",
        font_weight="700",
        box_shadow=f"0 0 40px {AZUL_MARINO_NEON}80",
        transition="all 0.2s",
        _hover={
            "transform": "translateY(-2px)",
            "box_shadow": f"0 0 60px {AZUL_MARINO_NEON}cc",
            "& .arrow-icon": {"transform": "translateX(4px)"},
        },
    )


def _cta_secundario() -> rx.Component:
    """
    CTA secundario "Conocer más" con glassmorphism.

    Estilo Neon:
    - Fondo translúcido con blur.
    - Borde adaptativo.
    - Hover: borde azul marino + fondo más opaco.

    ✅ ADAPTATIVO: fondo y borde cambian según el modo.
    """
    return enlace_navegacion(
        "/contacto",
        rx.icon("message-circle", size=18),
        rx.text("Conocer más", as_="span", font_weight="600"),
        display="flex",
        align_items="center",
        gap="0.5rem",
        background=rx.color_mode_cond(
            light="rgba(255, 255, 255, 0.6)",
            dark="rgba(255, 255, 255, 0.05)",
        ),
        color=TEXTO_HOME_PRINCIPAL,
        padding="1rem 2rem",
        border_radius=RADIO_PASTILLA,
        font_size="1rem",
        border=f"1px solid {BORDE_HOME_MEDIO}",
        backdrop_filter="blur(12px)",
        transition="all 0.2s",
        _hover={
            "background": rx.color_mode_cond(
                light="rgba(255, 255, 255, 0.9)",
                dark="rgba(255, 255, 255, 0.1)",
            ),
            "border_color": BORDE_HOME_AZUL,
        },
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

    ✅ ADAPTATIVO: fondo y borde cambian según el modo.

    Args:
        icono: Nombre del icono de Lucide.
        etiqueta: Texto visible del badge.
    """
    return rx.flex(
        rx.icon(icono, size=14, color=AZUL_MARINO_NEON),
        rx.text(
            etiqueta,
            font_size="0.75rem",
            font_weight="600",
            color=TEXTO_HOME_SUAVE,
        ),
        align="center",
        gap="0.4rem",
        padding="0.5rem 0.875rem",
        border_radius=RADIO_PASTILLA,
        background=rx.color_mode_cond(
            light="rgba(255, 255, 255, 0.7)",
            dark="rgba(255, 255, 255, 0.03)",
        ),
        border=f"1px solid {BORDE_HOME_SUAVE}",
        backdrop_filter="blur(12px)",
    )


# ======================================================================
# Contenido principal: Título + CTA
# ======================================================================


def _hero_titulo_y_cta() -> rx.Component:
    """
    Bloque superior del hero con:
    - Badge de inscripciones abiertas.
    - Título principal grande con gradiente de texto adaptativo.
    - Subtítulo.
    - CTA dual (primario + secundario).
    - Trust badges con credenciales.

    ✅ ADAPTATIVO: todos los colores respetan el color_mode.
    """
    return rx.vstack(
        # --- Badge de inscripciones abiertas ---
        rx.box(
            _badge_inscripciones_abiertas(),
            margin_bottom="1.5rem",
        ),
        # --- Título principal con gradiente adaptativo ---
        rx.heading(
            "Forja tu futuro como ",
            rx.text.span(
                "Técnico Superior",
                background=GRADIENTE_TEXTO_HOME,
                background_clip="text",
                color="transparent",
                webkit_background_clip="text",
            ),
            "",
            size="9",
            text_align="center",
            font_weight="900",
            letter_spacing="-0.04em",
            line_height="1.05",
            color=TEXTO_HOME_PRINCIPAL,
            max_width="60rem",
        ),
        # --- Subtítulo ---
        rx.text(
            "Formación técnica de excelencia con títulos de Provisión "
            "Nacional. 5 carreras, equipamiento moderno y docentes "
            "especializados.",
            font_size=["1rem", "1.125rem", "1.25rem"],
            text_align="center",
            color=TEXTO_HOME_MAS_SUAVE,
            max_width="42rem",
            line_height="1.6",
            margin_top="1.5rem",
        ),
        # --- CTA dual ---
        rx.flex(
            _cta_primario(),
            _cta_secundario(),
            gap="0.75rem",
            margin_top="2.5rem",
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
            margin_top="3rem",
            flex_wrap="wrap",
            justify="center",
            max_width="48rem",
        ),
        align="center",
        text_align="center",
        padding="6rem 1.5rem 4rem 1.5rem",
        position="relative",
        z_index="2",
        width="100%",
        max_width="72rem",
        margin="0 auto",
    )


# ======================================================================
# Hero principal completo
# ======================================================================


def hero_principal() -> rx.Component:
    """
    Hero completo del home con sistema de capas apiladas — Neon adaptativo.

    Orden de renderizado (de atrás hacia adelante):
    1. Gradiente adaptativo (light: claro, dark: oscuro).
    2. Orbes de glow azul marino en esquinas.
    3. Iconos flotantes (partículas) en azul marino.
    4. Contenido principal (título + CTA + trust badges).
    5. Explorador de carreras.

    Estilo Neon:
    - Fondo gradiente adaptativo (`FONDO_HOME_HERO`).
    - Orbes de glow para dar profundidad.
    - Partículas decorativas de baja opacidad.
    - Tipografía masiva (`size="9"`, `font_weight="900"`).
    - Espaciado generoso (`padding="6rem"`).

    ✅ ADAPTATIVO: el hero respeta el color_mode del usuario.
    """
    return rx.box(
        # CAPA 0: Fondo gradiente adaptativo
        rx.box(
            position="absolute",
            top="0",
            left="0",
            right="0",
            bottom="0",
            background=FONDO_HOME_HERO,
            z_index="-1",
            pointer_events="none",
        ),
        # CAPA 1: Orbes de glow azul marino en esquinas
        _orbes_glow(),
        # CAPA 2: Iconos flotantes (partículas) en azul marino
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