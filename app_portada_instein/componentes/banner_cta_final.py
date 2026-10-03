# app_portada_instein/componentes/banner_cta_final.py

"""
Banner CTA final — estilo Neon adaptativo (dark/light).

Banner de llamada a la acción con trust indicators y micro-interacciones.
Cierra visualmente el home con impacto.

Sistema de color (UX)
---------------------
✅ ADAPTATIVO: todos los colores respetan el color_mode del usuario.

- Fondo: gradiente adaptativo (`GRADIENTE_HOME_BANNER`).
    - Dark: `#0a0f1f` → `#0f172a` → `#1a237e` (azul marino profundo).
    - Light: `#eef2ff` → `#c7d2fe` → `#a5b4fc` (azul claro).
- Acentos: azul marino neon (`AZUL_MARINO_NEON` = `#3b5bdb`) en AMBOS modos.
- Texto: `TEXTO_HOME_PRINCIPAL` / `TEXTO_HOME_SUAVE` / `TEXTO_HOME_MAS_SUAVE`.
- Bordes: `BORDE_HOME_AZUL` / `BORDE_HOME_MEDIO`.
- Avatares: tintes azul marino con borde adaptativo.
- Punto verde: `#22c55e` (semántico, mismo en ambos modos).

Mejoras UX aplicadas
--------------------
1. Badge "Inscripciones abiertas" con punto verde pulsante.
2. Microcopy específico con urgencia y escasez ("30 cupos").
3. Trust indicators: avatares + rating + egresados.
4. Trust badges inline: título nacional + empleabilidad + convenios.
5. Dos orbes radiales decorativos (arriba-izq + abajo-der).
6. Botón primario con flecha animada en hover.
7. Botón secundario con WhatsApp (canal directo).
"""

import reflex as rx

from app_portada_instein.componentes.primitivos import enlace_navegacion
from app_portada_instein.infraestructura.constantes_visuales import (
    AZUL_MARINO_NEON,
    BORDE_HOME_AZUL,
    BORDE_HOME_MEDIO,
    GRADIENTE_HOME_BANNER,
    RADIO_EXTRA_GRANDE,
    RADIO_PASTILLA,
    TEXTO_HOME_MAS_SUAVE,
    TEXTO_HOME_PRINCIPAL,
    TEXTO_HOME_SUAVE,
    WHATSAPP_URL,
)


# ======================================================================
# Constantes locales
# ======================================================================

# Ancho máximo del banner.
ANCHO_MAXIMO_BANNER = "72rem"

# Padding del contenido.
PADDING_CONTENIDO = "4.5rem 1.5rem"

# Color del punto verde semántico (activo) — mismo en ambos modos.
COLOR_VERDE_ACTIVO = "#22c55e"

# Colores base para los avatares apilados (tintes azul marino).
COLORES_AVATARES = [
    "#3b5bdb",   # azul marino neon
    "#1a237e",   # azul marino profundo
    "#283593",   # azul índigo
    "#3949ab",   # azul indigo claro
    "#5c6bc0",   # azul medio
]


# ======================================================================
# Orbes radiales decorativos de fondo
# ======================================================================


def _orbes_radiales_fondo() -> rx.Component:
    """
    Dos orbes radiales decorativos en esquinas opuestas.

    Añade profundidad visual con:
    - Orbe azul marino neon en la esquina superior izquierda.
    - Orbe azul profundo en la esquina inferior derecha.

    ✅ ADAPTATIVO: en light mode los orbes tienen menos opacidad para
    no saturar el fondo claro.

    Ambos con `pointer-events: none`.
    """
    return rx.fragment(
        # Orbe azul marino neon - superior izquierda
        rx.box(
            position="absolute",
            top="-20%",
            left="-10%",
            width="50%",
            height="80%",
            background=(
                f"radial-gradient(circle at center, "
                f"{AZUL_MARINO_NEON} 0%, transparent 60%)"
            ),
            opacity=rx.color_mode_cond(     # ✅ adaptativo
                light="0.15",   # sutil en light
                dark="0.30",
            ),
            filter="blur(60px)",
            z_index="0",
            pointer_events="none",
        ),
        # Orbe azul profundo - inferior derecha
        rx.box(
            position="absolute",
            bottom="-20%",
            right="-10%",
            width="50%",
            height="80%",
            background=(
                "radial-gradient(circle at center, "
                "#1a237e 0%, transparent 60%)"
            ),
            opacity=rx.color_mode_cond(     # ✅ adaptativo
                light="0.12",
                dark="0.25",
            ),
            filter="blur(60px)",
            z_index="0",
            pointer_events="none",
        ),
    )


# ======================================================================
# Badge "Inscripciones abiertas"
# ======================================================================


def _badge_inscripciones_abiertas() -> rx.Component:
    """
    Badge con punto verde pulsante + texto "INSCRIPCIONES ABIERTAS".

    Coherente con el hero principal. Añade sensación de "activo ahora".

    ✅ ADAPTATIVO: el fondo azul y el texto cambian según el modo.
    """
    return rx.flex(
        rx.box(
            height="0.5rem",
            width="0.5rem",
            border_radius=RADIO_PASTILLA,
            background=COLOR_VERDE_ACTIVO,
            box_shadow=f"0 0 12px {COLOR_VERDE_ACTIVO}",
            animation="pulse 2s ease-in-out infinite",
            flex_shrink="0",
        ),
        rx.text(
            "INSCRIPCIONES ABIERTAS · GESTIÓN 2026",
            font_size="0.75rem",
            font_weight="700",
            color=TEXTO_HOME_PRINCIPAL,      # ✅ adaptativo
            letter_spacing="0.1em",
        ),
        align="center",
        gap="0.5rem",
        padding="0.5rem 1rem",
        border_radius=RADIO_PASTILLA,
        background=rx.color_mode_cond(       # ✅ adaptativo
            light="rgba(59, 91, 219, 0.08)",
            dark="rgba(59, 91, 219, 0.1)",
        ),
        border=f"1px solid {BORDE_HOME_AZUL}",   # ✅ adaptativo
        backdrop_filter="blur(12px)",
        width="fit-content",
        margin_bottom="1.5rem",
    )


# ======================================================================
# Trust indicators (avatares + rating)
# ======================================================================


def _avatars_apilados() -> rx.Component:
    """
    Fila de 5 avatares apilados con tintes azul marino.

    Simula "caras reales" que refuerzan la prueba social. Cada avatar
    tiene un tinte azul distinto y está solapado con el anterior.

    ✅ ADAPTATIVO: el borde del avatar cambia según el modo (para que
    contraste con el fondo del banner).
    """
    letras = ["A", "M", "J", "L", "S"]

    return rx.flex(
        *[
            rx.box(
                rx.text(
                    letra,
                    font_size="0.6875rem",
                    font_weight="800",
                    color="white",
                    line_height="1",
                ),
                height="1.75rem",
                width="1.75rem",
                border_radius=RADIO_PASTILLA,
                background=color,
                border=rx.color_mode_cond(      # ✅ adaptativo
                    light="2px solid #eef2ff",   # borde claro en light
                    dark="2px solid #0a0f1f",    # borde oscuro en dark
                ),
                display="flex",
                align_items="center",
                justify_content="center",
                margin_left="-0.5rem" if i > 0 else "0",
                flex_shrink="0",
            )
            for i, (letra, color) in enumerate(zip(letras, COLORES_AVATARES))
        ],
        align="center",
    )


def _trust_indicators() -> rx.Component:
    """
    Bloque de trust indicators: avatares + rating + egresados.

    Estructura:
        [👤👤👤👤👤]  ⭐ 4.9/5  ·  500+ egresados

    ✅ ADAPTATIVO: todos los textos cambian según el modo.
    """
    return rx.flex(
        # --- Avatares apilados ---
        _avatars_apilados(),
        # --- Rating + egresados ---
        rx.flex(
            rx.icon("star", size=14, color="#fbbf24", fill="#fbbf24"),
            rx.text(
                "4.9/5",
                font_size="0.8125rem",
                font_weight="700",
                color=TEXTO_HOME_PRINCIPAL,      # ✅ adaptativo
            ),
            rx.text(
                "·",
                font_size="0.8125rem",
                color=TEXTO_HOME_MAS_SUAVE,      # ✅ adaptativo
            ),
            rx.text(
                "500+ egresados",
                font_size="0.8125rem",
                font_weight="600",
                color=TEXTO_HOME_SUAVE,          # ✅ adaptativo
            ),
            align="center",
            gap="0.375rem",
        ),
        align="center",
        gap="1rem",
        margin_top="1.5rem",
        flex_wrap="wrap",
        justify="center",
    )


# ======================================================================
# Trust badges inline
# ======================================================================


def _trust_badge_inline(icono: str, texto: str) -> rx.Component:
    """
    Badge inline con icono + texto para credenciales.

    ✅ ADAPTATIVO: fondo, borde y texto cambian según el modo.
    """
    return rx.flex(
        rx.icon(icono, size=12, color=AZUL_MARINO_NEON),
        rx.text(
            texto,
            font_size="0.6875rem",
            font_weight="600",
            color=TEXTO_HOME_SUAVE,          # ✅ adaptativo
            white_space="nowrap",
        ),
        align="center",
        gap="0.375rem",
        padding="0.375rem 0.75rem",
        border_radius=RADIO_PASTILLA,
        background=rx.color_mode_cond(       # ✅ adaptativo
            light="rgba(59, 91, 219, 0.06)",
            dark="rgba(59, 91, 219, 0.08)",
        ),
        border=f"1px solid {BORDE_HOME_MEDIO}",   # ✅ adaptativo
        backdrop_filter="blur(12px)",
    )


def _trust_badges_row() -> rx.Component:
    """Fila de trust badges inline."""
    return rx.flex(
        _trust_badge_inline("award", "Título Nacional"),
        _trust_badge_inline("trending-up", "100% Empleabilidad"),
        _trust_badge_inline("building-2", "Convenios Empresariales"),
        gap="0.5rem",
        margin_top="1.25rem",
        flex_wrap="wrap",
        justify="center",
    )


# ======================================================================
# Botones del banner
# ======================================================================


def _boton_primario_banner() -> rx.Component:
    """
    Botón primario "Ver Carreras" con azul marino neon + flecha animada.

    Estilo Neon:
    - Fondo azul marino neon sólido.
    - Glow intenso (`box_shadow`).
    - Flecha `→` que se desplaza a la derecha en hover.
    - Elevación sutil al pasar el mouse.

    ✅ El azul marino es el mismo en ambos modos (color de marca).
    """
    return enlace_navegacion(
        "/carreras",
        rx.text("Ver Carreras", as_="span", font_weight="700"),
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


def _boton_secundario_banner() -> rx.Component:
    """
    Botón secundario "WhatsApp" con glassmorphism.

    Estilo Neon:
    - Fondo translúcido con blur adaptativo.
    - Borde adaptativo.
    - Hover: borde azul marino + fondo más opaco.

    ✅ ADAPTATIVO: el fondo y borde cambian según el modo.
    """
    return enlace_navegacion(
        WHATSAPP_URL,
        rx.icon("message-circle", size=18),
        rx.text("WhatsApp", as_="span", font_weight="600"),
        display="flex",
        align_items="center",
        gap="0.5rem",
        background=rx.color_mode_cond(       # ✅ adaptativo
            light="rgba(255, 255, 255, 0.6)",
            dark="rgba(255, 255, 255, 0.05)",
        ),
        color=TEXTO_HOME_PRINCIPAL,          # ✅ adaptativo
        padding="1rem 2rem",
        border_radius=RADIO_PASTILLA,
        font_size="1rem",
        border=f"1px solid {BORDE_HOME_MEDIO}",   # ✅ adaptativo
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
# Banner CTA final completo
# ======================================================================


def banner_cta_final() -> rx.Component:
    """
    Banner de llamada a la acción final — estilo Neon adaptativo.

    Estructura:
    - 2 orbes radiales decorativos (azul marino) en esquinas opuestas.
    - Badge "Inscripciones abiertas" con punto pulsante.
    - Título grande + subtítulo con urgencia ("30 cupos").
    - Trust indicators (avatares + rating + egresados).
    - Trust badges inline (título nacional, empleabilidad, convenios).
    - Par de botones (primario con flecha + secundario WhatsApp).
    - Fondo con gradiente adaptativo.

    ✅ ADAPTATIVO: todo el banner respeta el color_mode del usuario.

    El banner tiene `border_radius` grande y está centrado con
    `max_width="72rem"`, coherente con el resto del home.
    """
    return rx.box(
        # ==========================================================
        # Orbes radiales decorativos de fondo
        # ==========================================================
        _orbes_radiales_fondo(),
        # ==========================================================
        # Contenido
        # ==========================================================
        rx.vstack(
            # --- Badge "Inscripciones abiertas" ---
            _badge_inscripciones_abiertas(),
            # --- Título ---
            rx.heading(
                "¿Listo para empezar?",
                size="8",
                color=TEXTO_HOME_PRINCIPAL,      # ✅ adaptativo
                text_align="center",
                font_weight="900",
                letter_spacing="-0.03em",
                line_height="1.1",
            ),
            # --- Subtítulo con urgencia ---
            rx.text(
                "Solo ",
                rx.text.span(
                    "30 cupos",
                    font_weight="800",
                    color=TEXTO_HOME_PRINCIPAL,   # ✅ adaptativo
                ),
                " disponibles por carrera. "
                "Asegura tu lugar en la Gestión 2026 hoy mismo.",
                font_size="1.125rem",
                color=TEXTO_HOME_SUAVE,           # ✅ adaptativo
                text_align="center",
                max_width="42rem",
                margin_top="0.5rem",
                line_height="1.6",
            ),
            # --- Trust indicators (avatares + rating) ---
            _trust_indicators(),
            # --- Trust badges inline ---
            _trust_badges_row(),
            # --- Botones ---
            rx.flex(
                _boton_primario_banner(),
                _boton_secundario_banner(),
                gap="0.75rem",
                margin_top="2.5rem",
                flex_direction=["column", "row"],
                align="center",
                justify="center",
            ),
            align="center",
            position="relative",
            z_index="1",
            padding=PADDING_CONTENIDO,
        ),
        # ==========================================================
        # Contenedor principal
        # ==========================================================
        position="relative",
        width="100%",
        background=GRADIENTE_HOME_BANNER,        # ✅ adaptativo
        border_radius=RADIO_EXTRA_GRANDE,
        border=f"1px solid {BORDE_HOME_AZUL}",   # ✅ adaptativo
        overflow="hidden",
        max_width=ANCHO_MAXIMO_BANNER,
        margin="0 auto",
    )


__all__ = ["banner_cta_final"]