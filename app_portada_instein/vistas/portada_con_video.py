import reflex as rx


def titulo_del_ultimo_curso_publicado():
    return rx.flex(
        rx.heading(
            "Forja tu Futuro como ",
            rx.text.span("Profesional Técnico Superior", color=rx.color("accent", 11)),
            "",
            size="8",
        ),
        rx.text(
            "Sólida formación práctica con títulos de Provisión Nacional oficial. "
            "Estudia Sistemas Informáticos, Comercio Internacional, Electrónica, "
            "Contaduría y Secretariado Ejecutivo con equipamiento avanzado.",
            color_scheme="gray",
        ),
        rx.flex(
            rx.button("Más informacion", rx.icon(tag="info"), variant="outline"),
            rx.button(
                "Crear Cuenta Institucional",
                rx.icon(tag="square-arrow-out-up-right"),
                variant="solid",
            ),
            flex_direction=["column", "row", "row", "row"],
            spacing="2",
            justify="center",
            align="center",
            height="100%",
            width="100%",
        ),
        direction="column",
        spacing="2",
        justify="center",
        align="center",
        height="100%",
        width="100%",
    )


def icono_principal_de_curso():
    return rx.hstack(
        rx.image(
            src="/bitcoin-svgrepo-com.svg",
            width="auto",
            height="auto",
        ),
        justify="center",
        align="center",
        height="100%",
        width="100%",
    )


def video_informacion_instein() -> rx.Component:
    return rx.box(
        rx.video(
            src="https://youtu.be/uP00VWRCsrw?si=weTRFYQ81EBH6jXe",
            min_width="250px",
            height="auto",
        ),
        border_radius="1rem",
        padding="0.3em",
        background="#0c0b0b",
        border="1px solid rgba(255,255,255,0.1)",
    )


def card_ultimo_curso_portal_inicio():
    return rx.flex(
        rx.flex(
            rx.box(
                titulo_del_ultimo_curso_publicado(),
                padding="2em",
                width=["100%", "100%", "100%", "60%"],
            ),
            rx.box(
                video_informacion_instein(),
                padding="1em",
                width=["100%", "100%", "100%", "40%"],
            ),
            width="100%",
            justify="center",
            align="center",
            flex_direction=["column", "column", "column", "row"],
        ),
    )


def portada_inicio_con_video() -> rx.Component:
    return rx.center(
        rx.box(
            rx.box(
                card_ultimo_curso_portal_inicio(),
                max_width="72rem",
                border_radius="15px",
                width="100%",
            ),
        ),
    )
