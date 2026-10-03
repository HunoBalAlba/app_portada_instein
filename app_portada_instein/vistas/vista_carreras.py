"""
Vista con la lista completa de carreras (ruta "/carreras").

Estilo Google Play Store con filtros avanzados:
- Filtros por demanda laboral, puntuación, inscritos y graduados.
- Ordenamiento por múltiples métricas.
- Estado vacío cuando no hay resultados.
- Tarjetas enriquecidas con estadísticas y características.

Todos los colores usan tokens Radix (auto-adaptativos al color_mode).
Los colores semánticos (azul, amarillo, violeta, verde) se expresan
como `rx.color()` con la escala correcta según su rol.

Nota técnica: ACORDEÓN VACÍO UNIFICADO
--------------------------------------
✅ REFACTORIZADO: el estado vacío ya NO tiene su propio `_estado_vacio()`
local. Ahora delega en el componente genérico `estado_vacio`.

Nota técnica: on_load
---------------------
⚠️ Ya NO se usa `iniciar_carrusel_automatico` porque ese evento fue
eliminado del State (el auto-avance vive en el componente
`hero_carreras` con `rx.moment`).

Nota técnica: LAYOUT
--------------------
- Los tokens de color son `Var` reactivos, no strings. Usar SIEMPRE
  f-strings para concatenar con texto.
"""

from __future__ import annotations

import reflex as rx

from app_portada_instein.componentes.barra_navegacion import (
    barra_navegacion_superior,
)
from app_portada_instein.componentes.estado_vacio import estado_vacio
from app_portada_instein.componentes.hero_carreras import hero_carreras
from app_portada_instein.componentes.pie_pagina import (
    pie_pagina_institucional,
)
from app_portada_instein.dominio.estado_institucional import (
    EstadoInstitucional,
)
from app_portada_instein.infraestructura.constantes_visuales import (
    ANCHO_CONTENIDO,
    COLOR_ACENTO_BORDE,
    COLOR_ACENTO_FONDO,
    COLOR_ACENTO_SOLIDO,
    COLOR_ACENTO_TEXTO,
    COLOR_BORDE_SUAVE,
    COLOR_DIVISOR,
    COLOR_FONDO_CARTA,
    COLOR_FONDO_SUAVE,
    COLOR_TEXTO_APAGADO,
    COLOR_TEXTO_CUERPO,
    COLOR_TEXTO_PRINCIPAL,
    COLOR_TEXTO_SECUNDARIO,
    NOMBRE_INSTITUTO,
    PADDING_LATERAL,
    RADIO_EXTRA_GRANDE,
    RADIO_GRANDE,
    RADIO_MEDIO,
    RADIO_PASTILLA,
)


# ======================================================================
# Constantes locales
# ======================================================================

COLOR_PUNTUACION_TEXTO = rx.color("amber", 11)
COLOR_PUNTUACION_FONDO = rx.color("amber", 3)

COLOR_EMPLEABILIDAD_TEXTO = rx.color("violet", 11)
COLOR_EMPLEABILIDAD_FONDO = rx.color("violet", 3)

DEMANDA_ALTA_TEXTO = rx.color("green", 11)
DEMANDA_ALTA_FONDO = rx.color("green", 3)

DEMANDA_MEDIA_TEXTO = rx.color("amber", 11)
DEMANDA_MEDIA_FONDO = rx.color("amber", 3)

DEMANDA_BAJA_TEXTO = rx.color("gray", 11)
DEMANDA_BAJA_FONDO = rx.color("gray", 3)


# ======================================================================
# Helpers de filtros
# ======================================================================


def _icono_por_filtro(filtro: str) -> str:
    """Devuelve el nombre del icono Lucide correspondiente a cada filtro."""
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
                color=rx.cond(activo, "white", COLOR_TEXTO_SECUNDARIO),
            ),
            rx.text(
                etiqueta,
                font_size="0.8125rem",
                font_weight="600",
                color=rx.cond(activo, "white", COLOR_TEXTO_CUERPO),
                white_space="nowrap",
            ),
            align="center",
            gap="0.375rem",
        ),
        padding="0.5rem 1rem",
        border_radius=RADIO_PASTILLA,
        background=rx.cond(
            activo, COLOR_ACENTO_SOLIDO, COLOR_FONDO_SUAVE
        ),
        border=rx.cond(
            activo,
            f"1px solid {COLOR_ACENTO_SOLIDO}",
            f"1px solid {COLOR_BORDE_SUAVE}",
        ),
        cursor="pointer",
        transition="all 0.2s cubic-bezier(0.4, 0, 0.2, 1)",
        on_click=EstadoInstitucional.cambiar_filtro(valor),
        box_shadow=rx.cond(
            activo,
            f"0 4px 12px -2px {COLOR_ACENTO_SOLIDO}",
            "none",
        ),
        _hover={
            "transform": "translateY(-1px)",
            "background": rx.cond(
                activo, COLOR_ACENTO_SOLIDO, COLOR_FONDO_CARTA
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
            color=rx.cond(activo, "white", COLOR_TEXTO_CUERPO),
            white_space="nowrap",
        ),
        padding="0.375rem 0.875rem",
        border_radius=RADIO_PASTILLA,
        background=rx.cond(
            activo, COLOR_ACENTO_SOLIDO, COLOR_FONDO_CARTA
        ),
        border=rx.cond(
            activo,
            f"1px solid {COLOR_ACENTO_SOLIDO}",
            f"1px solid {COLOR_BORDE_SUAVE}",
        ),
        cursor="pointer",
        transition="all 0.2s",
        on_click=EstadoInstitucional.cambiar_orden(valor),
        _hover={
            "background": rx.cond(
                activo, COLOR_ACENTO_SOLIDO, COLOR_FONDO_SUAVE
            ),
        },
    )


def _etiqueta_grupo(texto: str) -> rx.Component:
    """Etiqueta en mayúsculas para encabezar un grupo de filtros."""
    return rx.text(
        texto,
        font_size="0.6875rem",
        font_weight="700",
        color=COLOR_TEXTO_SECUNDARIO,
        text_transform="uppercase",
        letter_spacing="0.075em",
        margin_bottom="0.25rem",
    )


def _barra_filtros() -> rx.Component:
    """Barra con los filtros + ordenamientos."""
    return rx.vstack(
        rx.vstack(
            _etiqueta_grupo("Filtrar por"),
            rx.flex(
                _filtro_pill(
                    "Todos", "todos", EstadoInstitucional.filtro_activo
                ),
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
        rx.vstack(
            _etiqueta_grupo("Ordenar por"),
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
    color_texto: rx.Var,
    color_fondo: rx.Var,
) -> rx.Component:
    """Item individual de estadística con icono + valor + etiqueta."""
    return rx.flex(
        rx.box(
            rx.icon(tag=icono, size=16, color=color_texto),
            padding="0.5rem",
            border_radius="0.625rem",
            background=color_fondo,
            display="flex",
            align_items="center",
            justify_content="center",
            flex_shrink="0",
        ),
        rx.vstack(
            rx.text(
                valor,
                font_size="0.9375rem",
                font_weight="700",
                color=COLOR_TEXTO_PRINCIPAL,
                line_height="1.1",
            ),
            rx.text(
                etiqueta,
                font_size="0.625rem",
                color=COLOR_TEXTO_SECUNDARIO,
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
    """Muestra las estadísticas visibles de una carrera."""
    stats = carrera["estadisticas"]

    return rx.flex(
        _stat_item(
            icono="star",
            valor=f"{stats['puntuacion']}",
            etiqueta="Puntuación",
            color_texto=COLOR_PUNTUACION_TEXTO,
            color_fondo=COLOR_PUNTUACION_FONDO,
        ),
        _stat_item(
            icono="briefcase",
            valor=f"{stats['tasa_empleabilidad']}%",
            etiqueta="Empleabilidad",
            color_texto=COLOR_EMPLEABILIDAD_TEXTO,
            color_fondo=COLOR_EMPLEABILIDAD_FONDO,
        ),
        justify="between",
        align="center",
        width="100%",
        gap="0.5rem",
        flex_wrap="wrap",
    )


# ======================================================================
# Badge de demanda laboral
# ======================================================================


def _badges_demanda(carrera: dict) -> rx.Component:
    """Badge de demanda laboral con color según nivel."""
    demanda = carrera["estadisticas"]["demanda_laboral"]

    color_texto = rx.match(
        demanda,
        ("alta", DEMANDA_ALTA_TEXTO),
        ("media", DEMANDA_MEDIA_TEXTO),
        DEMANDA_BAJA_TEXTO,
    )
    color_fondo = rx.match(
        demanda,
        ("alta", DEMANDA_ALTA_FONDO),
        ("media", DEMANDA_MEDIA_FONDO),
        DEMANDA_BAJA_FONDO,
    )

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
        border_radius=RADIO_PASTILLA,
        background=color_fondo,
        width="fit-content",
        flex_shrink="0",
    )


# ======================================================================
# Características (chips)
# ======================================================================


def _chip_caracteristica(
    caracteristica: dict,
    color_carrera: rx.Var,
) -> rx.Component:
    """Chip individual de característica."""
    return rx.box(
        rx.flex(
            rx.icon(
                tag=caracteristica["icono"],
                size=12,
                color=color_carrera,
            ),
            rx.text(
                caracteristica["etiqueta"],
                font_size="0.6875rem",
                font_weight="600",
                color=COLOR_TEXTO_CUERPO,
                white_space="nowrap",
            ),
            align="center",
            gap="0.25rem",
        ),
        padding="0.375rem 0.75rem",
        border_radius=RADIO_PASTILLA,
        background=COLOR_FONDO_SUAVE,
        border=f"1px solid {COLOR_BORDE_SUAVE}",
        width="fit-content",
    )


def _caracteristicas_carrera(carrera: dict) -> rx.Component:
    """Chips con las características principales de la carrera."""
    return rx.flex(
        rx.foreach(
            carrera["caracteristicas"],
            lambda c: _chip_caracteristica(
                c, carrera["color_principal"]
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


def _item_carrera_enriquecido(
    carrera: dict,
    indice: int,
) -> rx.Component:
    """Item de carrera con layout de 3 zonas."""
    color_carrera = carrera["color_principal"]

    return rx.link(
        rx.box(
            rx.flex(
                rx.box(
                    rx.text(
                        (indice + 1).to_string(),
                        font_size="1.5rem",
                        font_weight="800",
                        color=COLOR_TEXTO_APAGADO,
                        line_height="1",
                    ),
                    width="2.5rem",
                    display="flex",
                    align_items="center",
                    justify_content="center",
                    flex_shrink="0",
                    align_self="center",
                ),
                rx.box(
                    rx.image(
                        src="/" + carrera["imagen_archivo"],
                        alt=carrera["nombre"],
                        width="100%",
                        height="100%",
                        object_fit="cover",
                        border_radius=RADIO_GRANDE,
                    ),
                    width="4.5rem",
                    height="4.5rem",
                    flex_shrink="0",
                    border_radius=RADIO_GRANDE,
                    overflow="hidden",
                    box_shadow=f"0 8px 20px -8px {color_carrera}80",
                    align_self="start",
                ),
                rx.vstack(
                    rx.flex(
                        rx.text(
                            carrera["nombre_corto"],
                            font_size="1.125rem",
                            font_weight="700",
                            color=COLOR_TEXTO_PRINCIPAL,
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
                        color=COLOR_TEXTO_SECUNDARIO,
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
            rx.box(
                _stats_carrera(carrera),
                width="100%",
                margin_top="1rem",
                padding_top="1rem",
                border_top=f"1px solid {COLOR_DIVISOR}",
            ),
            rx.box(
                _caracteristicas_carrera(carrera),
                width="100%",
                margin_top="0.75rem",
            ),
            padding="1.5rem",
            border_radius="1.25rem",
            background=COLOR_FONDO_CARTA,
            border=f"1px solid {COLOR_BORDE_SUAVE}",
            transition="all 0.25s cubic-bezier(0.4, 0, 0.2, 1)",
            height="100%",
            display="flex",
            flex_direction="column",
            _hover={
                "background": COLOR_FONDO_SUAVE,
                "border_color": color_carrera,
                "transform": "translateY(-3px)",
                "box_shadow": f"0 16px 40px -12px {color_carrera}44",
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
# Encabezado de la sección
# ======================================================================


def _encabezado_seccion() -> rx.Component:
    """Encabezado con título, subtítulo y contador de resultados."""
    return rx.flex(
        rx.vstack(
            rx.heading(
                "Explora nuestras carreras",
                size="7",
                font_weight="800",
                color=COLOR_TEXTO_PRINCIPAL,
                line_height="1.1",
            ),
            rx.text(
                "Filtra y ordena según tus prioridades: demanda laboral, "
                "puntuación, estudiantes inscritos y más.",
                font_size="0.9375rem",
                color=COLOR_TEXTO_SECUNDARIO,
                max_width="42rem",
            ),
            align="start",
            spacing="2",
            flex="1",
        ),
        rx.box(
            rx.text(
                EstadoInstitucional.carreras_filtradas_y_ordenadas
                .length()
                .to_string(),
                font_size="2rem",
                font_weight="800",
                color=COLOR_ACENTO_TEXTO,
                line_height="1",
            ),
            rx.text(
                "resultados",
                font_size="0.6875rem",
                color=COLOR_TEXTO_SECUNDARIO,
                text_transform="uppercase",
                letter_spacing="0.05em",
            ),
            text_align="center",
            padding="1rem 1.5rem",
            border_radius=RADIO_GRANDE,
            background=COLOR_ACENTO_FONDO,
            border=f"1px solid {COLOR_ACENTO_BORDE}",
            flex_shrink="0",
        ),
        justify="between",
        align="center",
        width="100%",
        margin_bottom="2rem",
        flex_wrap="wrap",
        gap="1.5rem",
    )


# ======================================================================
# Vista completa
# ======================================================================


@rx.page(
    route="/carreras",
    title=f"Carreras | {NOMBRE_INSTITUTO}",
)
def vista_carreras() -> rx.Component:
    """
    Página con la oferta académica completa + filtros avanzados.

    ✅ REFACTORIZADO: el estado vacío delega en el componente genérico
    `estado_vacio`.

    ⚠️ El auto-avance del carrusel vive en `hero_carreras` con
    `rx.moment`. NO hay `on_load` que iniciar.
    """
    return rx.vstack(
        barra_navegacion_superior(),
        rx.box(
            hero_carreras(),
            rx.box(
                _encabezado_seccion(),
                _barra_filtros(),
                rx.cond(
                    EstadoInstitucional.carreras_filtradas_y_ordenadas
                    .length()
                    > 0,
                    _grid_carreras_enriquecido(),
                    estado_vacio(
                        titulo="No se encontraron carreras",
                        mensaje=(
                            "Prueba ajustando los filtros o limpiando "
                            "la selección actual."
                        ),
                        icono="search-x",
                        tamano_icono=48,
                        boton_accion_etiqueta="Limpiar filtros",
                        boton_accion_icono="rotate-ccw",
                        boton_accion_on_click=(
                            EstadoInstitucional.cambiar_filtro("todos")
                        ),
                        boton_accion_color_scheme="crimson",
                    ),
                ),
                max_width=ANCHO_CONTENIDO,
                margin="0 auto",
                padding=(
                    f"2rem {PADDING_LATERAL} 4rem {PADDING_LATERAL}"
                ),
                width="100%",
            ),
            width="100%",
        ),
        pie_pagina_institucional(),
        align="center",
        min_height="100vh",
        width="100%",
    )


__all__ = ["vista_carreras"]