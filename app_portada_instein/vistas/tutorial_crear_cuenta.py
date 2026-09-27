import reflex as rx


def imagen_16_9():
    return rx.aspect_ratio(
        rx.image(
            src="/gif_1.gif",
            width="100%",
            height="100%",
        ),
        ratio=16 / 9,
    )


def imagen_16_9_impaar():
    return rx.box(
        rx.inset(
            rx.image(
                src="/desk_m.gif",
                alt="Carrera banner",
                height="auto",
                width="auto",
            ),
            side="top",
            pt="current",
        ),
    )


def tutorial_crear_cuenta_usuario(
    titulo: str,
    sub_titulo: str,
    horario: str,
    inicio_clases: str,
) -> rx.Component:
    return rx.card(
        rx.inset(
            rx.image(
                src="/laptop2.webp",
                alt="Carrera banner",
                width="100%",
                height="auto",
                max_height="20rem",
            ),
            side="top",
            pb="current",
        ),
        rx.vstack(
            rx.flex(
                rx.flex(
                    rx.heading(
                        "Plataforma web de seguimiento academico ",
                        size="6",
                        weight="bold",
                        align="center",
                    ),
                    rx.text(
                        "Inicie una cuenta institucional ",
                        size="2",
                        color_scheme="gray",
                    ),
                    rx.badge(
                        "Acceda a su Historial Académico",
                        variant="outline",
                        size="1",
                    ),
                    align="center",
                    justify="center",
                    direction="column",
                    spacing="2",
                    width="100%",
                ),
                justify="between",
                width="100%",
            ),
            rx.button(
                "Crear Cuenta",
                rx.icon(tag="trending-up"),
                variant="solid",
                width="100%",
            ),
            spacing="2",
            width="100%",
        ),
        spacing="2",
        max_width="50rem",
    )


def cuadro_de_tutorial() -> rx.Component:
    return rx.box(
        tutorial_crear_cuenta_usuario(
            "Como crear una cuenta de usuario",
            "PY",
            "Lunes -viernes 19:00-21:00",
            "20 de Abril, 2025",
        ),
    )


class State(rx.State):
    opcion: str = "video2"


def ver_archivos_multimedia_9_16():
    return rx.vstack(
        rx.cond(
            State.opcion == "video1",
            rx.box(
                rx.aspect_ratio(
                    rx.video(
                        src="/video1.mp4",
                        width="100%",
                        height="100%",
                    ),
                    ratio=9 / 16,
                ),
                width=["240px", "280px", "360px", "420px", "500px"],
            ),
            rx.box(
                rx.aspect_ratio(
                    rx.video(
                        src="/tutorial.mp4",
                        width="100%",
                        height="100%",
                    ),
                    ratio=9 / 16,
                ),
                width=["240px", "280px", "360px", "420px", "500px"],
            ),
        ),
        width="100%",
    )


def segment_control_video_y_portada_curso():
    return rx.vstack(
        rx.segmented_control.root(
            rx.segmented_control.item("Crear cuenta", value="video2"),
            rx.segmented_control.item("Inicio de Sesion", value="video1"),
            on_change=State.setvar("opcion"),
            value=State.opcion,
            side="bottom",
        ),
    )


def video_e_imagenes_ultima_publicacion():
    return rx.box(
        rx.flex(
            segment_control_video_y_portada_curso(),
            ver_archivos_multimedia_9_16(),
            justify="between",
            direction="column",
            spacing="1",
        ),
    )