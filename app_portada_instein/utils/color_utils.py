"""
Utilidades auxiliares para manipulación de colores.

✅ ACTUALIZADO: se agregan helpers para el esquema de color azul
   (primario + marino) y generación de paletas coherentes.
"""

from __future__ import annotations

from typing import Optional


# ======================================================================
# COLORES BASE DEL PROYECTO
# ======================================================================

# Azul primario (solicitado): #0000FF
AZUL_PRIMARIO = "#0000FF"
# Azul marino (solicitado): #000080
AZUL_MARINO = "#000080"

# Equivalentes Radix (profesionales, con contraste WCAG AA)
RADIX_BLUE_9 = "#0090FF"       # accent-9 light
RADIX_BLUE_10 = "#0077FF"      # accent-10 light (hover)
RADIX_BLUE_11 = "#006ADC"      # accent-11 light (texto)
RADIX_BLUE_12 = "#00254D"      # accent-12 light (texto máximo)

RADIX_BLUE_9_DARK = "#3E63DD"  # accent-9 dark
RADIX_BLUE_12_DARK = "#C2D6FF" # accent-12 dark


# ======================================================================
# FUNCIONES BÁSICAS
# ======================================================================

def invertir_color_hexadecimal(color_hexadecimal: str) -> str:
    """
    Invierte un color hexadecimal (ej: '#9ebae4' → '#61451b').

    Args:
        color_hexadecimal: Color en formato #RRGGBB.

    Returns:
        Color invertido en el mismo formato.

    Raises:
        ValueError: Si el color no tiene 6 dígitos hexadecimales.
    """
    codigo = color_hexadecimal.strip().lstrip("#")
    if len(codigo) != 6:
        raise ValueError("Se esperaba un color de 6 dígitos como #RRGGBB")

    rojo = 255 - int(codigo[0:2], 16)
    verde = 255 - int(codigo[2:4], 16)
    azul = 255 - int(codigo[4:6], 16)
    return f"#{rojo:02x}{verde:02x}{azul:02x}"


# ======================================================================
# HELPERS PARA EL ESQUEMA AZUL
# ======================================================================

def hex_a_rgb(color_hex: str) -> tuple[int, int, int]:
    """
    Convierte '#RRGGBB' a tupla (r, g, b).

    Args:
        color_hex: Color en formato #RRGGBB.

    Returns:
        Tupla (r, g, b) con valores 0-255.
    """
    codigo = color_hex.strip().lstrip("#")
    if len(codigo) != 6:
        raise ValueError("Se esperaba un color de 6 dígitos como #RRGGBB")
    return (int(codigo[0:2], 16), int(codigo[2:4], 16), int(codigo[4:6], 16))


def rgb_a_hex(rojo: int, verde: int, azul: int) -> str:
    """Convierte (r, g, b) a '#rrggbb'."""
    return f"#{rojo:02x}{verde:02x}{azul:02x}"


def aclarar(color_hex: str, factor: float = 0.2) -> str:
    """
    Aclara un color mezclándolo con blanco.

    Args:
        color_hex: Color base.
        factor: 0.0 = sin cambio, 1.0 = blanco puro.

    Returns:
        Color aclarado.
    """
    r, g, b = hex_a_rgb(color_hex)
    r = int(r + (255 - r) * factor)
    g = int(g + (255 - g) * factor)
    b = int(b + (255 - b) * factor)
    return rgb_a_hex(r, g, b)


def oscurecer(color_hex: str, factor: float = 0.2) -> str:
    """
    Oscurece un color mezclándolo con negro.

    Args:
        color_hex: Color base.
        factor: 0.0 = sin cambio, 1.0 = negro puro.

    Returns:
        Color oscurecido.
    """
    r, g, b = hex_a_rgb(color_hex)
    r = int(r * (1 - factor))
    g = int(g * (1 - factor))
    b = int(b * (1 - factor))
    return rgb_a_hex(r, g, b)


def generar_paleta_azul() -> dict[str, str]:
    """
    Genera la paleta completa del azul del proyecto.

    Returns:
        Diccionario con los 12 pasos de la escala Radix blue + base.
    """
    return {
        # Equivalentes Radix (recomendados)
        "blue_1": "#FBFDFF",
        "blue_2": "#F4FAFF",
        "blue_3": "#DCF2FF",
        "blue_4": "#C9EAFF",
        "blue_5": "#B4E1FF",
        "blue_6": "#9BD5FF",
        "blue_7": "#7AC0FF",
        "blue_8": "#4DA3FF",
        "blue_9": RADIX_BLUE_9,     # #0090FF  ← acento principal
        "blue_10": RADIX_BLUE_10,   # #0077FF  ← hover
        "blue_11": RADIX_BLUE_11,   # #006ADC  ← texto acento
        "blue_12": RADIX_BLUE_12,   # #00254D  ← texto máximo
        # Colores base del proyecto
        "azul_primario": AZUL_PRIMARIO,   # #0000FF
        "azul_marino": AZUL_MARINO,       # #000080
    }


def color_contraste_para(fondo_hex: str) -> str:
    """
    Devuelve '#FFFFFF' o '#000000' según qué contraste mejor con el fondo.

    Usa la fórmula de luminancia relativa (WCAG).

    Args:
        fondo_hex: Color de fondo en #RRGGBB.

    Returns:
        '#FFFFFF' o '#000000'.
    """
    r, g, b = hex_a_rgb(fondo_hex)

    def _canal(c: int) -> float:
        c_norm = c / 255.0
        return c_norm / 12.92 if c_norm <= 0.03928 else ((c_norm + 0.055) / 1.055) ** 2.4

    luminancia = 0.2126 * _canal(r) + 0.7152 * _canal(g) + 0.0722 * _canal(b)
    return "#FFFFFF" if luminancia < 0.5 else "#000000"