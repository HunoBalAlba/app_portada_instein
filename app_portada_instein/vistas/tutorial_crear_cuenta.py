
import reflex as rx

def imagen_16_9():
    return rx.aspect_ratio(
        rx.image(
            src="/gif_1.gif",
            width="100%",
            height="100%",
        ),
        ratio=16/9,
    )
def imagen_16_9_impaar():
    return rx.box(
        rx.inset(
                        rx.image(
                            # src="/Diseño sin título.png",
                            src="/desk_m.gif",
                            # src="/conta_2.avif",
                            # src="/web_site.avif",
                            # src="https://web.reflex-assets.dev/other/reflex_banner.png",
                            alt="Carrera banner",
                            # width="100%",
                            height="auto",
                            width="auto",
                            # height="100%",
                        ),
                        side="top",
                        pt="current",
                        
                    ),
        #     rx.aspect_ratio(
        #     rx.image(
        #         src="/desk_m.gif",
        #         width="100%",
        #         height="100%",
        #     ),
        #     ratio=16/9,
        # ),
        # width=["240px", "280px", "360px", "420px", "500px"],
    )

def tutorial_crear_cuenta_usuario(titulo:str, sub_titulo: str, horario: str,inicio_clases:str)->rx.Component:
    return rx.card(
        
        rx.inset(
                        rx.image(
                            # src="/Diseño sin título.png",
                            #src="/desk_m.gif",
                            src="/laptop2.webp",
                            # src="/conta_2.avif",
                            # src="/web_site.avif",
                            # src="https://web.reflex-assets.dev/other/reflex_banner.png",
                            alt="Carrera banner",
                            width="100%",
                            height="auto",
                            #width="auto",
                            max_height="20rem",
                        ),
                        #width="100%",
                        side="top",
                        pb="current",
                        
                    ),
        # rx.hstack(
        #         rx.video(url=rx.get_upload_url("video.mp4"),width="200px"),
        #         #rx.image(src="/gif_1.gif",width="300px",border_radius="15px,50px"),
        #     ),
        
        rx.vstack(
            #imagen_16_9_impaar(),
                # rx.inset(
                #     # rx.image(
                #     #     src="/python_I.webp",
                #     #     width="100%",
                #     #     height="auto",
                #     # ),
                # imagen_16_9_impaar(),
                #     side="top",
                #     pb="current",
                # ),
                # rx.text(
                #     sub_titulo,
                # ),

                rx.flex(
                    #rx.flex(
                        #rx.avatar(fallback=initials),
                        # rx.flex(
                        #     rx.image(
                        #         src="/avatar_1.svg",
                        #         #width="100%",
                        #         width="auto",
                        #         height="50px",
                        #     ),
                        #     align_items="center",
                        # ),
                        
                        rx.flex(
                            rx.heading("Plataforma web de seguimiento academico ", size="6", weight="bold",align="center"),
                            # rx.text(
                            #     "Acceda a su historial Academico", size="1", color_scheme="gray"
                            # ), Inicie una cuenta institucional
                            
                            rx.text(
                                    "Inicie una cuenta institucional ", size="2", color_scheme="gray"
                                ),
                            rx.badge("Acceda a su Historial Académico", variant="outline",size="1",),
                                
                            align="center",
                            justify="center",
                            direction="column",
                            spacing="2",
                            width="100%",

                        ),
                        
                    #     direction="row",
                    #     align_items="left",
                    #     spacing="2",
                    # ),
                    
                    # rx.flex(
                    #     dialog_mostrar_detalles_curso(titulo,sub_titulo,horario,inicio_clases),
                    #     #rx.icon(tag="square-arrow-out-up-right"),
                    #     align_items="center",
                    # ),
                justify="between",
                width="100%",
                ),
                rx.button("Crear Cuenta",rx.icon(tag="trending-up"),variant="solid",width="100%",),#arrow-big-up
            
        # colocar temṕorizador
        #cuenta_regresiva(),
        spacing="2",
        width="100%",
        ),
        #width="100%",
        spacing="2",
        max_width="50rem",
    ),

def cuadro_de_tutorial()->rx.Component:
    return rx.box(
        tutorial_crear_cuenta_usuario("Como crear una cuenta de usuario", "PY", "Lunes -viernes 19:00-21:00","20 de Abril, 2025"),
        #tutorial_crear_cuenta_usuario("Machine Learning", "ML", "Lunes -viernes 19:00-21:00               gsto","20 de Abril, 2025"),
                
    )


##############################

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
        #style={"height": 300},
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
        #width="360px",
        #height="",
    )

def video_e_imagenes_ultima_publicacion():
    return rx.box(
        rx.flex(
            #cabecera_del_archivos_multimedia(),
            
            segment_control_video_y_portada_curso(),
            ver_archivos_multimedia_9_16(),

            justify="between",
            direction="column",
            spacing="1",
            #align="center",
        ),
    )