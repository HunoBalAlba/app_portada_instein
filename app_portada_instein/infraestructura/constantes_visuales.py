# app_portada_instein/infraestructura/constantes_visuales.py

"""
Constantes visuales, datos institucionales y utilidades de estilo.

✅ ESQUEMA DE COLOR: azul marino (`#000080`) + azul primario (`#0000FF`)
   traducidos a la paleta Radix `blue` como equivalente profesional
   (WCAG AA garantizado).

✅ HOME: estilo Neon adaptativo con azul marino neon
   (`AZUL_MARINO_NEON` = `#3b5bdb`) como acento en ambos modos.

Este módulo es la ÚNICA FUENTE DE VERDAD para:

1. Datos institucionales (nombre, teléfonos, direcciones, redes).
2. Sombras, radios y dimensiones reutilizables.
3. Paleta de colores semántica (adaptativa al color_mode).
4. Esquema Neon del home (tokens adaptativos light/dark).
5. Estilos predefinidos (páginas, enlaces, botones).
6. Fuentes y hojas de estilo externas.

Filosofía de color
------------------
- Colores semánticos (texto, bordes, fondos) usan tokens Radix vía
  `rx.color(...)` — adaptativos al color_mode automáticamente.
- Colores del home usan tokens adaptativos (`rx.color_mode_cond`) —
  el fondo, el texto y los bordes cambian; el AZUL MARINO permanece
  como acento de marca en ambos modos.
- El AZUL MARINO NEON (`AZUL_MARINO_NEON` = `#3b5bdb`) es el acento
  ÚNICO del proyecto. Todas las carreras comparten el mismo acento.

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

Nota técnica: TIPADO DE `REDES_SOCIALES`
----------------------------------------
`REDES_SOCIALES` usa `TypedDict` (`RedSocial`) en lugar de `dict`
genérico. Esto garantiza que `rx.foreach` sobre las redes no falle
con `ForeachVarError: Could not foreach over var of type Any`.

Nota técnica: NOMBRES DE ICONOS LUCIDE
--------------------------------------
Los iconos siguen el formato **kebab-case** oficial de Lucide
(https://lucide.dev/icons). Reflex tolera snake_case pero kebab-case
evita sorpresas al actualizar la versión de Lucide:

    ✅ music-2        ❌ music_2
    ✅ circle-play    ❌ circle_play
    ✅ message-circle ❌ message_circle
"""

from __future__ import annotations

import reflex as rx
from typing import TypedDict


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
# 2. ESQUEMA DE COLOR BASE (azul primario + azul marino)
# ======================================================================

# --- Colores base solicitados (referencia) ---
COLOR_AZUL_PRIMARIO_HEX = "#0000FF"      # Azul primario (puro)
COLOR_AZUL_MARINO_HEX = "#000080"        # Azul marino

# --- Tokens Radix equivalentes (los que se usan en la práctica) ---
# La paleta Radix `blue` es el equivalente profesional del azul puro.
COLOR_PRIMARIO = rx.color("blue", 9)      # Botones, CTAs
COLOR_PRIMARIO_HOVER = rx.color("blue", 10)
COLOR_PRIMARIO_ACTIVO = rx.color("blue", 11)
COLOR_MARINO = rx.color("blue", 12)       # Texto principal, headers
COLOR_MARINO_SUAVE = rx.color("blue", 11)

# Nombre del accent para `rx.theme(accent_color=...)`
ACCENT_COLOR_TEMA = "blue"


# ======================================================================
# 3. REDES SOCIALES
# ======================================================================

TIKTOK_URL = "https://www.tiktok.com/@instein.oficial"
FACEBOOK_URL = "https://www.facebook.com/instein.oficial"
INSTAGRAM_URL = "https://www.instagram.com/instein.oficial"
TELEGRAM_URL = "https://t.me/instein_oficial"
DISCORD_URL = "https://discord.gg/instein"
YOUTUBE_URL = "https://www.youtube.com/@instein_oficial"
WHATSAPP_CANAL_URL = "https://whatsapp.com/channel/instein"


class RedSocial(TypedDict):
    """
    Estructura de una red social institucional.

    Attributes:
        nombre: Nombre visible (ej: "Facebook").
        icono: Nombre del icono Lucide en kebab-case.
        url: URL del perfil institucional.
        color: Color corporativo oficial (hex, no cambia con el modo).
    """

    nombre: str
    icono: str
    url: str
    color: str


# Colores corporativos de cada red (NO cambian con el modo; son de marca).
REDES_SOCIALES: list[RedSocial] = [
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
        "icono": "music-2",
        "url": TIKTOK_URL,
        "color": "#000000",
    },
    {
        "nombre": "YouTube",
        "icono": "circle-play",
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
        "icono": "message-circle",
        "url": DISCORD_URL,
        "color": "#5865F2",
    },
]


# ======================================================================
# 4. SOMBRAS
# ======================================================================

SOMBRA_SUAVE = "0 1px 2px 0 rgb(0 0 0 / 0.05)"
SOMBRA_MEDIA = "0 4px 12px -2px rgb(0 0 255 / 0.25)"
SOMBRA_FUERTE = "0 10px 25px -5px rgb(0 0 255 / 0.20)"
SOMBRA_CAJA = "0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)"


def sombra_hover_acento() -> rx.Var | str:
    """
    Sombra tintada de acento para estados hover.

    Se calcula dinámicamente porque depende del accent_color del tema.
    """
    return f"0 12px 32px -8px {rx.color('blue', 8)}"


# ======================================================================
# 5. RADIOS
# ======================================================================

RADIO_PEQUENO = "0.5rem"
RADIO_MEDIO = "0.75rem"
RADIO_GRANDE = "1rem"
RADIO_EXTRA_GRANDE = "1.5rem"
RADIO_PASTILLA = "9999px"
RADIO_BORDE = "var(--radius-2)"


# ======================================================================
# 6. DIMENSIONES
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
# 7. PALETA SEMÁNTICA (tokens Radix — adaptativos al color_mode)
# ======================================================================
# Todos los colores de acento usan la paleta `blue`.
# ----------------------------------------------------------------------

# --- Texto ---
COLOR_TEXTO_PRINCIPAL = rx.color("gray", 12)
COLOR_TEXTO_SECUNDARIO = rx.color("gray", 11)
COLOR_TEXTO_CUERPO = rx.color("gray", 11)
COLOR_TEXTO_APAGADO = rx.color("gray", 10)
COLOR_GRIS = rx.color("gray", 11)
COLOR_TEXTO = rx.color("gray", 11)

# --- Fondos ---
COLOR_FONDO_CARTA = rx.color("gray", 1)
COLOR_FONDO_SUAVE = rx.color("gray", 2)
COLOR_FONDO_GRIS = rx.color("gray", 3)

# --- Bordes ---
COLOR_BORDE_SUAVE = rx.color("gray", 6)
COLOR_BORDE_HOVER = rx.color("gray", 7)
COLOR_BORDE_ACTIVO = rx.color("gray", 8)
COLOR_DIVISOR = rx.color("gray", 4)
BORDE_PREDETERMINADO = f"1px solid {COLOR_BORDE_SUAVE}"

# --- Acento (forzado a `blue`) ---
COLOR_ACENTO_SOLIDO = rx.color("blue", 9)
COLOR_ACENTO_TEXTO_SOLIDO = "var(--blue-9-contrast)"
COLOR_ACENTO_TEXTO = rx.color("blue", 11)
COLOR_ACENTO_FONDO = rx.color("blue", 3)
COLOR_ACENTO_BORDE = rx.color("blue", 7)
COLOR_ACENTO = rx.color("blue", 1)
COLOR_FONDO_ACENTO = COLOR_ACENTO_FONDO  # Alias retrocompatible

# --- Estados semánticos (éxito, warning, error) ---
COLOR_EXITO_TEXTO = rx.color("green", 11)
COLOR_EXITO_FONDO = rx.color("green", 3)
COLOR_EXITO_SOLIDO = rx.color("green", 9)

COLOR_ALERTA_TEXTO = rx.color("amber", 11)
COLOR_ALERTA_FONDO = rx.color("amber", 3)

COLOR_ERROR_TEXTO = rx.color("red", 11)
COLOR_ERROR_FONDO = rx.color("red", 3)


# ======================================================================
# 8. ESQUEMA NEON (colores hex de referencia)
# ======================================================================
# Inspirado en neon.com: mucho contraste y espaciado generoso.
#
# ⚠️  Estos colores son HEX/RGBA intencionales (NO son tokens Radix).
#     Se usan como valores de referencia para los tokens adaptativos
#     de la sección 14.
# ----------------------------------------------------------------------

# --- Colores base ---
AZUL_MARINO_HEX = "#000080"
AZUL_MARINO_PROFUNDO = "#0a0f2e"      # #000080 oscurecido
AZUL_MARINO_CLARO = "#1a237e"         # #000080 aclarado
AZUL_MARINO_NEON = "#3b5bdb"          # Azul "neon" para glows y acentos

# --- Fondos oscuros para el home ---
FONDO_HOME_OSCURO = "#0a0f1f"
FONDO_HOME_OSCURO_2 = "#0f172a"
FONDO_HOME_CARD = "rgba(15, 23, 42, 0.6)"
FONDO_HOME_CARD_HOVER = "rgba(26, 35, 126, 0.4)"

# --- Texto sobre fondo oscuro ---
TEXTO_OSCURO_PRINCIPAL = "#ffffff"
TEXTO_OSCURO_SUAVE = "rgba(255, 255, 255, 0.8)"
TEXTO_OSCURO_MAS_SUAVE = "rgba(255, 255, 255, 0.6)"
TEXTO_OSCURO_APAGADO = "rgba(255, 255, 255, 0.4)"

# --- Bordes sobre fondo oscuro ---
BORDE_OSCURO_SUAVE = "rgba(255, 255, 255, 0.08)"
BORDE_OSCURO_MEDIO = "rgba(255, 255, 255, 0.15)"
BORDE_OSCURO_AZUL = "rgba(59, 91, 219, 0.4)"

# --- Gradientes Neon-style (dark fijo) ---
GRADIENTE_HOME = "linear-gradient(180deg, #0a0f1f 0%, #0f172a 100%)"
GRADIENTE_HOME_HERO = (
    "linear-gradient(135deg, #0a0f1f 0%, #0f172a 50%, #1a237e 100%)"
)
GRADIENTE_TEXTO_AZUL = (
    "linear-gradient(135deg, #ffffff 0%, #a5b4fc 100%)"
)

# --- Tokens Radix para acentos azul marino ---
COLOR_MARINO_TEXTO = rx.color("blue", 11)
COLOR_MARINO_SOLIDO = rx.color("blue", 9)
COLOR_MARINO_HOVER = rx.color("blue", 10)
COLOR_MARINO_FONDO = rx.color("blue", 3)
COLOR_MARINO_BORDE = rx.color("blue", 7)
COLOR_MARINO_GLOW = rx.color("blue", 8)


# ======================================================================
# 9. HELPERS DE ESTILO
# ======================================================================


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
            "box_shadow": f"0 12px 32px -8px {rx.color('blue', 7)}",
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
    """Estilo para un contenedor de icono con fondo sólido de acento."""
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
    """Estilo para un contenedor de icono con fondo suave de acento."""
    return {
        "padding": tamano,
        "border_radius": radio,
        "background": rx.color("blue", 3),
        "border": f"1px solid {rx.color('blue', 6)}",
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
# 10. ESTILOS PREDEFINIDOS
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
# 11. FUENTES
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
# 12. ANIMACIONES CSS GLOBALES
# ======================================================================

ESTILOS_GLOBALES_CSS = {
    "@keyframes pulse": {
        "0%": {"transform": "scale(0.95)", "opacity": "0.5"},
        "50%": {"transform": "scale(1.1)", "opacity": "1"},
        "100%": {"transform": "scale(0.95)", "opacity": "0.5"},
    },
    # Pulso azul (coherente con el esquema)
    "@keyframes borderPulse": {
        "0%": {
            "border-color": "rgba(0, 144, 255, 0.3)",
            "box-shadow": "0 0 0 0 rgba(0, 144, 255, 0.2)",
        },
        "50%": {
            "border-color": "rgba(0, 144, 255, 1)",
            "box-shadow": "0 0 0 4px rgba(0, 144, 255, 0.4)",
        },
        "100%": {
            "border-color": "rgba(0, 144, 255, 0.3)",
            "box-shadow": "0 0 0 0 rgba(0, 144, 255, 0)",
        },
    },
}


# ======================================================================
# 13. HELPERS DE COLOR POR CARRERA — DEPRECADOS Y ELIMINADOS
# ======================================================================
# ❌ ELIMINADOS: `color_carrera_adaptativo()` y
#    `color_suave_carrera_adaptativo()`.
#
# Motivo
# ------
# El proyecto decidió unificar el acento visual bajo un único azul
# marino (`AZUL_MARINO_NEON` = `#3b5bdb`). Los dos helpers existían
# solo para mantener compatibilidad durante la migración. Una vez
# completada, se eliminaron para reducir indirección y evitar que
# nuevos componentes los usen por error.
#
# Migración aplicada
# ------------------
# Los siguientes archivos migraron de los helpers a constantes
# directas (`AZUL_MARINO_NEON`, `FONDO_AZUL_SUAVE`):
#
# - `componentes/tarjetas_carrera.py`
# - `componentes/vinetas.py`
# - `componentes/secciones_detalle.py`
# - `componentes/hero_carreras.py`
# - `componentes/explorador/helpers.py`
# - `componentes/explorador/buscador.py`
# - `componentes/explorador/contenido.py`
# - `componentes/explorador/widgets_explorador.py`
# - `vistas/vista_detalle_carrera.py`
#
# Cómo revertir (si algún día se quiere colorear por carrera)
# -----------------------------------------------------------
# 1. Crear un módulo DEDICADO `infraestructura/colores_carrera.py`
#    con funciones que lean `carrera["color_principal"]` y
#    `carrera["color_suave"]`, aplicando `rx.color_mode_cond` para
#    light/dark.
#
# 2. NO reintroducir los helpers en este módulo. Este archivo debe
#    seguir siendo la única fuente de verdad para constantes visuales
#    globales, no para reglas de negocio por carrera.
#
# 3. Migrar los componentes consumidores al nuevo módulo.
#
# Referencia del acento único
# ---------------------------
# - Color sólido: `AZUL_MARINO_NEON` (`#3b5bdb`).
# - Color suave adaptativo: `FONDO_AZUL_SUAVE` (Var adaptativa).
# - Borde adaptativo: `BORDE_HOME_AZUL` (Var adaptativa).
# ----------------------------------------------------------------------


# ======================================================================
# 14. TOKENS ADAPTATIVOS DEL HOME (dark ↔ light)
# ======================================================================
# Estos tokens encapsulan la lógica de `rx.color_mode_cond` para que
# los componentes del home puedan cambiar entre modo claro y oscuro
# sin repetir el condicional en cada uno.
#
# ✅ El AZUL MARINO es el acento en AMBOS modos (color de marca).
#    Lo que cambia es el fondo, el texto y los bordes.
# ----------------------------------------------------------------------

# --- Fondos principales ---
FONDO_HOME = rx.color_mode_cond(
    light="#f8fafc",
    dark="#0a0f1f",
)

FONDO_HOME_CARD_ADAPTATIVO = rx.color_mode_cond(
    light="rgba(255, 255, 255, 0.8)",      # blanco translúcido
    dark="rgba(15, 23, 42, 0.6)",          # azul oscuro translúcido
)

FONDO_HOME_HERO = rx.color_mode_cond(
    light="linear-gradient(135deg, #f8fafc 0%, #e0e7ff 50%, #c7d2fe 100%)",
    dark="linear-gradient(135deg, #0a0f1f 0%, #0f172a 50%, #1a237e 100%)",
)

# --- Texto ---
TEXTO_HOME_PRINCIPAL = rx.color_mode_cond(
    light="#0f172a",       # gris muy oscuro
    dark="#ffffff",
)

TEXTO_HOME_SUAVE = rx.color_mode_cond(
    light="rgba(15, 23, 42, 0.75)",
    dark="rgba(255, 255, 255, 0.8)",
)

TEXTO_HOME_MAS_SUAVE = rx.color_mode_cond(
    light="rgba(15, 23, 42, 0.6)",
    dark="rgba(255, 255, 255, 0.6)",
)

TEXTO_HOME_APAGADO = rx.color_mode_cond(
    light="rgba(15, 23, 42, 0.4)",
    dark="rgba(255, 255, 255, 0.4)",
)

# --- Bordes ---
BORDE_HOME_SUAVE = rx.color_mode_cond(
    light="rgba(15, 23, 42, 0.1)",
    dark="rgba(255, 255, 255, 0.08)",
)

BORDE_HOME_MEDIO = rx.color_mode_cond(
    light="rgba(15, 23, 42, 0.15)",
    dark="rgba(255, 255, 255, 0.15)",
)

BORDE_HOME_AZUL = rx.color_mode_cond(
    light="rgba(59, 91, 219, 0.5)",
    dark="rgba(59, 91, 219, 0.4)",
)

# --- Glassmorphism (fondo de la barra sticky) ---
FONDO_BARRA_HOME = rx.color_mode_cond(
    light="rgba(255, 255, 255, 0.75)",
    dark="rgba(10, 15, 31, 0.75)",
)

# --- Gradiente de texto del título ---
GRADIENTE_TEXTO_HOME = rx.color_mode_cond(
    light="linear-gradient(135deg, #1a237e 0%, #3b5bdb 100%)",
    dark="linear-gradient(135deg, #ffffff 0%, #a5b4fc 100%)",
)

# --- Fondos tintados del acento (azul marino translúcido) ---
FONDO_AZUL_SUAVE = rx.color_mode_cond(
    light="rgba(59, 91, 219, 0.1)",
    dark="rgba(59, 91, 219, 0.15)",
)

FONDO_AZUL_MUY_SUAVE = rx.color_mode_cond(
    light="rgba(59, 91, 219, 0.05)",
    dark="rgba(59, 91, 219, 0.1)",
)

# --- Sombra hover de cards ---
SOMBRA_HOVER_CARD_HOME = rx.color_mode_cond(
    light=f"0 20px 40px -10px {AZUL_MARINO_NEON}40",
    dark=f"0 20px 40px -10px {AZUL_MARINO_NEON}",
)

# --- Gradiente del banner CTA final (adaptativo) ---
GRADIENTE_HOME_BANNER = rx.color_mode_cond(
    light="linear-gradient(135deg, #eef2ff 0%, #c7d2fe 50%, #a5b4fc 100%)",
    dark="linear-gradient(135deg, #0a0f1f 0%, #0f172a 50%, #1a237e 100%)",
)


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
    # --- Esquema de color base ---
    "ACCENT_COLOR_TEMA",
    "COLOR_AZUL_MARINO_HEX",
    "COLOR_AZUL_PRIMARIO_HEX",
    "COLOR_MARINO",
    "COLOR_MARINO_SUAVE",
    "COLOR_PRIMARIO",
    "COLOR_PRIMARIO_ACTIVO",
    "COLOR_PRIMARIO_HOVER",
    # --- Redes sociales ---
    "DISCORD_URL",
    "FACEBOOK_URL",
    "INSTAGRAM_URL",
    "REDES_SOCIALES",
    "RedSocial",
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
    # --- Esquema Neon (hex de referencia) ---
    "AZUL_MARINO_CLARO",
    "AZUL_MARINO_HEX",
    "AZUL_MARINO_NEON",
    "AZUL_MARINO_PROFUNDO",
    "BORDE_OSCURO_AZUL",
    "BORDE_OSCURO_MEDIO",
    "BORDE_OSCURO_SUAVE",
    "COLOR_MARINO_BORDE",
    "COLOR_MARINO_FONDO",
    "COLOR_MARINO_GLOW",
    "COLOR_MARINO_HOVER",
    "COLOR_MARINO_SOLIDO",
    "COLOR_MARINO_TEXTO",
    "FONDO_HOME_CARD",
    "FONDO_HOME_CARD_HOVER",
    "FONDO_HOME_OSCURO",
    "FONDO_HOME_OSCURO_2",
    "GRADIENTE_HOME",
    "GRADIENTE_HOME_HERO",
    "GRADIENTE_TEXTO_AZUL",
    "TEXTO_OSCURO_APAGADO",
    "TEXTO_OSCURO_MAS_SUAVE",
    "TEXTO_OSCURO_PRINCIPAL",
    "TEXTO_OSCURO_SUAVE",
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
    # --- Tokens adaptativos del home ---
    "FONDO_HOME",
    "FONDO_HOME_CARD_ADAPTATIVO",
    "FONDO_HOME_HERO",
    "TEXTO_HOME_PRINCIPAL",
    "TEXTO_HOME_SUAVE",
    "TEXTO_HOME_MAS_SUAVE",
    "TEXTO_HOME_APAGADO",
    "BORDE_HOME_SUAVE",
    "BORDE_HOME_MEDIO",
    "BORDE_HOME_AZUL",
    "FONDO_BARRA_HOME",
    "GRADIENTE_TEXTO_HOME",
    "FONDO_AZUL_SUAVE",
    "FONDO_AZUL_MUY_SUAVE",
    "SOMBRA_HOVER_CARD_HOME",
    "GRADIENTE_HOME_BANNER",
]