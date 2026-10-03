"""
Vista "Becas y Reconocimientos" (ruta "/becas").

Programa institucional de becas por innovación. No hay becas generales
ni descuentos comerciales. Las becas se otorgan a estudiantes activos
del instituto que presenten un proyecto con puntaje de innovación ≥ 90
en las ferias internas.

Contenido:
- Hero con badge "Programa de becas por innovación".
- Grid de 3 tarjetas con las bases del programa.
- Sección explicativa: ¿cómo funciona el programa?
- Timeline del proceso de evaluación (5 etapas).
- Grid de áreas de innovación evaluadas (5 áreas).
- Sección de niveles de beca por puntaje (3 niveles).
- Requisitos para participar.
- Proyectos ganadores (ejemplos destacados).
- Preguntas frecuentes del programa.
- CTA final hacia /contacto.

Sistema de color (UX)
---------------------
- Acentos institucionales: accent crimson.
- Áreas de innovación: colores distintos (blue, cyan, violet, orange,
  green).
- Niveles de beca: verde (30%), ámbar (50%), crimson (100%).
- Textos: neutros (`gray-11`/`gray-12`).

Nota técnica: ACORDEÓN FAQ UNIFICADO
------------------------------------
✅ REFACTORIZADO: la sección de preguntas frecuentes ya NO tiene su
propio `EstadoFAQBecas` ni su propio item. Ahora delega en el
componente genérico `acordeon_faq` con variante `"light"`, que usa
el `EstadoAcordeonFaq` global.

Esto elimina ~60 líneas de código duplicado.

Nota técnica: `ItemFaq` ES `TypedDict`
--------------------------------------
`PREGUNTAS_BECA` ahora es `list[ItemFaq]` (TypedDict), no `list[dict]`.
Los items se construyen con **dicts literales**:

    {"pregunta": "¿...?", "respuesta": "..."}

NO con `ItemFaq(pregunta=..., respuesta=...)`.

Nota técnica: LAYOUT
--------------------
- `rx.flex` y `rx.vstack` (Radix Themes) NO aceptan listas en
  `direction`, `align`, `justify`. Usar `rx.breakpoints(...)`.
"""

from __future__ import annotations

import reflex as rx

from app_portada_instein.componentes.acordeon_faq import (
    ItemFaq,
    acordeon_faq,
)
from app_portada_instein.componentes.barra_navegacion import (
    barra_navegacion_superior,
)
from app_portada_instein.componentes.pie_pagina import (
    pie_pagina_institucional,
)
from app_portada_instein.infraestructura.constantes_visuales import (
    COLOR_ACENTO_FONDO,
    COLOR_ACENTO_SOLIDO,
    COLOR_ACENTO_TEXTO,
    COLOR_BORDE_SUAVE,
    COLOR_DIVISOR,
    COLOR_FONDO_CARTA,
    COLOR_FONDO_SUAVE,
    COLOR_TEXTO_CUERPO,
    COLOR_TEXTO_PRINCIPAL,
    COLOR_TEXTO_SECUNDARIO,
    NOMBRE_INSTITUTO,
    RADIO_EXTRA_GRANDE,
    RADIO_GRANDE,
    RADIO_MEDIO,
    RADIO_PASTILLA,
)


# ======================================================================
# Constantes locales
# ======================================================================

ANCHO_MAXIMO = "72rem"
ANCHO_CONTENIDO = "64rem"
PADDING_LATERAL = "1.5rem"


# ======================================================================
# Datos: bases del programa (3 tarjetas del hero)
# ======================================================================

BASES_PROGRAMA: list[dict] = [
    {
        "icono": "trophy",
        "titulo": "Se gana en las ferias",
        "descripcion": (
            "Las becas se otorgan en las ferias de innovación internas "
            "del instituto. No son automáticas ni por promedio."
        ),
        "color": "amber",
    },
    {
        "icono": "target",
        "titulo": "Mínimo 90 puntos",
        "descripcion": (
            "El proyecto debe obtener un puntaje de innovación igual o "
            "superior a 90 sobre 100 para ser elegible."
        ),
        "color": "violet",
    },
    {
        "icono": "users",
        "titulo": "Solo estudiantes activos",
        "descripcion": (
            "Debes estar inscrito y cursando una carrera del instituto "
            "al momento de la feria."
        ),
        "color": "blue",
    },
]


# ======================================================================
# Datos: proceso de evaluación (timeline)
# ======================================================================

PASOS_PROCESO: list[dict] = [
    {
        "numero": "01",
        "icono": "clipboard-list",
        "titulo": "Forma tu equipo y elige un área",
        "descripcion": (
            "Puedes participar individualmente o en equipos de hasta 3 "
            "estudiantes. Elige el área de innovación en la que "
            "competirás."
        ),
    },
    {
        "numero": "02",
        "icono": "lightbulb",
        "titulo": "Desarrolla tu proyecto",
        "descripcion": (
            "Trabaja durante el semestre en tu proyecto con apoyo de "
            "docentes mentores. Documenta todo el proceso."
        ),
    },
    {
        "numero": "03",
        "icono": "presentation",
        "titulo": "Preséntalo en la feria",
        "descripcion": (
            "Expón tu proyecto en la feria de innovación del instituto "
            "con un stand y una presentación de 10 minutos."
        ),
    },
    {
        "numero": "04",
        "icono": "scale",
        "titulo": "Evaluación del jurado",
        "descripcion": (
            "Un jurado de docentes y profesionales externos evalúa "
            "originalidad, impacto, viabilidad e innovación técnica."
        ),
    },
    {
        "numero": "05",
        "icono": "trophy",
        "titulo": "Beca otorgada",
        "descripcion": (
            "Si obtienes 90 puntos o más, accedes a la beca según el "
            "nivel alcanzado. Se aplica al siguiente semestre."
        ),
    },
]


# ======================================================================
# Datos: áreas de innovación evaluadas
# ======================================================================

AREAS_INNOVACION: list[dict] = [
    {
        "icono": "cpu",
        "titulo": "Tecnología e Informática",
        "descripcion": (
            "Software, hardware, automatización, IA aplicada, "
            "ciberseguridad."
        ),
        "carrera": "Sistemas Informáticos",
        "color": "blue",
    },
    {
        "icono": "circuit-board",
        "titulo": "Electrónica y Control",
        "descripcion": (
            "Circuitos, robótica, telecomunicaciones, domótica, "
            "energías renovables."
        ),
        "carrera": "Electrónica",
        "color": "cyan",
    },
    {
        "icono": "globe",
        "titulo": "Comercio y Logística",
        "descripcion": (
            "Importación/exportación, logística, comercio digital, "
            "trámites aduaneros."
        ),
        "carrera": "Comercio Internacional",
        "color": "orange",
    },
    {
        "icono": "calculator",
        "titulo": "Gestión Financiera",
        "descripcion": (
            "Contabilidad digital, finanzas, emprendimiento, "
            "automatización contable."
        ),
        "carrera": "Contaduría General",
        "color": "violet",
    },
    {
        "icono": "briefcase",
        "titulo": "Innovación Administrativa",
        "descripcion": (
            "Procesos, gestión documental, atención al cliente, "
            "organización empresarial."
        ),
        "carrera": "Secretariado Ejecutivo",
        "color": "green",
    },
]


# ======================================================================
# Datos: niveles de beca según puntaje
# ======================================================================

NIVELES_BECA: list[dict] = [
    {
        "rango": "90 - 93",
        "puntos": "90-93 pts",
        "titulo": "Beca Bronce",
        "porcentaje": "30%",
        "descripcion": (
            "Cubre el 30% de la mensualidad del siguiente semestre."
        ),
        "icono": "medal",
        "color": "amber",
    },
    {
        "rango": "94 - 97",
        "puntos": "94-97 pts",
        "titulo": "Beca Plata",
        "porcentaje": "50%",
        "descripcion": (
            "Cubre el 50% de la mensualidad del siguiente semestre."
        ),
        "icono": "award",
        "color": "violet",
    },
    {
        "rango": "98 - 100",
        "puntos": "98-100 pts",
        "titulo": "Beca Oro",
        "porcentaje": "100%",
        "descripcion": (
            "Cubre el 100% de la mensualidad del siguiente semestre."
        ),
        "icono": "trophy",
        "color": "crimson",
    },
]


# ======================================================================
# Datos: requisitos para participar
# ======================================================================

REQUISITOS_BECA: list[dict] = [
    {
        "icono": "user-check",
        "texto": "Ser estudiante activo del instituto al momento de la feria",
    },
    {
        "icono": "users",
        "texto": "Participar individualmente o en equipos de hasta 3 personas",
    },
    {
        "icono": "lightbulb",
        "texto": "Presentar un proyecto original de innovación en cualquier área",
    },
    {
        "icono": "file-text",
        "texto": "Documentar el proceso y entregar la memoria del proyecto",
    },
    {
        "icono": "presentation",
        "texto": "Exponer el proyecto en la feria con stand y presentación",
    },
    {
        "icono": "shield-check",
        "texto": "No tener sanciones disciplinarias vigentes",
    },
    {
        "icono": "handshake",
        "texto": "Aceptar los términos y condiciones del programa de becas",
    },
]


# ======================================================================
# Datos: proyectos ganadores destacados
# ======================================================================

PROYECTOS_GANADORES: list[dict] = [
    {
        "anio": "2025",
        "titulo": "Sistema de riego inteligente con IoT",
        "equipo": "Equipo Electrónica",
        "puntaje": "96",
        "beca": "Beca Plata · 50%",
        "descripcion": (
            "Sistema de riego automatizado con sensores de humedad y "
            "control desde app móvil. Redujo el consumo de agua en 40%."
        ),
        "color": "cyan",
    },
    {
        "anio": "2025",
        "titulo": "Plataforma de gestión para microempresas",
        "equipo": "Equipo Sistemas",
        "puntaje": "94",
        "beca": "Beca Plata · 50%",
        "descripcion": (
            "Aplicación web para digitalizar inventarios, ventas y "
            "facturación de microempresas locales."
        ),
        "color": "blue",
    },
    {
        "anio": "2024",
        "titulo": "Optimización de rutas para exportadoras",
        "equipo": "Equipo Comercio Int.",
        "puntaje": "91",
        "beca": "Beca Bronce · 30%",
        "descripcion": (
            "Modelo de optimización logística para reducir costos de "
            "transporte en exportaciones bolivianas."
        ),
        "color": "orange",
    },
]


# ======================================================================
# Datos: preguntas frecuentes del programa
# ======================================================================
# ✅ Ahora es `list[ItemFaq]` (TypedDict) en lugar de `list[dict]`.
# Se construye con dicts literales:
#     {"pregunta": "...", "respuesta": "..."}
# ----------------------------------------------------------------------

PREGUNTAS_BECA: list[ItemFaq] = [
    {
        "pregunta": "¿Hay becas por promedio académico?",
        "respuesta": (
            "No. En INSTEIN no otorgamos becas por promedio ni por "
            "situación socioeconómica. Nuestro único programa de becas "
            "es el de innovación, y se gana presentando un proyecto "
            "destacado en las ferias internas."
        ),
    },
    {
        "pregunta": "¿Hay descuentos por pago adelantado o familiar?",
        "respuesta": (
            "No manejamos descuentos comerciales de ningún tipo. La "
            "mensualidad es única y el único beneficio económico "
            "disponible es la beca por innovación."
        ),
    },
    {
        "pregunta": "¿Cuántas veces al año se puede participar?",
        "respuesta": (
            "Hay dos ferias al año, una por semestre. Puedes participar "
            "en todas las que quieras. Si ya tienes una beca activa, "
            "puedes intentar mejorarla en la siguiente feria."
        ),
    },
    {
        "pregunta": "¿La beca aplica retroactiva al semestre actual?",
        "respuesta": (
            "No. La beca se aplica al semestre siguiente al de la feria "
            "en la que ganaste. Así todos los estudiantes compiten en "
            "igualdad de condiciones al inicio de cada semestre."
        ),
    },
    {
        "pregunta": "¿Cuánto dura la beca?",
        "respuesta": (
            "La beca cubre una mensualidad completa. Si quieres "
            "mantenerla para el siguiente semestre, debes volver a "
            "participar en la feria y volver a obtener 90 puntos o más."
        ),
    },
    {
        "pregunta": "¿Puedo participar si estoy en primer semestre?",
        "respuesta": (
            "Sí. No hay restricción por semestre. Cualquier estudiante "
            "activo puede participar, incluso si acaba de ingresar. "
            "Mentores y docentes te apoyarán en el desarrollo."
        ),
    },
    {
        "pregunta": "¿Qué pasa si mi proyecto no llega a 90 puntos?",
        "respuesta": (
            "Puedes seguir mejorándolo y presentarlo en la siguiente "
            "feria. Recibirás retroalimentación del jurado para "
            "fortalecer tu propuesta."
        ),
    },
    {
        "pregunta": "¿Los equipos comparten la beca?",
        "respuesta": (
            "Sí. Si ganas en equipo, la beca se otorga a cada integrante "
            "de manera individual, aplicada a su propia mensualidad."
        ),
    },
]


# ======================================================================
# HERO
# ======================================================================


def _hero_becas() -> rx.Component:
    """Hero con badge + título + subtítulo."""
    return rx.vstack(
        # --- Badge ---
        rx.flex(
            rx.icon("trophy", size=12, color=COLOR_ACENTO_TEXTO),
            rx.text(
                "PROGRAMA DE BECAS POR INNOVACIÓN",
                font_size="0.75rem",
                font_weight="700",
                color=COLOR_ACENTO_TEXTO,
                letter_spacing="0.05em",
            ),
            align="center",
            gap="0.5rem",
            padding="0.5rem 1rem",
            border_radius=RADIO_PASTILLA,
            background=COLOR_ACENTO_FONDO,
            border=f"1px solid {COLOR_ACENTO_TEXTO}",
            width="fit-content",
            margin_bottom="1rem",
        ),
        # --- Título ---
        rx.heading(
            "Becas y ",
            rx.text.span(
                "Reconocimientos",
                color=COLOR_ACENTO_TEXTO,
            ),
            "",
            size="8",
            font_weight="900",
            color=COLOR_TEXTO_PRINCIPAL,
            text_align="center",
            letter_spacing="-0.03em",
            line_height="1.1",
        ),
        # --- Subtítulo ---
        rx.text(
            "En INSTEIN no damos becas por promedio ni descuentos "
            "comerciales. Premiamos la innovación real: si tu proyecto "
            "destaca en nuestras ferias internas, te becamos.",
            font_size="1rem",
            color=COLOR_TEXTO_CUERPO,
            text_align="center",
            max_width="52rem",
            line_height="1.7",
            margin_top="0.5rem",
        ),
        align="center",
        spacing="3",
        padding=f"5rem {PADDING_LATERAL} 3rem {PADDING_LATERAL}",
        max_width=ANCHO_MAXIMO,
        margin="0 auto",
        width="100%",
    )


# ======================================================================
# Bases del programa (3 tarjetas)
# ======================================================================


def _tarjeta_base(item: dict) -> rx.Component:
    """Tarjeta de base del programa."""
    color_scheme = item["color"]

    return rx.box(
        rx.vstack(
            rx.flex(
                rx.icon(
                    item["icono"],
                    size=22,
                    color=rx.color(color_scheme, 11),
                ),
                height="2.75rem",
                width="2.75rem",
                border_radius=RADIO_GRANDE,
                background=rx.color(color_scheme, 3),
                border=f"1px solid {rx.color(color_scheme, 7)}",
                align="center",
                justify="center",
                margin_bottom="0.75rem",
            ),
            rx.text(
                item["titulo"],
                font_size="0.9375rem",
                font_weight="800",
                color=COLOR_TEXTO_PRINCIPAL,
                line_height="1.3",
            ),
            rx.text(
                item["descripcion"],
                font_size="0.8125rem",
                color=COLOR_TEXTO_CUERPO,
                line_height="1.6",
            ),
            align="start",
            spacing="1",
            width="100%",
        ),
        padding="1.5rem",
        border_radius=RADIO_EXTRA_GRANDE,
        border=f"1px solid {COLOR_BORDE_SUAVE}",
        background=COLOR_FONDO_CARTA,
        width="100%",
        height="100%",
        transition="all 0.2s",
        _hover={
            "transform": "translateY(-4px)",
            "border_color": rx.color(color_scheme, 7),
            "box_shadow": f"0 12px 32px -8px {rx.color(color_scheme, 9)}",
        },
    )


def _grid_bases() -> rx.Component:
    """Grid con las 3 bases del programa."""
    return rx.box(
        rx.grid(
            *[_tarjeta_base(item) for item in BASES_PROGRAMA],
            columns=rx.breakpoints(initial="1", sm="1", md="3", lg="3"),
            spacing="4",
            width="100%",
        ),
        max_width=ANCHO_MAXIMO,
        margin="0 auto",
        padding=f"0 {PADDING_LATERAL} 4rem {PADDING_LATERAL}",
        width="100%",
    )


# ======================================================================
# Proceso de evaluación (timeline)
# ======================================================================


def _paso_timeline(paso: dict, indice: int, total: int) -> rx.Component:
    """Paso individual del timeline."""
    es_ultimo = indice == total - 1

    return rx.flex(
        # --- Indicador ---
        rx.vstack(
            rx.box(
                rx.text(
                    paso["numero"],
                    font_size="0.875rem",
                    font_weight="900",
                    color="white",
                    line_height="1",
                ),
                height="2.5rem",
                width="2.5rem",
                border_radius=RADIO_PASTILLA,
                background=COLOR_ACENTO_SOLIDO,
                display="flex",
                align_items="center",
                justify_content="center",
                flex_shrink="0",
                box_shadow=f"0 4px 12px -2px {COLOR_ACENTO_SOLIDO}",
            ),
            rx.cond(
                not es_ultimo,
                rx.box(
                    width="2px",
                    background=COLOR_DIVISOR,
                    flex="1",
                    min_height="2rem",
                ),
                rx.fragment(),
            ),
            align="center",
            spacing="0",
            height="100%",
            flex_shrink="0",
        ),
        # --- Contenido del paso ---
        rx.box(
            rx.flex(
                rx.flex(
                    rx.icon(
                        paso["icono"],
                        size=20,
                        color=COLOR_ACENTO_TEXTO,
                    ),
                    height="2.5rem",
                    width="2.5rem",
                    border_radius=RADIO_MEDIO,
                    background=COLOR_ACENTO_FONDO,
                    border=f"1px solid {COLOR_ACENTO_TEXTO}",
                    align="center",
                    justify="center",
                    flex_shrink="0",
                ),
                rx.vstack(
                    rx.text(
                        paso["titulo"],
                        font_size="1rem",
                        font_weight="700",
                        color=COLOR_TEXTO_PRINCIPAL,
                        line_height="1.3",
                    ),
                    rx.text(
                        paso["descripcion"],
                        font_size="0.875rem",
                        color=COLOR_TEXTO_CUERPO,
                        line_height="1.6",
                    ),
                    align="start",
                    spacing="1",
                    flex="1",
                    min_width="0",
                ),
                align="start",
                gap="1rem",
                width="100%",
            ),
            padding="1.25rem",
            border_radius=RADIO_EXTRA_GRANDE,
            background=COLOR_FONDO_CARTA,
            border=f"1px solid {COLOR_BORDE_SUAVE}",
            width="100%",
            margin_bottom="1rem" if not es_ultimo else "0",
            margin_left="0.75rem",
            transition="all 0.2s",
            _hover={
                "border_color": COLOR_ACENTO_TEXTO,
                "box_shadow": f"0 8px 20px -8px {COLOR_ACENTO_SOLIDO}",
            },
        ),
        align="start",
        gap="1rem",
        width="100%",
    )


def _seccion_proceso() -> rx.Component:
    """Sección del proceso de evaluación."""
    total = len(PASOS_PROCESO)

    return rx.box(
        rx.vstack(
            rx.vstack(
                rx.text(
                    "CÓMO FUNCIONA",
                    font_size="0.75rem",
                    font_weight="700",
                    letter_spacing="0.15em",
                    color=COLOR_ACENTO_TEXTO,
                ),
                rx.heading(
                    "El camino a la beca",
                    size="7",
                    font_weight="800",
                    color=COLOR_TEXTO_PRINCIPAL,
                    text_align="center",
                    letter_spacing="-0.03em",
                ),
                rx.text(
                    "De la idea al reconocimiento en 5 etapas claras.",
                    font_size="0.9375rem",
                    color=COLOR_TEXTO_SECUNDARIO,
                    text_align="center",
                    max_width="42rem",
                ),
                align="center",
                spacing="2",
                margin_bottom="3rem",
            ),
            rx.vstack(
                *[
                    _paso_timeline(paso, i, total)
                    for i, paso in enumerate(PASOS_PROCESO)
                ],
                spacing="0",
                width="100%",
            ),
            width="100%",
            align="center",
        ),
        max_width=ANCHO_CONTENIDO,
        margin="0 auto",
        padding=f"3rem {PADDING_LATERAL}",
        width="100%",
    )


# ======================================================================
# Áreas de innovación
# ======================================================================


def _tarjeta_area(item: dict) -> rx.Component:
    """Tarjeta de área de innovación."""
    color_scheme = item["color"]

    return rx.box(
        rx.vstack(
            rx.flex(
                rx.icon(
                    item["icono"],
                    size=20,
                    color=rx.color(color_scheme, 11),
                ),
                height="2.5rem",
                width="2.5rem",
                border_radius=RADIO_GRANDE,
                background=rx.color(color_scheme, 3),
                border=f"1px solid {rx.color(color_scheme, 7)}",
                align="center",
                justify="center",
                margin_bottom="0.75rem",
            ),
            rx.text(
                item["titulo"],
                font_size="0.9375rem",
                font_weight="800",
                color=COLOR_TEXTO_PRINCIPAL,
                line_height="1.3",
            ),
            rx.text(
                item["descripcion"],
                font_size="0.8125rem",
                color=COLOR_TEXTO_CUERPO,
                line_height="1.6",
            ),
            rx.flex(
                rx.icon(
                    "graduation-cap",
                    size=12,
                    color=rx.color(color_scheme, 11),
                ),
                rx.text(
                    item["carrera"],
                    font_size="0.6875rem",
                    font_weight="700",
                    color=rx.color(color_scheme, 11),
                    text_transform="uppercase",
                    letter_spacing="0.05em",
                ),
                align="center",
                gap="0.375rem",
                margin_top="0.5rem",
                padding="0.25rem 0.625rem",
                border_radius=RADIO_PASTILLA,
                background=rx.color(color_scheme, 3),
                border=f"1px solid {rx.color(color_scheme, 7)}",
                width="fit-content",
            ),
            align="start",
            spacing="1",
            width="100%",
            height="100%",
        ),
        padding="1.5rem",
        border_radius=RADIO_EXTRA_GRANDE,
        border=f"1px solid {COLOR_BORDE_SUAVE}",
        background=COLOR_FONDO_CARTA,
        width="100%",
        height="100%",
        transition="all 0.2s",
        _hover={
            "transform": "translateY(-4px)",
            "border_color": rx.color(color_scheme, 7),
        },
    )


def _seccion_areas() -> rx.Component:
    """Sección con las áreas de innovación."""
    return rx.box(
        rx.vstack(
            rx.vstack(
                rx.text(
                    "ÁREAS DE INNOVACIÓN",
                    font_size="0.75rem",
                    font_weight="700",
                    letter_spacing="0.15em",
                    color=COLOR_ACENTO_TEXTO,
                ),
                rx.heading(
                    "Compite en tu área",
                    size="7",
                    font_weight="800",
                    color=COLOR_TEXTO_PRINCIPAL,
                    text_align="center",
                    letter_spacing="-0.03em",
                ),
                rx.text(
                    "Puedes presentar tu proyecto en cualquiera de las "
                    "5 áreas de innovación, alineadas con las carreras "
                    "del instituto.",
                    font_size="0.9375rem",
                    color=COLOR_TEXTO_SECUNDARIO,
                    text_align="center",
                    max_width="42rem",
                ),
                align="center",
                spacing="2",
                margin_bottom="2rem",
            ),
            rx.grid(
                *[_tarjeta_area(item) for item in AREAS_INNOVACION],
                columns=rx.breakpoints(
                    initial="1", sm="2", md="2", lg="3"
                ),
                spacing="4",
                width="100%",
                align_items="stretch",
            ),
            width="100%",
            align="center",
        ),
        max_width=ANCHO_MAXIMO,
        margin="0 auto",
        padding=f"3rem {PADDING_LATERAL}",
        width="100%",
    )


# ======================================================================
# Niveles de beca
# ======================================================================


def _tarjeta_nivel(
    nivel: dict,
    destacado: bool = False,
) -> rx.Component:
    """Tarjeta de nivel de beca."""
    color_scheme = nivel["color"]

    return rx.box(
        rx.vstack(
            # --- Badge de puntaje ---
            rx.flex(
                rx.text(
                    nivel["puntos"],
                    font_size="0.6875rem",
                    font_weight="700",
                    color=rx.color(color_scheme, 11),
                    letter_spacing="0.05em",
                    text_transform="uppercase",
                ),
                padding="0.25rem 0.625rem",
                border_radius=RADIO_PASTILLA,
                background=rx.color(color_scheme, 3),
                border=f"1px solid {rx.color(color_scheme, 7)}",
                width="fit-content",
            ),
            # --- Icono grande ---
            rx.flex(
                rx.icon(
                    nivel["icono"],
                    size=28,
                    color=rx.color(color_scheme, 11),
                ),
                height="3.5rem",
                width="3.5rem",
                border_radius=RADIO_EXTRA_GRANDE,
                background=rx.color(color_scheme, 3),
                border=f"2px solid {rx.color(color_scheme, 7)}",
                align="center",
                justify="center",
                margin_top="0.5rem",
            ),
            # --- Título ---
            rx.text(
                nivel["titulo"],
                font_size="1.125rem",
                font_weight="900",
                color=COLOR_TEXTO_PRINCIPAL,
                text_align="center",
                line_height="1.2",
            ),
            # --- Porcentaje grande ---
            rx.flex(
                rx.text(
                    nivel["porcentaje"],
                    font_size="3rem",
                    font_weight="900",
                    color=rx.color(color_scheme, 11),
                    line_height="1",
                    letter_spacing="-0.03em",
                ),
                align="center",
                justify="center",
            ),
            rx.text(
                "de la mensualidad",
                font_size="0.75rem",
                font_weight="600",
                color=COLOR_TEXTO_SECUNDARIO,
                text_transform="uppercase",
                letter_spacing="0.05em",
            ),
            # --- Descripción ---
            rx.text(
                nivel["descripcion"],
                font_size="0.8125rem",
                color=COLOR_TEXTO_CUERPO,
                line_height="1.6",
                text_align="center",
                margin_top="0.5rem",
            ),
            align="center",
            spacing="2",
            width="100%",
            height="100%",
        ),
        padding="2rem 1.5rem",
        border_radius=RADIO_EXTRA_GRANDE,
        background=COLOR_FONDO_CARTA,
        border=rx.cond(
            destacado,
            f"2px solid {rx.color(color_scheme, 9)}",
            f"1px solid {COLOR_BORDE_SUAVE}",
        ),
        width="100%",
        height="100%",
        transition="all 0.3s",
        position="relative",
        _hover={
            "transform": "translateY(-6px)",
            "border_color": rx.color(color_scheme, 9),
            "box_shadow": f"0 16px 40px -10px {rx.color(color_scheme, 9)}",
        },
    )


def _seccion_niveles() -> rx.Component:
    """Sección con los 3 niveles de beca."""
    return rx.box(
        rx.vstack(
            rx.vstack(
                rx.text(
                    "NIVELES DE BECA",
                    font_size="0.75rem",
                    font_weight="700",
                    letter_spacing="0.15em",
                    color=COLOR_ACENTO_TEXTO,
                ),
                rx.heading(
                    "Según tu puntaje de innovación",
                    size="7",
                    font_weight="800",
                    color=COLOR_TEXTO_PRINCIPAL,
                    text_align="center",
                    letter_spacing="-0.03em",
                ),
                rx.text(
                    "A mayor puntaje, mayor porcentaje de beca. Todos "
                    "los niveles se aplican al siguiente semestre.",
                    font_size="0.9375rem",
                    color=COLOR_TEXTO_SECUNDARIO,
                    text_align="center",
                    max_width="42rem",
                ),
                align="center",
                spacing="2",
                margin_bottom="2.5rem",
            ),
            rx.grid(
                _tarjeta_nivel(NIVELES_BECA[0]),
                _tarjeta_nivel(NIVELES_BECA[1]),
                _tarjeta_nivel(NIVELES_BECA[2], destacado=True),
                columns=rx.breakpoints(initial="1", md="3"),
                spacing="4",
                width="100%",
                align_items="stretch",
            ),
            width="100%",
            align="center",
        ),
        max_width=ANCHO_MAXIMO,
        margin="0 auto",
        padding=f"3rem {PADDING_LATERAL}",
        width="100%",
    )


# ======================================================================
# Requisitos
# ======================================================================


def _item_requisito(item: dict) -> rx.Component:
    """Item individual de requisito."""
    return rx.flex(
        rx.flex(
            rx.icon(
                item["icono"],
                size=16,
                color=COLOR_ACENTO_TEXTO,
            ),
            height="2rem",
            width="2rem",
            border_radius=RADIO_MEDIO,
            background=COLOR_ACENTO_FONDO,
            border=f"1px solid {COLOR_ACENTO_TEXTO}",
            align="center",
            justify="center",
            flex_shrink="0",
        ),
        rx.text(
            item["texto"],
            font_size="0.875rem",
            color=COLOR_TEXTO_CUERPO,
            line_height="1.5",
            flex="1",
        ),
        align="center",
        gap="0.875rem",
        width="100%",
        padding="0.875rem 1rem",
        border_radius=RADIO_MEDIO,
        background=COLOR_FONDO_SUAVE,
        border=f"1px solid {COLOR_BORDE_SUAVE}",
        transition="all 0.2s",
        _hover={
            "border_color": COLOR_ACENTO_TEXTO,
            "transform": "translateX(4px)",
        },
    )


def _seccion_requisitos() -> rx.Component:
    """Sección con los requisitos para participar."""
    return rx.box(
        rx.vstack(
            rx.vstack(
                rx.text(
                    "REQUISITOS",
                    font_size="0.75rem",
                    font_weight="700",
                    letter_spacing="0.15em",
                    color=COLOR_ACENTO_TEXTO,
                ),
                rx.heading(
                    "Para participar en la feria",
                    size="7",
                    font_weight="800",
                    color=COLOR_TEXTO_PRINCIPAL,
                    text_align="center",
                    letter_spacing="-0.03em",
                ),
                rx.text(
                    "Cumpliendo estos requisitos, cualquier estudiante "
                    "activo puede competir por una beca.",
                    font_size="0.9375rem",
                    color=COLOR_TEXTO_SECUNDARIO,
                    text_align="center",
                    max_width="42rem",
                ),
                align="center",
                spacing="2",
                margin_bottom="2rem",
            ),
            rx.vstack(
                *[_item_requisito(item) for item in REQUISITOS_BECA],
                spacing="2",
                width="100%",
                max_width="48rem",
                margin="0 auto",
            ),
            width="100%",
            align="center",
        ),
        max_width=ANCHO_MAXIMO,
        margin="0 auto",
        padding=f"3rem {PADDING_LATERAL}",
        width="100%",
    )


# ======================================================================
# Proyectos ganadores
# ======================================================================


def _tarjeta_ganador(proyecto: dict) -> rx.Component:
    """Tarjeta de proyecto ganador."""
    color_scheme = proyecto["color"]

    return rx.box(
        rx.vstack(
            # --- Año + puntaje ---
            rx.flex(
                rx.flex(
                    rx.text(
                        proyecto["anio"],
                        font_size="0.6875rem",
                        font_weight="700",
                        color=rx.color(color_scheme, 11),
                        letter_spacing="0.05em",
                    ),
                    padding="0.25rem 0.625rem",
                    border_radius=RADIO_PASTILLA,
                    background=rx.color(color_scheme, 3),
                    border=f"1px solid {rx.color(color_scheme, 7)}",
                    width="fit-content",
                ),
                rx.flex(
                    rx.icon(
                        "star",
                        size=12,
                        color=rx.color("amber", 9),
                        fill=rx.color("amber", 9),
                    ),
                    rx.text(
                        f"{proyecto['puntaje']} pts",
                        font_size="0.6875rem",
                        font_weight="700",
                        color=rx.color(color_scheme, 11),
                    ),
                    align="center",
                    gap="0.25rem",
                    padding="0.25rem 0.625rem",
                    border_radius=RADIO_PASTILLA,
                    background=rx.color(color_scheme, 3),
                    border=f"1px solid {rx.color(color_scheme, 7)}",
                    width="fit-content",
                ),
                gap="0.5rem",
                flex_wrap="wrap",
                margin_bottom="0.75rem",
            ),
            # --- Título ---
            rx.text(
                proyecto["titulo"],
                font_size="1rem",
                font_weight="800",
                color=COLOR_TEXTO_PRINCIPAL,
                line_height="1.3",
            ),
            # --- Equipo ---
            rx.text(
                proyecto["equipo"],
                font_size="0.75rem",
                font_weight="600",
                color=COLOR_TEXTO_SECUNDARIO,
                text_transform="uppercase",
                letter_spacing="0.05em",
            ),
            # --- Descripción ---
            rx.text(
                proyecto["descripcion"],
                font_size="0.875rem",
                color=COLOR_TEXTO_CUERPO,
                line_height="1.6",
                margin_top="0.5rem",
            ),
            # --- Badge de beca ---
            rx.flex(
                rx.icon("trophy", size=12, color=rx.color("amber", 11)),
                rx.text(
                    proyecto["beca"],
                    font_size="0.6875rem",
                    font_weight="700",
                    color=rx.color("amber", 11),
                    text_transform="uppercase",
                    letter_spacing="0.05em",
                ),
                align="center",
                gap="0.375rem",
                padding="0.375rem 0.75rem",
                border_radius=RADIO_PASTILLA,
                background=rx.color("amber", 3),
                border=f"1px solid {rx.color('amber', 7)}",
                width="fit-content",
                margin_top="0.5rem",
            ),
            align="start",
            spacing="1",
            width="100%",
            height="100%",
        ),
        padding="1.5rem",
        border_radius=RADIO_EXTRA_GRANDE,
        border=f"1px solid {COLOR_BORDE_SUAVE}",
        background=COLOR_FONDO_CARTA,
        width="100%",
        height="100%",
        transition="all 0.2s",
        _hover={
            "transform": "translateY(-4px)",
            "border_color": rx.color(color_scheme, 7),
            "box_shadow": f"0 12px 32px -8px {rx.color(color_scheme, 9)}",
        },
    )


def _seccion_ganadores() -> rx.Component:
    """Sección con proyectos ganadores destacados."""
    return rx.box(
        rx.vstack(
            rx.vstack(
                rx.text(
                    "PROYECTOS GANADORES",
                    font_size="0.75rem",
                    font_weight="700",
                    letter_spacing="0.15em",
                    color=COLOR_ACENTO_TEXTO,
                ),
                rx.heading(
                    "Ejemplos que ya ganaron beca",
                    size="7",
                    font_weight="800",
                    color=COLOR_TEXTO_PRINCIPAL,
                    text_align="center",
                    letter_spacing="-0.03em",
                ),
                rx.text(
                    "Algunos de los proyectos destacados en ferias "
                    "anteriores. ¿Será el tuyo el próximo?",
                    font_size="0.9375rem",
                    color=COLOR_TEXTO_SECUNDARIO,
                    text_align="center",
                    max_width="42rem",
                ),
                align="center",
                spacing="2",
                margin_bottom="2rem",
            ),
            rx.grid(
                *[_tarjeta_ganador(p) for p in PROYECTOS_GANADORES],
                columns=rx.breakpoints(initial="1", md="2", lg="3"),
                spacing="4",
                width="100%",
                align_items="stretch",
            ),
            width="100%",
            align="center",
        ),
        max_width=ANCHO_MAXIMO,
        margin="0 auto",
        padding=f"3rem {PADDING_LATERAL}",
        width="100%",
    )


# ======================================================================
# Preguntas frecuentes (delegadas al acordeón unificado)
# ======================================================================


def _seccion_faq() -> rx.Component:
    """
    Sección de preguntas frecuentes del programa.

    ✅ REFACTORIZADO: usa el componente genérico `acordeon_faq` con
    variante `"light"`. El estado del acordeón vive en
    `EstadoAcordeonFaq` (compartido por toda la app).

    Estructura:
    1. Encabezado con etiqueta + título + subtítulo.
    2. Acordeón con las preguntas del programa.
    """
    return rx.box(
        rx.vstack(
            # --- Encabezado ---
            rx.vstack(
                rx.text(
                    "PREGUNTAS FRECUENTES",
                    font_size="0.75rem",
                    font_weight="700",
                    letter_spacing="0.15em",
                    color=COLOR_ACENTO_TEXTO,
                ),
                rx.heading(
                    "Dudas sobre las becas",
                    size="7",
                    font_weight="800",
                    color=COLOR_TEXTO_PRINCIPAL,
                    text_align="center",
                    letter_spacing="-0.03em",
                ),
                rx.text(
                    "Todo lo que necesitas saber antes de participar.",
                    font_size="0.9375rem",
                    color=COLOR_TEXTO_SECUNDARIO,
                    text_align="center",
                    max_width="42rem",
                ),
                align="center",
                spacing="2",
                margin_bottom="2rem",
            ),
            # --- Acordeón unificado ---
            acordeon_faq(
                items=PREGUNTAS_BECA,
                variante="light",
                icono="help-circle",
                color_acento=COLOR_ACENTO_TEXTO,
            ),
            width="100%",
            align="center",
        ),
        max_width=ANCHO_CONTENIDO,
        margin="0 auto",
        padding=f"3rem {PADDING_LATERAL}",
        width="100%",
    )


# ======================================================================
# CTA final
# ======================================================================


def _cta_becas() -> rx.Component:
    """Bloque CTA final."""
    return rx.box(
        rx.vstack(
            rx.flex(
                rx.icon("trophy", size=14, color=COLOR_ACENTO_TEXTO),
                rx.text(
                    "PRÓXIMA FERIA DE INNOVACIÓN",
                    font_size="0.6875rem",
                    font_weight="700",
                    color=COLOR_ACENTO_TEXTO,
                    letter_spacing="0.1em",
                ),
                align="center",
                gap="0.5rem",
                margin_bottom="1rem",
            ),
            rx.heading(
                "¿Tienes una idea innovadora?",
                size="7",
                font_weight="900",
                color=COLOR_TEXTO_PRINCIPAL,
                text_align="center",
                letter_spacing="-0.03em",
            ),
            rx.text(
                "Consulta las fechas de la próxima feria interna y "
                "comienza a preparar tu proyecto. Te apoyamos con "
                "mentores y recursos.",
                font_size="1rem",
                color=COLOR_TEXTO_CUERPO,
                text_align="center",
                max_width="42rem",
                line_height="1.6",
                margin_top="0.5rem",
            ),
            rx.flex(
                rx.link(
                    rx.icon("message-circle", size=18),
                    rx.text(
                        "Consultar por WhatsApp",
                        as_="span",
                        font_weight="700",
                    ),
                    href="/contacto",
                    text_decoration="none",
                    display="inline-flex",
                    align_items="center",
                    gap="0.5rem",
                    background=COLOR_ACENTO_SOLIDO,
                    color="white",
                    padding="1rem 2rem",
                    border_radius=RADIO_PASTILLA,
                    font_size="1rem",
                    box_shadow=(
                        f"0 10px 25px -5px {COLOR_ACENTO_SOLIDO}"
                    ),
                    transition="all 0.2s",
                    _hover={
                        "transform": "translateY(-2px)",
                        "filter": "brightness(1.1)",
                    },
                ),
                rx.link(
                    rx.icon("calendar-check", size=18),
                    rx.text(
                        "Ver calendario",
                        as_="span",
                        font_weight="600",
                    ),
                    href="/calendario",
                    text_decoration="none",
                    display="inline-flex",
                    align_items="center",
                    gap="0.5rem",
                    background="transparent",
                    color=COLOR_TEXTO_PRINCIPAL,
                    padding="1rem 2rem",
                    border_radius=RADIO_PASTILLA,
                    font_size="1rem",
                    border=f"1px solid {COLOR_BORDE_SUAVE}",
                    transition="all 0.2s",
                    _hover={
                        "transform": "translateY(-2px)",
                        "border_color": COLOR_ACENTO_TEXTO,
                    },
                ),
                gap="0.75rem",
                flex_direction=rx.breakpoints(initial="column", sm="row"),
                align="center",
                justify="center",
                margin_top="1.5rem",
            ),
            align="center",
            spacing="2",
        ),
        max_width=ANCHO_MAXIMO,
        margin="0 auto",
        padding=f"4rem {PADDING_LATERAL} 5rem {PADDING_LATERAL}",
        width="100%",
    )


# ======================================================================
# Vista completa
# ======================================================================


@rx.page(
    route="/becas",
    title=f"Becas y Reconocimientos | {NOMBRE_INSTITUTO}",
)
def vista_becas() -> rx.Component:
    """
    Página del programa de becas y reconocimientos del instituto.

    Aclaración importante: NO hay becas generales ni descuentos
    comerciales. El único programa de becas es el de innovación,
    que se gana en las ferias internas.
    """
    return rx.vstack(
        barra_navegacion_superior(),
        _hero_becas(),
        _grid_bases(),
        _seccion_proceso(),
        _seccion_areas(),
        _seccion_niveles(),
        _seccion_requisitos(),
        _seccion_ganadores(),
        _seccion_faq(),
        _cta_becas(),
        pie_pagina_institucional(),
        align="center",
        min_height="100vh",
        width="100%",
        spacing="0",
    )


__all__ = ["vista_becas"]