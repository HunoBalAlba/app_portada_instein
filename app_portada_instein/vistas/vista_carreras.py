"""
Vista con la lista completa de carreras (ruta "/carreras").
"""

import reflex as rx

from ..componentes.barra_navegacion import barra_navegacion_superior
from ..componentes.tarjetas_carrera import tarjeta_carrera
from ..dominio.estado_institucional import EstadoInstitucional
from ..infraestructura.constantes_visuales import NOMBRE_INSTITUTO


@rx.page(route="/carreras", title=f"Carreras | {NOMBRE_INSTITUTO}")
def vista_carreras() -> rx.Component:
    """Página con la oferta académica completa."""
    return rx.vstack(
        barra_navegacion_superior(),
        rx.box(
            rx.vstack(
                rx.text(
                    "OFERTA ACADÉMICA",
                    size="4",
                    text_transform="uppercase",
                ),
                rx.heading("Menú de Carreras", size="6"),
                rx.text(
                    "Selecciona un programa para ver el contenido académico completo.",
                    color_scheme="gray",
                ),
                spacing="1",
                padding="2rem 1.5rem 1rem 1.5rem",
            ),
            rx.vstack(
                rx.grid(
                    rx.foreach(EstadoInstitucional.carreras, tarjeta_carrera),
                    columns=rx.breakpoints(initial="1", sm="2", lg="3"),
                    spacing="4",
                ),
            ),
            padding_bottom="3rem",
            max_width="72rem",
            width="100%",
        ),
        align="center",
        min_height="100vh",
        width="100%",
    )