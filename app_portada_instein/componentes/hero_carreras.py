"""
Hero para la página de carreras, estilo Google Play Store:
- Carrusel de banners destacados con flechas de navegación.
- Indicadores de posición (dots).
- Grid de perspectiva sutil de fondo.
- Usa la imagen horizontal (`imagen_banner`) para el fondo del banner.
"""

import reflex as rx

from app_portada_instein.dominio.estado_institucional import EstadoInstitucional


# ======================================================================
# Grid de perspectiva de fondo
# ======================================================================


def _grid_perspectiva() -> rx.Component:
    """Grid de líneas radiales que simulan perspectiva."""
    angulos = [i * 45 for i in range(8)]

    return rx.box(
        *[
            rx.box(
                position="absolute",
                top="50%",
                left="50%",
                width="200%",
                height="1px",
                background=rx.color_mode_cond(
                    light="rgba(37, 99, 235, 0.03)",
                    dark="rgba(96, 165, 250, 0.05)",
                ),
                transform_origin="0 50%",
                transform=f"translate(0, -50%) rotate({angulo}deg)",
            )
            for angulo in angulos
        ],
        position="absolute",
        top="0",
        left="0",
        right="0",
        bottom="0",
        overflow="hidden",
        z_index="0",
        pointer_events="none",
    )


# ======================================================================
# Banner individual destacado (estilo Google Play)
# ======================================================================


def _banner_carrera(item: dict) -> rx.Component:
    """
    Banner horizontal grande, estilo Google Play Store.

    Recibe un dict con la estructura:
    {
        "carrera": { ...datos de la carrera... },
        "etiqueta": "Inscripciones abiertas",
    }

    Usa:
    - `imagen_banner` (16:9) como fondo del banner.
    - `imagen_archivo` (1:1) para el icono circular.
    """
    carrera = item["carrera"]
    etiqueta = item["etiqueta"]
    color = carrera["color_principal"]

    return rx.link(
        rx.box(
            # --- Imagen de fondo con overlay ---
            rx.box(
                rx.image(
                    src="/" + carrera["imagen_banner"],
                    alt=carrera["nombre"],
                    width="100%",
                    height="100%",
                    object_fit="cover",
                    position="absolute",
                    top="0",
                    left="0",
                    z_index="0",
                ),
                position="absolute",
                top="0",
                left="0",
                right="0",
                bottom="0",
                background=(
                    "linear-gradient(to top, rgba(0,0,0,0.85) 0%, "
                    "rgba(0,0,0,0.2) 60%, rgba(0,0,0,0.4) 100%)"
                ),
                z_index="1",
            ),
            # --- Contenido sobre la imagen ---
            rx.vstack(
                # --- Etiqueta superior ---
                rx.box(
                    rx.text(
                        etiqueta,
                        font_size="0.75rem",
                        font_weight="600",
                        color="#ffffff",
                    ),
                    padding="0.375rem 0.75rem",
                    background="rgba(0,0,0,0.6)",
                    backdrop_filter="blur(8px)",
                    border_radius="0.375rem",
                    width="fit-content",
                ),
                # --- Espaciador ---
                rx.box(flex="1"),
                # --- Título grande ---
                rx.heading(
                    carrera["nombre"],
                    font_size=["1.25rem", "1.5rem", "1.75rem"],
                    font_weight="800",
                    color="#ffffff",
                    line_height="1.2",
                    max_width="90%",
                ),
                # --- Footer: icono + subtítulo + CTA ---
                rx.flex(
                    # Icono circular
                    rx.box(
                        rx.image(
                            src="/" + carrera["imagen_archivo"],
                            alt=carrera["nombre"],
                            width="100%",
                            height="100%",
                            object_fit="cover",
                            border_radius="9999px",
                        ),
                        width="3rem",
                        height="3rem",
                        border_radius="9999px",
                        overflow="hidden",
                        border="2px solid rgba(255,255,255,0.3)",
                        flex_shrink="0",
                    ),
                    # Subtítulo
                    rx.vstack(
                        rx.text(
                            carrera["nombre_corto"],
                            font_size="0.875rem",
                            font_weight="600",
                            color="#ffffff",
                        ),
                        rx.text(
                            carrera["duracion"] + " · Técnico Superior",
                            font_size="0.75rem",
                            color="rgba(255,255,255,0.7)",
                        ),
                        align="start",
                        spacing="0",
                        flex="1",
                    ),
                    # Botón CTA
                    rx.box(
                        rx.text(
                            "Ver detalle",
                            font_size="0.75rem",
                            font_weight="600",
                            color="#ffffff",
                        ),
                        padding="0.5rem 0.875rem",
                        border_radius="0.375rem",
                        background="rgba(0,0,0,0.6)",
                        backdrop_filter="blur(8px)",
                        border="1px solid rgba(255,255,255,0.2)",
                        flex_shrink="0",
                    ),
                    align="center",
                    gap="0.75rem",
                    width="100%",
                    margin_top="1rem",
                ),
                align="start",
                justify="between",
                spacing="2",
                width="100%",
                height="100%",
                padding="1.25rem",
                position="relative",
                z_index="2",
            ),
            position="relative",
            height="20rem",
            border_radius="1rem",
            overflow="hidden",
            transition="all 0.3s",
            _hover={
                "transform": "translateY(-4px)",
                "box_shadow": f"0 20px 40px -10px {color}66",
            },
        ),
        href=f"/carrera/{carrera['id']}",
        text_decoration="none",
        width="100%",
    )


# ======================================================================
# Flecha de navegación (izquierda / derecha)
# ======================================================================


def _flecha_navegacion(direccion: str) -> rx.Component:
    """
    Flecha circular para navegar el carrusel.

    Args:
        direccion: "izquierda" o "derecha".
    """
    if direccion == "izquierda":
        icono = "chevron-left"
        evento = EstadoInstitucional.anterior_carrusel
        posicion = {"left": "-1.5rem"}
    else:
        icono = "chevron-right"
        evento = EstadoInstitucional.siguiente_carrusel
        posicion = {"right": "-1.5rem"}

    return rx.box(
        rx.icon(
            icono,
            size=22,
            color=rx.color_mode_cond(light="#0f172a", dark="#f1f5f9"),
        ),
        position="absolute",
        top="50%",
        transform="translateY(-50%)",
        height="2.75rem",
        width="2.75rem",
        border_radius="9999px",
        background=rx.color_mode_cond(light="#ffffff", dark="#1e293b"),
        border="1px solid " + rx.color_mode_cond(light="#e2e8f0", dark="#334155"),
        box_shadow="0 4px 12px -2px rgba(0,0,0,0.15)",
        display="flex",
        align_items="center",
        justify_content="center",
        cursor="pointer",
        z_index="10",
        transition="all 0.2s",
        on_click=evento,
        _hover={
            "transform": "translateY(-50%) scale(1.1)",
            "box_shadow": "0 8px 20px -4px rgba(0,0,0,0.2)",
        },
        **posicion,
    )


# ======================================================================
# Indicadores de posición (dots)
# ======================================================================


def _indicadores_dots() -> rx.Component:
    """Fila de dots que indican la posición actual del carrusel."""
    return rx.flex(
        rx.foreach(
            EstadoInstitucional.carreras_destacadas_con_etiquetas,
            lambda item, idx: rx.box(
                height="0.5rem",
                width=rx.cond(
                    EstadoInstitucional.indice_carrusel == idx,
                    "1.5rem",
                    "0.5rem",
                ),
                border_radius="9999px",
                background=rx.cond(
                    EstadoInstitucional.indice_carrusel == idx,
                    item["carrera"]["color_principal"],
                    rx.color_mode_cond(light="#cbd5e1", dark="#475569"),
                ),
                cursor="pointer",
                transition="all 0.3s",
                on_click=lambda: EstadoInstitucional.ir_a_banner(idx),
            ),
        ),
        gap="0.375rem",
        justify="center",
        align="center",
        margin_top="1.5rem",
        width="100%",
    )


# ======================================================================
# Carrusel completo
# ======================================================================


def _carrusel_carreras() -> rx.Component:
    """
    Carrusel de banners destacados con:
    - Un banner visible a la vez (el actual).
    - Flechas de navegación laterales.
    - Indicadores de posición debajo.
    """
    return rx.box(
        # --- Contenedor con flechas + banner ---
        rx.box(
            # --- Banner actual ---
            _banner_carrera(EstadoInstitucional.item_carrusel_actual),
            # --- Flechas de navegación ---
            _flecha_navegacion("izquierda"),
            _flecha_navegacion("derecha"),
            position="relative",
            width="100%",
            max_width="64rem",
            margin="0 auto",
        ),
        # --- Indicadores de posición ---
        _indicadores_dots(),
        width="100%",
    )


# ======================================================================
# Hero completo
# ======================================================================


def hero_carreras() -> rx.Component:
    """
    Hero de la página de carreras estilo Google Play Store con carrusel.
    """
    return rx.box(
        # --- Grid de perspectiva de fondo ---
        _grid_perspectiva(),
        # --- Carrusel ---
        rx.box(
            _carrusel_carreras(),
            max_width="72rem",
            margin="0 auto",
            padding="3rem 3rem 2rem 3rem",
            position="relative",
            z_index="1",
            width="100%",
        ),
        # --- Contenedor principal ---
        position="relative",
        width="100%",
        overflow="hidden",
    )
