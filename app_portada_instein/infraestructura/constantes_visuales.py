"""
Constantes visuales, datos institucionales y utilidades de estilo.

Este módulo es la ÚNICA FUENTE DE VERDAD para:

1. Datos institucionales (nombre, teléfonos, direcciones, redes).
2. Sombras, radios y dimensiones reutilizables.
3. Paleta de colores semántica (adaptativa al color_mode).
4. Estilos predefinidos (páginas, enlaces, botones).
5. Fuentes y hojas de estilo externas.

Filosofía de color
------------------
Todos los colores se expresan como **tokens Radix** mediante `rx.color()`
o como **variables CSS de Radix** (`var(--gray-N)`, `var(--accent-N)`).
Esto garantiza:

- Adaptación automática al modo claro/oscuro (sin `rx.color_mode_cond`).
- Coherencia con el `accent_color` definido en `rx.theme(...)`.
- Cumplimiento de contraste WCAG AA por defecto.

Escala Radix (steps 1 → 12)
---------------------------
| Step | Uso recomendado                              |
|------|----------------------------------------------|
| 1-2  | Fondo de app / fondo de tarjeta              |
| 3-5  | Fondo de componentes (chips, badges suaves)  |
| 6-8  | Bordes, separadores, hover de bordes         |
| 9-10 | Fondos sólidos con contraste (botones, CTA)  |
| 11   | Texto de bajo énfasis sobre fondo suave      |
| 12   | Texto principal de máximo contraste          |

Para fondos sólidos (`accent-9`), usa `var(--accent-9-contrast)`
como color de texto: Radix lo ajusta automáticamente según el accent.

Nota sobre reactividad
----------------------
`rx.color()` devuelve un `Var` reactivo: si se usa dentro del árbol de
componentes, se recalcula al cambiar el color_mode. Si una constante
se usa fuera del árbol (por ejemplo en `style={}` estático), NO se
actualizará dinámicamente. En esos casos, evalúa el color dentro de la
función que lo consume.
"""

from __future__ import annotations

import reflex as rx


# ======================================================================
# 1. DATOS INSTITUCIONALES
# ======================================================================

NOMBRE_INSTITUTO = "INSTEIN"
NOMBRE_COMPLETO_INSTITUTO = "INSTITUTO TÉCNICO INTEGRADO SAN ANTONIO DE PADUA"
TELEFONO_PRINCIPAL = "71282993"
TELEFONO_SECUNDARIO = "79104232"
WHATSAPP_URL = "https://wa.me/59171282993"
DIRECCION = "Calle Jorge Carrasco entre 3 y 4"
UBICACION_FISICA = "Galería FLOR DE ORO 1er. piso"
HORARIO_ATENCION = "Lunes a Viernes: 08:30 - 18:30"

ANIO_COPYRIGHT = "2026"
ENTIDAD_COPYRIGHT = "INSTEIN - Instituto Técnico Integrado San Antonio de Padua"
GITHUB_URL = "https://github.com/tu-usuario/instein"
EMAIL_CONTACTO = "contacto@instein.edu.bo"


# ======================================================================
# 2. REDES SOCIALES
# ======================================================================

TIKTOK_URL = "https://www.tiktok.com/@instein.oficial"
FACEBOOK_URL = "https://www.facebook.com/instein.oficial"
INSTAGRAM_URL = "https://www.instagram.com/instein.oficial"
TELEGRAM_URL = "https://t.me/instein_oficial"
DISCORD_URL = "https://discord.gg/instein"
YOUTUBE_URL = "https://www.youtube.com/@instein_oficial"
WHATSAPP_CANAL_URL = "https://whatsapp.com/channel/instein"

# Colores corporativos de cada red (NO cambian con el modo; son de marca).
REDES_SOCIALES: list[dict] = [
    {
        "nombre": "Facebook",
        "icono": "users",
        "url": FACEBOOK_URL,
        "color": "#1877F2",
    },
    {
        "nombre": "Instagram",
        "icono": "camera",
        "url": INSTAGRAM_URL,
        "color": "#E4405F",
    },
    {
        "nombre": "TikTok",
        "icono": "music_2",
        "url": TIKTOK_URL,
        "color": "#000000",
    },
    {
        "nombre": "YouTube",
        "icono": "circle_play",
        "url": YOUTUBE_URL,
        "color": "#FF0000",
    },
    {
        "nombre": "Telegram",
        "icono": "send",
        "url": TELEGRAM_URL,
        "color": "#0088cc",
    },
    {
        "nombre": "Discord",
        "icono": "message_circle",
        "url": DISCORD_URL,
        "color": "#5865F2",
    },
]


# ======================================================================
# 3. SOMBRAS
# ======================================================================
# Las sombras se expresan como strings porque no dependen del modo. Si en
# el futuro quieres variantes light/dark, envuélvelas en un helper
# `sombra_suave()` que retorne `rx.color_mode_cond(...)`.

SOMBRA_SUAVE = "0 1px 2px 0 rgb(0 0 0 / 0.05)"
SOMBRA_MEDIA = "0 4px 12px -2px rgb(37 99 235 / 0.30)"
SOMBRA_FUERTE = "0 10px 25px -5px rgb(37 99 235 / 0.25)"
SOMBRA_CAJA = "0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)"


def sombra_hover_acento() -> rx.Var | str:
    """
    Sombra tintada de acento para estados hover.

    Se calcula dinámicamente porque depende del accent_color del tema.
    """
    return f"0 12px 32px -8px {rx.color('accent', 8)}"


# ======================================================================
# 4. RADIOS
# ======================================================================

RADIO_PEQUENO = "0.5rem"
RADIO_MEDIO = "0.75rem"
RADIO_GRANDE = "1rem"
RADIO_EXTRA_GRANDE = "1.5rem"
RADIO_PASTILLA = "9999px"
RADIO_BORDE = "var(--radius-2)"


# ======================================================================
# 5. DIMENSIONES
# ======================================================================

ANCHO_CONTENIDO_VW = "90vw"
ANCHO_MENU_LATERAL = "32em"
ANCHO_CONTENIDO_MENU = "16em"
ANCHO_MAXIMO = "1480px"
ANCHO_CONTENIDO = "72rem"
ANCHO_SECCION = "64rem"
PADDING_LATERAL = "1.5rem"
TAMANOS_CAJA_COLOR = ["2.25rem", "2.25rem", "2.5rem"]


# ======================================================================
# 6. PALETA SEMÁNTICA (tokens Radix — adaptativos al color_mode)
# ======================================================================
# Todas estas constantes devuelven `Var` reactivos. Se recalculan
# automáticamente cuando el usuario cambia entre modo claro/oscuro.
# ----------------------------------------------------------------------

# --- Texto ---
COLOR_TEXTO_PRINCIPAL = rx.color("gray", 12)     # Máximo contraste
COLOR_TEXTO_SECUNDARIO = rx.color("gray", 11)    # Énfasis medio
COLOR_TEXTO_CUERPO = rx.color("gray", 11)        # Párrafos
COLOR_TEXTO_APAGADO = rx.color("gray", 10)       # Placeholder / meta
COLOR_GRIS = rx.color("gray", 11)
COLOR_TEXTO = rx.color("gray", 11)

# --- Fondos ---
COLOR_FONDO_CARTA = rx.color("gray", 1)          # Superficie de tarjeta
COLOR_FONDO_SUAVE = rx.color("gray", 2)          # Fondo secundario
COLOR_FONDO_GRIS = rx.color("gray", 3)           # Chips / badges grises

# --- Bordes ---
COLOR_BORDE_SUAVE = rx.color("gray", 6)          # Borde por defecto
COLOR_BORDE_HOVER = rx.color("gray", 7)          # Borde en hover
COLOR_BORDE_ACTIVO = rx.color("gray", 8)         # Borde activo/focus
COLOR_DIVISOR = rx.color("gray", 4)              # Línea divisoria sutil
BORDE_PREDETERMINADO = f"1px solid {COLOR_BORDE_SUAVE}"

# --- Acento (respeta accent_color del tema) ---
COLOR_ACENTO_SOLIDO = rx.color("accent", 9)      # Fondo sólido (botón)
COLOR_ACENTO_TEXTO_SOLIDO = "var(--accent-9-contrast)"  # Texto sobre sólido
COLOR_ACENTO_TEXTO = rx.color("accent", 11)      # Texto de acento
COLOR_ACENTO_FONDO = rx.color("accent", 3)       # Fondo suave de acento
COLOR_ACENTO_BORDE = rx.color("accent", 7)       # Borde de acento
COLOR_ACENTO = rx.color("accent", 1)             # Fondo casi neutro
COLOR_FONDO_ACENTO = COLOR_ACENTO_FONDO          # Alias retrocompatible

# --- Estados semánticos (éxito, warning, error) ---
COLOR_EXITO_TEXTO = rx.color("green", 11)
COLOR_EXITO_FONDO = rx.color("green", 3)
COLOR_EXITO_SOLIDO = rx.color("green", 9)

COLOR_ALERTA_TEXTO = rx.color("amber", 11)
COLOR_ALERTA_FONDO = rx.color("amber", 3)

COLOR_ERROR_TEXTO = rx.color("red", 11)
COLOR_ERROR_FONDO = rx.color("red", 3)


# ======================================================================
# 7. HELPERS DE ESTILO REACTIVOS
# ======================================================================
# Funciones que devuelven dicts de estilo listos para usar con `**`.
# Evitan repetir lógica en cada componente y garantizan consistencia.
# ----------------------------------------------------------------------


def estilo_tarjeta_acento(
    *,
    radio: str = RADIO_EXTRA_GRANDE,
    padding: str = "1.5rem",
) -> dict:
    """
    Estilo para tarjetas con borde de acento y hover elevado.

    Ideal para tarjetas de contenido en vistas de detalle.
    """
    return {
        "padding": padding,
        "border_radius": radio,
        "background": COLOR_FONDO_CARTA,
        "border": f"1px solid {COLOR_ACENTO_BORDE}",
        "box_shadow": SOMBRA_SUAVE,
        "width": "100%",
        "height": "100%",
        "transition": "all 0.25s cubic-bezier(0.4, 0, 0.2, 1)",
        "_hover": {
            "border_color": COLOR_ACENTO_SOLIDO,
            "box_shadow": f"0 12px 32px -8px {rx.color('accent', 7)}",
            "transform": "translateY(-2px)",
        },
    }


def estilo_badge_acento() -> dict:
    """Estilo para un badge pill con acento suave."""
    return {
        "padding": "0.25rem 0.625rem",
        "border_radius": RADIO_PASTILLA,
        "background": COLOR_ACENTO_FONDO,
        "border": f"1px solid {COLOR_ACENTO_BORDE}",
        "color": COLOR_ACENTO_TEXTO,
        "font_size": "0.6875rem",
        "font_weight": "700",
        "text_transform": "uppercase",
        "letter_spacing": "0.05em",
        "white_space": "nowrap",
    }


def estilo_icono_solido(
    color: rx.Var | str | None = None,
    *,
    tamano: str = "0.5rem",
    radio: str = RADIO_MEDIO,
) -> dict:
    """
    Estilo para un contenedor de icono con fondo sólido de acento.

    Args:
        color: Color de fondo. Si None, usa el accent sólido del tema.
        tamano: Padding interior.
        radio: Radio del borde.
    """
    return {
        "padding": tamano,
        "border_radius": radio,
        "background": color if color is not None else COLOR_ACENTO_SOLIDO,
        "display": "flex",
        "align_items": "center",
        "justify_content": "center",
        "flex_shrink": "0",
    }


def estilo_icono_suave(
    color: rx.Var | str | None = None,
    *,
    tamano: str = "0.5rem",
    radio: str = RADIO_MEDIO,
) -> dict:
    """
    Estilo para un contenedor de icono con fondo suave de acento.

    Args:
        color: Color de acento. Si None, usa el accent del tema.
        tamano: Padding interior.
        radio: Radio del borde.
    """
    c = color if color is not None else rx.color("accent", 11)
    return {
        "padding": tamano,
        "border_radius": radio,
        "background": rx.color("accent", 3),
        "border": f"1px solid {rx.color('accent', 6)}",
        "display": "flex",
        "align_items": "center",
        "justify_content": "center",
        "flex_shrink": "0",
    }


def estilo_enlace_acento() -> dict:
    """Estilo para enlaces con color de acento y hover subrayado."""
    return {
        "color": COLOR_ACENTO_TEXTO,
        "text_decoration": "none",
        "transition": "color 0.2s",
        "_hover": {
            "color": COLOR_ACENTO_SOLIDO,
            "text_decoration": "underline",
        },
    }


# ======================================================================
# 8. ESTILOS PREDEFINIDOS (compatibilidad con código existente)
# ======================================================================

ESTILO_PAGINA_PLANTILLA = {
    "padding_top": ["1em", "1em", "2em"],
    "padding_x": ["auto", "auto", "2em"],
}

ESTILO_CONTENIDO_PLANTILLA = {
    "padding": "1em",
    "margin_bottom": "2em",
    "min_height": "90vh",
}

ESTILO_ENLACE = estilo_enlace_acento()

ESTILO_BOTON_SUPERPUESTO = {
    "background_color": COLOR_FONDO_CARTA,
    "border_radius": RADIO_BORDE,
}

ESTILO_SELECTOR_COLOR = {
    "border_radius": "max(var(--radius-3), var(--radius-full))",
    "box_shadow": SOMBRA_CAJA,
    "cursor": "pointer",
    "display": "flex",
    "align_items": "center",
    "justify_content": "center",
    "transition": "transform 0.15s ease-in-out",
    "_active": {"transform": "translateY(2px) scale(0.95)"},
}


# ======================================================================
# 9. FUENTES
# ======================================================================

FUENTE_PRINCIPAL = "Inter"
FUENTE_MONOESPACIADA = "JetBrains Mono"

HOJAS_DE_ESTILO_BASE = [
    "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap",
    "https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&display=swap",
]

FALLBACK_SANS = (
    '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, '
    '"Helvetica Neue", Arial, sans-serif'
)
FALLBACK_MONO = (
    '"JetBrains Mono", "SF Mono", Monaco, "Cascadia Code", '
    '"Roboto Mono", Consolas, "Courier New", monospace'
)

ESTILO_BASE = {
    "font_family": f'"{FUENTE_PRINCIPAL}", {FALLBACK_SANS}',
    "code": {"font_family": f'"{FUENTE_MONOESPACIADA}", {FALLBACK_MONO}'},
    "pre": {"font_family": f'"{FUENTE_MONOESPACIADA}", {FALLBACK_MONO}'},
    "kbd": {"font_family": f'"{FUENTE_MONOESPACIADA}", {FALLBACK_MONO}'},
    "button": {"font_family": f'"{FUENTE_PRINCIPAL}", {FALLBACK_SANS}'},
    "input": {"font_family": f'"{FUENTE_PRINCIPAL}", {FALLBACK_SANS}'},
    "textarea": {"font_family": f'"{FUENTE_PRINCIPAL}", {FALLBACK_SANS}'},
    "select": {"font_family": f'"{FUENTE_PRINCIPAL}", {FALLBACK_SANS}'},
}


# ======================================================================
# 10. ANIMACIONES CSS GLOBALES
# ======================================================================

ESTILOS_GLOBALES_CSS = {
    "@keyframes pulse": {
        "0%": {"transform": "scale(0.95)", "opacity": "0.5"},
        "50%": {"transform": "scale(1.1)", "opacity": "1"},
        "100%": {"transform": "scale(0.95)", "opacity": "0.5"},
    },
    "@keyframes borderPulse": {
        "0%": {
            "border-color": "rgba(34, 197, 94, 0.3)",
            "box-shadow": "0 0 0 0 rgba(34, 197, 94, 0.2)",
        },
        "50%": {
            "border-color": "rgba(34, 197, 94, 1)",
            "box-shadow": "0 0 0 4px rgba(34, 197, 94, 0.4)",
        },
        "100%": {
            "border-color": "rgba(34, 197, 94, 0.3)",
            "box-shadow": "0 0 0 0 rgba(34, 197, 94, 0)",
        },
    },
}


# ======================================================================
# EXPORTS
# ======================================================================

__all__ = [
    # --- Datos institucionales ---
    "ANIO_COPYRIGHT",
    "DIRECCION",
    "EMAIL_CONTACTO",
    "ENTIDAD_COPYRIGHT",
    "GITHUB_URL",
    "HORARIO_ATENCION",
    "NOMBRE_COMPLETO_INSTITUTO",
    "NOMBRE_INSTITUTO",
    "TELEFONO_PRINCIPAL",
    "TELEFONO_SECUNDARIO",
    "UBICACION_FISICA",
    "WHATSAPP_URL",
    # --- Redes sociales ---
    "DISCORD_URL",
    "FACEBOOK_URL",
    "INSTAGRAM_URL",
    "REDES_SOCIALES",
    "TELEGRAM_URL",
    "TIKTOK_URL",
    "WHATSAPP_CANAL_URL",
    "YOUTUBE_URL",
    # --- Sombras ---
    "SOMBRA_CAJA",
    "SOMBRA_FUERTE",
    "SOMBRA_MEDIA",
    "SOMBRA_SUAVE",
    "sombra_hover_acento",
    # --- Radios ---
    "RADIO_BORDE",
    "RADIO_EXTRA_GRANDE",
    "RADIO_GRANDE",
    "RADIO_MEDIO",
    "RADIO_PASTILLA",
    "RADIO_PEQUENO",
    # --- Dimensiones ---
    "ANCHO_CONTENIDO",
    "ANCHO_CONTENIDO_MENU",
    "ANCHO_CONTENIDO_VW",
    "ANCHO_MAXIMO",
    "ANCHO_MENU_LATERAL",
    "ANCHO_SECCION",
    "PADDING_LATERAL",
    "TAMANOS_CAJA_COLOR",
    # --- Paleta semántica ---
    "BORDE_PREDETERMINADO",
    "COLOR_ACENTO",
    "COLOR_ACENTO_BORDE",
    "COLOR_ACENTO_FONDO",
    "COLOR_ACENTO_SOLIDO",
    "COLOR_ACENTO_TEXTO",
    "COLOR_ACENTO_TEXTO_SOLIDO",
    "COLOR_ALERTA_FONDO",
    "COLOR_ALERTA_TEXTO",
    "COLOR_BORDE_ACTIVO",
    "COLOR_BORDE_HOVER",
    "COLOR_BORDE_SUAVE",
    "COLOR_DIVISOR",
    "COLOR_ERROR_FONDO",
    "COLOR_ERROR_TEXTO",
    "COLOR_EXITO_FONDO",
    "COLOR_EXITO_SOLIDO",
    "COLOR_EXITO_TEXTO",
    "COLOR_FONDO_ACENTO",
    "COLOR_FONDO_CARTA",
    "COLOR_FONDO_GRIS",
    "COLOR_FONDO_SUAVE",
    "COLOR_GRIS",
    "COLOR_TEXTO",
    "COLOR_TEXTO_APAGADO",
    "COLOR_TEXTO_CUERPO",
    "COLOR_TEXTO_PRINCIPAL",
    "COLOR_TEXTO_SECUNDARIO",
    # --- Helpers de estilo ---
    "estilo_badge_acento",
    "estilo_enlace_acento",
    "estilo_icono_solido",
    "estilo_icono_suave",
    "estilo_tarjeta_acento",
    # --- Estilos predefinidos ---
    "ESTILO_BASE",
    "ESTILO_BOTON_SUPERPUESTO",
    "ESTILO_CONTENIDO_PLANTILLA",
    "ESTILO_ENLACE",
    "ESTILO_PAGINA_PLANTILLA",
    "ESTILO_SELECTOR_COLOR",
    "ESTILOS_GLOBALES_CSS",
    # --- Fuentes ---
    "FALLBACK_MONO",
    "FALLBACK_SANS",
    "FUENTE_MONOESPACIADA",
    "FUENTE_PRINCIPAL",
    "HOJAS_DE_ESTILO_BASE",
]
















# ======================================================================
# HELPERS DE COLOR ADAPTATIVO POR CARRERA
# ======================================================================


def color_carrera_adaptativo(carrera: dict) -> rx.Var:
    """
    Color principal de una carrera, adaptado al color_mode.

    Args:
        carrera: Dict de carrera con `color_principal` y
            `color_principal_dark`.

    Returns:
        Var reactivo que devuelve el hex correcto según el modo.
    """
    return rx.color_mode_cond(
        light=carrera["color_principal"],
        dark=carrera["color_principal_dark"],
    )


def color_suave_carrera_adaptativo(carrera: dict) -> rx.Var:
    """Color suave de una carrera, adaptado al color_mode."""
    return rx.color_mode_cond(
        light=carrera["color_suave"],
        dark=carrera["color_suave_dark"],
    )