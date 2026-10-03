# app_portada_instein/componentes/multimedia_institucional.py

"""
Sección multimedia institucional del home — estilo Neon adaptativo.

Muestra:
- Video institucional en formato 16:9 con glow azul adaptativo.
- Información sobre la plataforma web de seguimiento académico.
- Enlaces a redes sociales del instituto.

Sistema de color (UX)
---------------------
✅ ADAPTATIVO: todos los colores respetan el color_mode del usuario.

- Acentos: azul marino neon (`AZUL_MARINO_NEON` = `#3b5bdb`) en AMBOS modos.
- Texto: `TEXTO_HOME_PRINCIPAL` / `TEXTO_HOME_MAS_SUAVE` / `TEXTO_HOME_SUAVE`.
- Bordes: `BORDE_HOME_AZUL` / `BORDE_HOME_MEDIO` / `BORDE_HOME_SUAVE`.
- Fondos tintados: `FONDO_AZUL_SUAVE`.
- Título con gradiente: `GRADIENTE_TEXTO_HOME`.
- Redes sociales: colores corporativos oficiales (hex fijos), NO
  cambian con el tema (son colores de marca de terceros).

Estilo Neon:
- Tipografía masiva con gradiente de texto adaptativo.
- Glassmorphism (blur + bordes translúcidos).
- Hover con glow azul marino (más sutil en light).
- Padding generoso.
"""

import reflex as rx

from app_portada_instein.infraestructura.constantes_visuales import (
    AZUL_MARINO_NEON,
    BORDE_HOME_AZUL,
    BORDE_HOME_MEDIO,
    BORDE_HOME_SUAVE,
    FONDO_AZUL_SUAVE,
    GRADIENTE_TEXTO_HOME,
    RADIO_EXTRA_GRANDE,
    RADIO_GRANDE,
    RADIO_MEDIO,
    RADIO_PASTILLA,
    REDES_SOCIALES,
    TEXTO_HOME_MAS_SUAVE,
    TEXTO_HOME_PRINCIPAL,
    TEXTO_HOME_SUAVE,
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
    Video institucional en formato 16:9 con estilo Neon adaptativo.

    El video se muestra con:
    - Borde redondeado grande.
    - Glow azul sutil (box_shadow) adaptativo.
    - Fondo oscuro para darle protagonismo (independiente del modo,
      porque el contenido del video suele ser oscuro).
    - Borde translúcido azul marino en hover.

    ✅ ADAPTATIVO: el fondo del reproductor y el glow cambian según
    el color_mode. El video en sí no cambia.
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
        box_shadow=rx.color_mode_cond(
            light=f"0 20px 40px -10px rgba(0, 0, 0, 0.15), "
                  f"0 0 40px -10px {AZUL_MARINO_NEON}40",
            dark=f"0 20px 40px -10px rgba(0, 0, 0, 0.5), "
                 f"0 0 40px -10px {AZUL_MARINO_NEON}80",
        ),
        border=f"1px solid {BORDE_HOME_SUAVE}",           # ✅ adaptativo
        background=rx.color_mode_cond(                     # ✅ adaptativo
            light="#1a1a20",   # gris muy oscuro en light (video)
            dark="#0a0a0f",
        ),
        padding="0.25rem",
        transition="all 0.3s",
        _hover={
            "border_color": BORDE_HOME_AZUL,
            "box_shadow": rx.color_mode_cond(
                light=f"0 20px 40px -10px rgba(0, 0, 0, 0.15), "
                      f"0 0 60px -10px {AZUL_MARINO_NEON}80",
                dark=f"0 20px 40px -10px rgba(0, 0, 0, 0.5), "
                     f"0 0 60px -10px {AZUL_MARINO_NEON}cc",
            ),
        },
    )


# ======================================================================
# Información de la plataforma académica
# ======================================================================


def _badge_plataforma_oficial() -> rx.Component:
    """
    Badge "PLATAFORMA OFICIAL" con fondo azul marino neon + glow.

    Estilo Neon:
    - Fondo azul marino neon sólido (mismo en ambos modos).
    - Icono blanco.
    - Glow azul.

    ✅ El azul marino es el mismo en ambos modos (color de marca).
    """
    return rx.flex(
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
        background=AZUL_MARINO_NEON,
        padding="0.375rem 0.75rem",
        border_radius=RADIO_PASTILLA,
        width="fit-content",
        box_shadow=f"0 0 20px {AZUL_MARINO_NEON}80",
    )


def _badge_caracteristica() -> rx.Component:
    """
    Badge "Historial Académico Completo" con glassmorphism adaptativo.

    Estilo Neon:
    - Fondo azul marino translúcido adaptativo.
    - Borde azul marino adaptativo.
    - Texto adaptativo.

    ✅ ADAPTATIVO: el fondo y el texto cambian según el modo.
    """
    return rx.flex(
        rx.icon("graduation-cap", size=12, color=AZUL_MARINO_NEON),
        rx.text(
            "Historial Académico Completo",
            font_size="0.8125rem",
            font_weight="600",
            color=TEXTO_HOME_SUAVE,              # ✅ adaptativo
        ),
        align="center",
        gap="0.375rem",
        padding="0.5rem 0.875rem",
        border_radius=RADIO_PASTILLA,
        background=FONDO_AZUL_SUAVE,             # ✅ adaptativo
        border=f"1px solid {BORDE_HOME_AZUL}",   # ✅ adaptativo
        backdrop_filter="blur(12px)",
        width="fit-content",
    )


def _cta_crear_cuenta() -> rx.Component:
    """
    Botón CTA "Crear Cuenta Institucional" con glow azul marino.

    Estilo Neon:
    - Fondo azul marino neon.
    - Icono user-plus.
    - Glow que se intensifica en hover.

    ✅ El azul marino es el mismo en ambos modos (color de marca).
    """
    return rx.button(
        rx.icon("user-plus", size=18),
        rx.text(
            "Crear Cuenta Institucional",
            as_="span",
            font_weight="700",
        ),
        size="3",
        width="100%",
        max_width="24rem",
        cursor="pointer",
        background=AZUL_MARINO_NEON,
        color="white",
        border_radius=RADIO_MEDIO,
        box_shadow=f"0 10px 25px -5px {AZUL_MARINO_NEON}80",
        transition="all 0.2s",
        _hover={
            "transform": "translateY(-2px)",
            "box_shadow": f"0 15px 35px -5px {AZUL_MARINO_NEON}cc",
        },
    )


def _info_plataforma_academica() -> rx.Component:
    """
    Bloque de texto que describe la plataforma web de seguimiento académico.

    Incluye:
    - Badge "PLATAFORMA OFICIAL" con azul marino neon.
    - Título grande con span en gradiente de texto adaptativo.
    - Descripción de la plataforma.
    - Badge de características con glassmorphism.
    - Botón de CTA con glow azul marino.

    ✅ ADAPTATIVO: título, descripción y badges cambian según el modo.
    """
    return rx.vstack(
        # ==========================================================
        # Badge "PLATAFORMA OFICIAL"
        # ==========================================================
        _badge_plataforma_oficial(),
        # ==========================================================
        # Título con gradiente adaptativo
        # ==========================================================
        rx.heading(
            "Plataforma web de ",
            rx.text.span(
                "seguimiento académico",
                background=GRADIENTE_TEXTO_HOME,   # ✅ adaptativo
                background_clip="text",
                color="transparent",
                webkit_background_clip="text",
            ),
            "",
            size="7",
            font_weight="900",
            letter_spacing="-0.03em",
            line_height="1.15",
            color=TEXTO_HOME_PRINCIPAL,            # ✅ adaptativo
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
            color=TEXTO_HOME_MAS_SUAVE,            # ✅ adaptativo
            max_width="36rem",
        ),
        # ==========================================================
        # Badge de características
        # ==========================================================
        _badge_caracteristica(),
        # ==========================================================
        # Botón de CTA
        # ==========================================================
        _cta_crear_cuenta(),
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

    ⚠️ El color del botón NO es adaptativo (es el color de la marca).

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

    Muestra un título con azul marino y un grid responsive con botones
    en colores corporativos de cada red.

    ✅ ADAPTATIVO: el título y el icono cambian según el modo.
    """
    return rx.vstack(
        # --- Encabezado ---
        rx.flex(
            rx.icon(
                "share-2",
                size=18,
                color=AZUL_MARINO_NEON,           # mismo en ambos modos
            ),
            rx.text(
                "Síguenos en redes sociales",
                font_size="0.875rem",
                font_weight="700",
                letter_spacing="0.1em",
                text_transform="uppercase",
                color=TEXTO_HOME_PRINCIPAL,       # ✅ adaptativo
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
        spacing="4",
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

    Estilo Neon:
    - Glassmorphism en contenedores.
    - Glow azul marino en elementos interactivos.
    - Padding generoso.

    ✅ ADAPTATIVO: todos los colores respetan el color_mode del usuario.
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
                    padding=["0", "0", "0", "0 0 0 2rem"],
                    width=["100%", "100%", "100%", "40%"],
                ),
                width="100%",
                justify="center",
                align="center",
                flex_direction=["column", "column", "column", "row"],
                gap=["2rem", "2rem", "2rem", "3rem"],
            ),
            # ==========================================================
            # Redes sociales
            # ==========================================================
            rx.box(
                _redes_sociales_instituto(),
                padding_top="3rem",
                border_top=f"1px solid {BORDE_HOME_SUAVE}",   # ✅ adaptativo
                width="100%",
            ),
            spacing="6",
            width="100%",
        ),
        width="100%",
        max_width=ANCHO_MAXIMO_SECCION,
        margin="0 auto",
        padding=f"4rem {PADDING_LATERAL_SECCION}",
    )


__all__ = ["seccion_multimedia_institucional"]