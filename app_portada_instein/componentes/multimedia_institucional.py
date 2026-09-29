"""
Sección multimedia institucional del home.

Muestra:
- Video institucional en formato 16:9.
- Información sobre la plataforma web de seguimiento académico.
- Enlaces a redes sociales del instituto.

Sistema de color (UX)
---------------------
- Acentos institucionales (badge "PLATAFORMA OFICIAL", span del título,
  icono de redes sociales): accent crimson.
- Colores de marca de redes sociales (Facebook azul, Instagram rosa,
  TikTok negro, YouTube rojo, Telegram celeste, Discord violeta):
  hex fijos intencionales (son colores corporativos oficiales).
- Textos: neutros (`gray-11`/`gray-12`) para legibilidad.
- Fondos: `COLOR_FONDO_CARTA` (gray-1).
"""

import reflex as rx

from app_portada_instein.infraestructura.constantes_visuales import (
    COLOR_ACENTO_TEXTO,
    COLOR_BORDE_SUAVE,
    COLOR_FONDO_CARTA,
    COLOR_TEXTO_CUERPO,
    COLOR_TEXTO_PRINCIPAL,
    RADIO_EXTRA_GRANDE,
    RADIO_GRANDE,
    RADIO_MEDIO,
    RADIO_PASTILLA,
    REDES_SOCIALES,
)


# ======================================================================
# Constantes locales
# ======================================================================

ANCHO_MAXIMO_SECCION = "72rem"
PADDING_LATERAL_SECCION = "1.5rem"


# ======================================================================
# Video institucional
# ======================================================================


def _video_institucional() -> rx.Component:
    """
    Video institucional en formato 16:9 con estilo moderno.

    El video se muestra con un borde redondeado, sombra profunda y
    un fondo oscuro para darle protagonismo. Los `rgba` de la sombra
    son intencionales (funcionan igual en ambos modos).
    """
    return rx.box(
        rx.aspect_ratio(
            rx.video(
                src="/video_in.mp4",
                width="100%",
                height="100%",
                controls=True,
                auto_play=False,
                loop=False,
                muted=False,
                border_radius=RADIO_GRANDE,
            ),
            ratio=16 / 9,
        ),
        width="100%",
        border_radius=RADIO_EXTRA_GRANDE,
        overflow="hidden",
        box_shadow=(
            "0 20px 40px -10px rgba(0, 0, 0, 0.25), "
            "0 0 0 1px rgba(255, 255, 255, 0.05)"
        ),
        background="#0c0b0b",  # fondo del video (siempre oscuro)
        padding="0.25rem",
    )


# ======================================================================
# Información de la plataforma académica
# ======================================================================


def _info_plataforma_academica() -> rx.Component:
    """
    Bloque de texto que describe la plataforma web de seguimiento académico.

    Incluye:
    - Badge "PLATAFORMA OFICIAL" con accent institucional.
    - Título grande con span en accent.
    - Descripción de la plataforma.
    - Badge de características.
    - Botón de CTA para crear cuenta.

    Los colores de marca del badge/CTA usan accent (crimson).
    """
    return rx.vstack(
        # ==========================================================
        # Badge "PLATAFORMA OFICIAL"
        # ==========================================================
        rx.flex(
            rx.icon("award", size=12, color="white"),
            rx.text(
                "PLATAFORMA OFICIAL",
                font_size="0.625rem",
                font_weight="800",
                color="white",
                letter_spacing="0.1em",
            ),
            align="center",
            gap="0.375rem",
            background=rx.color("accent", 11),
            padding="0.375rem 0.75rem",
            border_radius=RADIO_PASTILLA,
            width="fit-content",
            box_shadow=f"0 4px 12px -2px {rx.color('accent', 11)}",
        ),
        # ==========================================================
        # Título
        # ==========================================================
        rx.heading(
            "Plataforma web de ",
            rx.text.span(
                "seguimiento académico",
                color=COLOR_ACENTO_TEXTO,
            ),
            "",
            size="7",
            font_weight="900",
            letter_spacing="-0.03em",
            line_height="1.15",
            color=COLOR_TEXTO_PRINCIPAL,
        ),
        # ==========================================================
        # Descripción
        # ==========================================================
        rx.text(
            "Accede a tu historial académico, calificaciones, asistencia y "
            "materiales de estudio desde cualquier dispositivo. Inicia sesión "
            "con tu cuenta institucional y mantén el control total de tu "
            "formación técnica.",
            font_size="1rem",
            line_height="1.7",
            color=COLOR_TEXTO_CUERPO,
            max_width="36rem",
        ),
        # ==========================================================
        # Badge de características
        # ==========================================================
        rx.badge(
            rx.flex(
                rx.icon("graduation-cap", size=12),
                rx.text("Historial Académico Completo", as_="span"),
                align="center",
                gap="0.375rem",
            ),
            variant="outline",
            color_scheme="crimson",
            size="2",
            padding="0.5rem 0.875rem",
        ),
        # ==========================================================
        # Botón de CTA
        # ==========================================================
        rx.button(
            rx.icon("user-plus", size=18),
            rx.text("Crear Cuenta Institucional", as_="span", font_weight="700"),
            size="3",
            variant="solid",
            color_scheme="crimson",
            width="100%",
            max_width="24rem",
            cursor="pointer",
            box_shadow=f"0 10px 25px -5px {rx.color('accent', 11)}",
            transition="all 0.2s",
            _hover={
                "transform": "translateY(-2px)",
                "box_shadow": f"0 15px 35px -5px {rx.color('accent', 11)}",
            },
        ),
        align="start",
        spacing="4",
        width="100%",
    )


# ======================================================================
# Tarjeta de red social (botón individual)
# ======================================================================


def _tarjeta_red_social(red: dict) -> rx.Component:
    """
    Botón individual de red social con icono y nombre.

    Usa el color corporativo oficial de cada red (hex fijo) porque son
    colores de marca de terceros y no deben cambiar con el tema.
    El hover aplica un efecto de elevación + brillo.

    Args:
        red: Dict con `nombre`, `icono`, `url`, `color`.
    """
    return rx.link(
        rx.flex(
            rx.icon(
                red["icono"],
                size=18,
                color="white",
            ),
            rx.text(
                red["nombre"],
                font_size="0.8125rem",
                font_weight="600",
                color="white",
            ),
            align="center",
            gap="0.5rem",
        ),
        href=red["url"],
        is_external=True,
        text_decoration="none",
        padding="0.625rem 1rem",
        border_radius=RADIO_MEDIO,
        background=red["color"],
        box_shadow=f"0 4px 12px -2px {red['color']}80",
        transition="all 0.2s",
        _hover={
            "transform": "translateY(-2px)",
            "box_shadow": f"0 8px 20px -4px {red['color']}cc",
            "filter": "brightness(1.1)",
        },
    )


# ======================================================================
# Sección de redes sociales completa
# ======================================================================


def _redes_sociales_instituto() -> rx.Component:
    """
    Sección con todas las redes sociales del instituto.

    Muestra un título con accent y un grid responsive con botones
    en colores corporativos de cada red.
    """
    return rx.vstack(
        # --- Encabezado ---
        rx.flex(
            rx.icon(
                "share-2",
                size=18,
                color=COLOR_ACENTO_TEXTO,
            ),
            rx.text(
                "Síguenos en redes sociales",
                font_size="0.875rem",
                font_weight="700",
                letter_spacing="0.05em",
                text_transform="uppercase",
                color=COLOR_TEXTO_PRINCIPAL,
            ),
            align="center",
            gap="0.5rem",
        ),
        # --- Grid de redes ---
        rx.flex(
            *[_tarjeta_red_social(red) for red in REDES_SOCIALES],
            gap="0.75rem",
            flex_wrap="wrap",
            justify="center",
        ),
        align="center",
        spacing="3",
        width="100%",
    )


# ======================================================================
# Sección multimedia completa del home
# ======================================================================


def seccion_multimedia_institucional() -> rx.Component:
    """
    Sección completa con:
    - Video institucional (columna izquierda).
    - Info de la plataforma académica (columna derecha).
    - Redes sociales (abajo, full width).

    Layout:
    - Desktop: 60% video / 40% info.
    - Tablet: stack vertical.
    - Móvil: stack vertical.
    """
    return rx.box(
        rx.vstack(
            # ==========================================================
            # Fila principal: video + info
            # ==========================================================
            rx.flex(
                # Video institucional
                rx.box(
                    _video_institucional(),
                    width=["100%", "100%", "100%", "60%"],
                ),
                # Info plataforma
                rx.box(
                    _info_plataforma_academica(),
                    padding="1.5rem 0 1.5rem 2rem",
                    width=["100%", "100%", "100%", "40%"],
                ),
                width="100%",
                justify="center",
                align="center",
                flex_direction=["column", "column", "column", "row"],
                gap="2rem",
            ),
            # ==========================================================
            # Redes sociales
            # ==========================================================
            rx.box(
                _redes_sociales_instituto(),
                padding_top="2rem",
                border_top=f"1px solid {COLOR_BORDE_SUAVE}",
                width="100%",
            ),
            spacing="6",
            width="100%",
        ),
        width="100%",
        max_width=ANCHO_MAXIMO_SECCION,
        margin="0 auto",
        padding=f"3rem {PADDING_LATERAL_SECCION}",
    )


__all__ = ["seccion_multimedia_institucional"]