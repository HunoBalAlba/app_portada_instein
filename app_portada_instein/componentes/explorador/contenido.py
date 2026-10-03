# app_portada_instein/componentes/explorador/contenido.py

"""
Grids de contenido dinámico del explorador — estilo Neon adaptativo.

Secciones:
- Info: descripción + datos rápidos.
- Plan: años + materias.
- Perfil: habilidades.
- Campo: salidas laborales.
- FAQ: acordeón de preguntas frecuentes.

Sistema de color (UX)
---------------------
✅ ADAPTATIVO: todos los colores respetan el color_mode del usuario.

- Fondo de cards: `FONDO_HOME_CARD_ADAPTATIVO`.
- Acentos: azul marino neon (`AZUL_MARINO_NEON` = `#3b5bdb`) en AMBOS modos.
- Texto: `TEXTO_HOME_PRINCIPAL` / `TEXTO_HOME_SUAVE` / `TEXTO_HOME_MAS_SUAVE`.
- Bordes: `BORDE_HOME_AZUL` / `BORDE_HOME_SUAVE`.
- Fondo tintado del icono: `FONDO_AZUL_SUAVE`.
- Sombra hover: `SOMBRA_HOVER_CARD_HOME`.

Nota técnica: ACORDEÓN FAQ UNIFICADO
------------------------------------
✅ REFACTORIZADO: la sección de FAQ ya NO tiene su propio `EstadoFAQ`
ni su propio item. Ahora delega en el componente genérico
`acordeon_faq` con variante `"neon"` (glassmorphism), que usa el
`EstadoAcordeonFaq` global.

⚠️ IMPORTANTE: las preguntas vienen como `Var` reactiva
(`EstadoInstitucional.preguntas_frecuentes_carrera_destacada`).
NO se pueden iterar en Python puro. Se pasan DIRECTO a
`acordeon_faq`, que internamente usa `rx.foreach`.

Esto elimina ~60 líneas de código duplicado.
"""

from __future__ import annotations

import reflex as rx

from app_portada_instein.componentes.acordeon_faq import acordeon_faq
from app_portada_instein.componentes.primitivos import (
    contenedor_clicable,
)
from app_portada_instein.dominio.estado_institucional import (
    EstadoInstitucional,
)
from app_portada_instein.infraestructura.constantes_visuales import (
    ANCHO_SECCION,
    AZUL_MARINO_NEON,
    BORDE_HOME_AZUL,
    BORDE_HOME_SUAVE,
    FONDO_AZUL_SUAVE,
    FONDO_HOME_CARD_ADAPTATIVO,
    RADIO_GRANDE,
    RADIO_MEDIO,
    RADIO_PASTILLA,
    SOMBRA_HOVER_CARD_HOME,
    TEXTO_HOME_MAS_SUAVE,
    TEXTO_HOME_PRINCIPAL,
    TEXTO_HOME_SUAVE,
)


# ======================================================================
# CARD GENÉRICA DE CONTENIDO
# ======================================================================


def _card_explorador(
    titulo: str,
    descripcion: str,
    icono: str = "circle-dot",
) -> rx.Component:
    """
    Card individual estilo Neon adaptativo.

    UX:
    - Icono azul marino con fondo tintado + borde azul.
    - Hover: elevación + borde azul + glow azul (adaptativo).

    ✅ ADAPTATIVO: fondo, textos y borde cambian según el modo.
    """
    return rx.box(
        rx.vstack(
            rx.flex(
                rx.icon(icono, size=20, color=AZUL_MARINO_NEON),
                height="2.5rem",
                width="2.5rem",
                border_radius=RADIO_MEDIO,
                background=FONDO_AZUL_SUAVE,
                border=f"1px solid {BORDE_HOME_AZUL}",
                align="center",
                justify="center",
                margin_bottom="0.75rem",
            ),
            rx.heading(
                titulo,
                size="3",
                font_weight="800",
                color=TEXTO_HOME_PRINCIPAL,
                line_height="1.3",
                letter_spacing="-0.02em",
            ),
            rx.text(
                descripcion,
                font_size="0.8125rem",
                color=TEXTO_HOME_MAS_SUAVE,
                line_height="1.5",
            ),
            align="start",
            spacing="1",
            width="100%",
        ),
        padding="1.25rem",
        border_radius=RADIO_GRANDE,
        background=FONDO_HOME_CARD_ADAPTATIVO,
        backdrop_filter="blur(12px)",
        border=f"1px solid {BORDE_HOME_SUAVE}",
        width="100%",
        transition="all 0.2s",
        _hover={
            "transform": "translateY(-4px)",
            "border_color": BORDE_HOME_AZUL,
            "box_shadow": SOMBRA_HOVER_CARD_HOME,
        },
    )


# ======================================================================
# CONTADOR DE ITEMS
# ======================================================================


def _contador_items(texto: str, cantidad) -> rx.Component:
    """
    Contador con etiqueta y badge numérico en azul marino.

    ✅ ADAPTATIVO: fondo del badge cambia según el modo.

    Args:
        texto: Texto descriptivo (ej: "Materias del año:").
        cantidad: Var de cantidad (con `.length()` o `.to_string()`).
    """
    return rx.flex(
        rx.text(
            texto,
            font_size="0.875rem",
            color=TEXTO_HOME_MAS_SUAVE,
        ),
        rx.text(
            cantidad,
            font_size="0.875rem",
            font_weight="700",
            color=AZUL_MARINO_NEON,
            padding="0.125rem 0.5rem",
            background=FONDO_AZUL_SUAVE,
            border=f"1px solid {BORDE_HOME_AZUL}",
            border_radius=RADIO_PASTILLA,
        ),
        align="center",
        gap="0.5rem",
        margin_bottom="1.5rem",
    )


# ======================================================================
# SECCIÓN: INFORMACIÓN
# ======================================================================


def _grid_info() -> rx.Component:
    """
    Grid con la información completa de la carrera.

    ✅ ADAPTATIVO: todos los textos y fondos cambian según el modo.
    """
    carrera = EstadoInstitucional.carrera_destacada

    return rx.vstack(
        # --- Descripción ---
        rx.box(
            rx.vstack(
                rx.flex(
                    rx.icon(
                        "file-text",
                        size=22,
                        color=AZUL_MARINO_NEON,
                    ),
                    rx.heading(
                        "Descripción de la Carrera",
                        size="4",
                        color=TEXTO_HOME_PRINCIPAL,
                        font_weight="800",
                        letter_spacing="-0.02em",
                    ),
                    align="center",
                    gap="0.5rem",
                    margin_bottom="0.75rem",
                ),
                rx.text(
                    carrera["descripcion"],
                    font_size="0.9375rem",
                    line_height="1.7",
                    color=TEXTO_HOME_SUAVE,
                ),
                align="start",
                spacing="2",
                width="100%",
            ),
            padding="1.5rem",
            border_radius=RADIO_GRANDE,
            background=FONDO_HOME_CARD_ADAPTATIVO,
            backdrop_filter="blur(12px)",
            border=f"1px solid {BORDE_HOME_AZUL}",
            width="100%",
            margin_bottom="1rem",
        ),
        # --- Grid de datos rápidos ---
        rx.grid(
            _card_explorador(
                "Duración",
                f"{carrera['duracion']} · 6 semestres",
                "clock",
            ),
            _card_explorador(
                "Título",
                "Técnico Superior en Provisión Nacional",
                "award",
            ),
            _card_explorador(
                "Certificación",
                "Resolución Ministerial R.M. 0871/2016",
                "shield-check",
            ),
            _card_explorador(
                "Modalidad",
                "Presencial · Turnos mañana, tarde y noche",
                "building-2",
            ),
            _card_explorador(
                "Ubicación",
                "Galería FLOR DE ORO - 1er piso",
                "map-pin",
            ),
            _card_explorador(
                "Contacto",
                "WhatsApp: 71282993 · Tel: 79104232",
                "phone",
            ),
            columns=rx.breakpoints(initial="1", sm="2", lg="2"),
            spacing="4",
            width="100%",
        ),
        spacing="0",
        width="100%",
        max_width=ANCHO_SECCION,
        margin="0 auto",
    )


# ======================================================================
# SECCIÓN: PLAN DE ESTUDIOS
# ======================================================================


def _pastilla_anio_explorador(anio: dict, indice: int) -> rx.Component:
    """
    Pastilla seleccionable para elegir el año del plan.

    ✅ ADAPTATIVO: la pastilla inactiva cambia según el modo.

    Estilo Neon:
    - Activa: fondo azul marino neon + texto blanco + glow azul.
    - Inactiva: fondo adaptativo + borde adaptativo.
    """
    esta_activo = EstadoInstitucional.indice_anio_explorador == indice

    return contenedor_clicable(
        rx.text(anio["anio"], size="2"),
        al_hacer_clic=lambda: (
            EstadoInstitucional.seleccionar_anio_explorador(indice)
        ),
        padding="0.625rem 1.125rem",
        border_radius=RADIO_MEDIO,
        background=rx.cond(
            esta_activo,
            AZUL_MARINO_NEON,
            rx.color_mode_cond(
                light="rgba(15, 23, 42, 0.05)",
                dark="rgba(255, 255, 255, 0.05)",
            ),
        ),
        color=rx.cond(
            esta_activo,
            "white",
            TEXTO_HOME_SUAVE,
        ),
        border=rx.cond(
            esta_activo,
            f"1px solid {AZUL_MARINO_NEON}",
            f"1px solid {BORDE_HOME_SUAVE}",
        ),
        box_shadow=rx.cond(
            esta_activo,
            f"0 0 20px {AZUL_MARINO_NEON}60",
            "none",
        ),
        font_weight="600",
        white_space="nowrap",
        display="inline-flex",
        align_items="center",
        transition="all 0.2s",
    )


def _grid_plan() -> rx.Component:
    """
    Grid con el plan de estudios agrupado por año.

    ✅ ADAPTATIVO: todos los textos cambian según el modo.
    """
    carrera = EstadoInstitucional.carrera_destacada

    return rx.vstack(
        # --- Encabezado + selector de año ---
        rx.box(
            rx.flex(
                rx.icon(
                    "book-open",
                    size=20,
                    color=AZUL_MARINO_NEON,
                ),
                rx.heading(
                    "Plan de Estudios",
                    size="4",
                    color=TEXTO_HOME_PRINCIPAL,
                    font_weight="800",
                    letter_spacing="-0.02em",
                ),
                align="center",
                gap="0.5rem",
                margin_bottom="1rem",
            ),
            rx.flex(
                rx.foreach(
                    carrera["plan_estudios"],
                    _pastilla_anio_explorador,
                ),
                gap="0.5rem",
                flex_wrap="wrap",
                margin_bottom="1rem",
            ),
            width="100%",
        ),
        # --- Contador de materias ---
        _contador_items(
            "Materias del año: ",
            EstadoInstitucional.materias_anio_explorador
            .length()
            .to_string(),
        ),
        # --- Grid de materias ---
        rx.grid(
            rx.foreach(
                EstadoInstitucional.materias_anio_explorador,
                lambda materia, idx: _card_explorador(
                    f"Materia {idx + 1}",
                    materia,
                    "book-open",
                ),
            ),
            columns=rx.breakpoints(initial="1", sm="2", lg="3"),
            spacing="3",
            width="100%",
        ),
        spacing="0",
        width="100%",
        max_width=ANCHO_SECCION,
        margin="0 auto",
    )


# ======================================================================
# SECCIÓN: PERFIL PROFESIONAL
# ======================================================================


def _grid_perfil() -> rx.Component:
    """
    Grid con el perfil profesional.

    ✅ ADAPTATIVO: las cards se adaptan según el modo.
    """
    return rx.grid(
        rx.foreach(
            EstadoInstitucional.perfil_carrera_destacada,
            lambda item, idx: _card_explorador(
                f"Habilidad {idx + 1}",
                item,
                "circle_check",
            ),
        ),
        columns=rx.breakpoints(initial="1", sm="2", lg="2"),
        spacing="3",
        width="100%",
        max_width=ANCHO_SECCION,
        margin="0 auto",
    )


# ======================================================================
# SECCIÓN: CAMPO LABORAL
# ======================================================================


def _grid_campo() -> rx.Component:
    """
    Grid con el campo laboral.

    ✅ ADAPTATIVO: las cards se adaptan según el modo.
    """
    return rx.grid(
        rx.foreach(
            EstadoInstitucional.campo_carrera_destacada,
            lambda item, idx: _card_explorador(
                f"Salida {idx + 1}",
                item,
                "briefcase",
            ),
        ),
        columns=rx.breakpoints(initial="1", sm="2", lg="2"),
        spacing="3",
        width="100%",
        max_width=ANCHO_SECCION,
        margin="0 auto",
    )


# ======================================================================
# SECCIÓN: FAQ (delegada al acordeón unificado)
# ======================================================================


def _grid_faq() -> rx.Component:
    """
    Grid con preguntas frecuentes específicas de la carrera.

    ✅ REFACTORIZADO: usa el componente genérico `acordeon_faq` con
    variante `"neon"` (glassmorphism, coherente con el estilo del
    explorador). El estado del acordeón vive en `EstadoAcordeonFaq`
    (compartido por toda la app).

    ⚠️ IMPORTANTE: pasamos el `Var` reactivo DIRECTO a `acordeon_faq`.
    NO se puede iterar en Python puro (lanzaría `VarTypeError`).
    El `rx.foreach` interno del acordeón se encarga de iterar en el
    frontend.

    Estructura:
    1. Contador de preguntas (reactivo).
    2. Acordeón con las preguntas (pasadas como Var).
    """
    return rx.vstack(
        # --- Contador de preguntas ---
        _contador_items(
            "Preguntas frecuentes de esta carrera",
            EstadoInstitucional.preguntas_frecuentes_carrera_destacada
            .length()
            .to_string(),
        ),
        # --- Acordeón unificado ---
        # Se pasa el Var directamente (NO iterar en Python).
        acordeon_faq(
            items=(
                EstadoInstitucional
                .preguntas_frecuentes_carrera_destacada
            ),
            variante="neon",
            icono="circle-help",
            color_acento=AZUL_MARINO_NEON,
        ),
        spacing="0",
        width="100%",
        max_width=ANCHO_SECCION,
        margin="0 auto",
    )


# ======================================================================
# CONTENIDO DINÁMICO
# ======================================================================


def _contenido_explorador() -> rx.Component:
    """
    Renderiza el contenido dinámico según la sección activa.

    ✅ ADAPTATIVO: todo el contenido se adapta al color_mode.
    """
    return rx.box(
        rx.match(
            EstadoInstitucional.seccion_explorador_activa,
            ("info", _grid_info()),
            ("plan", _grid_plan()),
            ("perfil", _grid_perfil()),
            ("campo", _grid_campo()),
            ("faq", _grid_faq()),
            _grid_info(),
        ),
        width="100%",
        min_height="20rem",
    )


# ======================================================================
# EXPORTS
# ======================================================================

__all__ = [
    "_contenido_explorador",
    "_grid_campo",
    "_grid_faq",
    "_grid_info",
    "_grid_perfil",
    "_grid_plan",
]