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
from .banner_cta_final import banner_cta_final

# ======================================================================
# Navegación
# ======================================================================
from .barra_navegacion import (
    barra_navegacion_superior,
    elemento_menu,
)
from .estadisticas_instituto import seccion_estadisticas

# ======================================================================
# Explorador de carrera (estilo Leonardo AI)
# ======================================================================
from .explorador_carrera import explorador_carrera_destacada

# ======================================================================
# Hero principal
# ======================================================================
from .hero_principal import hero_principal
from .multimedia_institucional import seccion_multimedia_institucional

# ======================================================================
# Pie de página
# ======================================================================
from .pie_pagina import pie_pagina_institucional

# ======================================================================
# Secciones adicionales del home
# ======================================================================
from .por_que_instein import seccion_por_que_instein
from .preguntas_frecuentes import seccion_preguntas_frecuentes
from .primitivos import (
    contenedor_clicable,
    enlace_navegacion,
    tarjeta_estilizada,
    tarjeta_informacion_pequena,
)

# ======================================================================
# Secciones de detalle
# ======================================================================
from .secciones_detalle import (
    seccion_informacion,
    seccion_perfil_y_campo_laboral,
    seccion_plan_estudios,
)

# ======================================================================
# Tarjetas de carrera y plan de estudios
# ======================================================================
from .tarjetas_carrera import (
    fila_materia,
    pastilla_anio,
    tarjeta_carrera,
)

# ======================================================================
# Viñetas
# ======================================================================
from .vinetas import (
    vineta_campo_laboral,
    vineta_perfil_profesional,
)


__all__ = [
    "banner_cta_final",
    # --- Navegación ---
    "barra_navegacion_superior",
    # --- Primitivos ---
    "contenedor_clicable",
    "elemento_menu",
    "enlace_navegacion",
    # --- Explorador de carrera ---
    "explorador_carrera_destacada",
    "fila_materia",
    # --- Hero principal ---
    "hero_principal",
    "pastilla_anio",
    # --- Pie de página ---
    "pie_pagina_institucional",
    "seccion_estadisticas",
    # --- Secciones de detalle ---
    "seccion_informacion",
    "seccion_multimedia_institucional",
    "seccion_perfil_y_campo_laboral",
    "seccion_plan_estudios",
    # --- Secciones adicionales ---
    "seccion_por_que_instein",
    "seccion_preguntas_frecuentes",
    # --- Tarjetas ---
    "tarjeta_carrera",
    "tarjeta_estilizada",
    "tarjeta_informacion_pequena",
    "vineta_campo_laboral",
    # --- Viñetas ---
    "vineta_perfil_profesional",
]
