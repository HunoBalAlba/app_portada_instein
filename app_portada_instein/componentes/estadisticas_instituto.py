"""
Bloque de estadísticas del instituto con iconos grandes
(inspirado en la sección de features de Discord).
"""

import reflex as rx


ESTADISTICAS: list[dict] = [
    {
        "valor": "5",
        "etiqueta": "Carreras Técnicas",
        "icono": "graduation-cap",
        "color": "#2563eb",
    },
    {
        "valor": "15+",
        "etiqueta": "Años de Experiencia",
        "icono": "award",
        "color": "#0891b2",
    },
    {
        "valor": "500+",
        "etiqueta": "Egresados",
        "icono": "users",
        "color": "#7c3aed",
    },
    {
        "valor": "100%",
        "etiqueta": "Empleabilidad",
        "icono": "trending-up",
        "color": "#16a34a",
    },
]


def _tarjeta_estadistica(stat: dict) -> rx.Component:
    """Renderiza una tarjeta individual de estadística."""
    return rx.box(
        rx.vstack(
            # --- Icono grande con halo ---
            rx.box(
                rx.icon(stat["icono"], size=28, color="#ffffff"),
                padding="1rem",
                border_radius="1rem",
                background=stat["color"],
                box_shadow=f"0 10px 25px -5px {stat['color']}88",
                display="flex",
                align_items="center",
                justify_content="center",
                margin_bottom="1rem",
            ),
            # --- Valor grande ---
            rx.heading(
                stat["valor"],
                size="7",
                color=rx.color_mode_cond(light="#0f172a", dark="#f1f5f9"),
            ),
            # --- Etiqueta ---
            rx.text(
                stat["etiqueta"],
                font_size="0.75rem",
                font_weight="600",
                letter_spacing="0.05em",
                text_transform="uppercase",
                color=rx.color_mode_cond(light="#64748b", dark="#94a3b8"),
            ),
            align="center",
            spacing="2",
        ),
        padding="1.75rem 1rem",
        border_radius="1.25rem",
        border=("1px solid " + rx.color_mode_cond(light="#e2e8f0", dark="#1e293b")),
        background=rx.color_mode_cond(light="#ffffff", dark="#0f1117"),
        flex="1",
        min_width="0",
        text_align="center",
        transition="all 0.3s",
        _hover={
            "transform": "translateY(-4px)",
            "border_color": stat["color"] + "88",
            "box_shadow": f"0 20px 40px -10px {stat['color']}55",
        },
    )


def seccion_estadisticas() -> rx.Component:
    """Bloque completo con todas las estadísticas del instituto."""
    return rx.box(
        rx.flex(
            *[_tarjeta_estadistica(s) for s in ESTADISTICAS],
            gap="1rem",
            width="100%",
            flex_direction=["column", "column", "row", "row"],
        ),
        width="100%",
        padding="2rem 1.5rem",
    )
