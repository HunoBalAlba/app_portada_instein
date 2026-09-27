"""
Vista con la lista completa de carreras (ruta "/carreras").

Estilo Google Play Store con filtros avanzados:
- Filtros por demanda laboral, puntuación, inscritos y graduados.
- Ordenamiento por múltiples métricas.
- Estado vacío cuando no hay resultados.
- Tarjetas enriquecidas con estadísticas y características.
"""

import reflex as rx

from app_portada_instein.componentes.barra_navegacion import barra_navegacion_superior
from app_portada_instein.componentes.hero_carreras import hero_carreras
from app_portada_instein.componentes.pie_pagina import pie_pagina_institucional
from app_portada_instein.dominio.estado_institucional import EstadoInstitucional
from app_portada_instein.infraestructura.constantes_visuales import NOMBRE_INSTITUTO


# ======================================================================
# Constantes locales
# ======================================================================

COLOR_AZUL = "#2563eb"
COLOR_AZUL_SUAVE = "#eff6ff"


# ======================================================================
# Iconos para filtros
# ======================================================================


def _icono_por_filtro(filtro: str) -> str:
    """Devuelve el icono de Lucide correspondiente a cada filtro."""
    iconos = {
        "demanda_alta": "trending-up",
        "puntuacion_top": "star",
        "mas_inscritos": "users",
        "mas_graduados": "graduation-cap",
        "todos": "list",
    }
    return iconos.get(filtro, "filter")


# ======================================================================
# Filtros tipo pill (estilo Google Play)
# ======================================================================


def _filtro_pill(
    etiqueta: str,
    valor: str,
    filtro_actual: str,
) -> rx.Component:
    """Botón pill de filtro con estado activo controlado por el State."""
    activo = filtro_actual == valor

    return rx.box(
        rx.flex(
            rx.icon(
                tag=_icono_por_filtro(valor),
                size=14,
                color=rx.cond(
                    activo,
                    "#ffffff",
                    rx.color_mode_cond(light="#64748b", dark="#94a3b8"),
                ),
            ),
            rx.text(
                etiqueta,
                font_size="0.8125rem",
                font_weight="600",
                color=rx.cond(
                    activo,
                    "#ffffff",
                    rx.color_mode_cond(light="#334155", dark="#cbd5e1"),
                ),
                white_space="nowrap",
            ),
            align="center",
            gap="0.375rem",
        ),
        padding="0.5rem 1rem",
        border_radius="9999px",
        background=rx.cond(
            activo,
            COLOR_AZUL,
            rx.color_mode_cond(light="#f1f5f9", dark="#1e293b"),
        ),
        border="1px solid "
        + rx.cond(
            activo,
            COLOR_AZUL,
            rx.color_mode_cond(light="#e2e8f0", dark="#334155"),
        ),
        cursor="pointer",
        transition="all 0.2s cubic-bezier(0.4, 0, 0.2, 1)",
        on_click=EstadoInstitucional.cambiar_filtro(valor),
        box_shadow=rx.cond(
            activo,
            f"0 4px 12px -2px {COLOR_AZUL}66",
            "none",
        ),
        _hover={
            "transform": "translateY(-1px)",
            "background": rx.cond(
                activo,
                "#1d4ed8",
                rx.color_mode_cond(light="#e2e8f0", dark="#334155"),
            ),
        },
    )


def _orden_pill(etiqueta: str, valor: str) -> rx.Component:
    """Pill de ordenamiento con estado activo."""
    activo = EstadoInstitucional.orden_activo == valor

    return rx.box(
        rx.text(
            etiqueta,
            font_size="0.75rem",
            font_weight="600",
            color=rx.cond(
                activo,
                "#ffffff",
                rx.color_mode_cond(light="#475569", dark="#cbd5e1"),
            ),
            white_space="nowrap",
        ),
        padding="0.375rem 0.875rem",
        border_radius="9999px",
        background=rx.cond(
            activo,
            COLOR_AZUL,
            rx.color_mode_cond(light="#ffffff", dark="#1e293b"),
        ),
        border="1px solid "
        + rx.cond(
            activo,
            COLOR_AZUL,
            rx.color_mode_cond(light="#e2e8f0", dark="#334155"),
        ),
        cursor="pointer",
        transition="all 0.2s",
        on_click=EstadoInstitucional.cambiar_orden(valor),
        _hover={
            "background": rx.cond(
                activo,
                "#1d4ed8",
                rx.color_mode_cond(light="#f8fafc", dark="#334155"),
            ),
        },
    )


def _barra_filtros() -> rx.Component:
    """Barra con los filtros + ordenamientos."""
    return rx.vstack(
        # --- Grupo 1: Filtros por métricas ---
        rx.vstack(
            rx.text(
                "Filtrar por",
                font_size="0.6875rem",
                font_weight="700",
                color=rx.color_mode_cond(light="#64748b", dark="#94a3b8"),
                text_transform="uppercase",
                letter_spacing="0.075em",
                margin_bottom="0.25rem",
            ),
            rx.flex(
                _filtro_pill("Todos", "todos", EstadoInstitucional.filtro_activo),
                _filtro_pill(
                    "Alta demanda laboral",
                    "demanda_alta",
                    EstadoInstitucional.filtro_activo,
                ),
                _filtro_pill(
                    "Mejor puntuación",
                    "puntuacion_top",
                    EstadoInstitucional.filtro_activo,
                ),
                _filtro_pill(
                    "Más inscritos",
                    "mas_inscritos",
                    EstadoInstitucional.filtro_activo,
                ),
                _filtro_pill(
                    "Más graduados",
                    "mas_graduados",
                    EstadoInstitucional.filtro_activo,
                ),
                gap="0.5rem",
                flex_wrap="wrap",
                width="100%",
            ),
            align="start",
            spacing="1",
            width="100%",
        ),
        # --- Grupo 2: Ordenamiento ---
        rx.vstack(
            rx.text(
                "Ordenar por",
                font_size="0.6875rem",
                font_weight="700",
                color=rx.color_mode_cond(light="#64748b", dark="#94a3b8"),
                text_transform="uppercase",
                letter_spacing="0.075em",
                margin_bottom="0.25rem",
            ),
            rx.flex(
                _orden_pill("Puntuación", "puntuacion_desc"),
                _orden_pill("Inscritos", "inscritos_desc"),
                _orden_pill("Graduados", "graduados_desc"),
                _orden_pill("Empleabilidad", "empleabilidad_desc"),
                _orden_pill("Salario promedio", "salario_desc"),
                gap="0.5rem",
                flex_wrap="wrap",
                width="100%",
            ),
            align="start",
            spacing="1",
            width="100%",
        ),
        spacing="4",
        width="100%",
        margin_bottom="2rem",
    )


# ======================================================================
# Estadísticas de carrera
# ======================================================================


def _stat_item(
    icono: str,
    valor: str,
    etiqueta: str,
    color: str,
) -> rx.Component:
    """Item individual de estadística con icono + valor + etiqueta."""
    return rx.flex(
        # --- Icono con fondo tintado ---
        rx.box(
            rx.icon(tag=icono, size=16, color=color),
            padding="0.5rem",
            border_radius="0.625rem",
            background=color + "15",
            display="flex",
            align_items="center",
            justify_content="center",
            flex_shrink="0",
        ),
        # --- Valor + etiqueta ---
        rx.vstack(
            rx.text(
                valor,
                font_size="0.9375rem",
                font_weight="700",
                color=rx.color_mode_cond(light="#0f172a", dark="#f1f5f9"),
                line_height="1.1",
            ),
            rx.text(
                etiqueta,
                font_size="0.625rem",
                color=rx.color_mode_cond(light="#64748b", dark="#94a3b8"),
                text_transform="uppercase",
                letter_spacing="0.05em",
                line_height="1.1",
            ),
            spacing="0",
            align="start",
        ),
        align="center",
        gap="0.5rem",
        min_width="fit-content",
    )


def _stats_carrera(carrera: dict) -> rx.Component:
    """Muestra las 4 estadísticas de una carrera distribuidas uniformemente."""
    stats = carrera["estadisticas"]
    color = carrera["color_principal"]

    return rx.flex(
        _stat_item(
            icono="star",
            valor=f"{stats['puntuacion']}",
            etiqueta="Puntuación",
            color="#fbbf24",
        ),
        _stat_item(
            icono="users",
            valor=f"{stats['estudiantes_inscritos']}",
            etiqueta="Inscritos",
            color=color,
        ),
        _stat_item(
            icono="graduation-cap",
            valor=f"{stats['estudiantes_graduados']}",
            etiqueta="Graduados",
            color="#16a34a",
        ),
        _stat_item(
            icono="briefcase",
            valor=f"{stats['tasa_empleabilidad']}%",
            etiqueta="Empleabilidad",
            color="#7c3aed",
        ),
        justify="between",
        align="center",
        width="100%",
        gap="0.5rem",
        flex_wrap="wrap",
    )


# ======================================================================
# Badge de demanda
# ======================================================================


def _badges_demanda(carrera: dict) -> rx.Component:
    """Badge de demanda laboral con color según nivel."""
    demanda = carrera["estadisticas"]["demanda_laboral"]
    colores = {
        "alta": ("#15803d", "#dcfce7"),
        "media": ("#b45309", "#fef3c7"),
        "baja": ("#475569", "#f1f5f9"),
    }
    color_texto, color_fondo = colores.get(demanda, ("#475569", "#f1f5f9"))

    return rx.box(
        rx.flex(
            rx.icon(tag="trending-up", size=12, color=color_texto),
            rx.text(
                f"Demanda {demanda}",
                font_size="0.6875rem",
                font_weight="700",
                color=color_texto,
                text_transform="capitalize",
                white_space="nowrap",
            ),
            align="center",
            gap="0.25rem",
        ),
        padding="0.25rem 0.625rem",
        border_radius="9999px",
        background=color_fondo,
        width="fit-content",
        flex_shrink="0",
    )


# ======================================================================
# Características (chips)
# ======================================================================


def _caracteristicas_carrera(carrera: dict) -> rx.Component:
    """Chips con las características principales de la carrera."""
    return rx.flex(
        rx.foreach(
            carrera["caracteristicas"],
            lambda c: rx.box(
                rx.flex(
                    rx.icon(
                        tag=c["icono"],
                        size=12,
                        color=carrera["color_principal"],
                    ),
                    rx.text(
                        c["etiqueta"],
                        font_size="0.6875rem",
                        font_weight="600",
                        color=rx.color_mode_cond(light="#334155", dark="#cbd5e1"),
                        white_space="nowrap",
                    ),
                    align="center",
                    gap="0.25rem",
                ),
                padding="0.375rem 0.75rem",
                border_radius="9999px",
                background=rx.color_mode_cond(light="#f8fafc", dark="#1e293b"),
                border="1px solid "
                + rx.color_mode_cond(light="#e2e8f0", dark="#334155"),
                width="fit-content",
            ),
        ),
        gap="0.5rem",
        flex_wrap="wrap",
        align="center",
        justify="start",
        width="100%",
    )


# ======================================================================
# Item enriquecido de carrera
# ======================================================================


def _item_carrera_enriquecido(carrera: dict, indice: int) -> rx.Component:
    """
    Item de carrera con layout de 3 zonas:

    - **Zona 1**: ranking + icono + nombre/lema + badge demanda.
    - **Zona 2**: 4 estadísticas distribuidas.
    - **Zona 3**: chips de características.
    """
    return rx.link(
        rx.box(
            # =========================================================
            # ZONA 1: HEADER
            # =========================================================
            rx.flex(
                # --- Ranking ---
                rx.box(
                    rx.text(
                        (indice + 1).to_string(),
                        font_size="1.5rem",
                        font_weight="800",
                        color=rx.color_mode_cond(light="#cbd5e1", dark="#475569"),
                        line_height="1",
                    ),
                    width="2.5rem",
                    display="flex",
                    align_items="center",
                    justify_content="center",
                    flex_shrink="0",
                    align_self="center",
                ),
                # --- Icono ---
                rx.box(
                    rx.image(
                        src="/" + carrera["imagen_archivo"],
                        alt=carrera["nombre"],
                        width="100%",
                        height="100%",
                        object_fit="cover",
                        border_radius="1rem",
                    ),
                    width="4.5rem",
                    height="4.5rem",
                    flex_shrink="0",
                    border_radius="1rem",
                    overflow="hidden",
                    box_shadow=f"0 8px 20px -8px {carrera['color_principal']}80",
                    align_self="start",
                ),
                # --- Info ---
                rx.vstack(
                    rx.flex(
                        rx.text(
                            carrera["nombre_corto"],
                            font_size="1.125rem",
                            font_weight="700",
                            color=rx.color_mode_cond(light="#0f172a", dark="#f1f5f9"),
                            line_height="1.3",
                        ),
                        _badges_demanda(carrera),
                        align="center",
                        justify="between",
                        gap="0.5rem",
                        flex_wrap="wrap",
                        width="100%",
                    ),
                    rx.text(
                        carrera["lema"],
                        font_size="0.8125rem",
                        color=rx.color_mode_cond(light="#64748b", dark="#94a3b8"),
                        line_height="1.4",
                        width="100%",
                    ),
                    align="start",
                    spacing="2",
                    flex="1",
                    min_width="0",
                    width="100%",
                ),
                align="start",
                gap="1rem",
                width="100%",
            ),
            # =========================================================
            # ZONA 2: ESTADÍSTICAS
            # =========================================================
            rx.box(
                _stats_carrera(carrera),
                width="100%",
                margin_top="1rem",
                padding_top="1rem",
                border_top="1px solid "
                + rx.color_mode_cond(light="#f1f5f9", dark="#1e293b"),
            ),
            # =========================================================
            # ZONA 3: CARACTERÍSTICAS
            # =========================================================
            rx.box(
                _caracteristicas_carrera(carrera),
                width="100%",
                margin_top="0.75rem",
            ),
            # =========================================================
            # CONTENEDOR
            # =========================================================
            padding="1.5rem",
            border_radius="1.25rem",
            background=rx.color_mode_cond(light="#ffffff", dark="#0f1117"),
            border="1px solid " + rx.color_mode_cond(light="#e2e8f0", dark="#1e293b"),
            transition="all 0.25s cubic-bezier(0.4, 0, 0.2, 1)",
            height="100%",
            display="flex",
            flex_direction="column",
            _hover={
                "background": rx.color_mode_cond(light="#f8fafc", dark="#1e293b"),
                "border_color": carrera["color_principal"] + "66",
                "transform": "translateY(-3px)",
                "box_shadow": f"0 16px 40px -12px {carrera['color_principal']}44",
            },
        ),
        href=f"/carrera/{carrera['id']}",
        text_decoration="none",
        width="100%",
        height="100%",
    )


# ======================================================================
# Grid de carreras
# ======================================================================


def _grid_carreras_enriquecido() -> rx.Component:
    """Grid de carreras con altura uniforme por fila."""
    return rx.grid(
        rx.foreach(
            EstadoInstitucional.carreras_filtradas_y_ordenadas,
            _item_carrera_enriquecido,
        ),
        columns=rx.breakpoints(
            initial="1",
            sm="1",
            md="1",
            lg="2",
            xl="2",
        ),
        spacing="4",
        width="100%",
        align_items="stretch",
    )


# ======================================================================
# Estado vacío
# ======================================================================


def _estado_vacio() -> rx.Component:
    """Mensaje cuando no hay resultados."""
    return rx.flex(
        rx.box(
            rx.icon(
                "search-x",
                size=48,
                color=rx.color_mode_cond(light="#cbd5e1", dark="#475569"),
            ),
            padding="1.5rem",
            border_radius="1rem",
            background=rx.color_mode_cond(light="#f8fafc", dark="#1e293b"),
            display="flex",
            align_items="center",
            justify_content="center",
        ),
        rx.vstack(
            rx.heading(
                "No se encontraron carreras",
                size="5",
                font_weight="700",
                color=rx.color_mode_cond(light="#0f172a", dark="#f1f5f9"),
            ),
            rx.text(
                "Prueba ajustando los filtros o limpiando la selección actual.",
                font_size="0.875rem",
                color=rx.color_mode_cond(light="#64748b", dark="#94a3b8"),
                text_align="center",
            ),
            spacing="2",
            align="center",
        ),
        direction="column",
        align="center",
        gap="1.5rem",
        padding="4rem 1.5rem",
        width="100%",
    )


# ======================================================================
# Vista completa
# ======================================================================


@rx.page(
    route="/carreras",
    title=f"Carreras | {NOMBRE_INSTITUTO}",
    on_load=EstadoInstitucional.auto_avanzar_carrusel,
)
def vista_carreras() -> rx.Component:
    """Página con la oferta académica completa + filtros avanzados."""
    return rx.vstack(
        # --- Barra de navegación ---
        barra_navegacion_superior(),
        # --- Contenido principal ---
        rx.box(
            # --- Hero con banners destacados ---
            hero_carreras(),
            # --- Sección "Listas de éxitos" ---
            rx.box(
                # --- Encabezado ---
                rx.flex(
                    rx.vstack(
                        rx.heading(
                            "Explora nuestras carreras",
                            size="7",
                            font_weight="800",
                            color=rx.color_mode_cond(light="#0f172a", dark="#f1f5f9"),
                            line_height="1.1",
                        ),
                        rx.text(
                            "Filtra y ordena según tus prioridades: demanda laboral, "
                            "puntuación, estudiantes inscritos y más.",
                            font_size="0.9375rem",
                            color=rx.color_mode_cond(light="#64748b", dark="#94a3b8"),
                            max_width="42rem",
                        ),
                        align="start",
                        spacing="2",
                        flex="1",
                    ),
                    # --- Contador de resultados ---
                    rx.box(
                        rx.text(
                            EstadoInstitucional.carreras_filtradas_y_ordenadas.length().to_string(),
                            font_size="2rem",
                            font_weight="800",
                            color=COLOR_AZUL,
                            line_height="1",
                        ),
                        rx.text(
                            "resultados",
                            font_size="0.6875rem",
                            color=rx.color_mode_cond(light="#64748b", dark="#94a3b8"),
                            text_transform="uppercase",
                            letter_spacing="0.05em",
                        ),
                        text_align="center",
                        padding="1rem 1.5rem",
                        border_radius="1rem",
                        background=COLOR_AZUL_SUAVE,
                        border="1px solid " + COLOR_AZUL + "33",
                        flex_shrink="0",
                    ),
                    justify="between",
                    align="center",
                    width="100%",
                    margin_bottom="2rem",
                    flex_wrap="wrap",
                    gap="1.5rem",
                ),
                # --- Filtros ---
                _barra_filtros(),
                # --- Grid de carreras o estado vacío ---
                rx.cond(
                    EstadoInstitucional.carreras_filtradas_y_ordenadas.length() > 0,
                    _grid_carreras_enriquecido(),
                    _estado_vacio(),
                ),
                max_width="72rem",
                margin="0 auto",
                padding="2rem 1.5rem 4rem 1.5rem",
                width="100%",
            ),
            width="100%",
        ),
        # --- Pie de página ---
        pie_pagina_institucional(),
        align="center",
        min_height="100vh",
        width="100%",
    )