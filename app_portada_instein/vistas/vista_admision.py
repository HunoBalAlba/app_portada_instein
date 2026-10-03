"""
Vista "Guía de Admisión" (ruta "/admision").

Contenido:
- Hero con badge "Inscripciones abiertas todo el año".
- Grid de 3 tarjetas destacadas (sin fechas, sin sorteo, proceso rápido).
- Proceso de admisión paso a paso (timeline de 5 pasos).
- Requisitos: documentos + académicos.
- Grid de beneficios del instituto.
- Formas de inscripción (presencial, WhatsApp, online).
- Preguntas frecuentes de admisión (acordeón).
- CTA final hacia /contacto.

Sistema de color (UX)
---------------------
- Acentos institucionales: accent crimson.
- Pasos del proceso: azul (secuenciales).
- Requisitos: violeta (documentales).
- Formas de inscripción: colores semánticos distintos (verde, verde
  WhatsApp, azul).
- Textos: neutros (`gray-11`/`gray-12`).

Nota técnica: ACORDEÓN FAQ UNIFICADO
------------------------------------
✅ REFACTORIZADO: la sección de preguntas frecuentes ya NO tiene su
propio `EstadoFAQAdmision` ni su propio item. Ahora delega en el
componente genérico `acordeon_faq` con variante `"light"`, que usa
el `EstadoAcordeonFaq` global.

Esto elimina ~60 líneas de código duplicado.

Nota técnica: `ItemFaq` ES `TypedDict`
--------------------------------------
`PREGUNTAS_ADMISION` ahora es `list[ItemFaq]` (TypedDict), no
`list[dict]`. Los items se construyen con **dicts literales**:

    {"pregunta": "¿...?", "respuesta": "..."}

NO con `ItemFaq(pregunta=..., respuesta=...)`.

Nota técnica: LAYOUT
--------------------
- Los tokens de color son `Var` reactivos, no strings. Usar SIEMPRE
  f-strings para concatenar con texto.
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
    EMAIL_CONTACTO,
    NOMBRE_INSTITUTO,
    RADIO_EXTRA_GRANDE,
    RADIO_GRANDE,
    RADIO_MEDIO,
    RADIO_PASTILLA,
    TELEFONO_PRINCIPAL,
    WHATSAPP_URL,
)


# ======================================================================
# Constantes locales
# ======================================================================

ANCHO_MAXIMO = "72rem"
ANCHO_CONTENIDO = "64rem"
PADDING_LATERAL = "1.5rem"


# ======================================================================
# Datos: ventajas destacadas (3 tarjetas del hero)
# ======================================================================

VENTAJAS_DESTACADAS: list[dict] = [
    {
        "icono": "calendar-check",
        "titulo": "Sin fechas límite",
        "descripcion": (
            "Inscripciones abiertas todo el año. No pierdas tu cupo "
            "porque se te pasó una fecha."
        ),
        "color": "green",
    },
    {
        "icono": "shield-check",
        "titulo": "Sin sorteo aleatorio",
        "descripcion": (
            "Los cupos se asignan por orden de inscripción. Tu esfuerzo "
            "y decisión son lo único que importa."
        ),
        "color": "blue",
    },
    {
        "icono": "zap",
        "titulo": "Proceso en 24 horas",
        "descripcion": (
            "Desde que te inscribes hasta que empiezas clases puede "
            "pasar menos de un día."
        ),
        "color": "amber",
    },
]


# ======================================================================
# Datos: pasos del proceso de admisión
# ======================================================================

PASOS_ADMISION: list[dict] = [
    {
        "numero": "01",
        "icono": "clipboard-list",
        "titulo": "Elige tu carrera",
        "descripcion": (
            "Explora las 5 carreras técnicas disponibles y elige la que "
            "mejor se alinee con tus metas profesionales."
        ),
    },
    {
        "numero": "02",
        "icono": "file-text",
        "titulo": "Reúne los documentos",
        "descripcion": (
            "Prepara tus documentos personales y académicos. La lista "
            "completa está en la sección de requisitos."
        ),
    },
    {
        "numero": "03",
        "icono": "message-circle",
        "titulo": "Contáctanos",
        "descripcion": (
            "Escríbenos por WhatsApp, llámanos o visítanos. Te guiaremos "
            "durante todo el proceso."
        ),
    },
    {
        "numero": "04",
        "icono": "calendar-clock",
        "titulo": "Agenda tu entrevista",
        "descripcion": (
            "Coordinamos una entrevista breve (15-20 minutos) para "
            "conocerte y resolver todas tus dudas."
        ),
    },
    {
        "numero": "05",
        "icono": "graduation-cap",
        "titulo": "¡Inicia tus clases!",
        "descripcion": (
            "Una vez confirmada tu inscripción, te damos la bienvenida "
            "y comienzas el siguiente lunes disponible."
        ),
    },
]


# ======================================================================
# Datos: requisitos
# ======================================================================

REQUISITOS_DOCUMENTOS: list[dict] = [
    {
        "icono": "file-text",
        "texto": "Fotocopia del diploma de bachiller",
    },
    {
        "icono": "id-card",
        "texto": "Fotocopia del carnet de identidad (ambas caras)",
    },
    {
        "icono": "image",
        "texto": "2 fotografías tamaño carnet (fondo rojo)",
    },
    {
        "icono": "file-signature",
        "texto": "Formulario de inscripción (te lo damos nosotros)",
    },
    {
        "icono": "receipt",
        "texto": "Comprobante de pago de matrícula",
    },
]

REQUISITOS_ACADEMICOS: list[dict] = [
    {
        "icono": "graduation-cap",
        "texto": "Haber concluido el bachillerato (o estar por concluir)",
    },
    {
        "icono": "users",
        "texto": "Ser mayor de 17 años al momento de la inscripción",
    },
    {
        "icono": "heart",
        "texto": (
            "Compromiso con la formación técnica y los valores "
            "institucionales"
        ),
    },
    {
        "icono": "target",
        "texto": "Disposición para cumplir con el plan de estudios (3 años)",
    },
    {
        "icono": "languages",
        "texto": "Conocimientos básicos de lectoescritura y matemática",
    },
]


# ======================================================================
# Datos: beneficios de elegir INSTEIN
# ======================================================================

BENEFICIOS: list[dict] = [
    {
        "icono": "award",
        "titulo": "Título Nacional",
        "descripcion": "Validez oficial con R.M. 0871/2016",
        "color": "blue",
    },
    {
        "icono": "briefcase",
        "titulo": "Formación práctica",
        "descripcion": "Laboratorios y docentes especializados",
        "color": "cyan",
    },
    {
        "icono": "trending-up",
        "titulo": "100% empleabilidad",
        "descripcion": "Egresados trabajando en su área",
        "color": "violet",
    },
    {
        "icono": "building-2",
        "titulo": "Convenios con empresas",
        "descripcion": "Más de 15 aliados en la industria",
        "color": "orange",
    },
    {
        "icono": "book-open",
        "titulo": "Formación integral",
        "descripcion": "Habilidades técnicas + blandas",
        "color": "green",
    },
    {
        "icono": "users",
        "titulo": "Comunidad activa",
        "descripcion": "Red de 500+ egresados conectados",
        "color": "pink",
    },
    {
        "icono": "wallet",
        "titulo": "Planes de pago",
        "descripcion": "Mensualidades accesibles y becas",
        "color": "amber",
    },
]


# ======================================================================
# Datos: formas de inscripción
# ======================================================================

FORMAS_INSCRIPCION: list[dict] = [
    {
        "icono": "map-pin",
        "titulo": "Presencial",
        "subtitulo": "Visítanos en el campus",
        "descripcion": (
            "Galería FLOR DE ORO, 1er piso. Calle Jorge Carrasco entre "
            "3 y 4."
        ),
        "cta_texto": "Ver ubicación",
        "cta_url": "/contacto",
        "externo": False,
        "color": "blue",
    },
    {
        "icono": "message-circle",
        "titulo": "WhatsApp",
        "subtitulo": "La forma más rápida",
        "descripcion": (
            f"Escríbenos al {TELEFONO_PRINCIPAL}. Te respondemos en "
            f"minutos."
        ),
        "cta_texto": "Abrir WhatsApp",
        "cta_url": WHATSAPP_URL,
        "externo": True,
        "color": "green",
    },
    {
        "icono": "mail",
        "titulo": "Correo electrónico",
        "subtitulo": "Para consultas formales",
        "descripcion": (
            f"Escríbenos a {EMAIL_CONTACTO} y te enviamos toda la "
            f"información."
        ),
        "cta_texto": "Enviar correo",
        "cta_url": f"mailto:{EMAIL_CONTACTO}",
        "externo": True,
        "color": "violet",
    },
]


# ======================================================================
# Datos: preguntas frecuentes de admisión
# ======================================================================
# ✅ Ahora es `list[ItemFaq]` (TypedDict) en lugar de `list[dict]`.
# Se construye con dicts literales:
#     {"pregunta": "...", "respuesta": "..."}
# ----------------------------------------------------------------------

PREGUNTAS_ADMISION: list[ItemFaq] = [
    {
        "pregunta": "¿Realmente puedo inscribirme en cualquier momento?",
        "respuesta": (
            "Sí. Como instituto privado, no tenemos fechas límite de "
            "inscripción. Puedes iniciar tu proceso cualquier día del "
            "año y comenzar clases el siguiente lunes disponible."
        ),
    },
    {
        "pregunta": "¿Hay examen de admisión?",
        "respuesta": (
            "No hay examen de admisión. Solo coordinamos una entrevista "
            "breve para conocerte, entender tus metas y asegurarnos de "
            "que la carrera elegida sea la adecuada para ti."
        ),
    },
    {
        "pregunta": "¿Los cupos son limitados?",
        "respuesta": (
            "Cada carrera tiene un cupo máximo por turno para garantizar "
            "la calidad educativa. Por eso recomendamos inscribirse lo "
            "antes posible. Los cupos se asignan por orden de "
            "inscripción."
        ),
    },
    {
        "pregunta": "¿Cuánto cuesta estudiar en INSTEIN?",
        "respuesta": (
            "Ofrecemos planes de pago accesibles con mensualidades "
            "cómodas. Escríbenos por WhatsApp para recibir el detalle "
            "de costos de tu carrera específica."
        ),
    },
    {
        "pregunta": "¿Hay becas o descuentos disponibles?",
        "respuesta": (
            "Sí. Contamos con becas por mérito académico, descuentos "
            "por pago anual adelantado y convenios con empresas. "
            "Consulta con admisiones los detalles."
        ),
    },
    {
        "pregunta": "¿Puedo visitar el campus antes de inscribirme?",
        "respuesta": (
            "Por supuesto. Te invitamos a conocer nuestras "
            "instalaciones, laboratorios y aulas. Coordina tu visita "
            "por WhatsApp o teléfono."
        ),
    },
    {
        "pregunta": "¿Qué pasa si no tengo todos los documentos?",
        "respuesta": (
            "No te preocupes. Puedes iniciar el proceso con lo que "
            "tengas y completar la documentación en los primeros días "
            "de clases."
        ),
    },
    {
        "pregunta": "¿Puedo trabajar mientras estudio?",
        "respuesta": (
            "Sí. Todas las carreras tienen turno nocturno (19:00 - "
            "22:00) y turno de sábados (09:00 - 14:30) especialmente "
            "diseñados para estudiantes que trabajan."
        ),
    },
]


# ======================================================================
# HERO
# ======================================================================


def _hero_admision() -> rx.Component:
    """Hero con badge + título + subtítulo."""
    return rx.vstack(
        # --- Badge ---
        rx.flex(
            rx.box(
                height="0.5rem",
                width="0.5rem",
                border_radius=RADIO_PASTILLA,
                background=rx.color("green", 9),
                animation="pulse 2s ease-in-out infinite",
            ),
            rx.text(
                "INSCRIPCIONES ABIERTAS TODO EL AÑO",
                font_size="0.75rem",
                font_weight="700",
                color=COLOR_TEXTO_PRINCIPAL,
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
            "Guía de ",
            rx.text.span(
                "Admisión",
                color=COLOR_ACENTO_TEXTO,
            ),
            "",
            size="9",
            font_weight="900",
            color=COLOR_TEXTO_PRINCIPAL,
            text_align="center",
            letter_spacing="-0.03em",
            line_height="1.1",
        ),
        # --- Subtítulo ---
        rx.text(
            "Todo lo que necesitas saber para convertirte en Técnico "
            "Superior. Sin fechas límite, sin sorteo, sin "
            "complicaciones.",
            font_size="1rem",
            color=COLOR_TEXTO_CUERPO,
            text_align="center",
            max_width="48rem",
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
# Ventajas destacadas
# ======================================================================


def _tarjeta_ventaja(item: dict) -> rx.Component:
    """Tarjeta de ventaja destacada."""
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
            "box_shadow": (
                f"0 12px 32px -8px {rx.color(color_scheme, 9)}"
            ),
        },
    )


def _grid_ventajas() -> rx.Component:
    """Grid con las 3 tarjetas de ventajas destacadas."""
    return rx.box(
        rx.grid(
            *[_tarjeta_ventaja(item) for item in VENTAJAS_DESTACADAS],
            columns=rx.breakpoints(
                initial="1", sm="1", md="3", lg="3"
            ),
            spacing="4",
            width="100%",
        ),
        max_width=ANCHO_MAXIMO,
        margin="0 auto",
        padding=f"0 {PADDING_LATERAL} 4rem {PADDING_LATERAL}",
        width="100%",
    )


# ======================================================================
# Proceso de admisión (timeline)
# ======================================================================


def _paso_timeline(
    paso: dict,
    indice: int,
    total: int,
) -> rx.Component:
    """Paso individual del timeline de admisión."""
    es_ultimo = indice == total - 1

    return rx.flex(
        # --- Indicador (círculo con número + línea) ---
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
                # Icono del paso
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
                # Título + descripción
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
                "box_shadow": (
                    f"0 8px 20px -8px {COLOR_ACENTO_SOLIDO}"
                ),
            },
        ),
        align="start",
        gap="1rem",
        width="100%",
    )


def _seccion_proceso() -> rx.Component:
    """Sección del proceso de admisión paso a paso."""
    total = len(PASOS_ADMISION)

    return rx.box(
        rx.vstack(
            # --- Encabezado ---
            rx.vstack(
                rx.text(
                    "PROCESO DE ADMISIÓN",
                    font_size="0.75rem",
                    font_weight="700",
                    letter_spacing="0.15em",
                    color=COLOR_ACENTO_TEXTO,
                ),
                rx.heading(
                    "Inscríbete en 5 pasos",
                    size="7",
                    font_weight="800",
                    color=COLOR_TEXTO_PRINCIPAL,
                    text_align="center",
                    letter_spacing="-0.03em",
                ),
                rx.text(
                    "Un proceso simple y rápido. Sin exámenes de "
                    "admisión, sin sorteos, sin complicaciones.",
                    font_size="0.9375rem",
                    color=COLOR_TEXTO_SECUNDARIO,
                    text_align="center",
                    max_width="42rem",
                ),
                align="center",
                spacing="2",
                margin_bottom="3rem",
            ),
            # --- Timeline de pasos ---
            rx.vstack(
                *[
                    _paso_timeline(paso, i, total)
                    for i, paso in enumerate(PASOS_ADMISION)
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
# Requisitos
# ======================================================================


def _tarjeta_requisito(item: dict) -> rx.Component:
    """Item individual de requisito."""
    return rx.flex(
        rx.flex(
            rx.icon(
                item["icono"],
                size=16,
                color=rx.color("violet", 11),
            ),
            height="2rem",
            width="2rem",
            border_radius=RADIO_MEDIO,
            background=rx.color("violet", 3),
            border=f"1px solid {rx.color('violet', 7)}",
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
            "border_color": rx.color("violet", 7),
            "transform": "translateX(4px)",
        },
    )


def _columna_requisitos(
    titulo: str,
    icono: str,
    items: list[dict],
) -> rx.Component:
    """Columna de requisitos (documentos o académicos)."""
    return rx.box(
        rx.vstack(
            # --- Encabezado de la columna ---
            rx.flex(
                rx.flex(
                    rx.icon(
                        icono,
                        size=18,
                        color=rx.color("violet", 11),
                    ),
                    height="2.25rem",
                    width="2.25rem",
                    border_radius=RADIO_MEDIO,
                    background=rx.color("violet", 3),
                    border=f"1px solid {rx.color('violet', 7)}",
                    align="center",
                    justify="center",
                    flex_shrink="0",
                ),
                rx.text(
                    titulo,
                    font_size="1rem",
                    font_weight="700",
                    color=COLOR_TEXTO_PRINCIPAL,
                ),
                align="center",
                gap="0.75rem",
                margin_bottom="1rem",
            ),
            # --- Lista de items ---
            rx.vstack(
                *[_tarjeta_requisito(item) for item in items],
                spacing="2",
                width="100%",
            ),
            align="start",
            spacing="2",
            width="100%",
        ),
        padding="1.5rem",
        border_radius=RADIO_EXTRA_GRANDE,
        background=COLOR_FONDO_CARTA,
        border=f"1px solid {COLOR_BORDE_SUAVE}",
        width="100%",
        height="100%",
    )


def _seccion_requisitos() -> rx.Component:
    """Sección con los requisitos de admisión."""
    return rx.box(
        rx.vstack(
            # --- Encabezado ---
            rx.vstack(
                rx.text(
                    "REQUISITOS",
                    font_size="0.75rem",
                    font_weight="700",
                    letter_spacing="0.15em",
                    color=COLOR_ACENTO_TEXTO,
                ),
                rx.heading(
                    "Lo que necesitas para inscribirte",
                    size="7",
                    font_weight="800",
                    color=COLOR_TEXTO_PRINCIPAL,
                    text_align="center",
                    letter_spacing="-0.03em",
                ),
                rx.text(
                    "Documentos personales y académicos. Si te falta "
                    "algo, contáctanos y te ayudamos a resolverlo.",
                    font_size="0.9375rem",
                    color=COLOR_TEXTO_SECUNDARIO,
                    text_align="center",
                    max_width="42rem",
                ),
                align="center",
                spacing="2",
                margin_bottom="2rem",
            ),
            # --- Grid de 2 columnas ---
            rx.grid(
                _columna_requisitos(
                    "Documentos personales",
                    "file-text",
                    REQUISITOS_DOCUMENTOS,
                ),
                _columna_requisitos(
                    "Requisitos académicos",
                    "graduation-cap",
                    REQUISITOS_ACADEMICOS,
                ),
                columns=rx.breakpoints(initial="1", md="2"),
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
# Beneficios
# ======================================================================


def _tarjeta_beneficio(item: dict) -> rx.Component:
    """Tarjeta individual de beneficio."""
    color_scheme = item["color"]

    return rx.box(
        rx.vstack(
            rx.flex(
                rx.icon(
                    item["icono"],
                    size=20,
                    color=rx.color(color_scheme, 11),
                ),
                height="2.25rem",
                width="2.25rem",
                border_radius=RADIO_MEDIO,
                background=rx.color(color_scheme, 3),
                border=f"1px solid {rx.color(color_scheme, 7)}",
                align="center",
                justify="center",
                margin_bottom="0.75rem",
            ),
            rx.text(
                item["titulo"],
                font_size="0.875rem",
                font_weight="700",
                color=COLOR_TEXTO_PRINCIPAL,
                line_height="1.3",
            ),
            rx.text(
                item["descripcion"],
                font_size="0.75rem",
                color=COLOR_TEXTO_SECUNDARIO,
                line_height="1.5",
            ),
            align="start",
            spacing="1",
            width="100%",
        ),
        padding="1.25rem",
        border_radius=RADIO_EXTRA_GRANDE,
        background=COLOR_FONDO_CARTA,
        border=f"1px solid {COLOR_BORDE_SUAVE}",
        width="100%",
        height="100%",
        transition="all 0.2s",
        _hover={
            "transform": "translateY(-4px)",
            "border_color": rx.color(color_scheme, 7),
            "box_shadow": (
                f"0 12px 32px -8px {rx.color(color_scheme, 9)}"
            ),
        },
    )


def _seccion_beneficios() -> rx.Component:
    """Sección con los beneficios de elegir INSTEIN."""
    return rx.box(
        rx.vstack(
            # --- Encabezado ---
            rx.vstack(
                rx.text(
                    "¿POR QUÉ ELEGIRNOS?",
                    font_size="0.75rem",
                    font_weight="700",
                    letter_spacing="0.15em",
                    color=COLOR_ACENTO_TEXTO,
                ),
                rx.heading(
                    "Razones para estudiar en INSTEIN",
                    size="7",
                    font_weight="800",
                    color=COLOR_TEXTO_PRINCIPAL,
                    text_align="center",
                    letter_spacing="-0.03em",
                ),
                rx.text(
                    "Formación de excelencia con respaldo oficial y "
                    "proyección profesional real.",
                    font_size="0.9375rem",
                    color=COLOR_TEXTO_SECUNDARIO,
                    text_align="center",
                    max_width="42rem",
                ),
                align="center",
                spacing="2",
                margin_bottom="2rem",
            ),
            # --- Grid de beneficios ---
            rx.grid(
                *[_tarjeta_beneficio(item) for item in BENEFICIOS],
                columns=rx.breakpoints(
                    initial="1", sm="2", md="2", lg="4"
                ),
                spacing="4",
                width="100%",
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
# Formas de inscripción
# ======================================================================


def _tarjeta_forma_inscripcion(item: dict) -> rx.Component:
    """Tarjeta individual de forma de inscripción."""
    color_scheme = item["color"]

    return rx.box(
        rx.vstack(
            # --- Icono grande ---
            rx.flex(
                rx.icon(
                    item["icono"],
                    size=24,
                    color="white",
                ),
                height="3rem",
                width="3rem",
                border_radius=RADIO_GRANDE,
                background=rx.color(color_scheme, 9),
                align="center",
                justify="center",
                margin_bottom="1rem",
                box_shadow=(
                    f"0 8px 20px -6px {rx.color(color_scheme, 9)}"
                ),
            ),
            # --- Título + subtítulo ---
            rx.text(
                item["titulo"],
                font_size="1rem",
                font_weight="800",
                color=COLOR_TEXTO_PRINCIPAL,
                line_height="1.2",
            ),
            rx.text(
                item["subtitulo"],
                font_size="0.75rem",
                font_weight="600",
                color=rx.color(color_scheme, 11),
                text_transform="uppercase",
                letter_spacing="0.05em",
            ),
            # --- Descripción ---
            rx.text(
                item["descripcion"],
                font_size="0.875rem",
                color=COLOR_TEXTO_CUERPO,
                line_height="1.6",
                margin_top="0.5rem",
            ),
            # --- CTA ---
            rx.link(
                rx.text(
                    item["cta_texto"],
                    as_="span",
                    font_size="0.875rem",
                    font_weight="700",
                ),
                rx.icon("arrow-right", size=14),
                href=item["cta_url"],
                is_external=item["externo"],
                text_decoration="none",
                display="inline-flex",
                align_items="center",
                gap="0.375rem",
                margin_top="1rem",
                padding="0.625rem 1.25rem",
                border_radius=RADIO_PASTILLA,
                background=rx.color(color_scheme, 9),
                color="white",
                transition="all 0.2s",
                _hover={
                    "transform": "translateY(-2px)",
                    "filter": "brightness(1.1)",
                },
            ),
            align="start",
            spacing="1",
            width="100%",
            height="100%",
        ),
        padding="1.75rem",
        border_radius=RADIO_EXTRA_GRANDE,
        background=COLOR_FONDO_CARTA,
        border=f"1px solid {COLOR_BORDE_SUAVE}",
        width="100%",
        height="100%",
        transition="all 0.2s",
        _hover={
            "border_color": rx.color(color_scheme, 7),
        },
    )


def _seccion_formas_inscripcion() -> rx.Component:
    """Sección con las 3 formas de inscripción."""
    return rx.box(
        rx.vstack(
            # --- Encabezado ---
            rx.vstack(
                rx.text(
                    "FORMAS DE INSCRIPCIÓN",
                    font_size="0.75rem",
                    font_weight="700",
                    letter_spacing="0.15em",
                    color=COLOR_ACENTO_TEXTO,
                ),
                rx.heading(
                    "Elige cómo contactarnos",
                    size="7",
                    font_weight="800",
                    color=COLOR_TEXTO_PRINCIPAL,
                    text_align="center",
                    letter_spacing="-0.03em",
                ),
                rx.text(
                    "Tres canales para iniciar tu proceso de admisión. "
                    "Elige el que más te convenga.",
                    font_size="0.9375rem",
                    color=COLOR_TEXTO_SECUNDARIO,
                    text_align="center",
                    max_width="42rem",
                ),
                align="center",
                spacing="2",
                margin_bottom="2rem",
            ),
            # --- Grid de 3 tarjetas ---
            rx.grid(
                *[
                    _tarjeta_forma_inscripcion(item)
                    for item in FORMAS_INSCRIPCION
                ],
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
# Preguntas frecuentes (delegadas al acordeón unificado)
# ======================================================================


def _seccion_faq() -> rx.Component:
    """
    Sección de preguntas frecuentes de admisión.

    ✅ REFACTORIZADO: usa el componente genérico `acordeon_faq` con
    variante `"light"`. El estado del acordeón vive en
    `EstadoAcordeonFaq` (compartido por toda la app).

    Estructura:
    1. Encabezado con etiqueta + título + subtítulo.
    2. Acordeón con las preguntas de admisión.
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
                    "Dudas comunes sobre admisión",
                    size="7",
                    font_weight="800",
                    color=COLOR_TEXTO_PRINCIPAL,
                    text_align="center",
                    letter_spacing="-0.03em",
                ),
                rx.text(
                    "Las preguntas que más nos hacen quienes quieren "
                    "estudiar con nosotros.",
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
                items=PREGUNTAS_ADMISION,
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


def _cta_admision() -> rx.Component:
    """Bloque CTA final hacia /contacto."""
    return rx.box(
        rx.vstack(
            rx.flex(
                rx.box(
                    height="0.5rem",
                    width="0.5rem",
                    border_radius=RADIO_PASTILLA,
                    background=rx.color("green", 9),
                    animation="pulse 2s ease-in-out infinite",
                ),
                rx.text(
                    "INSCRIPCIONES ABIERTAS",
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
                "¿Listo para dar el primer paso?",
                size="7",
                font_weight="900",
                color=COLOR_TEXTO_PRINCIPAL,
                text_align="center",
                letter_spacing="-0.03em",
            ),
            rx.text(
                "Nuestro equipo de admisiones está disponible para "
                "guiarte en cada paso del proceso.",
                font_size="1rem",
                color=COLOR_TEXTO_CUERPO,
                text_align="center",
                max_width="36rem",
                line_height="1.6",
                margin_top="0.5rem",
            ),
            rx.flex(
                # --- CTA primario ---
                rx.link(
                    rx.icon("message-circle", size=18),
                    rx.text(
                        "Contactar ahora",
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
                # --- CTA secundario (WhatsApp) ---
                rx.link(
                    rx.icon("phone", size=18),
                    rx.text(
                        "Llamar: " + TELEFONO_PRINCIPAL,
                        as_="span",
                        font_weight="600",
                    ),
                    href=f"tel:+591{TELEFONO_PRINCIPAL}",
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
                flex_direction=rx.breakpoints(
                    initial="column", sm="row"
                ),
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
    route="/admision",
    title=f"Guía de Admisión | {NOMBRE_INSTITUTO}",
)
def vista_admision() -> rx.Component:
    """Página de la guía de admisión del instituto."""
    return rx.vstack(
        barra_navegacion_superior(),
        _hero_admision(),
        _grid_ventajas(),
        _seccion_proceso(),
        _seccion_requisitos(),
        _seccion_beneficios(),
        _seccion_formas_inscripcion(),
        _seccion_faq(),
        _cta_admision(),
        pie_pagina_institucional(),
        align="center",
        min_height="100vh",
        width="100%",
        spacing="0",
    )


__all__ = ["vista_admision"]