"""
Explorador de carrera estilo "Leonardo AI":
- Buscador de carreras.
- Grid de imágenes de carreras que NAVEGAN al detalle.
- Panel flotante para acceso rápido.
- Barra de opciones (info, plan, perfil, campo, faq).
- Contenido dinámico:
  - Info: detalles completos de la carrera.
  - Plan: plan de estudios agrupado por año.
  - Perfil: habilidades del perfil profesional.
  - Campo: salidas laborales.
  - FAQ: preguntas frecuentes específicas.

Al hacer clic en cualquier tarjeta se navega a `/carrera/{id}`.
"""

import reflex as rx

from app_portada_instein.componentes.primitivos import (
    contenedor_clicable,
    enlace_navegacion,
)
from app_portada_instein.dominio.estado_institucional import EstadoInstitucional


# ======================================================================
# Buscador de carreras
# ======================================================================

def _buscador_carreras() -> rx.Component:
    """Buscador central estilo Leonardo AI."""
    return rx.box(
        rx.flex(
            rx.box(
                rx.icon(
                    "search",
                    size=20,
                    color=rx.color_mode_cond(light="#64748b", dark="#94a3b8"),
                ),
                padding="0.5rem",
                display="flex",
                align_items="center",
                justify_content="center",
            ),
            rx.input(
                placeholder="Busca una carrera: Sistemas, Contaduría, Electrónica...",
                value=EstadoInstitucional.texto_busqueda_carrera,
                on_change=EstadoInstitucional.actualizar_busqueda_carrera,
                variant="soft",
                size="3",
                width="100%",
                border="none",
                background="transparent",
                _focus={"box_shadow": "none", "outline": "none"},
            ),
            rx.box(
                rx.icon(
                    "sparkles",
                    size=18,
                    color=rx.color_mode_cond(light="#94a3b8", dark="#64748b"),
                ),
                padding="0.5rem",
                display="flex",
                align_items="center",
                justify_content="center",
            ),
            align="center",
            width="100%",
            gap="0.5rem",
        ),
        width="100%",
        max_width="48rem",
        margin="0 auto 1.5rem auto",
        padding="0.75rem 1rem",
        border_radius="1rem",
        background=rx.color_mode_cond(
            light="rgba(255,255,255,0.9)",
            dark="rgba(15,17,23,0.9)",
        ),
        border=(
            "1px solid "
            + rx.color_mode_cond(light="#e2e8f0", dark="#1e293b")
        ),
        backdrop_filter="blur(12px)",
        box_shadow="0 10px 30px -10px rgba(0,0,0,0.15)",
        transition="all 0.2s",
    )


# ======================================================================
# Card de imagen de carrera (con navegación al detalle)
# ======================================================================

def _card_imagen_carrera(carrera: dict) -> rx.Component:
    """
    Card con la imagen de la carrera.

    Al hacer clic, navega al detalle de la carrera (`/carrera/{id}`)
    usando `enlace_navegacion`.
    """
    esta_activa = EstadoInstitucional.id_carrera_destacada == carrera["id"]
    color = carrera["color_principal"]

    return enlace_navegacion(
        f"/carrera/{carrera['id']}",
        rx.box(
            # --- Imagen de la carrera ---
            rx.box(
                rx.image(
                    src="/" + carrera["imagen_archivo"],
                    alt=carrera["nombre"],
                    width="100%",
                    height="100%",
                    object_fit="cover",
                ),
                width="100%",
                height="8rem",
                overflow="hidden",
                border_radius="0.75rem",
                position="relative",
                background=rx.cond(
                    esta_activa,
                    f"linear-gradient(135deg, {color}33, {color}88)",
                    "transparent",
                ),
            ),
            # --- Título + duración ---
            rx.vstack(
                rx.heading(
                    carrera["nombre_corto"],
                    size="3",
                    font_weight="700",
                    color=rx.color_mode_cond(light="#0f172a", dark="#f1f5f9"),
                ),
                rx.text(
                    carrera["duracion"],
                    font_size="0.75rem",
                    color=rx.color_mode_cond(light="#64748b", dark="#94a3b8"),
                ),
                align="start",
                spacing="1",
                width="100%",
                margin_top="0.75rem",
            ),
            # --- Icono check si está activa ---
            # rx.cond(
            #     esta_activa,
            #     rx.box(
            #         rx.icon("check_circle", size=20, color="#ffffff"),
            #         position="absolute",
            #         top="0.5rem",
            #         right="0.5rem",
            #         background=color,
            #         border_radius="9999px",
            #         padding="0.25rem",
            #         display="flex",
            #         align_items="center",
            #         justify_content="center",
            #         box_shadow=f"0 4px 12px -2px {color}88",
            #     ),
            #     rx.fragment(),
            # ),
            position="relative",
            width="100%",
        ),
        # --- Estilos de la tarjeta ---
        padding="0.75rem",
        border_radius="1rem",
        background=rx.color_mode_cond(light="#ffffff", dark="#0f1117"),
        border=rx.cond(
            False,
            f"2px solid {color}",
            "1px solid "
            + rx.color_mode_cond(light="#e2e8f0", dark="#1e293b"),
        ),
        box_shadow=rx.cond(
            False,
            f"0 15px 30px -10px {color}55",
            "0 2px 6px -2px rgba(0,0,0,0.08)",
        ),
        transition="all 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
        width="100%",
        _hover={
            "transform": "translateY(-4px)",
            "border_color": color,
            "box_shadow": f"0 20px 40px -12px {color}66",
        },
    )


def _grid_imagenes_carreras() -> rx.Component:
    """Grid con las imágenes de todas las carreras."""
    return rx.box(
        rx.flex(
            rx.text(
                "Carreras disponibles",
                font_size="0.75rem",
                font_weight="700",
                letter_spacing="0.1em",
                text_transform="uppercase",
                color=rx.color_mode_cond(light="#64748b", dark="#94a3b8"),
            ),
            rx.text(
                EstadoInstitucional.carreras_filtradas.length().to_string(),
                font_size="0.75rem",
                font_weight="700",
                color=rx.color_mode_cond(light="#0f172a", dark="#f1f5f9"),
                padding="0.125rem 0.5rem",
                background=rx.color_mode_cond(light="#f1f5f9", dark="#1e293b"),
                border_radius="9999px",
            ),
            align="center",
            gap="0.5rem",
            margin_bottom="1rem",
        ),
        rx.grid(
            rx.foreach(
                EstadoInstitucional.carreras_filtradas,
                _card_imagen_carrera,
            ),
            columns=rx.breakpoints(initial="2", sm="2", md="3", lg="5"),
            spacing="3",
            width="100%",
        ),
        width="100%",
        max_width="72rem",
        margin="0 auto 3rem auto",
    )


# ======================================================================
# Cabecera de la carrera seleccionada
# ======================================================================

def _cabecera_carrera() -> rx.Component:
    """Cabecera con badge + nombre + lema de la carrera destacada."""
    carrera = EstadoInstitucional.carrera_destacada
    color_principal = carrera["color_principal"]

    return rx.vstack(
        rx.flex(
            rx.icon("star", size=12, color="#ffffff"),
            rx.text(
                "CARRERA SELECCIONADA",
                font_size="0.625rem",
                font_weight="800",
                color="#ffffff",
                letter_spacing="0.1em",
            ),
            align="center",
            gap="0.375rem",
            background=color_principal,
            padding="0.375rem 0.75rem",
            border_radius="9999px",
            width="fit-content",
            box_shadow=f"0 4px 12px -2px {color_principal}66",
        ),
        rx.heading(
            carrera["nombre"],
            size="7",
            text_align="center",
            font_weight="900",
            letter_spacing="-0.03em",
            color=rx.color_mode_cond(light="#0f172a", dark="#f1f5f9"),
            max_width="48rem",
        ),
        rx.text(
            carrera["lema"],
            font_size="0.9375rem",
            text_align="center",
            color=rx.color_mode_cond(light="#475569", dark="#94a3b8"),
            max_width="42rem",
        ),
        align="center",
        spacing="3",
        margin_bottom="2rem",
    )


# ======================================================================
# Botón de opción (tab circular)
# ======================================================================

def _boton_opcion_explorador(
    icono: str,
    etiqueta: str,
    id_seccion: str,
) -> rx.Component:
    """Botón circular con icono y etiqueta debajo."""
    esta_activa = EstadoInstitucional.seccion_explorador_activa == id_seccion
    color_carrera = EstadoInstitucional.carrera_destacada["color_principal"]

    return contenedor_clicable(
        rx.vstack(
            rx.flex(
                rx.icon(
                    icono,
                    size=22,
                    color=rx.cond(
                        esta_activa,
                        "#ffffff",
                        rx.color_mode_cond(light="#475569", dark="#cbd5e1"),
                    ),
                ),
                height="3rem",
                width="3rem",
                border_radius="9999px",
                background=rx.cond(
                    esta_activa,
                    color_carrera,
                    rx.color_mode_cond(
                        light="rgba(255,255,255,0.9)",
                        dark="rgba(15,17,23,0.9)",
                    ),
                ),
                border=rx.cond(
                    esta_activa,
                    "none",
                    "1px solid "
                    + rx.color_mode_cond(light="#e2e8f0", dark="#334155"),
                ),
                align="center",
                justify="center",
                box_shadow=rx.cond(
                    esta_activa,
                    f"0 8px 20px -4px {color_carrera}88",
                    "0 2px 6px -2px rgba(0,0,0,0.08)",
                ),
                transition="all 0.2s",
                backdrop_filter="blur(12px)",
            ),
            rx.text(
                etiqueta,
                font_size="0.75rem",
                font_weight=rx.cond(esta_activa, "700", "600"),
                color=rx.cond(
                    esta_activa,
                    color_carrera,
                    rx.color_mode_cond(light="#64748b", dark="#94a3b8"),
                ),
                white_space="nowrap",
            ),
            align="center",
            spacing="2",
        ),
        al_hacer_clic=lambda: EstadoInstitucional.seleccionar_seccion_explorador(
            id_seccion
        ),
        transition="all 0.2s",
        _hover={"transform": "translateY(-2px)"},
    )


def _barra_opciones_explorador() -> rx.Component:
    """Barra horizontal con las opciones del explorador."""
    return rx.flex(
        _boton_opcion_explorador("info", "Información", "info"),
        _boton_opcion_explorador("book-open", "Plan", "plan"),
        _boton_opcion_explorador("user-check", "Perfil", "perfil"),
        _boton_opcion_explorador("briefcase", "Campo", "campo"),
        _boton_opcion_explorador("help-circle", "FAQ", "faq"),
        gap="1.25rem",
        justify="center",
        align="start",
        flex_wrap="wrap",
        width="100%",
        margin_bottom="2.5rem",
    )


# ======================================================================
# Card de contenido dinámico
# ======================================================================

def _card_explorador(
    titulo: str,
    descripcion: str,
    icono: str = "circle-dot",
) -> rx.Component:
    """Card individual estilo "Featured"."""
    color_carrera = EstadoInstitucional.carrera_destacada["color_principal"]

    return rx.box(
        rx.vstack(
            rx.flex(
                rx.icon(icono, size=20, color=color_carrera),
                height="2.5rem",
                width="2.5rem",
                border_radius="0.75rem",
                background=color_carrera + "15",
                align="center",
                justify="center",
                margin_bottom="0.75rem",
            ),
            rx.heading(
                titulo,
                size="3",
                font_weight="700",
                color=rx.color_mode_cond(light="#0f172a", dark="#f1f5f9"),
                line_height="1.3",
            ),
            rx.text(
                descripcion,
                font_size="0.8125rem",
                color=rx.color_mode_cond(light="#64748b", dark="#94a3b8"),
                line_height="1.5",
            ),
            align="start",
            spacing="1",
            width="100%",
        ),
        padding="1.25rem",
        border_radius="1rem",
        background=rx.color_mode_cond(light="#ffffff", dark="#0f1117"),
        border="1px solid "
        + rx.color_mode_cond(light="#e2e8f0", dark="#1e293b"),
        width="100%",
        transition="all 0.2s",
        _hover={
            "transform": "translateY(-4px)",
            "border_color": color_carrera + "44",
            "box_shadow": f"0 15px 30px -10px {color_carrera}33",
        },
    )


# ======================================================================
# Sección: INFORMACIÓN
# ======================================================================

def _grid_info() -> rx.Component:
    """Grid con la información completa de la carrera."""
    carrera = EstadoInstitucional.carrera_destacada
    color_carrera = carrera["color_principal"]

    return rx.vstack(
        rx.box(
            rx.vstack(
                rx.flex(
                    rx.icon("file-text", size=22, color=color_carrera),
                    rx.heading(
                        "Descripción de la Carrera",
                        size="4",
                        color=rx.color_mode_cond(light="#0f172a", dark="#f1f5f9"),
                    ),
                    align="center",
                    gap="0.5rem",
                    margin_bottom="0.75rem",
                ),
                rx.text(
                    carrera["descripcion"],
                    font_size="0.9375rem",
                    line_height="1.7",
                    color=rx.color_mode_cond(light="#475569", dark="#cbd5e1"),
                ),
                align="start",
                spacing="2",
                width="100%",
            ),
            padding="1.5rem",
            border_radius="1rem",
            background=rx.color_mode_cond(light="#ffffff", dark="#0f1117"),
            border=f"1px solid {color_carrera}33",
            width="100%",
            margin_bottom="1rem",
        ),
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
        max_width="64rem",
        margin="0 auto",
    )


# ======================================================================
# Sección: PLAN DE ESTUDIOS
# ======================================================================

def _pastilla_anio_explorador(anio: dict, indice: int) -> rx.Component:
    """Pastilla seleccionable para elegir el año del plan."""
    esta_activo = EstadoInstitucional.indice_anio_explorador == indice
    color_carrera = EstadoInstitucional.carrera_destacada["color_principal"]

    return contenedor_clicable(
        rx.text(anio["anio"], size="2"),
        al_hacer_clic=lambda: EstadoInstitucional.seleccionar_anio_explorador(indice),
        padding="0.625rem 1.125rem",
        border_radius="0.75rem",
        background=rx.cond(
            esta_activo,
            color_carrera,
            rx.color_mode_cond(light="#f1f5f9", dark="#1e293b"),
        ),
        color=rx.cond(
            esta_activo,
            "#ffffff",
            rx.color_mode_cond(light="#475569", dark="#cbd5e1"),
        ),
        border=f"1px solid {rx.cond(esta_activo, 'transparent', color_carrera + '44')}",
        box_shadow=rx.cond(
            esta_activo,
            f"0 4px 12px -2px {color_carrera}66",
            "none",
        ),
        font_weight="600",
        white_space="nowrap",
        display="inline-flex",
        align_items="center",
        transition="all 0.2s",
    )


def _grid_plan() -> rx.Component:
    """Grid con el plan de estudios agrupado por año."""
    carrera = EstadoInstitucional.carrera_destacada
    color_carrera = carrera["color_principal"]

    return rx.vstack(
        rx.box(
            rx.flex(
                rx.icon("book-open", size=20, color=color_carrera),
                rx.heading(
                    "Plan de Estudios",
                    size="4",
                    color=rx.color_mode_cond(light="#0f172a", dark="#f1f5f9"),
                ),
                align="center",
                gap="0.5rem",
                margin_bottom="1rem",
            ),
            rx.flex(
                rx.foreach(
                    carrera["plan_estudios"],
                    lambda anio, idx: _pastilla_anio_explorador(anio, idx),
                ),
                gap="0.5rem",
                flex_wrap="wrap",
                margin_bottom="1rem",
            ),
            width="100%",
        ),
        rx.flex(
            rx.text(
                "Materias del año: ",
                font_size="0.875rem",
                color=rx.color_mode_cond(light="#64748b", dark="#94a3b8"),
            ),
            rx.text(
                EstadoInstitucional.materias_anio_explorador.length().to_string(),
                font_size="0.875rem",
                font_weight="700",
                color=color_carrera,
                padding="0.125rem 0.5rem",
                background=color_carrera + "15",
                border_radius="9999px",
            ),
            align="center",
            gap="0.5rem",
            margin_bottom="1.5rem",
        ),
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
        max_width="64rem",
        margin="0 auto",
    )


# ======================================================================
# Sección: PERFIL PROFESIONAL
# ======================================================================

def _grid_perfil() -> rx.Component:
    """Grid con el perfil profesional."""
    return rx.grid(
        rx.foreach(
            EstadoInstitucional.perfil_carrera_destacada,
            lambda item, idx: _card_explorador(
                f"Habilidad {idx + 1}",
                item,
                "check-circle",
            ),
        ),
        columns=rx.breakpoints(initial="1", sm="2", lg="2"),
        spacing="3",
        width="100%",
        max_width="64rem",
        margin="0 auto",
    )


# ======================================================================
# Sección: CAMPO LABORAL
# ======================================================================

def _grid_campo() -> rx.Component:
    """Grid con el campo laboral."""
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
        max_width="64rem",
        margin="0 auto",
    )


# ======================================================================
# Sección: FAQ
# ======================================================================

class EstadoFAQ(rx.State):
    """Estado del acordeón de FAQ del explorador."""

    indice_faq_abierto: int = -1

    @rx.event
    def alternar_faq(self, indice: int):
        """Abre o cierra una pregunta del FAQ."""
        if self.indice_faq_abierto == indice:
            self.indice_faq_abierto = -1
        else:
            self.indice_faq_abierto = indice


def _item_faq_explorador(pregunta: dict, indice: int) -> rx.Component:
    """Item individual del FAQ con acordeón."""
    esta_abierta = EstadoFAQ.indice_faq_abierto == indice
    color_carrera = EstadoInstitucional.carrera_destacada["color_principal"]

    return rx.box(
        rx.box(
            rx.flex(
                rx.icon(
                    "help-circle",
                    size=18,
                    color=color_carrera,
                    flex_shrink="0",
                ),
                rx.text(
                    pregunta["pregunta"],
                    font_size="0.9375rem",
                    font_weight="600",
                    color=rx.color_mode_cond(light="#1e293b", dark="#f1f5f9"),
                    flex="1",
                ),
                rx.icon(
                    "chevron-down",
                    size=18,
                    color=rx.color_mode_cond(light="#64748b", dark="#94a3b8"),
                    transform=rx.cond(
                        esta_abierta,
                        "rotate(180deg)",
                        "rotate(0deg)",
                    ),
                    transition="transform 0.3s",
                    flex_shrink="0",
                ),
                align="center",
                gap="0.75rem",
                width="100%",
            ),
            on_click=lambda: EstadoFAQ.alternar_faq(indice),
            cursor="pointer",
            padding="1.125rem 1.25rem",
            role="button",
            tab_index=0,
            width="100%",
        ),
        rx.cond(
            esta_abierta,
            rx.box(
                rx.text(
                    pregunta["respuesta"],
                    font_size="0.875rem",
                    line_height="1.6",
                    color=rx.color_mode_cond(light="#475569", dark="#cbd5e1"),
                ),
                padding="0 1.25rem 1.25rem 3.25rem",
            ),
            rx.fragment(),
        ),
        width="100%",
        border=rx.cond(
            esta_abierta,
            f"1px solid {color_carrera}66",
            "1px solid "
            + rx.color_mode_cond(light="#e2e8f0", dark="#1e293b"),
        ),
        border_radius="0.875rem",
        background=rx.color_mode_cond(light="#ffffff", dark="#0f1117"),
        transition="all 0.2s",
        _hover={"border_color": color_carrera + "44"},
    )


def _grid_faq() -> rx.Component:
    """Grid con preguntas frecuentes específicas de la carrera."""
    return rx.vstack(
        rx.flex(
            rx.text(
                "Preguntas frecuentes de esta carrera",
                font_size="0.875rem",
                color=rx.color_mode_cond(light="#64748b", dark="#94a3b8"),
            ),
            rx.text(
                EstadoInstitucional.preguntas_frecuentes_carrera_destacada.length().to_string(),
                font_size="0.875rem",
                font_weight="700",
                color=EstadoInstitucional.carrera_destacada["color_principal"],
                padding="0.125rem 0.5rem",
                background=EstadoInstitucional.carrera_destacada["color_principal"] + "15",
                border_radius="9999px",
            ),
            align="center",
            gap="0.5rem",
            margin_bottom="1.5rem",
        ),
        rx.vstack(
            rx.foreach(
                EstadoInstitucional.preguntas_frecuentes_carrera_destacada,
                lambda pregunta, idx: _item_faq_explorador(pregunta, idx),
            ),
            width="100%",
            spacing="3",
        ),
        spacing="0",
        width="100%",
        max_width="64rem",
        margin="0 auto",
    )


# ======================================================================
# Contenido dinámico
# ======================================================================

def _contenido_explorador() -> rx.Component:
    """Renderiza el contenido dinámico según la sección activa."""
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
# Panel flotante de selección (también navega al detalle)
# ======================================================================

def _panel_flotante_selector() -> rx.Component:
    """
    Botón flotante que abre un panel con todas las carreras.

    Cada tarjeta del panel NAVEGA al detalle de la carrera.
    """
    return rx.box(
        rx.cond(
            EstadoInstitucional.mostrar_panel_flotante,
            rx.box(
                position="fixed",
                top="0",
                left="0",
                right="0",
                bottom="0",
                background="rgba(0,0,0,0.5)",
                backdrop_filter="blur(4px)",
                z_index="998",
                on_click=EstadoInstitucional.cerrar_panel_flotante,
                cursor="pointer",
            ),
            rx.fragment(),
        ),
        contenedor_clicable(
            rx.icon("layout-grid", size=22, color="#ffffff"),
            position="fixed",
            bottom="2rem",
            right="2rem",
            height="3.5rem",
            width="3.5rem",
            border_radius="9999px",
            background=rx.color("accent", 11),
            display="flex",
            align_items="center",
            justify_content="center",
            box_shadow="0 20px 40px -10px rgba(37, 99, 235, 0.5)",
            z_index="999",
            transition="all 0.3s",
            al_hacer_clic=EstadoInstitucional.alternar_panel_flotante,
            _hover={
                "transform": "scale(1.1)",
                "box_shadow": "0 25px 50px -12px rgba(37, 99, 235, 0.6)",
            },
        ),
        rx.cond(
            EstadoInstitucional.mostrar_panel_flotante,
            rx.box(
                rx.vstack(
                    rx.flex(
                        rx.heading(
                            "Elige una carrera",
                            size="4",
                            color=rx.color_mode_cond(light="#0f172a", dark="#f1f5f9"),
                        ),
                        contenedor_clicable(
                            rx.icon(
                                "x",
                                size=18,
                                color=rx.color_mode_cond(light="#64748b", dark="#94a3b8"),
                            ),
                            padding="0.5rem",
                            border_radius="0.5rem",
                            al_hacer_clic=EstadoInstitucional.cerrar_panel_flotante,
                            _hover={
                                "background": rx.color_mode_cond(light="#f1f5f9", dark="#1e293b"),
                            },
                        ),
                        align="center",
                        justify="between",
                        width="100%",
                        margin_bottom="1rem",
                    ),
                    rx.grid(
                        rx.foreach(
                            EstadoInstitucional.carreras,
                            _card_imagen_carrera,
                        ),
                        columns=rx.breakpoints(initial="1", sm="2"),
                        spacing="3",
                        width="100%",
                    ),
                    spacing="2",
                    width="100%",
                ),
                position="fixed",
                bottom="6rem",
                right="2rem",
                width=["calc(100% - 4rem)", "calc(100% - 4rem)", "24rem", "28rem"],
                max_height="70vh",
                overflow_y="auto",
                padding="1.5rem",
                border_radius="1.25rem",
                background=rx.color_mode_cond(light="#ffffff", dark="#0f1117"),
                border="1px solid "
                + rx.color_mode_cond(light="#e2e8f0", dark="#1e293b"),
                box_shadow="0 30px 60px -15px rgba(0,0,0,0.4)",
                z_index="999",
                animation="deslizar_desde_abajo 0.3s ease-out",
            ),
            rx.fragment(),
        ),
    )


# ======================================================================
# Explorador completo
# ======================================================================

def explorador_carrera_destacada() -> rx.Component:
    """
    Explorador completo estilo Leonardo AI con navegación al detalle.

    - Buscador de carreras.
    - Grid de imágenes que navegan a `/carrera/{id}`.
    - Panel flotante de acceso rápido.
    """
    return rx.box(
        _panel_flotante_selector(),
        rx.vstack(
            _buscador_carreras(),
            _grid_imagenes_carreras(),
            width="100%",
            align="center",
            spacing="4",
            padding="2rem 1.5rem",
            max_width="72rem",
            margin="0 auto",
        ),
        width="100%",
        position="relative",
    )