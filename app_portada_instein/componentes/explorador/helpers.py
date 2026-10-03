# app_portada_instein/componentes/explorador/helpers.py

"""
Helpers de color del explorador.

✅ REFACTORIZADO: TODAS las carreras usan azul marino (`AZUL_MARINO_NEON`)
   como acento ÚNICO del proyecto. Ya no hay colores de marca
   individuales.

Los helpers mantienen la misma firma que antes para no romper los
componentes que los consumen (`color_carrera(carrera)`,
`color_carrera_destacada()`, etc.), pero todos devuelven el mismo
color azul marino.

Nota técnica: COLOR_SUAVE adaptativo
------------------------------------
`COLOR_SUAVE` es un `rx.Var` (`FONDO_AZUL_SUAVE`) que se adapta
automáticamente al color_mode del usuario:

- Light mode: `rgba(59, 91, 219, 0.10)` (más suave, sobre fondo claro)
- Dark mode:  `rgba(59, 91, 219, 0.15)` (más visible, sobre fondo oscuro)

⚠️ Si algún componente espera un `str` para concatenar en f-strings
(ej: `f"{color_suave}80"`), debe migrar a usar `FONDO_AZUL_SUAVE`
directamente (que ya incluye su propia transparencia) o definir una
opacidad adicional por separado.

Nota técnica: ACENTO ÚNICO
--------------------------
Los helpers `color_carrera_adaptativo()` y
`color_suave_carrera_adaptativo()` fueron ELIMINADOS de
`constantes_visuales.py`. Este módulo usa directamente
`AZUL_MARINO_NEON` y `FONDO_AZUL_SUAVE`.
"""

from __future__ import annotations

import reflex as rx

from app_portada_instein.infraestructura.constantes_visuales import (
    AZUL_MARINO_NEON,
    FONDO_AZUL_SUAVE,
)


# ======================================================================
# Constantes de color del explorador
# ======================================================================

COLOR_PRINCIPAL: str = AZUL_MARINO_NEON
"""Color sólido principal (para iconos, bordes, hovers).

Es un `str` hex fijo (`#3b5bdb`) porque el acento es el mismo en
ambos modos.
"""

COLOR_SUAVE: rx.Var = FONDO_AZUL_SUAVE
"""Color suave de fondo (para contenedores tintados).

Es un `rx.Var` adaptativo que cambia según el color_mode del usuario.
"""


# ======================================================================
# Helpers (compatibilidad con código existente)
# ======================================================================


def color_carrera(carrera: dict | None = None) -> str:
    """
    Color principal del acento global.

    ✅ REFACTORIZADO: SIEMPRE devuelve azul marino neon, sin importar
    la carrera. Se mantiene el parámetro `carrera` por compatibilidad
    con los llamadores existentes.

    Args:
        carrera: Dict de la carrera (no usado en esta versión).

    Returns:
        Hex del azul marino neon (`#3b5bdb`).
    """
    return COLOR_PRINCIPAL


def color_suave_carrera(carrera: dict | None = None) -> rx.Var:
    """
    Color suave de fondo del acento global.

    ✅ REFACTORIZADO: SIEMPRE devuelve `FONDO_AZUL_SUAVE` (adaptativo
    light/dark).

    Args:
        carrera: Dict de la carrera (no usado en esta versión).

    Returns:
        Var reactiva con el fondo azul marino translúcido.
    """
    return COLOR_SUAVE


def color_carrera_destacada() -> str:
    """
    Color principal del acento global.

    ✅ REFACTORIZADO: SIEMPRE devuelve azul marino neon.

    Returns:
        Hex del azul marino neon (`#3b5bdb`).
    """
    return COLOR_PRINCIPAL


def color_suave_carrera_destacada() -> rx.Var:
    """
    Color suave de fondo del acento global.

    ✅ REFACTORIZADO: SIEMPRE devuelve `FONDO_AZUL_SUAVE` (adaptativo).

    Returns:
        Var reactiva con el fondo azul marino translúcido.
    """
    return COLOR_SUAVE


__all__ = [
    "COLOR_PRINCIPAL",
    "COLOR_SUAVE",
    "color_carrera",
    "color_carrera_destacada",
    "color_suave_carrera",
    "color_suave_carrera_destacada",
]