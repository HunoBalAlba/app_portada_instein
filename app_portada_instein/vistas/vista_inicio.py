"""
Vista de la página de inicio (ruta "/").

Composición de secciones (orden de arriba a abajo):
1. Barra de navegación superior (sticky).
2. Hero principal con título, CTA y explorador de carreras.
3. Sección multimedia institucional (video + redes sociales).
4. Estadísticas del instituto (5 carreras, 500+ egresados, etc.).
5. Sección "¿Por qué INSTEIN?" con tarjetas de beneficios.
6. Preguntas frecuentes (acordeón).
7. Banner CTA final con llamado a la acción.
8. Pie de página institucional.

Todas las secciones respetan el mismo ancho máximo (`72rem`) y
mantienen un espaciado vertical consistente entre ellas.
"""

import reflex as rx

from app_portada_instein.componentes.banner_cta_final import banner_cta_final
from app_portada_instein.componentes.barra_navegacion import barra_navegacion_superior
from app_portada_instein.componentes.estadisticas_instituto import seccion_estadisticas
from app_portada_instein.componentes.hero_principal import hero_principal
from app_portada_instein.componentes.multimedia_institucional import (
    seccion_multimedia_institucional,
)
from app_portada_instein.componentes.pie_pagina import pie_pagina_institucional
from app_portada_instein.componentes.por_que_instein import seccion_por_que_instein
from app_portada_instein.componentes.preguntas_frecuentes import (
    seccion_preguntas_frecuentes,
)
from app_portada_instein.infraestructura.constantes_visuales import NOMBRE_INSTITUTO


# ======================================================================
# Constantes de layout
# ======================================================================

# Ancho máximo de las secciones (coincide con el de otras vistas).
MAX_WIDTH_CONTENIDO = "100%"

# Ancho interno de las secciones que necesitan centrar su contenido.
MAX_WIDTH_INTERNO = "72rem"


# ======================================================================
# Vista
# ======================================================================


@rx.page(route="/", title=f"Inicio | {NOMBRE_INSTITUTO}")
def vista_inicio() -> rx.Component:
    """
    Página principal de bienvenida del instituto.

    Estructura:
    - Barra de navegación sticky en la parte superior.
    - Contenido principal (todas las secciones).
    - Pie de página al final.

    El layout usa `rx.vstack` para apilar las secciones verticalmente,
    con `width="100%"` para ocupar todo el ancho del viewport.
    """
    return rx.vstack(
        # =============================================================
        # 1. BARRA DE NAVEGACIÓN (sticky)
        # =============================================================
        barra_navegacion_superior(),
        # =============================================================
        # 2. CONTENIDO PRINCIPAL
        # =============================================================
        rx.box(
            # ---------------------------------------------------------
            # 2.1 Hero principal
            # Título, subtítulo, CTA y explorador de carreras.
            # ---------------------------------------------------------
            hero_principal(),
            # ---------------------------------------------------------
            # 2.2 Multimedia institucional
            # Video institucional + info de la plataforma + redes.
            # ---------------------------------------------------------
            seccion_multimedia_institucional(),
            # ---------------------------------------------------------
            # 2.3 Estadísticas del instituto
            # Carreras, años de experiencia, egresados, empleabilidad.
            # ---------------------------------------------------------
            seccion_estadisticas(),
            # ---------------------------------------------------------
            # 2.4 ¿Por qué INSTEIN?
            # Grid de tarjetas con los beneficios del instituto.
            # ---------------------------------------------------------
            seccion_por_que_instein(),
            # ---------------------------------------------------------
            # 2.5 Preguntas frecuentes
            # Acordeón con las dudas más comunes.
            # ---------------------------------------------------------
            seccion_preguntas_frecuentes(),
            # ---------------------------------------------------------
            # 2.6 Banner CTA final
            # Llamado a la acción con fondo oscuro.
            # ---------------------------------------------------------
            rx.box(
                banner_cta_final(),
                padding="0 1.5rem 3rem 1.5rem",
                width="100%",
                display="flex",
                justify_content="center",
            ),
            # ---------------------------------------------------------
            # Contenedor principal
            # ---------------------------------------------------------
            padding_bottom="3rem",
            max_width=MAX_WIDTH_CONTENIDO,
            width="100%",
        ),
        # =============================================================
        # 3. PIE DE PÁGINA
        # =============================================================
        pie_pagina_institucional(),
        # =============================================================
        # Layout del contenedor raíz
        # =============================================================
        align="center",
        min_height="100vh",
        width="100%",
        spacing="0",
    )