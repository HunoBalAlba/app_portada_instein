"""
Banner CTA final con fondo oscuro y botón grande.
"""

import reflex as rx

from app_portada_instein.componentes.primitivos import enlace_navegacion


def banner_cta_final() -> rx.Component:
    """
    Banner de llamada a la acción final con fondo oscuro degradado.
    """
    return rx.box(
        # --- Grid de fondo sutil ---
        rx.box(
            position="absolute",
            top="0",
            left="0",
            right="0",
            bottom="0",
            background=(
                "radial-gradient(ellipse at 50% 50%, rgba(96, 165, 250, 0.15) 0%, transparent 70%)"
            ),
            z_index="0",
        ),
        # --- Contenido ---
        rx.vstack(
            rx.heading(
                "¿Listo para empezar?",
                size="8",
                color="#ffffff",
                text_align="center",
                font_weight="900",
            ),
            rx.text(
                "Únete a los 500+ estudiantes que ya están forjando su futuro "
                "profesional en INSTEIN.",
                font_size="1.125rem",
                color="rgba(255,255,255,0.8)",
                text_align="center",
                max_width="42rem",
                margin_top="0.5rem",
            ),
            rx.flex(
                enlace_navegacion(
                    "/carreras",
                    rx.icon("graduation-cap", size=18),
                    rx.text("Ver Carreras", as_="span", font_weight="700"),
                    display="flex",
                    align_items="center",
                    gap="0.5rem",
                    background="#ffffff",
                    color="#0f172a",
                    padding="0.875rem 1.75rem",
                    border_radius="9999px",
                    font_size="0.9375rem",
                    box_shadow="0 10px 25px -5px rgba(255,255,255,0.3)",
                    transition="all 0.2s",
                    _hover={
                        "transform": "translateY(-2px)",
                        "box_shadow": "0 15px 35px -5px rgba(255,255,255,0.4)",
                    },
                ),
                enlace_navegacion(
                    "/contacto",
                    rx.icon("phone", size=18),
                    rx.text("Contactar", as_="span", font_weight="600"),
                    display="flex",
                    align_items="center",
                    gap="0.5rem",
                    background="transparent",
                    color="#ffffff",
                    padding="0.875rem 1.75rem",
                    border_radius="9999px",
                    font_size="0.9375rem",
                    border="1px solid rgba(255,255,255,0.3)",
                    transition="all 0.2s",
                    _hover={
                        "background": "rgba(255,255,255,0.1)",
                        "border_color": "rgba(255,255,255,0.5)",
                    },
                ),
                gap="0.75rem",
                margin_top="2rem",
                flex_direction=["column", "row"],
                align="center",
                justify="center",
            ),
            align="center",
            position="relative",
            z_index="1",
            padding="4rem 1.5rem",
        ),
        # --- Contenedor ---
        position="relative",
        width="100%",
        background="linear-gradient(135deg, #0f172a 0%, #1e293b 100%)",
        border_radius="1.5rem",
        overflow="hidden",
        max_width="72rem",
        margin="0 auto",
    )
