import reflex as rx
def titulo_del_ultimo_curso_publicado():
    return rx.flex(
        #rx.he("titulo",size="9"),
        #rx.heading("Machine learning - Python", size="9", weight="bold"),

        #rx.heading("blockchain descentralizado", size="8"),
        # rx.vstack(
        #     rx.text(
        #         "Formando profesionales de excelencia con título en Provisión Nacional bajo resoluciones ministeriales vigentes.",
        #         size="6",
        #         color="gray",
        #     ),
        #     rx.heading("cursos de actualización ",size="6"),
        #     rx.text(
        #         "para todo publico.",
        #         size="6",
        #         color="gray",
        #     ),
            
        # ),
        # rx.el.h1(
        #             "Forja tu Futuro como ",
        #             rx.el.span(
        #                 "Profesional Técnico Superior",
        #                 class_name="text-indigo-600 dark:text-indigo-400",
        #             ),
        #             class_name="text-4xl sm:text-5xl md:text-6xl font-black text-gray-900 dark:text-white tracking-tight leading-none mb-6",
        #         ),
        #         rx.el.p(
        #             "Sólida formación práctica con títulos de Provisión Nacional oficial. Estudia Sistemas Informáticos, Comercio Internacional, Electrónica, Contaduría y Secretariado Ejecutivo con equipamiento avanzado.",
        #             class_name="text-lg text-gray-600 dark:text-gray-300 max-w-2xl mb-8",
        #         ),
        rx.heading(
            "Forja tu Futuro como ",
            rx.text.span( "Profesional Técnico Superior", color=rx.color("accent", 11)),
            "",
            size="8"
        ),
        rx.text(
            "Sólida formación práctica con títulos de Provisión Nacional oficial. Estudia Sistemas Informáticos, Comercio Internacional, Electrónica, Contaduría y Secretariado Ejecutivo con equipamiento avanzado.",
            color_scheme="gray"        
        ),
        
        #rx.text("Aprenderas a crear predicciones basado en datos.",size="4"),
        rx.flex(
            rx.button("Más informacion",rx.icon(tag="info"),variant="outline"),#square-arrow-out-up-right #info #inspection_pane
            rx.button("Crear Cuenta Institucional",rx.icon(tag="square-arrow-out-up-right"),variant="solid"),#arrow-big-up
            # direction="row",
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
                # rx.aspect_ratio(
                #     rx.image(
                #         #src="/python_I.webp",#fondo_2.jpg
                #         src="/fondo_2.jpg",
                #         width="100%",
                #         height="100%",
                #     ),
                #     ratio=16/9,
                #     #side="bottom",
                # ),
                #rx.icon(tag="award",size=200,color="indigo"),
                #award

                rx.image(
                    #src="/python-svgrepo-com.svg",#attach-svgrepo-com
                    src="/bitcoin-svgrepo-com.svg",#bitcoin-svgrepo-com
                    #width="100%",

                    width="auto",
                    height="auto",
                    #height="250px",

                ),

                #align_items="center",
                #direction="column",
                #spacing="9",
                
                justify="center",
                align="center",
                height="100%",
                width="100%",
            ),
# rx.video(
#     src="https://www.youtube.com/embed/9bZkp7q19f0",
#     width="400px",
#     height="auto",
# )
def video_informacion_instein()->rx.Component:
    return rx.box(
            rx.video(
                src="https://youtu.be/uP00VWRCsrw?si=weTRFYQ81EBH6jXe", min_width="250px", height="auto",
                ),#https://www.youtube.com/watch?v=Hy3uhBVRdtk&t=13s
            #rx.video(url="https://www.youtube.com/watch?v=BGKlxg3L2Y8", width="400px", height="auto"),#https://www.youtube.com/watch?v=Hy3uhBVRdtk&t=13s
            border_radius="1rem",
            padding="0.3em",
            background="#0c0b0b",
            #min_width=["0px", "320px", "480px", "640px", "800px"],
            border="1px solid rgba(255,255,255,0.1)",
        ),

def card_ultimo_curso_portal_inicio():
    return rx.flex(
        #cabecera_de_detalle_curso(),
        rx.flex(
            rx.box(titulo_del_ultimo_curso_publicado(), 
                   padding="2em",
                   #background=rx.color("accent",8),
                   width=["100%", "100%", "100%", "60%"]),
            rx.box(video_informacion_instein(),
                   padding="1em",
                   #background=rx.color("accent",8),
                    width=["100%", "100%", "100%", "40%"]),
                        
            #spacing="5",
            width="100%",
            justify="center",
            align="center",
            flex_direction=["column", "column", "column", "row"],
        ),
        #pie_de_detalle_de_curso(),
    )

def portada_inicio_con_video()->rx.Component:
        return rx.center(
        rx.box(
            # rx.hstack(
            #     card_mostrar_mas_detalle_de_curso_publicado("titulo","sub_titulo","horario","inicio_clases"),
            #     max_width="800px",
            #     #max_width="900px",
            #     padding="0.5em",
            #     #padding="1.5em",
            #     border=f"1px solid {rx.color('accent', 7)}",
            #     border_radius="15px",
            #     #border_radius="25px",
            #     width="100%",
            #     # justify="center",
            #     # align="center",
            # ),
            rx.box(
                #card_mostrar_mas_detalle_de_curso_publicado("titulo","sub_titulo","horario","inicio_clases"),
                card_ultimo_curso_portal_inicio(),

                #max_width="900px",
                max_width="72rem",
                #max_width="900px",
                #padding="3em",
                #padding="1.5em",
                #border=f"1px solid {rx.color('accent', 8)}",
                border_radius="15px",
                #border_radius="25px",
                width="100%",
                # justify="center",
                # align="center",
            ),
        ),
    )

