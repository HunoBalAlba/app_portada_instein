"""
Banner CTA final con fondo oscuro, trust indicators y micro-interacciones.

Sistema de color (UX)
---------------------
Este banner mantiene un fondo OSCURO INTENCIONAL (independiente del
color_mode) para crear un cierre visual impactante. Los colores se
eligen para garantizar contraste sobre el fondo oscuro:

- Fondo: gradiente oscuro (`#0f172a` → `#1e293b`) intencional.
- Orbes radiales: accent crimson + azul en esquinas opuestas.
- Texto: blanco puro / blanco con opacidad.
- Botón primario: fondo blanco, texto oscuro (máximo contraste).
- Botón secundario: transparente con borde blanco.

Mejoras UX aplicadas
--------------------
1. Badge "Inscripciones abiertas" con punto verde pulsante.
2. Microcopy específico con urgencia y escasez ("30 cupos").
3. Trust indicators: avatares + rating + egresados.
4. Trust badges inline: título nacional + empleabilidad.
5. Dos orbes radiales decorativos (arriba-izq + abajo-der).
6. Botón primario con flecha animada en hover.
7. Botón secundario con WhatsApp (canal directo).
"""

import reflex as rx

from app_portada_instein.componentes.primitivos import enlace_navegacion
from app_portada_instein.infraestructura.constantes_visuales import (
    COLOR_ACENTO_SOLIDO,
    RADIO_EXTRA_GRANDE,
    RADIO_PASTILLA,
    WHATSAPP_URL,
)


# ======================================================================
# Constantes locales
# ======================================================================

# Ancho máximo del banner.
ANCHO_MAXIMO_BANNER = "72rem"

# Padding del contenido.
PADDING_CONTENIDO = "4.5rem 1.5rem"

# Colores del gradiente oscuro (intencionales, NO dependen del modo).
GRADIENTE_OSCURO = "linear-gradient(135deg, #0f172a 0%, #1e293b 100%)"

# Colores del texto sobre el fondo oscuro.
COLOR_TEXTO_BLANCO = "#ffffff"
COLOR_TEXTO_BLANCO_SUAVE = "rgba(255,255,255,0.8)"
COLOR_TEXTO_BLANCO_MAS_SUAVE = "rgba(255,255,255,0.6)"


# ======================================================================
# Orbes radiales decorativos de fondo
# ======================================================================


def _orbes_radiales_fondo() -> rx.Component:
    """
    Dos orbes radiales decorativos en esquinas opuestas.

    Añade profundidad visual con:
    - Orbe accent (crimson) en la esquina superior izquierda.
    - Orbe azul cian en la esquina inferior derecha.

    Ambos con opacidad baja y `pointer-events: none`.
    """
    return rx.fragment(
        # Orbe accent superior izquierda
        rx.box(
            position="absolute",
            top="-20%",
            left="-10%",
            width="50%",
            height="80%",
            background=(
                f"radial-gradient(circle at center, "
                f"{COLOR_ACENTO_SOLIDO} 0%, transparent 60%)"
            ),
            opacity="0.25",
            filter="blur(40px)",
            z_index="0",
            pointer_events="none",
        ),
        # Orbe azul inferior derecha
        rx.box(
            position="absolute",
            bottom="-20%",
            right="-10%",
            width="50%",
            height="80%",
            background=(
                "radial-gradient(circle at center, "
                "#3b82f6 0%, transparent 60%)"
            ),
            opacity="0.20",
            filter="blur(40px)",
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
    """
    return rx.flex(
        rx.box(
            height="0.5rem",
            width="0.5rem",
            border_radius=RADIO_PASTILLA,
            background="#22c55e",
            animation="pulse 2s ease-in-out infinite",
        ),
        rx.text(
            "INSCRIPCIONES ABIERTAS · GESTIÓN 2026",
            font_size="0.75rem",
            font_weight="700",
            color=COLOR_TEXTO_BLANCO,
            letter_spacing="0.05em",
        ),
        align="center",
        gap="0.5rem",
        padding="0.5rem 1rem",
        border_radius=RADIO_PASTILLA,
        background="rgba(255,255,255,0.08)",
        border="1px solid rgba(255,255,255,0.15)",
        backdrop_filter="blur(8px)",
        width="fit-content",
        margin_bottom="1.5rem",
    )


# ======================================================================
# Trust indicators (avatares + rating)
# ======================================================================


def _avatars_apilados() -> rx.Component:
    """
    Fila de 5 avatares apilados con degradado.

    Simula "caras reales" que refuerzan la prueba social. Cada avatar
    tiene un color distinto y está solapado con el anterior.
    """
    colores = ["#2563eb", "#0891b2", "#7c3aed", "#ea580c", "#16a34a"]

    return rx.flex(
        *[
            rx.box(
                # Inicial del "estudiante" decorativa
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
                border="2px solid #0f172a",
                display="flex",
                align_items="center",
                justify_content="center",
                margin_left="-0.5rem" if i > 0 else "0",
                flex_shrink="0",
            )
            for i, (letra, color) in enumerate(
                zip(["A", "M", "J", "L", "S"], colores)
            )
        ],
        align="center",
    )


def _trust_indicators() -> rx.Component:
    """
    Bloque de trust indicators: avatares + rating + egresados.

    Estructura:
    [👤👤👤👤👤]  ⭐ 4.9/5  ·  500+ egresados
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
                color=COLOR_TEXTO_BLANCO,
            ),
            rx.text(
                "·",
                font_size="0.8125rem",
                color=COLOR_TEXTO_BLANCO_MAS_SUAVE,
            ),
            rx.text(
                "500+ egresados",
                font_size="0.8125rem",
                font_weight="600",
                color=COLOR_TEXTO_BLANCO_SUAVE,
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
    """Badge inline con icono + texto para credenciales."""
    return rx.flex(
        rx.icon(icono, size=12, color=COLOR_TEXTO_BLANCO),
        rx.text(
            texto,
            font_size="0.6875rem",
            font_weight="600",
            color=COLOR_TEXTO_BLANCO_SUAVE,
            white_space="nowrap",
        ),
        align="center",
        gap="0.375rem",
        padding="0.375rem 0.75rem",
        border_radius=RADIO_PASTILLA,
        background="rgba(255,255,255,0.06)",
        border="1px solid rgba(255,255,255,0.1)",
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
    Botón primario "Ver Carreras" con fondo blanco + flecha animada.

    La flecha `→` se mueve a la derecha al hacer hover.
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
        background=COLOR_TEXTO_BLANCO,
        color="#0f172a",
        padding="1rem 2rem",
        border_radius=RADIO_PASTILLA,
        font_size="1rem",
        box_shadow="0 10px 25px -5px rgba(255, 255, 255, 0.3)",
        transition="all 0.2s",
        _hover={
            "transform": "translateY(-2px)",
            "box_shadow": "0 15px 35px -5px rgba(255, 255, 255, 0.4)",
            "& .arrow-icon": {"transform": "translateX(4px)"},
        },
    )


def _boton_secundario_banner() -> rx.Component:
    """
    Botón secundario "WhatsApp" con borde blanco.

    Redirige directamente a WhatsApp (canal directo de conversión).
    """
    return enlace_navegacion(
        WHATSAPP_URL,
        rx.icon("message-circle", size=18),
        rx.text("WhatsApp", as_="span", font_weight="600"),
        display="flex",
        align_items="center",
        gap="0.5rem",
        background="transparent",
        color=COLOR_TEXTO_BLANCO,
        padding="1rem 2rem",
        border_radius=RADIO_PASTILLA,
        font_size="1rem",
        border="1px solid rgba(255, 255, 255, 0.3)",
        transition="all 0.2s",
        _hover={
            "background": "rgba(255, 255, 255, 0.1)",
            "border_color": "rgba(255, 255, 255, 0.5)",
        },
    )


# ======================================================================
# Banner CTA final completo
# ======================================================================


def banner_cta_final() -> rx.Component:
    """
    Banner de llamada a la acción final con fondo oscuro degradado.

    Estructura:
    - 2 orbes radiales decorativos en esquinas opuestas.
    - Badge "Inscripciones abiertas" con punto pulsante.
    - Título grande + subtítulo con urgencia.
    - Trust indicators (avatares + rating + egresados).
    - Trust badges inline (título nacional, empleabilidad, convenios).
    - Par de botones (primario con flecha + secundario WhatsApp).
    - Fondo con gradiente oscuro intencional.
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
                color=COLOR_TEXTO_BLANCO,
                text_align="center",
                font_weight="900",
                letter_spacing="-0.03em",
            ),
            # --- Subtítulo con urgencia ---
            rx.text(
                "Solo ",
                rx.text.span(
                    "30 cupos",
                    font_weight="800",
                    color=COLOR_TEXTO_BLANCO,
                ),
                " disponibles por carrera. "
                "Asegura tu lugar en la Gestión 2026 hoy mismo.",
                font_size="1.125rem",
                color=COLOR_TEXTO_BLANCO_SUAVE,
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
        background=GRADIENTE_OSCURO,
        border_radius=RADIO_EXTRA_GRANDE,
        overflow="hidden",
        max_width=ANCHO_MAXIMO_BANNER,
        margin="0 auto",
    )


__all__ = ["banner_cta_final"]