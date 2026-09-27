"""
Sección "¿Por qué elegir INSTEIN?" con cards de features
estilo Qdrant: icono + título + descripción + link "Ver más →".
"""

import reflex as rx


RAZONES: list[dict] = [
    {
        "icono": "award",
        "titulo": "Título de Provisión Nacional",
        "descripcion": (
            "Todos nuestros títulos están autorizados por el Ministerio de "
            "Educación con Resolución Ministerial R.M. 0871/2016."
        ),
        "color": "#2563eb",
    },
    {
        "icono": "briefcase",
        "titulo": "Formación Práctica",
        "descripcion": (
            "Laboratorios equipados y docentes especializados con experiencia "
            "real en el campo profesional."
        ),
        "color": "#0891b2",
    },
    {
        "icono": "users",
        "titulo": "Alta Empleabilidad",
        "descripcion": (
            "El 100% de nuestros egresados encuentra trabajo en su área "
            "en menos de 6 meses tras graduarse."
        ),
        "color": "#7c3aed",
    },
    {
        "icono": "building-2",
        "titulo": "Convenios Empresariales",
        "descripcion": (
            "Prácticas profesionales garantizadas en empresas líderes "
            "de la región y del país."
        ),
        "color": "#ea580c",
    },
    {
        "icono": "book-open",
        "titulo": "Formación Integral",
        "descripcion": (
            "Además de la técnica, desarrollamos habilidades blandas, "
            "liderazgo y pensamiento crítico."
        ),
        "color": "#16a34a",
    },
    {
        "icono": "heart",
        "titulo": "Comunidad",
        "descripcion": (
            "Una red de 500+ egresados que se apoyan mutuamente y "
            "comparten oportunidades profesionales."
        ),
        "color": "#db2777",
    },
]


def _tarjeta_razon(razon: dict) -> rx.Component:
    """Tarjeta individual de razón para elegir INSTEIN."""
    return rx.box(
        rx.vstack(
            # --- Icono ---
            rx.box(
                rx.icon(razon["icono"], size=24, color=razon["color"]),
                padding="0.75rem",
                border_radius="0.875rem",
                background=razon["color"] + "15",
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
                color=rx.color_mode_cond(light="#0f172a", dark="#f1f5f9"),
                font_weight="700",
            ),
            # --- Descripción ---
            rx.text(
                razon["descripcion"],
                font_size="0.875rem",
                line_height="1.6",
                color=rx.color_mode_cond(light="#475569", dark="#94a3b8"),
            ),
            # --- Link "Ver más →" ---
            rx.flex(
                rx.text(
                    "Ver más",
                    font_size="0.875rem",
                    font_weight="600",
                    color=razon["color"],
                ),
                rx.icon("arrow-right", size=14, color=razon["color"]),
                align="center",
                gap="0.25rem",
                margin_top="0.5rem",
                transition="all 0.2s",
            ),
            align="start",
            spacing="1",
            width="100%",
        ),
        padding="1.5rem",
        border_radius="1.25rem",
        border=(
            "1px solid "
            + rx.color_mode_cond(light="#e2e8f0", dark="#1e293b")
        ),
        background=rx.color_mode_cond(light="#ffffff", dark="#0f1117"),
        transition="all 0.3s",
        width="100%",
        height="100%",
        _hover={
            "transform": "translateY(-4px)",
            "border_color": razon["color"] + "66",
            "box_shadow": f"0 20px 40px -10px {razon['color']}33",
        },
    )


def seccion_por_que_instein() -> rx.Component:
    """
    Sección completa "¿Por qué elegir INSTEIN?" con grid de razones.
    """
    return rx.box(
        rx.vstack(
            # --- Encabezado ---
            rx.vstack(
                rx.text(
                    "¿POR QUÉ INSTEIN?",
                    font_size="0.75rem",
                    font_weight="700",
                    letter_spacing="0.15em",
                    color=rx.color("accent", 11),
                ),
                rx.heading(
                    "Formación que transforma",
                    size="7",
                    color=rx.color_mode_cond(light="#0f172a", dark="#f1f5f9"),
                    text_align="center",
                ),
                rx.text(
                    "Todo lo que necesitas para convertirte en un profesional "
                    "técnico de excelencia está en INSTEIN.",
                    font_size="1rem",
                    color=rx.color_mode_cond(light="#475569", dark="#94a3b8"),
                    text_align="center",
                    max_width="42rem",
                ),
                align="center",
                spacing="2",
                margin_bottom="3rem",
            ),
            # --- Grid de razones ---
            rx.grid(
                *[_tarjeta_razon(r) for r in RAZONES],
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