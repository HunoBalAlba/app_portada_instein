"""
Capa de presentación: componentes reutilizables.

Cada módulo agrupa componentes con una responsabilidad concreta
(primitivos, navegación, tarjetas, viñetas, secciones, widgets).
"""

from .primitivos import (
    contenedor_clicable,
    enlace_navegacion,
    tarjeta_estilizada,
    tarjeta_informacion_pequena,
)
from .barra_navegacion import (
    barra_navegacion_superior,
    elemento_menu,
)
from .tarjetas_carrera import (
    tarjeta_carrera,
    pastilla_anio,
    fila_materia,
)
from .vinetas import (
    vineta_perfil_profesional,
    vineta_campo_laboral,
)
from .secciones_detalle import (
    seccion_informacion,
    seccion_plan_estudios,
    seccion_perfil_y_campo_laboral,
)
from .widgets_home import (
    hero_bienvenida,
    pastilla_carrera_destacada,
    bloque_texto_carrera_destacada,
    cuadro_resumen_multimedia,
)

__all__ = [
    # Primitivos
    "contenedor_clicable",
    "enlace_navegacion",
    "tarjeta_estilizada",
    "tarjeta_informacion_pequena",
    # Navegación
    "barra_navegacion_superior",
    "elemento_menu",
    # Tarjetas
    "tarjeta_carrera",
    "pastilla_anio",
    "fila_materia",
    # Viñetas
    "vineta_perfil_profesional",
    "vineta_campo_laboral",
    # Secciones
    "seccion_informacion",
    "seccion_plan_estudios",
    "seccion_perfil_y_campo_laboral",
    # Widgets home
    "hero_bienvenida",
    "pastilla_carrera_destacada",
    "bloque_texto_carrera_destacada",
    "cuadro_resumen_multimedia",
]