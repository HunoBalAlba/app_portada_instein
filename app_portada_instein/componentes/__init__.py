"""
Capa de presentación: componentes reutilizables.

Cada módulo agrupa componentes con una responsabilidad concreta:
- primitivos: helpers base (contenedor_clicable, enlace_navegacion, etc.)
- barra_navegacion: navbar superior con enlaces y botón de tema
- tarjetas_carrera: tarjetas y filas de carreras/materias
- vinetas: viñetas para listas con iconos
- secciones_detalle: secciones de la vista de detalle
- explorador_carrera: explorador estilo Leonardo AI
- hero_principal: hero unificado del home
- por_que_instein: sección "¿Por qué INSTEIN?"
- estadisticas_instituto: bloque de estadísticas
- preguntas_frecuentes: FAQ con acordeón
- banner_cta_final: banner CTA final
- pie_pagina: footer institucional
"""

# ======================================================================
# Primitivos
# ======================================================================
from .primitivos import (
    contenedor_clicable,
    enlace_navegacion,
    tarjeta_estilizada,
    tarjeta_informacion_pequena,
)

from .multimedia_institucional import seccion_multimedia_institucional
# ======================================================================
# Navegación
# ======================================================================
from .barra_navegacion import (
    barra_navegacion_superior,
    elemento_menu,
)

# ======================================================================
# Tarjetas de carrera y plan de estudios
# ======================================================================
from .tarjetas_carrera import (
    tarjeta_carrera,
    pastilla_anio,
    fila_materia,
)

# ======================================================================
# Viñetas
# ======================================================================
from .vinetas import (
    vineta_perfil_profesional,
    vineta_campo_laboral,
)

# ======================================================================
# Secciones de detalle
# ======================================================================
from .secciones_detalle import (
    seccion_informacion,
    seccion_plan_estudios,
    seccion_perfil_y_campo_laboral,
)

# ======================================================================
# Explorador de carrera (estilo Leonardo AI)
# ======================================================================
from .explorador_carrera import explorador_carrera_destacada

# ======================================================================
# Hero principal
# ======================================================================
from .hero_principal import hero_principal

# ======================================================================
# Secciones adicionales del home
# ======================================================================
from .por_que_instein import seccion_por_que_instein
from .estadisticas_instituto import seccion_estadisticas
from .preguntas_frecuentes import seccion_preguntas_frecuentes
from .banner_cta_final import banner_cta_final

# ======================================================================
# Pie de página
# ======================================================================
from .pie_pagina import pie_pagina_institucional


__all__ = [
    # --- Primitivos ---
    "contenedor_clicable",
    "enlace_navegacion",
    "tarjeta_estilizada",
    "tarjeta_informacion_pequena",

    # --- Navegación ---
    "barra_navegacion_superior",
    "elemento_menu",

    # --- Tarjetas ---
    "tarjeta_carrera",
    "pastilla_anio",
    "fila_materia",

    # --- Viñetas ---
    "vineta_perfil_profesional",
    "vineta_campo_laboral",

    # --- Secciones de detalle ---
    "seccion_informacion",
    "seccion_plan_estudios",
    "seccion_perfil_y_campo_laboral",

    # --- Explorador de carrera ---
    "explorador_carrera_destacada",

    # --- Hero principal ---
    "hero_principal",

    # --- Secciones adicionales ---
    "seccion_por_que_instein",
    "seccion_estadisticas",
    "seccion_preguntas_frecuentes",
    "banner_cta_final",

    # --- Pie de página ---
    "pie_pagina_institucional",

    "seccion_multimedia_institucional",
]