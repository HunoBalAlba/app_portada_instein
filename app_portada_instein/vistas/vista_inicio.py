"""
Vista de la página de inicio (ruta "/") — versión refactorizada.
"""

import reflex as rx

from ..componentes.barra_navegacion import barra_navegacion_superior
from ..componentes.hero_principal import hero_principal
from ..componentes.multimedia_institucional import (
    seccion_multimedia_institucional,
)
from ..componentes.por_que_instein import seccion_por_que_instein
from ..componentes.estadisticas_instituto import seccion_estadisticas
from ..componentes.preguntas_frecuentes import seccion_preguntas_frecuentes
from ..componentes.banner_cta_final import banner_cta_final
from ..componentes.pie_pagina import pie_pagina_institucional
from ..infraestructura.constantes_visuales import (
    NOMBRE_INSTITUTO,
    TELEFONO_PRINCIPAL,
    UBICACION_FISICA,
)


def _boton_ver_carreras() -> rx.Component:
    """CTA principal hacia la vista de carreras."""
    return rx.box(
        rx.link(
            rx.flex(
                rx.icon("book-open", size=20, color="#ffffff"),
                rx.text(
                    "Ver Carreras Disponibles",
                    as_="span",
                    font_weight="700",
                ),
                align="center",
                gap="0.75rem",
            ),
            rx.icon("arrow-right", size=20, color="rgba(255,255,255,0.7)"),
            href="/carreras",
            display="flex",
            align_items="center",
            justify_content="space-between",
            width="100%",
            background=rx.color("accent", 11),
            padding="1.25rem",
            border_radius="1rem",
            color="#ffffff",
            box_shadow="0 10px 25px -5px rgb(37 99 235 / 0.25)",
            transition="all 0.2s",
            text_decoration="none",
        ),
        padding="0 1rem",
        margin_bottom="2rem",
    )


def _tarjetas_informacion_rapida() -> rx.Component:
    """Bloque con ubicación e informes de contacto rápido."""
    return rx.flex(
        rx.box(
            rx.icon("map-pin", size=20, color="#60a5fa", margin_bottom="0.5rem"),
            rx.text(
                "Ubicación",
                color_scheme="gray",
                font_weight="700",
                text_transform="uppercase",
            ),
            rx.text(UBICACION_FISICA),
            padding="1rem",
            border_radius="1rem",
            border=f"1px solid {rx.color('accent', 8)}",
            flex="1",
            box_shadow="0 1px 2px 0 rgb(0 0 0 / 0.05)",
            min_width="0",
        ),
        rx.box(
            rx.icon("phone-call", size=20, color="#60a5fa", margin_bottom="0.5rem"),
            rx.text(
                "Informes",
                font_size="0.625rem",
                color_scheme="gray",
                font_weight="700",
                text_transform="uppercase",
            ),
            rx.text(
                TELEFONO_PRINCIPAL,
                font_size="0.75rem",
                font_weight="700",
            ),
            padding="1rem",
            border_radius="1rem",
            border=f"1px solid {rx.color('accent', 8)}",
            flex="1",
            box_shadow="0 1px 2px 0 rgb(0 0 0 / 0.05)",
        ),
        gap="1rem",
        padding="1.5rem 1rem",
    )


@rx.page(route="/", title=f"Inicio | {NOMBRE_INSTITUTO}")
def vista_inicio() -> rx.Component:
    """Página principal de bienvenida del instituto."""
    return rx.vstack(
        # --- Barra de navegación ---
        barra_navegacion_superior(),

        # --- Contenido principal ---
        rx.box(
            # Hero unificado: título + CTA + carrera destacada + selector
            hero_principal(),

            # Multimedia institucional (video + info + redes sociales)
            seccion_multimedia_institucional(),

            # Estadísticas del instituto
            seccion_estadisticas(),

            # Sección "¿Por qué INSTEIN?"
            seccion_por_que_instein(),

            # # CTA hacia carreras
            # _boton_ver_carreras(),

            # # Información rápida (ubicación + informes)
            # _tarjetas_informacion_rapida(),

            # FAQ
            seccion_preguntas_frecuentes(),

            # Banner final
            rx.box(
                banner_cta_final(),
                padding="0 1.5rem 3rem 1.5rem",
                width="100%",
            ),

            padding_bottom="3rem",
            max_width="100%",
            width="100%",
        ),

        # --- Pie de página ---
        pie_pagina_institucional(),

        align="center",
        min_height="100vh",
        width="100%",
    )