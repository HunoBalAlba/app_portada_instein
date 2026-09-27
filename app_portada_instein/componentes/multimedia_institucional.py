"""
Sección multimedia institucional del home.

Muestra:
- Video institucional en formato 16:9.
- Información sobre la plataforma web de seguimiento académico.
- Enlaces a redes sociales del instituto.
"""

import reflex as rx

from app_portada_instein.infraestructura.constantes_visuales import (
    REDES_SOCIALES,
)


# ======================================================================
# Video institucional
# ======================================================================


def _video_institucional() -> rx.Component:
    """
    Video institucional en formato 16:9 con estilo moderno.

    El video se muestra con un borde redondeado, sombra profunda y
    un degradado de fondo para darle protagonismo.
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
                border_radius="1rem",
            ),
            ratio=16 / 9,
        ),
        width="100%",
        border_radius="1.25rem",
        overflow="hidden",
        box_shadow=("0 20px 40px -10px rgba(0, 0, 0, 0.25), 0 0 0 1px rgba(255, 255, 255, 0.05)"),
        background="#0c0b0b",
        padding="0.25rem",
    )


# ======================================================================
# Información de la plataforma académica
# ======================================================================


def _info_plataforma_academica() -> rx.Component:
    """
    Bloque de texto que describe la plataforma web de seguimiento académico.

    Incluye:
    - Título grande con acento.
    - Descripción de la plataforma.
    - Badge destacado.
    - Botón de CTA para crear cuenta.
    """
    return rx.vstack(
        # --- Badge "Plataforma Oficial" ---
        rx.flex(
            rx.icon("award", size=12, color="#ffffff"),
            rx.text(
                "PLATAFORMA OFICIAL",
                font_size="0.625rem",
                font_weight="800",
                color="#ffffff",
                letter_spacing="0.1em",
            ),
            align="center",
            gap="0.375rem",
            background=rx.color("accent", 11),
            padding="0.375rem 0.75rem",
            border_radius="9999px",
            width="fit-content",
            box_shadow="0 4px 12px -2px rgba(37, 99, 235, 0.5)",
        ),
        # --- Título ---
        rx.heading(
            "Plataforma web de ",
            rx.text.span(
                "seguimiento académico",
                color=rx.color("accent", 11),
            ),
            "",
            size="7",
            font_weight="900",
            letter_spacing="-0.03em",
            line_height="1.15",
            color=rx.color_mode_cond(light="#0f172a", dark="#f1f5f9"),
        ),
        # --- Descripción ---
        rx.text(
            "Accede a tu historial académico, calificaciones, asistencia y "
            "materiales de estudio desde cualquier dispositivo. Inicia sesión "
            "con tu cuenta institucional y mantén el control total de tu "
            "formación técnica.",
            font_size="1rem",
            line_height="1.7",
            color=rx.color_mode_cond(light="#475569", dark="#cbd5e1"),
            max_width="36rem",
        ),
        # --- Badge de características ---
        rx.badge(
            rx.flex(
                rx.icon("graduation-cap", size=12),
                rx.text("Historial Académico Completo", as_="span"),
                align="center",
                gap="0.375rem",
            ),
            variant="outline",
            color_scheme="blue",
            size="2",
            padding="0.5rem 0.875rem",
        ),
        # --- Botón de CTA ---
        rx.button(
            rx.icon("user-plus", size=18),
            rx.text("Crear Cuenta Institucional", as_="span", font_weight="700"),
            size="3",
            variant="solid",
            width="100%",
            max_width="24rem",
            cursor="pointer",
            box_shadow="0 10px 25px -5px rgba(37, 99, 235, 0.4)",
            transition="all 0.2s",
            _hover={
                "transform": "translateY(-2px)",
                "box_shadow": "0 15px 35px -5px rgba(37, 99, 235, 0.5)",
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

    El botón se colorea con el color corporativo de cada red al
    hacer hover.
    """
    return rx.link(
        rx.flex(
            rx.icon(
                red["icono"],
                size=18,
                color="#ffffff",
            ),
            rx.text(
                red["nombre"],
                font_size="0.8125rem",
                font_weight="600",
                color="#ffffff",
            ),
            align="center",
            gap="0.5rem",
        ),
        href=red["url"],
        is_external=True,
        text_decoration="none",
        padding="0.625rem 1rem",
        border_radius="0.75rem",
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

    Muestra un título y un grid responsive con botones de colores.
    """
    return rx.vstack(
        # --- Encabezado ---
        rx.flex(
            rx.icon(
                "share-2",
                size=18,
                color=rx.color("accent", 11),
            ),
            rx.text(
                "Síguenos en redes sociales",
                font_size="0.875rem",
                font_weight="700",
                letter_spacing="0.05em",
                text_transform="uppercase",
                color=rx.color_mode_cond(light="#0f172a", dark="#f1f5f9"),
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
    """
    return rx.box(
        rx.vstack(
            # --- Fila principal: video + info ---
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
            # --- Redes sociales ---
            rx.box(
                _redes_sociales_instituto(),
                padding_top="2rem",
                border_top=("1px solid " + rx.color_mode_cond(light="#e2e8f0", dark="#1e293b")),
                width="100%",
            ),
            spacing="6",
            width="100%",
        ),
        width="100%",
        max_width="72rem",
        margin="0 auto",
        padding="3rem 1.5rem",
    )
