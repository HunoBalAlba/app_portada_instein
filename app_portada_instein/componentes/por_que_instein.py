# app_portada_instein/componentes/por_que_instein.py

"""
Sección "¿Por qué elegir INSTEIN?" — estilo Neon adaptativo.

Cards de features con icono + título + descripción + CTA que abre un
diálogo con información ampliada.

Sistema de color (UX)
---------------------
✅ ADAPTATIVO: todos los colores respetan el color_mode del usuario.

- Fondo: `FONDO_HOME_CARD_ADAPTATIVO` (light: blanco translúcido,
  dark: azul oscuro translúcido).
- Acentos: azul marino neon (`AZUL_MARINO_NEON` = `#3b5bdb`) en AMBOS modos.
- Texto: `TEXTO_HOME_PRINCIPAL` / `TEXTO_HOME_MAS_SUAVE` / `TEXTO_HOME_SUAVE`.
- Bordes: `BORDE_HOME_AZUL` / `BORDE_HOME_MEDIO` / `BORDE_HOME_SUAVE`.
- Fondo tintado: `FONDO_AZUL_SUAVE` / `FONDO_AZUL_MUY_SUAVE`.

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
- Header: título + descripción (accesibilidad).
- Cuerpo: icono grande + descripción ampliada + lista de puntos.
- Pie: botones "Cerrar" (soft) y "Más información" (solid azul marino),
  responsive: columna en móvil, fila en desktop.
"""

import reflex as rx

from app_portada_instein.infraestructura.constantes_visuales import (
    AZUL_MARINO_NEON,
    BORDE_HOME_AZUL,
    BORDE_HOME_MEDIO,
    BORDE_HOME_SUAVE,
    FONDO_AZUL_MUY_SUAVE,
    FONDO_AZUL_SUAVE,
    FONDO_HOME_CARD_ADAPTATIVO,
    RADIO_EXTRA_GRANDE,
    RADIO_GRANDE,
    RADIO_MEDIO,
    SOMBRA_HOVER_CARD_HOME,
    TEXTO_HOME_MAS_SUAVE,
    TEXTO_HOME_PRINCIPAL,
    TEXTO_HOME_SUAVE,
)


# ======================================================================
# Estructura de razones
# ======================================================================
# Cada razón incluye:
# - icono, titulo, descripcion (para la card)
# - detalle: párrafo largo mostrado en el diálogo
# - puntos: lista de beneficios concretos mostrados en el diálogo
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
    },
]


# ======================================================================
# Contenido del diálogo (detalle de razón)
# ======================================================================


def _contenido_dialogo_razon(razon: dict) -> rx.Component:
    """
    Contenido del diálogo: icono + descripción ampliada + lista de puntos.

    Estilo Neon adaptativo:
    - Icono grande con fondo tintado azul marino + borde azul + glow.
    - Descripción ampliada adaptativa.
    - Lista de puntos con iconos `circle_check` azul marino.

    ✅ ADAPTATIVO: fondo y textos cambian según el color_mode.

    Args:
        razon: Dict con los datos de la razón.
    """
    return rx.vstack(
        # ==========================================================
        # Icono grande con fondo tintado + glow
        # ==========================================================
        rx.box(
            rx.icon(razon["icono"], size=32, color=AZUL_MARINO_NEON),
            padding="1rem",
            border_radius=RADIO_EXTRA_GRANDE,
            background=FONDO_AZUL_SUAVE,          # ✅ adaptativo
            border=f"1px solid {BORDE_HOME_AZUL}",
            box_shadow=rx.color_mode_cond(         # ✅ adaptativo
                light=f"0 0 30px {AZUL_MARINO_NEON}30",
                dark=f"0 0 30px {AZUL_MARINO_NEON}40",
            ),
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
            color=TEXTO_HOME_SUAVE,                # ✅ adaptativo
            text_align="center",
        ),
        # ==========================================================
        # Lista de puntos clave
        # ==========================================================
        rx.box(
            rx.vstack(
                rx.foreach(
                    razon["puntos"],
                    lambda punto: rx.flex(
                        rx.icon(
                            "circle_check",
                            size=16,
                            color=AZUL_MARINO_NEON,
                            flex_shrink="0",
                            margin_top="0.125rem",
                        ),
                        rx.text(
                            punto,
                            font_size=["0.8125rem", "0.875rem", "0.875rem"],
                            color=TEXTO_HOME_SUAVE,    # ✅ adaptativo
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
            background=FONDO_AZUL_MUY_SUAVE,             # ✅ adaptativo
            border=f"1px solid {BORDE_HOME_SUAVE}",      # ✅ adaptativo
            border_radius=RADIO_MEDIO,
            backdrop_filter="blur(12px)",
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
    """Botón 'Cerrar' (soft gray) que cierra el diálogo."""
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
    """
    Botón 'Más información' con azul marino neon + glow.

    Al hacer clic: cierra el diálogo y navega a /contacto.

    ✅ El azul marino es el mismo en ambos modos (color de marca).
    """
    return rx.dialog.close(
        rx.button(
            rx.icon("message-circle", size=16),
            rx.text("Más información", as_="span", font_weight="700"),
            on_click=rx.redirect("/contacto"),
            size="3",
            cursor="pointer",
            width=rx.breakpoints(initial="100%", sm="auto"),
            background=AZUL_MARINO_NEON,
            color="white",
            box_shadow=f"0 0 20px {AZUL_MARINO_NEON}60",
            transition="all 0.2s",
            _hover={
                "transform": "translateY(-1px)",
                "box_shadow": f"0 0 30px {AZUL_MARINO_NEON}cc",
            },
        ),
    )


def _pie_dialogo_razon() -> rx.Component:
    """
    Pie del diálogo responsive.

    - **Móvil**: botones apilados en columna, CTA primario arriba.
    - **Tablet/Desktop**: botones en fila alineados a la derecha.

    ✅ ADAPTATIVO: el borde superior cambia según el modo.

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
        padding=[
            "1rem 1rem 0 1rem",
            "1rem 1.5rem 0 1.5rem",
            "1rem 2rem 0 2rem",
        ],
        border_top=f"1px solid {BORDE_HOME_SUAVE}",   # ✅ adaptativo
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

    Estilo Neon adaptativo:
    - Card con glassmorphism adaptativo.
    - Icono azul marino con glow.
    - CTA "Ver más →" azul marino.
    - Hover: elevación + borde azul + glow adaptativo.
    - Diálogo con fondo y textos adaptativos.

    ✅ ADAPTATIVO: card, diálogo y textos respetan el color_mode.

    Args:
        razon: Dict con los datos de la razón.
    """
    return rx.dialog.root(
        # ==========================================================
        # TRIGGER: la card clicable
        # ==========================================================
        rx.dialog.trigger(
            rx.box(
                rx.vstack(
                    # --- Icono con fondo tintado + glow ---
                    rx.box(
                        rx.icon(
                            razon["icono"],
                            size=24,
                            color=AZUL_MARINO_NEON,
                        ),
                        padding="0.75rem",
                        border_radius=RADIO_GRANDE,
                        background=FONDO_AZUL_SUAVE,          # ✅ adaptativo
                        border=f"1px solid {BORDE_HOME_AZUL}",
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
                        color=TEXTO_HOME_PRINCIPAL,           # ✅ adaptativo
                        font_weight="800",
                        letter_spacing="-0.02em",
                    ),
                    # --- Descripción ---
                    rx.text(
                        razon["descripcion"],
                        font_size="0.875rem",
                        line_height="1.6",
                        color=TEXTO_HOME_MAS_SUAVE,           # ✅ adaptativo
                    ),
                    # --- CTA "Ver más →" ---
                    rx.flex(
                        rx.text(
                            "Ver más",
                            font_size="0.875rem",
                            font_weight="700",
                            color=AZUL_MARINO_NEON,
                        ),
                        rx.icon(
                            "arrow-right",
                            size=14,
                            color=AZUL_MARINO_NEON,
                        ),
                        align="center",
                        gap="0.25rem",
                        margin_top="0.75rem",
                        transition="all 0.2s",
                    ),
                    align="start",
                    spacing="1",
                    width="100%",
                ),
                # --- Estilos de la card ---
                cursor="pointer",
                padding="1.75rem",
                border_radius=RADIO_EXTRA_GRANDE,
                border=f"1px solid {BORDE_HOME_SUAVE}",              # ✅ adaptativo
                background=FONDO_HOME_CARD_ADAPTATIVO,                # ✅ adaptativo
                backdrop_filter="blur(12px)",
                transition="all 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
                width="100%",
                height="100%",
                _hover={
                    "transform": "translateY(-4px)",
                    "border_color": BORDE_HOME_AZUL,
                    "box_shadow": SOMBRA_HOVER_CARD_HOME,             # ✅ adaptativo
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
                    color=TEXTO_HOME_PRINCIPAL,           # ✅ adaptativo
                    line_height="1.2",
                    letter_spacing="-0.02em",
                ),
                rx.dialog.description(
                    "Conoce por qué esta característica hace la diferencia.",
                    font_size="0.8125rem",
                    color=TEXTO_HOME_MAS_SUAVE,           # ✅ adaptativo
                ),
                spacing="1",
                align="start",
                width="100%",
                padding=[
                    "1.25rem 1rem 0 1rem",
                    "1.5rem 1.5rem 0 1.5rem",
                    "1.5rem 2rem 0 2rem",
                ],
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
                # Scrollbar estilizada adaptativa
                css={
                    "&::-webkit-scrollbar": {"width": "8px"},
                    "&::-webkit-scrollbar-thumb": {
                        "background": BORDE_HOME_MEDIO,   # ✅ adaptativo
                        "border_radius": "4px",
                    },
                    "&::-webkit-scrollbar-track": {
                        "background": "transparent",
                    },
                    "scrollbar-width": "thin",
                    "scrollbar-color": (
                        f"{BORDE_HOME_MEDIO} transparent"
                    ),
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
            width=[
                "calc(100vw - 1.5rem)",
                "calc(100vw - 2rem)",
                "100%",
            ],
            padding="0",
            border_radius=RADIO_EXTRA_GRANDE,
            background=FONDO_HOME_CARD_ADAPTATIVO,   # ✅ adaptativo
            border=f"1px solid {BORDE_HOME_AZUL}",   # ✅ adaptativo
            box_shadow=rx.color_mode_cond(            # ✅ adaptativo
                light=(
                    f"0 30px 60px -15px rgba(0, 0, 0, 0.25), "
                    f"0 0 40px -10px {AZUL_MARINO_NEON}20"
                ),
                dark=(
                    f"0 30px 60px -15px rgba(0, 0, 0, 0.5), "
                    f"0 0 40px -10px {AZUL_MARINO_NEON}40"
                ),
            ),
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
    Sección completa "¿Por qué elegir INSTEIN?" — estilo Neon adaptativo.

    El encabezado (número + título) se renderiza desde `vista_inicio.py`
    con `separador_numerado`. Este componente SOLO renderiza el grid.

    Estilo Neon:
    - Cards con glassmorphism adaptativo.
    - Iconos azul marino con glow.
    - Grid responsive de 6 cards.
    - Cada card abre su propio diálogo independiente.

    ✅ ADAPTATIVO: todo el bloque respeta el color_mode del usuario.
    """
    return rx.box(
        rx.vstack(
            # ==========================================================
            # Grid de razones (cada una con su diálogo)
            # ==========================================================
            rx.grid(
                *[_tarjeta_razon_con_dialogo(r) for r in RAZONES],
                columns=rx.breakpoints(
                    initial="1",
                    sm="2",
                    md="2",
                    lg="3",
                ),
                spacing="4",
                width="100%",
            ),
            align="center",
            width="100%",
            max_width="72rem",
            margin="0 auto",
        ),
        width="100%",
        padding=[
            "0 1rem 4rem 1rem",
            "0 1.5rem 4rem 1.5rem",
            "0 1.5rem 4rem 1.5rem",
        ],
    )


__all__ = [
    "RAZONES",
    "seccion_por_que_instein",
]