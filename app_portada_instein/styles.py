"""
Estilos, constantes visuales y datos institucionales.

Tipografías:
- Inter → texto general de la interfaz (misma que usa reflex.dev/docs).
- JetBrains Mono → bloques de código y contenido técnico.
"""


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
# 2. SOMBRAS Y RADIOS
# ======================================================================

SOMBRA_SUAVE = "0 1px 2px 0 rgb(0 0 0 / 0.05)"
SOMBRA_MEDIA = "0 4px 12px -2px rgb(37 99 235 / 0.30)"
SOMBRA_FUERTE = "0 10px 25px -5px rgb(37 99 235 / 0.25)"
SOMBRA_CAJA = "0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)"

RADIO_PEQUENO = "0.5rem"
RADIO_MEDIO = "0.75rem"
RADIO_GRANDE = "1rem"
RADIO_EXTRA_GRANDE = "1.5rem"
RADIO_PASTILLA = "9999px"
RADIO_BORDE = "var(--radius-2)"

# ======================================================================
# 3. COLORES SEMÁNTICOS — usar variables CSS de Radix
# ======================================================================

BORDE_PREDETERMINADO = "1px solid var(--gray-5)"
COLOR_TEXTO = "var(--gray-11)"
COLOR_GRIS = "var(--gray-11)"
COLOR_FONDO_GRIS = "var(--gray-3)"

COLOR_TEXTO_ACENTO = "var(--accent-10)"
COLOR_ACENTO = "var(--accent-1)"
COLOR_FONDO_ACENTO = "var(--accent-3)"

HOVER_COLOR_ACENTO = {"_hover": {"color": COLOR_TEXTO_ACENTO}}
HOVER_FONDO_ACENTO = {"_hover": {"background_color": COLOR_ACENTO}}

# ======================================================================
# 4. DIMENSIONES
# ======================================================================

ANCHO_CONTENIDO_VW = "90vw"
ANCHO_MENU_LATERAL = "32em"
ANCHO_CONTENIDO_MENU = "16em"
ANCHO_MAXIMO = "1480px"
TAMANOS_CAJA_COLOR = ["2.25rem", "2.25rem", "2.5rem"]

# ======================================================================
# 5. ESTILOS PREDEFINIDOS
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

ESTILO_ENLACE = {
    "color": COLOR_TEXTO_ACENTO,
    "text_decoration": "none",
    **HOVER_COLOR_ACENTO,
}

ESTILO_BOTON_SUPERPUESTO = {
    "background_color": "white",
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
# 6. FUENTES Y HOJAS DE ESTILO EXTERNAS
# ======================================================================
# Inter → misma fuente que usa la documentación oficial de Reflex
# (construida sobre Radix Themes).
# JetBrains Mono → fuente monoespaciada para bloques de código.

FUENTE_PRINCIPAL = "Inter"
FUENTE_MONOESPACIADA = "JetBrains Mono"

HOJAS_DE_ESTILO_BASE = [
    # Inter (texto general) — pesos 400 a 900 + versión variable.
    "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap",
    # JetBrains Mono (bloques de código)
    "https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&display=swap",
]

# ======================================================================
# 6.bis FUENTES POR ETIQUETA HTML
# ======================================================================
# Reflex NO soporta selectores anidados por etiqueta HTML dentro de
# `style=`. Sin embargo, sí permite pasar reglas sueltas que aplican
# a elementos específicos vía la API `style`. Para aplicar la fuente
# a <code>, <pre>, <kbd>, <button>, <input>, etc., usamos un dict con
# las claves correspondientes.
#
# ⚠️ Nota importante: para selectores complejos por etiqueta HTML
# (por ejemplo `code { font-family: ... }`), Reflex ignora estas
# reglas si están dentro de `style=`. La forma correcta es:
#   1. Crear `assets/styles/global.css` con los selectores CSS puros.
#   2. Añadirlo a `stylesheets=[...]` en `rx.App`.
#
# `ESTILO_BASE` se mantiene por compatibilidad con el código existente
# y para documentar la intención. Su contenido se aplica como base
# para todos los componentes de Reflex.

# Cadena de fallbacks estándar de Radix Themes para máxima compatibilidad
# cross-platform (macOS, Windows, Linux, Android, iOS).
FALLBACK_SANS = (
    '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif'
)
FALLBACK_MONO = (
    '"JetBrains Mono", "SF Mono", Monaco, "Cascadia Code", '
    '"Roboto Mono", Consolas, "Courier New", monospace'
)

ESTILO_BASE = {
    "font_family": f'"{FUENTE_PRINCIPAL}", {FALLBACK_SANS}',
    "code": {
        "font_family": f'"{FUENTE_MONOESPACIADA}", {FALLBACK_MONO}',
    },
    "pre": {
        "font_family": f'"{FUENTE_MONOESPACIADA}", {FALLBACK_MONO}',
    },
    "kbd": {
        "font_family": f'"{FUENTE_MONOESPACIADA}", {FALLBACK_MONO}',
    },
    "button": {
        "font_family": f'"{FUENTE_PRINCIPAL}", {FALLBACK_SANS}',
    },
    "input": {
        "font_family": f'"{FUENTE_PRINCIPAL}", {FALLBACK_SANS}',
    },
    "textarea": {
        "font_family": f'"{FUENTE_PRINCIPAL}", {FALLBACK_SANS}',
    },
    "select": {
        "font_family": f'"{FUENTE_PRINCIPAL}", {FALLBACK_SANS}',
    },
}

# ======================================================================
# 7. ANIMACIONES CSS GLOBALES
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


__all__ = [
    "ANCHO_CONTENIDO_MENU",
    # Dimensiones
    "ANCHO_CONTENIDO_VW",
    "ANCHO_MAXIMO",
    "ANCHO_MENU_LATERAL",
    "ANIO_COPYRIGHT",
    # Colores
    "BORDE_PREDETERMINADO",
    "COLOR_ACENTO",
    "COLOR_FONDO_ACENTO",
    "COLOR_FONDO_GRIS",
    "COLOR_GRIS",
    "COLOR_TEXTO",
    "COLOR_TEXTO_ACENTO",
    "DIRECCION",
    "EMAIL_CONTACTO",
    "ENTIDAD_COPYRIGHT",
    # Animaciones
    "ESTILOS_GLOBALES_CSS",
    "ESTILO_BASE",
    "ESTILO_BOTON_SUPERPUESTO",
    "ESTILO_CONTENIDO_PLANTILLA",
    "ESTILO_ENLACE",
    # Estilos
    "ESTILO_PAGINA_PLANTILLA",
    "ESTILO_SELECTOR_COLOR",
    "FALLBACK_MONO",
    "FALLBACK_SANS",
    "FUENTE_MONOESPACIADA",
    # Fuentes
    "FUENTE_PRINCIPAL",
    "GITHUB_URL",
    "HOJAS_DE_ESTILO_BASE",
    "HORARIO_ATENCION",
    "HOVER_COLOR_ACENTO",
    "HOVER_FONDO_ACENTO",
    "NOMBRE_COMPLETO_INSTITUTO",
    # Datos institucionales
    "NOMBRE_INSTITUTO",
    "RADIO_BORDE",
    "RADIO_EXTRA_GRANDE",
    "RADIO_GRANDE",
    "RADIO_MEDIO",
    "RADIO_PASTILLA",
    "RADIO_PEQUENO",
    "SOMBRA_CAJA",
    "SOMBRA_FUERTE",
    "SOMBRA_MEDIA",
    # Sombras y radios
    "SOMBRA_SUAVE",
    "TAMANOS_CAJA_COLOR",
    "TELEFONO_PRINCIPAL",
    "TELEFONO_SECUNDARIO",
    "UBICACION_FISICA",
    "WHATSAPP_URL",
]
