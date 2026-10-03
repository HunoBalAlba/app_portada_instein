"""
Vista de detalle de una carrera específica
(ruta dinámica "/carrera/[carrera_id]").

Estructura:
- Encabezado sticky con breadcrumb, botón de regreso y progreso de scroll.
- Hero con contenedor orbital (imagen + iconos orbitando).
- Hero con información textual: nombre, lema, badges, CTA.
- Pestañas (Tabs) con las 3 secciones principales del detalle.
- Sección de preguntas frecuentes (fuera de las tabs, como sección aparte).
- Botón flotante "volver arriba".
- Pie de página institucional.

Sistema de color (UX)
---------------------
El ACENTO VISUAL es ÚNICO para todas las carreras: azul marino neon
(`AZUL_MARINO_NEON` = `#3b5bdb`). Se aplica a TODOS los elementos que
identifican al usuario "dónde está":

- Tabs activos (subrayado y texto).
- Encabezado sticky (borde inferior, breadcrumb).
- Botón de regreso (hover).
- Iconos orbitales del hero.
- Badge "TÉCNICO SUPERIOR".
- Iconos y bordes del FAQ abierto.
- Botón flotante "volver arriba".
- Badges informativos del hero.

Los TEXTOS largos son NEUTROS (`gray-11`/`gray-12`) para mantener
legibilidad.

Nota técnica: ACORDEÓN FAQ UNIFICADO
------------------------------------
✅ REFACTORIZADO: la sección de preguntas frecuentes delega en
`acordeon_faq` con variante `"light"`.

⚠️ IMPORTANTE: los items del acordeón vienen como `Var` reactiva
(`carrera_seleccionada["preguntas_frecuentes"]`), NO como lista
estática de Python. Por eso:

- NO se puede iterar en Python (lanzaría `VarTypeError`).
- Se pasa el `Var` DIRECTO a `acordeon_faq`, que internamente usa
  `rx.foreach` para iterar en el frontend.
- Se accede a los campos con `item["pregunta"]` / `item["respuesta"]`
  (compatible con `Var`).

Nota técnica: COLORES ADAPTATIVOS
---------------------------------
Los colores adaptativos (light/dark) NO se exponen como `@rx.var`
porque `rx.color_mode_cond()` devuelve un `Var` reactivo del frontend,
no un `str` serializable.

Los helpers `color_carrera_adaptativo` y `color_suave_carrera_adaptativo`
fueron ELIMINADOS de `constantes_visuales.py`. Este archivo usa
directamente `AZUL_MARINO_NEON` (str) y `FONDO_AZUL_SUAVE` (Var
adaptativo).

Nota técnica: VALIDACIÓN DE RUTA
--------------------------------
El decorador `@rx.page` incluye
`on_load=EstadoInstitucional.redirigir_si_carrera_invalida`. Si el
`carrera_id` no corresponde a ninguna carrera (o no es convertible a
int), el evento redirige a `/404?origen=carrera`.
"""

from __future__ import annotations

import reflex as rx

from app_portada_instein.componentes.acordeon_faq import acordeon_faq
from app_portada_instein.componentes.barra_navegacion import (
    barra_navegacion_superior,
)
from app_portada_instein.componentes.pie_pagina import (
    pie_pagina_institucional,
)
from app_portada_instein.componentes.primitivos import enlace_navegacion
from app_portada_instein.componentes.secciones_detalle import (
    seccion_informacion,
    seccion_perfil_y_campo_laboral,
    seccion_plan_estudios,
)
from app_portada_instein.datos.modelos_carrera import IconoAnimado
from app_portada_instein.dominio.estado_institucional import (
    EstadoInstitucional,
)
from app_portada_instein.infraestructura.constantes_visuales import (
    # Layout
    ANCHO_CONTENIDO,
    ANCHO_SECCION,
    # Acento único del proyecto
    AZUL_MARINO_NEON,
    FONDO_AZUL_SUAVE,
    # Colores neutros
    COLOR_ACENTO_BORDE,
    COLOR_ACENTO_FONDO,
    COLOR_ACENTO_SOLIDO,
    COLOR_ACENTO_TEXTO,
    COLOR_ACENTO_TEXTO_SOLIDO,
    COLOR_BORDE_HOVER,
    COLOR_BORDE_SUAVE,
    COLOR_FONDO_CARTA,
    COLOR_FONDO_SUAVE,
    COLOR_TEXTO_CUERPO,
    COLOR_TEXTO_PRINCIPAL,
    COLOR_TEXTO_SECUNDARIO,
    # Datos
    NOMBRE_INSTITUTO,
    PADDING_LATERAL,
    RADIO_EXTRA_GRANDE,
    RADIO_MEDIO,
    RADIO_PASTILLA,
)


# ======================================================================
# Constantes locales de layout
# ======================================================================

# Padding inferior del bloque de pestañas para dejar respirar el footer.
PADDING_INFERIOR_PESTANAS = f"0 {PADDING_LATERAL} 6rem {PADDING_LATERAL}"

# Tamaños del contenedor orbital de la imagen central (responsive).
TAMANO_IMAGEN_ORBITAL = ["10rem", "13rem", "15rem"]

# Ancho del espaciador invisible en el header sticky.
ANCHO_ESPACIADOR_HEADER = "6rem"


# ======================================================================
# Helpers de color (delegan en el acento único)
# ======================================================================


def _color_carrera_actual() -> str:
    """
    Color principal del acento global (azul marino neon).

    ✅ REFACTORIZADO: ya no depende de la carrera seleccionada.
    Mantiene el nombre por compatibilidad con los usos internos
    (tabs, header sticky, botón flotante, badges, FAQs).

    Returns:
        Hex del azul marino neon (`#3b5bdb`).
    """
    return AZUL_MARINO_NEON


def _color_suave_carrera_actual() -> rx.Var:
    """
    Color suave de fondo del acento global.

    ✅ REFACTORIZADO: usa `FONDO_AZUL_SUAVE` (adaptativo light/dark)
    en lugar del color suave de la carrera.

    Returns:
        Var reactiva con el fondo azul marino translúcido, adaptado
        al color_mode actual.
    """
    return FONDO_AZUL_SUAVE


# ======================================================================
# Triggers de pestañas (con acento cuando activos)
# ======================================================================


def _tabs_trigger(texto: str, icono: str, value: str) -> rx.Component:
    """
    Trigger de pestaña responsive con el acento cuando activo.

    - Móvil: solo texto (heading size 4).
    - Tablet/desktop: icono + texto (heading size 5).
    - Estado activo: texto y subrayado con el acento.
    """
    color_carrera = _color_carrera_actual()

    return rx.tabs.trigger(
        rx.mobile_only(
            rx.hstack(
                rx.heading(texto, size="4"),
                spacing="2",
                align="center",
                width="100%",
            ),
        ),
        rx.tablet_and_desktop(
            rx.hstack(
                rx.icon(icono, size=24),
                rx.heading(texto, size="5"),
                spacing="2",
                align="center",
                width="100%",
            ),
        ),
        value=value,
        color=COLOR_TEXTO_SECUNDARIO,
        _hover={
            "color": color_carrera,
        },
        _selected={
            "color": color_carrera,
            "border_color": color_carrera,
        },
    )


def _pestana_trigger_con_contador(
    texto: str,
    icono: str,
    value: str,
    contador: str | None = None,
) -> rx.Component:
    """
    Trigger de pestaña con icono + texto + contador opcional.

    Args:
        texto: Etiqueta visible.
        icono: Nombre del icono de Lucide.
        value: Valor único de la pestaña.
        contador: Texto opcional (ej: número de items).
    """
    hijos = [
        rx.icon(icono, size=18),
        rx.text(
            texto,
            font_size="0.875rem",
            font_weight="600",
            white_space="nowrap",
        ),
    ]

    if contador is not None:
        hijos.append(
            rx.text(
                contador,
                font_size="0.6875rem",
                font_weight="700",
                padding="0.125rem 0.5rem",
                border_radius=RADIO_PASTILLA,
                background=COLOR_FONDO_SUAVE,
                color=COLOR_TEXTO_SECUNDARIO,
            )
        )

    return rx.tabs.trigger(
        rx.flex(
            *hijos,
            align="center",
            justify="center",
            gap="0.5rem",
            width="100%",
        ),
        value=value,
        padding="0.75rem 1rem",
        cursor="pointer",
        transition="all 0.2s",
        color=COLOR_TEXTO_SECUNDARIO,
        border_radius=RADIO_MEDIO,
        _hover={
            "background": COLOR_FONDO_SUAVE,
            "color": COLOR_TEXTO_PRINCIPAL,
        },
        _selected={
            "color": COLOR_TEXTO_PRINCIPAL,
            "background": COLOR_FONDO_CARTA,
            "box_shadow": "0 2px 8px -2px rgb(0 0 0 / 0.08)",
        },
    )


# ======================================================================
# Encabezado sticky con breadcrumb
# ======================================================================


def _encabezado_fijo_detalle() -> rx.Component:
    """
    Encabezado sticky con:
    - Botón de regreso a /carreras (con hover del acento).
    - Breadcrumb: Carreras > [Nombre corto].
    - Espaciador a la derecha para balance visual.
    - Borde inferior con el acento.
    """
    nombre_corto = EstadoInstitucional.carrera_seleccionada["nombre_corto"]
    color_carrera = _color_carrera_actual()

    return rx.box(
        rx.flex(
            # --- Botón de regreso (hover con el acento) ---
            enlace_navegacion(
                "/carreras",
                rx.icon("arrow-left", size=18),
                rx.text("Volver", font_size="0.8125rem", font_weight="600"),
                color=COLOR_TEXTO_PRINCIPAL,
                padding="0.5rem 0.875rem",
                border_radius=RADIO_MEDIO,
                background=COLOR_FONDO_CARTA,
                border=f"1px solid {COLOR_BORDE_SUAVE}",
                display="flex",
                align_items="center",
                gap="0.375rem",
                transition="all 0.2s",
                flex_shrink="0",
                text_decoration="none",
                _hover={
                    "background": COLOR_FONDO_SUAVE,
                    "border_color": color_carrera,
                    "transform": "translateX(-2px)",
                },
            ),
            # --- Breadcrumb central ---
            rx.flex(
                rx.text(
                    "Carreras",
                    font_size="0.8125rem",
                    color=COLOR_TEXTO_SECUNDARIO,
                ),
                rx.icon(
                    "chevron-right",
                    size=14,
                    color=COLOR_TEXTO_SECUNDARIO,
                ),
                rx.text(
                    nombre_corto,
                    font_size="0.8125rem",
                    font_weight="600",
                    color=COLOR_TEXTO_PRINCIPAL,
                ),
                align="center",
                gap="0.375rem",
                display=rx.breakpoints(initial="none", md="flex"),
            ),
            # --- Espaciador invisible para balance ---
            rx.box(width=ANCHO_ESPACIADOR_HEADER, flex_shrink="0"),
            align="center",
            justify="between",
            width="100%",
        ),
        align="center",
        justify="center",
        width="100%",
        padding="0.75rem 1.5rem",
        background=rx.color("gray", 1, alpha=True),
        backdrop_filter="blur(12px)",
        border_bottom=f"1px solid {COLOR_BORDE_SUAVE}",
        position="sticky",
        top="0",
        z_index="50",
    )


# ======================================================================
# Iconos orbitales
# ======================================================================


def _anillos_saturno(color: str | rx.Var) -> rx.Component:
    """
    Dibuja los anillos característicos de Saturno alrededor del icono.

    Args:
        color: Color del anillo (hex estático o Var adaptativa).
    """
    return rx.box(
        rx.box(
            position="absolute",
            top="50%",
            left="50%",
            width="1.8rem",
            height="0.45rem",
            border=f"2px solid {color}",
            border_radius=RADIO_PASTILLA,
            transform="translate(-50%, -50%)",
            opacity="0.8",
        ),
        rx.box(
            position="absolute",
            top="50%",
            left="50%",
            width="2.2rem",
            height="0.65rem",
            border=f"1.5px solid {color}",
            border_radius=RADIO_PASTILLA,
            transform="translate(-50%, -50%)",
            opacity="0.4",
        ),
        position="absolute",
        top="50%",
        left="50%",
        width="0",
        height="0",
        z_index="5",
        pointer_events="none",
    )


def _icono_orbital(icono_animado: IconoAnimado) -> rx.Component:
    """
    Renderiza un icono orbitando alrededor de la imagen de la carrera.

    Args:
        icono_animado: Dict `IconoAnimado` con la configuración orbital.
    """
    periodo = icono_animado["periodo"]
    keyframe_orbita = icono_animado["keyframe_orbita"]
    desfase = icono_animado["desfase_temporal"]
    color_icono = icono_animado["color"]
    tiene_anillos = icono_animado["tiene_anillos"]

    return rx.box(
        rx.box(
            rx.cond(
                tiene_anillos,
                _anillos_saturno(color_icono),
                rx.fragment(),
            ),
            rx.icon(
                icono_animado["nombre"],
                size=18,
                color="white",
            ),
            padding="0.5rem",
            border_radius="0.625rem",
            background=color_icono,
            box_shadow=f"0 6px 16px -4px {color_icono}",
            display="flex",
            align_items="center",
            justify_content="center",
            position="relative",
        ),
        position="absolute",
        top="50%",
        left="50%",
        transform_origin="center center",
        animation=f"{keyframe_orbita} {periodo}s linear {desfase}s infinite",
        z_index="20",
    )


# ======================================================================
# Contenedor orbital con imagen central + iconos orbitando
# ======================================================================


def _contenedor_orbital_imagen() -> rx.Component:
    """
    Contenedor cuadrado con:
    - Anillo decorativo exterior (órbita visible).
    - Halo radial con el acento.
    - 4 iconos orbitando con elipses keplerianas.
    - Imagen central de la carrera con anillo del acento.

    ✅ REFACTORIZADO: todos los colores usan el acento único
    (`AZUL_MARINO_NEON`) y `FONDO_AZUL_SUAVE` (adaptativo), en lugar
    de los colores por carrera.
    """
    carrera = EstadoInstitucional.carrera_seleccionada
    color_principal = _color_carrera_actual()

    return rx.box(
        # --- Anillo decorativo exterior ---
        rx.box(
            position="absolute",
            top="5%",
            left="5%",
            right="5%",
            bottom="5%",
            border=rx.color_mode_cond(
                light=f"1px dashed {AZUL_MARINO_NEON}33",
                dark=f"1px dashed {AZUL_MARINO_NEON}55",
            ),
            border_radius=RADIO_PASTILLA,
            z_index="0",
        ),
        # --- Halo radial (f-strings para concatenar Vars) ---
        rx.box(
            position="absolute",
            top="0",
            left="0",
            right="0",
            bottom="0",
            background=rx.color_mode_cond(
                light=(
                    f"radial-gradient(circle at 50% 50%, "
                    f"{AZUL_MARINO_NEON}33 0%, "
                    f"transparent 60%)"
                ),
                dark=(
                    f"radial-gradient(circle at 50% 50%, "
                    f"{AZUL_MARINO_NEON}44 0%, "
                    f"transparent 60%)"
                ),
            ),
            border_radius=RADIO_PASTILLA,
            filter="blur(20px)",
            z_index="1",
        ),
        # --- Iconos orbitales ---
        rx.box(
            rx.foreach(
                carrera["iconos_animados"],
                _icono_orbital,
            ),
            position="absolute",
            top="0",
            left="0",
            right="0",
            bottom="0",
            z_index="5",
        ),
        # --- Imagen central ---
        rx.box(
            rx.image(
                src=f"/{carrera['imagen_archivo']}",
                alt=carrera["nombre"],
                width="100%",
                height="100%",
                object_fit="cover",
                border_radius=RADIO_PASTILLA,
            ),
            position="absolute",
            top="50%",
            left="50%",
            transform="translate(-50%, -50%)",
            width=TAMANO_IMAGEN_ORBITAL,
            height=TAMANO_IMAGEN_ORBITAL,
            border_radius=RADIO_PASTILLA,
            border=f"3px solid {color_principal}",
            box_shadow=f"0 15px 30px -8px {color_principal}",
            overflow="hidden",
            z_index="10",
            animation="pulso_central 3s ease-in-out infinite",
        ),
        # --- Contenedor ---
        position="relative",
        width="100%",
        max_width="20rem",
        aspect_ratio="1",
        margin="0 auto",
        display="flex",
        align_items="center",
        justify_content="center",
        overflow="visible",
    )


# ======================================================================
# Badge informativo reutilizable
# ======================================================================


def _badge_info(
    icono: str,
    texto: str,
    color: str | rx.Var,
    fondo_suave: bool = True,
) -> rx.Component:
    """
    Badge informativo con icono + texto y borde con el acento.

    El texto es NEUTRO (`gray-11`) y solo el icono y el borde usan el
    acento. Fondo neutro suave.
    """
    return rx.flex(
        rx.icon(icono, size=12, color=color),
        rx.text(
            texto,
            font_size="0.75rem",
            font_weight="600",
            color=COLOR_TEXTO_PRINCIPAL,
            white_space="nowrap",
        ),
        align="center",
        gap="0.375rem",
        padding="0.375rem 0.75rem",
        border_radius=RADIO_PASTILLA,
        background=COLOR_FONDO_SUAVE if fondo_suave else "transparent",
        border=f"1px solid {color}",
    )


# ======================================================================
# Hero de carrera
# ======================================================================


def _hero_carrera() -> rx.Component:
    """
    Bloque de presentación principal:
    - Columna izquierda: contenedor orbital con imagen + iconos.
    - Columna derecha: nombre, lema, badges y CTA.
    """
    carrera = EstadoInstitucional.carrera_seleccionada
    color_principal = _color_carrera_actual()

    return rx.flex(
        # --- Columna izquierda: contenedor orbital ---
        rx.box(
            _contenedor_orbital_imagen(),
            width=["100%", "100%", "100%", "40%"],
            flex_shrink="0",
        ),
        # --- Columna derecha: información textual ---
        rx.vstack(
            # --- Badge de categoría ---
            rx.flex(
                rx.icon("award", size=12, color="white"),
                rx.text(
                    "TÉCNICO SUPERIOR",
                    font_size="0.625rem",
                    font_weight="800",
                    color="white",
                    letter_spacing="0.1em",
                ),
                align="center",
                gap="0.375rem",
                background=color_principal,
                padding="0.375rem 0.75rem",
                border_radius=RADIO_PASTILLA,
                width="fit-content",
                box_shadow=f"0 4px 12px -2px {color_principal}",
            ),
            # --- Nombre de la carrera ---
            rx.heading(
                carrera["nombre"],
                size="8",
                font_weight="800",
                color=COLOR_TEXTO_PRINCIPAL,
                line_height="1.1",
                text_align="left",
                letter_spacing="-0.025em",
            ),
            # --- Lema ---
            rx.text(
                carrera["lema"],
                font_size="1rem",
                color=COLOR_TEXTO_CUERPO,
                line_height="1.6",
                max_width="36rem",
            ),
            # --- Badges informativos ---
            rx.flex(
                _badge_info("clock", carrera["duracion"], color_principal),
                _badge_info(
                    "building-2", carrera["modalidad"], color_principal
                ),
                wrap="wrap",
                gap="0.5rem",
                margin_top="0.5rem",
            ),
            align="start",
            spacing="4",
            width=["100%", "100%", "100%", "60%"],
        ),
        width="100%",
        justify="center",
        align="center",
        gap=["2rem", "2.5rem", "3rem", "3rem"],
        padding=[
            "2rem 1.5rem",
            "2.5rem 1.5rem",
            "3rem 1.5rem",
            "3rem 1.5rem",
        ],
        flex_direction=["column", "column", "column", "row"],
    )


# ======================================================================
# Sección: PREGUNTAS FRECUENTES (delegada al acordeón unificado)
# ======================================================================


def _seccion_preguntas_frecuentes() -> rx.Component:
    """
    Sección completa con las preguntas frecuentes de la carrera.

    ✅ REFACTORIZADO: usa el componente genérico `acordeon_faq` con
    variante `"light"`.

    ⚠️ IMPORTANTE: pasamos el `Var` reactivo DIRECTO a `acordeon_faq`.
    NO se puede iterar en Python puro (lanzaría `VarTypeError`).
    El `rx.foreach` interno del acordeón se encarga de iterar en el
    frontend.

    Estructura:
    1. Encabezado con icono + título + contador reactivo.
    2. Acordeón con las preguntas (pasadas como Var).
    """
    carrera = EstadoInstitucional.carrera_seleccionada
    color_carrera = _color_carrera_actual()
    color_suave_carrera = _color_suave_carrera_actual()

    return rx.vstack(
        # --- Encabezado ---
        rx.flex(
            rx.box(
                rx.icon("circle-help", size=20, color=color_carrera),
                padding="0.625rem",
                border_radius=RADIO_MEDIO,
                background=color_suave_carrera,
                border=f"1px solid {color_carrera}",
                display="flex",
                align_items="center",
                justify_content="center",
                flex_shrink="0",
            ),
            rx.vstack(
                rx.text(
                    "Preguntas frecuentes",
                    font_size="0.9375rem",
                    font_weight="800",
                    color=COLOR_TEXTO_PRINCIPAL,
                    text_transform="uppercase",
                    letter_spacing="0.05em",
                    line_height="1.2",
                ),
                rx.text(
                    "Respuestas a las dudas más comunes de esta carrera.",
                    font_size="0.75rem",
                    color=COLOR_TEXTO_SECUNDARIO,
                    line_height="1.4",
                ),
                spacing="1",
                align="start",
                flex="1",
                min_width="0",
            ),
            # Contador reactivo (usa .length().to_string() en vez de len())
            rx.box(
                rx.text(
                    carrera["preguntas_frecuentes"]
                    .length()
                    .to_string(),
                    font_size="0.6875rem",
                    font_weight="700",
                    color=COLOR_TEXTO_SECUNDARIO,
                    text_transform="uppercase",
                    letter_spacing="0.05em",
                ),
                padding="0.25rem 0.625rem",
                border_radius=RADIO_PASTILLA,
                background=COLOR_FONDO_SUAVE,
                border=f"1px solid {color_carrera}",
                flex_shrink="0",
            ),
            align="center",
            gap="0.75rem",
            width="100%",
            margin_bottom="1.5rem",
            flex_wrap="wrap",
        ),
        # --- Acordeón unificado ---
        # Se pasa el Var directamente (NO iterar en Python).
        acordeon_faq(
            items=carrera["preguntas_frecuentes"],
            variante="light",
            icono="circle-help",
            color_acento=AZUL_MARINO_NEON,
            tamano_texto_pregunta="0.9375rem",
            tamano_texto_respuesta="0.875rem",
            padding_cabecera="1.125rem 1.25rem",
            padding_respuesta="0 1.25rem 1.25rem 3.5rem",
        ),
        spacing="0",
        width="100%",
        max_width=ANCHO_SECCION,
        margin="0 auto",
        padding=f"0 {PADDING_LATERAL}",
    )


# ======================================================================
# Pestañas de secciones del detalle
# ======================================================================


def _pestanas_secciones_detalle() -> rx.Component:
    """Sistema de pestañas con `rx.tabs.root` para las 3 secciones."""
    return rx.tabs.root(
        rx.tabs.list(
            _tabs_trigger("Info", "info", value="info"),
            _tabs_trigger("Plan", "book-open-text", value="plan"),
            _tabs_trigger("Perfil", "target", value="perfil"),
            width="100%",
            gap="0.25rem",
            padding="0.375rem",
            border_radius=RADIO_EXTRA_GRANDE,
        ),
        rx.tabs.content(
            seccion_informacion(),
            margin_top="1.5rem",
            value="info",
        ),
        rx.tabs.content(
            seccion_plan_estudios(),
            margin_top="1.5rem",
            value="plan",
        ),
        rx.tabs.content(
            seccion_perfil_y_campo_laboral(),
            margin_top="1.5rem",
            value="perfil",
        ),
        default_value="info",
        width="100%",
    )


# ======================================================================
# Botón flotante "volver arriba"
# ======================================================================


def _boton_volver_arriba() -> rx.Component:
    """Botón flotante para volver al inicio de la página."""
    color_principal = _color_carrera_actual()

    return rx.box(
        rx.icon(
            "arrow-up",
            size=20,
            color="white",
        ),
        position="fixed",
        bottom="2rem",
        right="2rem",
        height="3rem",
        width="3rem",
        border_radius=RADIO_PASTILLA,
        background=color_principal,
        box_shadow=f"0 10px 30px -8px {color_principal}",
        display=rx.breakpoints(initial="none", md="flex"),
        align_items="center",
        justify_content="center",
        cursor="pointer",
        z_index="40",
        transition="all 0.25s cubic-bezier(0.4, 0, 0.2, 1)",
        on_click=rx.call_script(
            "window.scrollTo({top: 0, behavior: 'smooth'})"
        ),
        _hover={
            "transform": "translateY(-3px)",
            "box_shadow": f"0 15px 40px -8px {color_principal}",
        },
    )


# ======================================================================
# Vista completa
# ======================================================================


@rx.page(
    route="/carrera/[carrera_id]",
    title=f"Detalle de Carrera | {NOMBRE_INSTITUTO}",
    on_load=EstadoInstitucional.redirigir_si_carrera_invalida,
)
def vista_detalle_carrera() -> rx.Component:
    """
    Página de detalle con:
    - Encabezado sticky con breadcrumb.
    - Hero con contenedor orbital + info textual + CTA.
    - Pestañas (Info, Plan, Perfil).
    - Sección de preguntas frecuentes (fuera de las tabs).
    - Botón flotante "volver arriba".
    - Pie de página institucional.

    El `on_load` (`redirigir_si_carrera_invalida`) redirige a
    `/404?origen=carrera` si el `carrera_id` de la URL no existe o no
    es válido.
    """
    return rx.vstack(
        # --- Barra de navegación principal ---
        barra_navegacion_superior(),
        # --- Contenido principal ---
        rx.box(
            # --- Encabezado sticky con breadcrumb ---
            _encabezado_fijo_detalle(),
            # --- Hero con contenedor orbital + info ---
            _hero_carrera(),
            # --- Pestañas de secciones ---
            rx.box(
                _pestanas_secciones_detalle(),
                padding=PADDING_INFERIOR_PESTANAS,
                max_width=ANCHO_CONTENIDO,
                margin="0 auto",
                width="100%",
            ),
            # --- Sección de preguntas frecuentes (fuera de las tabs) ---
            _seccion_preguntas_frecuentes(),
            # --- Botón flotante "volver arriba" ---
            _boton_volver_arriba(),
            # --- Contenedor principal ---
            padding_bottom="3rem",
            width="100%",
        ),
        # --- Pie de página ---
        pie_pagina_institucional(),
        # --- Layout del contenedor raíz ---
        align="center",
        min_height="100vh",
        width="100%",
        spacing="0",
    )


__all__ = ["vista_detalle_carrera"]