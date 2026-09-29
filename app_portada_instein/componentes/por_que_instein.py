"""
Sección "¿Por qué elegir INSTEIN?" con cards de features
estilo Qdrant: icono + título + descripción + CTA que abre un diálogo
con información ampliada.

Sistema de color (UX)
---------------------
Cada razón tiene su propio color de marca (azul, cyan, violeta, naranja,
verde, rosa) para dar variedad visual al grid. Los colores son los
mismos que los del catálogo de carreras, así que hay coherencia total.

Elementos con color de marca por razón:
- Icono.
- Fondo tintado del icono.
- Texto y borde del CTA "Ver más".
- Borde hover de la tarjeta.
- Sombra hover.
- Iconos de check en el diálogo.

Elementos neutros:
- Título de la tarjeta.
- Descripción.
- Bordes base.
- Fondo base.

Elementos con accent institucional:
- Etiqueta "¿POR QUÉ INSTEIN?".
- Botón "Más información" del diálogo.

Patrón de diálogo
-----------------
Se usa `rx.dialog.trigger` (patrón declarativo de Radix Themes) en lugar
de `on_click` manual. Cada card envuelve su propio `rx.dialog.root` con
su contenido específico. Esto evita un State global y permite tener N
diálogos independientes sin colisiones.
"""

import reflex as rx

from app_portada_instein.infraestructura.constantes_visuales import (
    COLOR_ACENTO_TEXTO,
    COLOR_BORDE_SUAVE,
    COLOR_FONDO_CARTA,
    COLOR_FONDO_SUAVE,
    COLOR_TEXTO_CUERPO,
    COLOR_TEXTO_PRINCIPAL,
    COLOR_TEXTO_SECUNDARIO,
    RADIO_EXTRA_GRANDE,
    RADIO_GRANDE,
    RADIO_MEDIO,
)


# ======================================================================
# Estructura de razones
# ======================================================================
# Cada razón incluye:
# - icono, titulo, descripcion (para la card)
# - detalle: párrafo largo mostrado en el diálogo
# - puntos: lista de beneficios concretos mostrados en el diálogo
# - color_light, color_dark: color de marca adaptativo
# ----------------------------------------------------------------------

RAZONES: list[dict] = [
    {
        "id": 0,
        "icono": "award",
        "titulo": "Título de Provisión Nacional",
        "descripcion": (
            "Todos nuestros títulos están autorizados por el Ministerio de "
            "Educación con Resolución Ministerial R.M. 0871/2016."
        ),
        "detalle": (
            "Nuestros títulos tienen validez nacional y están respaldados "
            "por resoluciones ministeriales vigentes. Al egresar, recibirás "
            "un Técnico Superior en Provisión Nacional reconocido por "
            "empleadores de todo el país."
        ),
        "puntos": [
            "Resolución Ministerial R.M. 0871/2016",
            "Registro en el sistema educativo boliviano",
            "Reconocido por empresas públicas y privadas",
            "Válido para continuar estudios universitarios",
        ],
        "color_light": "#2563eb",
        "color_dark": "#60a5fa",
    },
    {
        "id": 1,
        "icono": "briefcase",
        "titulo": "Formación Práctica",
        "descripcion": (
            "Laboratorios equipados y docentes especializados con experiencia "
            "real en el campo profesional."
        ),
        "detalle": (
            "En INSTEIN no solo estudias teoría: practicas desde el primer "
            "año con equipamiento moderno y docentes que trabajan activamente "
            "en la industria. Nuestros laboratorios replican entornos reales "
            "de trabajo."
        ),
        "puntos": [
            "Laboratorios con equipamiento de última generación",
            "Docentes en activo en la industria",
            "Proyectos prácticos desde el primer semestre",
            "Prácticas profesionales garantizadas",
        ],
        "color_light": "#0891b2",
        "color_dark": "#22d3ee",
    },
    {
        "id": 2,
        "icono": "users",
        "titulo": "Alta Empleabilidad",
        "descripcion": (
            "El 100% de nuestros egresados encuentra trabajo en su área "
            "en menos de 6 meses tras graduarse."
        ),
        "detalle": (
            "Nuestra tasa de empleabilidad es del 100%. Esto se debe a la "
            "combinación de formación práctica, convenios con empresas y "
            "una red activa de egresados que comparten oportunidades "
            "laborales."
        ),
        "puntos": [
            "100% de empleabilidad en menos de 6 meses",
            "Salario promedio superior al mercado",
            "Red de 500+ egresados activos",
            "Bolsa de trabajo institucional",
        ],
        "color_light": "#7c3aed",
        "color_dark": "#a78bfa",
    },
    {
        "id": 3,
        "icono": "building-2",
        "titulo": "Convenios Empresariales",
        "descripcion": (
            "Prácticas profesionales garantizadas en empresas líderes "
            "de la región y del país."
        ),
        "detalle": (
            "Tenemos convenios activos con más de 15 empresas líderes en "
            "sus sectores. Esto garantiza que cada estudiante realice "
            "prácticas profesionales en un entorno real antes de graduarse."
        ),
        "puntos": [
            "Más de 15 empresas aliadas",
            "Prácticas garantizadas para todos los estudiantes",
            "Convenios en Santa Cruz, La Paz y Cochabamba",
            "Posibilidad de contratación al finalizar prácticas",
        ],
        "color_light": "#ea580c",
        "color_dark": "#fb923c",
    },
    {
        "id": 4,
        "icono": "book-open",
        "titulo": "Formación Integral",
        "descripcion": (
            "Además de la técnica, desarrollamos habilidades blandas, "
            "liderazgo y pensamiento crítico."
        ),
        "detalle": (
            "Un profesional técnico completo no solo domina su área: también "
            "sabe comunicar, liderar equipos y resolver problemas. En "
            "INSTEIN formamos profesionales completos para el mundo laboral "
            "actual."
        ),
        "puntos": [
            "Talleres de liderazgo y trabajo en equipo",
            "Comunicación efectiva y oratoria",
            "Pensamiento crítico y resolución de problemas",
            "Ética profesional y responsabilidad social",
        ],
        "color_light": "#16a34a",
        "color_dark": "#4ade80",
    },
    {
        "id": 5,
        "icono": "heart",
        "titulo": "Comunidad",
        "descripcion": (
            "Una red de 500+ egresados que se apoyan mutuamente y "
            "comparten oportunidades profesionales."
        ),
        "detalle": (
            "Al egresar no estás solo: te unes a una comunidad activa de "
            "más de 500 profesionales que se apoyan mutuamente, comparten "
            "oportunidades y participan en eventos institucionales."
        ),
        "puntos": [
            "Grupo de WhatsApp y Telegram activos",
            "Eventos anuales de networking",
            "Mentorías de egresados a estudiantes actuales",
            "Bolsa de trabajo exclusiva para egresados",
        ],
        "color_light": "#db2777",
        "color_dark": "#f472b6",
    },
]


# ======================================================================
# Helpers internos
# ======================================================================


def _color_adaptativo(razon: dict) -> rx.Var:
    """Devuelve el color de la razón adaptado al color_mode."""
    return rx.color_mode_cond(
        light=razon["color_light"],
        dark=razon["color_dark"],
    )


def _fondo_tintado(razon: dict) -> rx.Var:
    """Devuelve el fondo tintado del color de la razón."""
    return rx.color_mode_cond(
        light=f"{razon['color_light']}15",
        dark=f"{razon['color_dark']}20",
    )


# ======================================================================
# Contenido del diálogo (detalle de razón)
# ======================================================================


def _contenido_dialogo_razon(razon: dict) -> rx.Component:
    """
    Contenido del diálogo: icono + título + descripción ampliada +
    lista de puntos + CTA de contacto.

    Usa `rx.inset(side="x")` para la lista de puntos, siguiendo el
    patrón de Radix Themes.

    Args:
        razon: Dict con los datos de la razón.
    """
    color_razon = _color_adaptativo(razon)

    return rx.vstack(
        # ==========================================================
        # Icono grande con fondo tintado
        # ==========================================================
        rx.box(
            rx.icon(razon["icono"], size=32, color=color_razon),
            padding="1rem",
            border_radius=RADIO_EXTRA_GRANDE,
            background=_fondo_tintado(razon),
            border=f"1px solid {color_razon}",
            display="flex",
            align_items="center",
            justify_content="center",
            width="fit-content",
        ),
        # ==========================================================
        # Descripción ampliada
        # ==========================================================
        rx.text(
            razon["detalle"],
            font_size="0.9375rem",
            line_height="1.7",
            color=COLOR_TEXTO_CUERPO,
            text_align="center",
        ),
        # ==========================================================
        # Lista de puntos clave (con rx.inset side="x")
        # ==========================================================
        rx.inset(
            rx.vstack(
                rx.foreach(
                    razon["puntos"],
                    lambda punto: rx.flex(
                        rx.icon(
                            "check-circle",
                            size=16,
                            color=color_razon,
                            flex_shrink="0",
                            margin_top="0.125rem",
                        ),
                        rx.text(
                            punto,
                            font_size="0.875rem",
                            color=COLOR_TEXTO_CUERPO,
                            line_height="1.5",
                        ),
                        align="start",
                        gap="0.625rem",
                        width="100%",
                    ),
                ),
                spacing="2",
                align="start",
                width="100%",
                padding="1rem",
                background=COLOR_FONDO_SUAVE,
                border_radius=RADIO_MEDIO,
            ),
            side="x",
            margin_top="0.5rem",
            margin_bottom="0.5rem",
        ),
        spacing="4",
        align="center",
        width="100%",
    )


# ======================================================================
# Pie del diálogo (CTA + botón cerrar)
# ======================================================================


def _pie_dialogo_razon() -> rx.Component:
    """
    Pie del diálogo con CTA "Más información" + botón "Cerrar".

    Sigue el patrón de Radix Themes:
    - `rx.dialog.close` envuelve el botón de cerrar.
    - `rx.flex(justify="end")` alinea los botones a la derecha.
    """
    return rx.flex(
        rx.dialog.close(
            rx.button(
                "Cerrar",
                variant="soft",
                color_scheme="gray",
                cursor="pointer",
            ),
        ),
        rx.dialog.close(
            rx.button(
                rx.icon("message-circle", size=16),
                rx.text("Más información", as_="span", font_weight="700"),
                on_click=rx.redirect("/contacto"),
                variant="solid",
                color_scheme="crimson",
                cursor="pointer",
            ),
        ),
        spacing="3",
        justify="end",
        width="100%",
        margin_top="0.5rem",
    )


# ======================================================================
# Diálogo por razón (envuelve la card + el contenido del diálogo)
# ======================================================================


def _tarjeta_razon_con_dialogo(razon: dict) -> rx.Component:
    """
    Envuelve la card + el diálogo en un `rx.dialog.root`.

    Estructura:
    - `rx.dialog.trigger`: la card clicable que abre el diálogo.
    - `rx.dialog.content`: el contenido del diálogo (título, detalle,
      puntos, CTA, cerrar).

    Args:
        razon: Dict con los datos de la razón.
    """
    color_razon = _color_adaptativo(razon)

    return rx.dialog.root(
        # ==========================================================
        # TRIGGER: la card clicable
        # ==========================================================
        rx.dialog.trigger(
            rx.box(
                rx.vstack(
                    # --- Icono con fondo tintado ---
                    rx.box(
                        rx.icon(razon["icono"], size=24, color=color_razon),
                        padding="0.75rem",
                        border_radius=RADIO_GRANDE,
                        background=_fondo_tintado(razon),
                        display="flex",
                        align_items="center",
                        justify_content="center",
                        width="fit-content",
                        margin_bottom="1rem",
                    ),
                    # --- Título ---
                    rx.heading(
                        razon["titulo"],
                        size="3",
                        color=COLOR_TEXTO_PRINCIPAL,
                        font_weight="700",
                    ),
                    # --- Descripción ---
                    rx.text(
                        razon["descripcion"],
                        font_size="0.875rem",
                        line_height="1.6",
                        color=COLOR_TEXTO_CUERPO,
                    ),
                    # --- CTA "Ver más →" ---
                    rx.flex(
                        rx.text(
                            "Ver más",
                            font_size="0.875rem",
                            font_weight="600",
                            color=color_razon,
                        ),
                        rx.icon("arrow-right", size=14, color=color_razon),
                        align="center",
                        gap="0.25rem",
                        margin_top="0.5rem",
                        transition="all 0.2s",
                    ),
                    align="start",
                    spacing="1",
                    width="100%",
                ),
                # --- Estilos de la card ---
                cursor="pointer",
                padding="1.5rem",
                border_radius=RADIO_EXTRA_GRANDE,
                border=f"1px solid {COLOR_BORDE_SUAVE}",
                background=COLOR_FONDO_CARTA,
                transition="all 0.3s",
                width="100%",
                height="100%",
                _hover={
                    "transform": "translateY(-4px)",
                    "border_color": color_razon,
                    "box_shadow": f"0 20px 40px -10px {color_razon}",
                },
            ),
        ),
        # ==========================================================
        # CONTENT: el diálogo modal
        # ==========================================================
        rx.dialog.content(
            # --- Título del diálogo ---
            rx.dialog.title(
                razon["titulo"],
                font_size="1.25rem",
                font_weight="800",
                color=COLOR_TEXTO_PRINCIPAL,
            ),
            # --- Descripción del diálogo ---
            rx.dialog.description(
                "Conoce por qué esta característica hace la diferencia.",
                font_size="0.8125rem",
                color=COLOR_TEXTO_SECUNDARIO,
                margin_bottom="1rem",
            ),
            # --- Contenido principal ---
            _contenido_dialogo_razon(razon),
            # --- Pie: CTA + Cerrar ---
            _pie_dialogo_razon(),
            # --- Estilos del diálogo ---
            max_width="34rem",
            padding="2rem",
            border_radius=RADIO_EXTRA_GRANDE,
        ),
    )


# ======================================================================
# Sección completa
# ======================================================================


def seccion_por_que_instein() -> rx.Component:
    """
    Sección completa "¿Por qué elegir INSTEIN?" con grid de razones.

    Estructura:
    - Etiqueta "¿POR QUÉ INSTEIN?" con accent institucional.
    - Título grande.
    - Subtítulo.
    - Grid responsive de 6 tarjetas, cada una con su propio diálogo.
    """
    return rx.box(
        rx.vstack(
            # ==========================================================
            # Encabezado
            # ==========================================================
            rx.vstack(
                rx.text(
                    "¿POR QUÉ INSTEIN?",
                    font_size="0.75rem",
                    font_weight="700",
                    letter_spacing="0.15em",
                    color=COLOR_ACENTO_TEXTO,
                ),
                rx.heading(
                    "Formación que transforma",
                    size="7",
                    color=COLOR_TEXTO_PRINCIPAL,
                    text_align="center",
                ),
                rx.text(
                    "Todo lo que necesitas para convertirte en un profesional "
                    "técnico de excelencia está en INSTEIN.",
                    font_size="1rem",
                    color=COLOR_TEXTO_SECUNDARIO,
                    text_align="center",
                    max_width="42rem",
                ),
                align="center",
                spacing="2",
                margin_bottom="3rem",
            ),
            # ==========================================================
            # Grid de razones (cada una con su diálogo)
            # ==========================================================
            rx.grid(
                *[_tarjeta_razon_con_dialogo(r) for r in RAZONES],
                columns=rx.breakpoints(initial="1", sm="2", md="2", lg="3"),
                spacing="4",
                width="100%",
            ),
            align="center",
            width="100%",
        ),
        width="100%",
        padding="4rem 1.5rem",
    )


__all__ = [
    "RAZONES",
    "seccion_por_que_instein",
]