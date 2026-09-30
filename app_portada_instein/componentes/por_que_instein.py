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

Diseño UX del diálogo (FIX móvil)
---------------------------------
El diálogo aplica el mismo patrón que `vista_post.py` y `dialogos.py`
(blog): scroll interno en `flex: 1` + `min-height: 0`, marco en
`display: flex` + `flex-direction: column`, y altura máxima con `dvh`
para respetar la barra de URL móvil.

Estructura del diálogo:
- Header: icono grande + descripción ampliada.
- Cuerpo: lista de puntos (con scroll interno si es necesario).
- Pie: botones "Cerrar" (soft) y "Más información" (solid crimson),
  responsive: columna en móvil, fila en desktop.

Nota técnica: `rx.inset(side="x")` requiere padre con `display: flex`.
----------------------------------------------------------------------
Si el contenedor del `rx.inset` no es flex, el inset aplica el padding
de forma inconsistente. Envuélvelo en un `rx.box(..., display="flex",
flex_direction="column")` o usa `padding` directamente.
"""

import reflex as rx

from app_portada_instein.infraestructura.constantes_visuales import (
    COLOR_ACENTO_SOLIDO,
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
    Contenido del diálogo: icono + descripción ampliada + lista de puntos.

    El cuerpo del diálogo es responsive y hace scroll interno cuando el
    contenido excede el espacio (aunque con 4 puntos rara vez pasa).

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
            margin="0 auto",
        ),
        # ==========================================================
        # Descripción ampliada
        # ==========================================================
        rx.text(
            razon["detalle"],
            font_size=["0.875rem", "0.9375rem", "0.9375rem"],
            line_height="1.7",
            color=COLOR_TEXTO_CUERPO,
            text_align="center",
        ),
        # ==========================================================
        # Lista de puntos clave
        # ==========================================================
        # Usamos padding directo (más robusto que rx.inset, que requiere
        # que el padre sea flex para aplicar bien el "current" padding).
        rx.box(
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
                            font_size=["0.8125rem", "0.875rem", "0.875rem"],
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
            ),
            padding="1rem",
            background=COLOR_FONDO_SUAVE,
            border_radius=RADIO_MEDIO,
            width="100%",
        ),
        spacing="4",
        align="center",
        width="100%",
    )


# ======================================================================
# Pie del diálogo (CTA + botón cerrar) — responsive
# ======================================================================


def _boton_cerrar_dialogo() -> rx.Component:
    """Botón 'Cerrar' (soft) que cierra el diálogo."""
    return rx.dialog.close(
        rx.button(
            rx.icon("x", size=16),
            rx.text("Cerrar", as_="span", font_weight="600"),
            variant="soft",
            color_scheme="gray",
            size="3",
            cursor="pointer",
            width=rx.breakpoints(initial="100%", sm="auto"),
        ),
    )


def _boton_mas_informacion() -> rx.Component:
    """Botón 'Más información' (solid crimson) que cierra + navega."""
    return rx.dialog.close(
        rx.button(
            rx.icon("message-circle", size=16),
            rx.text("Más información", as_="span", font_weight="700"),
            on_click=rx.redirect("/contacto"),
            variant="solid",
            color_scheme="crimson",
            size="3",
            cursor="pointer",
            width=rx.breakpoints(initial="100%", sm="auto"),
            _hover={"filter": "brightness(1.1)"},
        ),
    )


def _pie_dialogo_razon() -> rx.Component:
    """
    Pie del diálogo responsive.

    - **Móvil**: botones apilados en columna, CTA primario arriba.
    - **Tablet/Desktop**: botones en fila alineados a la derecha.

    El pie fluye con el scroll (aparece al final del contenido).
    """
    return rx.box(
        # --- Móvil: columna, ancho completo ---
        rx.mobile_only(
            rx.vstack(
                _boton_mas_informacion(),
                _boton_cerrar_dialogo(),
                spacing="2",
                width="100%",
                align="stretch",
            ),
        ),
        # --- Tablet/Desktop: fila, alineado a la derecha ---
        rx.tablet_and_desktop(
            rx.flex(
                _boton_cerrar_dialogo(),
                _boton_mas_informacion(),
                spacing="3",
                justify="end",
                width="100%",
                flex_wrap="wrap",
            ),
        ),
        width="100%",
        padding=["1rem 1rem 0 1rem", "1rem 1.5rem 0 1.5rem", "1rem 2rem 0 2rem"],
        border_top=f"1px solid {COLOR_BORDE_SUAVE}",
        margin_top="1rem",
    )


# ======================================================================
# Diálogo por razón (envuelve la card + el contenido del diálogo)
# ======================================================================


def _tarjeta_razon_con_dialogo(razon: dict) -> rx.Component:
    """
    Envuelve la card + el diálogo en un `rx.dialog.root`.

    Estructura del diálogo (con FIX móvil):
    - Header: título + descripción corta (accesibilidad).
    - Cuerpo con scroll interno (`flex: 1` + `min-height: 0`).
    - Pie responsive al final del flujo.

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
        # CONTENT: el diálogo modal (con FIX móvil)
        # ==========================================================
        rx.dialog.content(
            # ------------------------------------------------------
            # Header: título + descripción (accesibilidad)
            # ------------------------------------------------------
            rx.vstack(
                rx.dialog.title(
                    razon["titulo"],
                    font_size=["1.125rem", "1.25rem", "1.25rem"],
                    font_weight="800",
                    color=COLOR_TEXTO_PRINCIPAL,
                    line_height="1.2",
                ),
                rx.dialog.description(
                    "Conoce por qué esta característica hace la diferencia.",
                    font_size="0.8125rem",
                    color=COLOR_TEXTO_SECUNDARIO,
                ),
                spacing="1",
                align="start",
                width="100%",
                padding=["1.25rem 1rem 0 1rem", "1.5rem 1.5rem 0 1.5rem", "1.5rem 2rem 0 2rem"],
            ),
            # ------------------------------------------------------
            # CONTENEDOR INTERNO CON SCROLL
            # flex="1" + min_height="0" → scroll real
            # ------------------------------------------------------
            rx.box(
                _contenido_dialogo_razon(razon),
                flex="1",
                min_height="0",
                width="100%",
                overflow_y="auto",
                overflow_x="hidden",
                padding=["1rem", "1.25rem 1.5rem", "1.25rem 2rem"],
                # Scrollbar estilizado
                css={
                    "&::-webkit-scrollbar": {"width": "8px"},
                    "&::-webkit-scrollbar-thumb": {
                        "background": COLOR_BORDE_SUAVE,
                        "border_radius": "4px",
                    },
                    "&::-webkit-scrollbar-track": {"background": "transparent"},
                    "scrollbar-width": "thin",
                    "scrollbar-color": f"{COLOR_BORDE_SUAVE} transparent",
                },
            ),
            # ------------------------------------------------------
            # PIE: botones responsive al final del flujo
            # ------------------------------------------------------
            _pie_dialogo_razon(),
            # ------------------------------------------------------
            # Estilos del marco del diálogo
            # ------------------------------------------------------
            max_width="34rem",
            width=["calc(100vw - 1.5rem)", "calc(100vw - 2rem)", "100%"],
            padding="0",
            border_radius=RADIO_EXTRA_GRANDE,
            background=COLOR_FONDO_CARTA,
            border=f"1px solid {COLOR_BORDE_SUAVE}",
            box_shadow="0 30px 60px -15px rgba(0,0,0,0.25)",
            overflow="hidden",
            # `display: flex` + `flex-direction: column` permite que el
            # box interno use `flex="1"` y active el scroll.
            display="flex",
            flex_direction="column",
            max_height=rx.breakpoints(
                initial="90dvh",
                sm="90dvh",
                md="88dvh",
                lg="85dvh",
            ),
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
        padding=["3rem 1rem", "3.5rem 1.5rem", "4rem 1.5rem"],
    )


__all__ = [
    "RAZONES",
    "seccion_por_que_instein",
]