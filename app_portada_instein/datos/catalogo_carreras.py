"""
Catálogo estático de carreras ofrecidas por el instituto.

Cada carrera define 4 iconos animados con órbitas elípticas keplerianas
achatadas verticalmente (perspectiva 3D tipo "disco visto de lado").

Los semiejes mayores están calibrados para que las órbitas se alejen
visiblemente del centro y cada icono tenga su propia trayectoria.
"""

from ..datos.modelos_carrera import Carrera, IconoAnimado


PALETA_COLORES: list[tuple[str, str]] = [
    ("#2563eb", "#eff6ff"),
    ("#0891b2", "#ecfeff"),
    ("#7c3aed", "#f5f3ff"),
    ("#ea580c", "#fff7ed"),
    ("#16a34a", "#f0fdf4"),
    ("#db2777", "#fdf2f8"),
    ("#0d9488", "#f0fdfa"),
    ("#d97706", "#fffbeb"),
    ("#4f46e5", "#eef2ff"),
    ("#dc2626", "#fef2f2"),
    ("#059669", "#ecfdf5"),
    ("#9333ea", "#faf5ff"),
]


def _icono_orbital_config(
    nombre: str,
    semieje_mayor: float,
    excentricidad: float,
    factor_perspectiva: float,
    angulo_inicial: int,
    periodo: float,
    desfase_temporal: float,
    color: str,
    tiene_anillos: bool = False,
) -> IconoAnimado:
    """
    Construye un IconoAnimado con los parámetros orbitales de su elipse.

    Args:
        nombre: Identificador del icono Lucide.
        semieje_mayor: Radio horizontal de la elipse en % del contenedor.
        excentricidad: Excentricidad orbital (0 = círculo).
        factor_perspectiva: Aplanamiento vertical (0.5 = disco de lado).
        angulo_inicial: Ángulo inicial en grados.
        periodo: Duración de una vuelta completa en segundos.
        desfase_temporal: Retraso inicial en segundos.
        color: Color hex del icono.
        tiene_anillos: Si debe dibujarse con anillos tipo Saturno.

    Returns:
        Diccionario IconoAnimado listo para renderizar.
    """
    sufijo = f"{angulo_inicial}_{int(semieje_mayor * 10)}"

    return {
        "nombre": nombre,
        "semieje_mayor": semieje_mayor,
        "excentricidad": excentricidad,
        "factor_perspectiva": factor_perspectiva,
        "angulo_inicial": angulo_inicial,
        "periodo": periodo,
        "desfase_temporal": desfase_temporal,
        "color": color,
        "tiene_anillos": tiene_anillos,
        "keyframe_orbita": f"orbita_{sufijo}",
    }


# Factor de aplanamiento por defecto (equivale a INCLINACION = 0.5).
PERSPECTIVA_DEFECTO = 0.5


CATALOGO_CARRERAS: list[Carrera] = [
    # ------------------------------------------------------------------
    # Carrera 0 — Sistemas Informáticos
    # ------------------------------------------------------------------
    {
        "id": 0,
        "nombre": "Sistemas Informáticos",
        "nombre_corto": "Sistemas",
        "duracion": "3 Años",
        "lema": "Tecnología, desarrollo y soluciones digitales",
        "descripcion": (
            "El Técnico Superior en Sistemas Informáticos es un profesional integral "
            "capacitado para diseñar, desarrollar, implementar y mantener soluciones "
            "informáticas orientadas a las necesidades de empresas, instituciones y "
            "emprendimientos."
        ),
        "perfil_profesional": [
            "Desarrollo de software y aplicaciones web y móviles.",
            "Administración de bases de datos y sistemas de información.",
            "Instalación y mantenimiento de redes y equipos informáticos.",
            "Soporte técnico especializado en hardware y software.",
            "Aplicación de buenas prácticas de ciberseguridad.",
        ],
        "campo_laboral": [
            "Empresas de desarrollo de software.",
            "Departamentos de TI en instituciones públicas y privadas.",
            "Emprendimientos tecnológicos independientes.",
            "Soporte técnico y consultoría informática.",
        ],
        "plan_estudios": [
            {
                "anio": "Primer Año",
                "materias": [
                    "Introducción a la Informática",
                    "Matemática Aplicada",
                    "Lógica de Programación",
                    "Ofimática Avanzada",
                    "Ensamblaje y Mantenimiento de PCs",
                    "Comunicación y Redacción",
                    "Inglés Técnico I",
                ],
            },
            {
                "anio": "Segundo Año",
                "materias": [
                    "Programación Estructurada",
                    "Base de Datos I",
                    "Redes de Computadoras I",
                    "Diseño Web (HTML/CSS/JS)",
                    "Sistemas Operativos",
                    "Contabilidad Básica",
                    "Inglés Técnico II",
                ],
            },
            {
                "anio": "Tercer Año",
                "materias": [
                    "Programación Orientada a Objetos",
                    "Base de Datos II",
                    "Redes de Computadoras II",
                    "Desarrollo de Aplicaciones Web",
                    "Desarrollo de Aplicaciones Móviles",
                    "Seguridad Informática",
                    "Proyecto de Grado",
                ],
            },
        ],
        "icono": "cpu",
        "color_principal": "#2563eb",
        "color_suave": "#eff6ff",
        "imagen_archivo": "sistemas.png",
        "iconos_animados": [
            _icono_orbital_config("code-2", 55.0, 0.25, PERSPECTIVA_DEFECTO, 0, 18.0, 0.0, "#2563eb", True),
            _icono_orbital_config("database", 70.0, 0.15, PERSPECTIVA_DEFECTO, 90, 24.0, 3.0, "#0891b2"),
            _icono_orbital_config("wifi", 62.0, 0.30, PERSPECTIVA_DEFECTO, 180, 21.0, 6.0, "#7c3aed"),
            _icono_orbital_config("terminal", 85.0, 0.20, PERSPECTIVA_DEFECTO, 270, 27.0, 9.0, "#ea580c"),
        ],
    },

    # ------------------------------------------------------------------
    # Carrera 1 — Contaduría General
    # ------------------------------------------------------------------
    {
        "id": 1,
        "nombre": "Contaduría General",
        "nombre_corto": "Contaduría",
        "duracion": "3 Años",
        "lema": "Gestión contable, tributaria y financiera",
        "descripcion": (
            "El Técnico Superior en Contaduría General es un profesional preparado "
            "para llevar registros contables, elaborar estados financieros, gestionar "
            "obligaciones tributarias y asesorar a empresas y emprendimientos."
        ),
        "perfil_profesional": [
            "Registro y análisis de operaciones contables.",
            "Elaboración de estados financieros y balances.",
            "Gestión de impuestos y obligaciones tributarias.",
            "Manejo de sistemas contables computarizados.",
            "Asesoramiento financiero a empresas y emprendedores.",
        ],
        "campo_laboral": [
            "Departamentos contables de empresas privadas.",
            "Instituciones públicas y organizaciones sin fines de lucro.",
            "Estudios contables y de auditoría.",
            "Emprendimientos propios como asesor contable.",
        ],
        "plan_estudios": [
            {
                "anio": "Primer Año",
                "materias": [
                    "Contabilidad Básica",
                    "Matemática Financiera",
                    "Documentos Mercantiles",
                    "Ofimática Aplicada",
                    "Introducción al Derecho",
                    "Comunicación y Redacción",
                    "Inglés Técnico I",
                ],
            },
            {
                "anio": "Segundo Año",
                "materias": [
                    "Contabilidad Intermedia",
                    "Contabilidad de Costos",
                    "Legislación Tributaria",
                    "Sistemas Contables Computarizados",
                    "Derecho Comercial",
                    "Estadística Aplicada",
                    "Inglés Técnico II",
                ],
            },
            {
                "anio": "Tercer Año",
                "materias": [
                    "Contabilidad Superior",
                    "Auditoría",
                    "Análisis de Estados Financieros",
                    "Contabilidad Gubernamental",
                    "Legislación Laboral y Social",
                    "Ética Profesional",
                    "Proyecto de Grado",
                ],
            },
        ],
        "icono": "calculator",
        "color_principal": "#0891b2",
        "color_suave": "#ecfeff",
        "imagen_archivo": "contaduria.png",
        "iconos_animados": [
            _icono_orbital_config("receipt", 55.0, 0.25, PERSPECTIVA_DEFECTO, 0, 18.0, 0.0, "#0891b2", True),
            _icono_orbital_config("coins", 70.0, 0.15, PERSPECTIVA_DEFECTO, 90, 24.0, 3.0, "#16a34a"),
            _icono_orbital_config("chart-line", 62.0, 0.30, PERSPECTIVA_DEFECTO, 180, 21.0, 6.0, "#ea580c"),
            _icono_orbital_config("wallet", 85.0, 0.20, PERSPECTIVA_DEFECTO, 270, 27.0, 9.0, "#7c3aed"),
        ],
    },

    # ------------------------------------------------------------------
    # Carrera 2 — Secretariado Ejecutivo
    # ------------------------------------------------------------------
    {
        "id": 2,
        "nombre": "Secretariado Ejecutivo",
        "nombre_corto": "Secretariado",
        "duracion": "3 Años",
        "lema": "Gestión administrativa y organización ejecutiva",
        "descripcion": (
            "El Técnico Superior en Secretariado Ejecutivo es un profesional altamente "
            "capacitado en la gestión administrativa, organización de agendas ejecutivas, "
            "atención al cliente, redacción de documentos y manejo de herramientas "
            "ofimáticas."
        ),
        "perfil_profesional": [
            "Redacción y gestión de correspondencia oficial.",
            "Organización de agendas, reuniones y eventos ejecutivos.",
            "Manejo avanzado de herramientas ofimáticas.",
            "Atención al cliente y protocolo empresarial.",
            "Gestión documental y archivo digital.",
        ],
        "campo_laboral": [
            "Gerencias y direcciones ejecutivas.",
            "Instituciones públicas y privadas.",
            "Recepción y atención al cliente.",
            "Coordinación de eventos corporativos.",
        ],
        "plan_estudios": [
            {
                "anio": "Primer Año",
                "materias": [
                    "Técnicas de Secretariado I",
                    "Ofimática Básica",
                    "Redacción y Ortografía",
                    "Introducción a la Administración",
                    "Documentos Mercantiles",
                    "Relaciones Humanas",
                    "Inglés Técnico I",
                ],
            },
            {
                "anio": "Segundo Año",
                "materias": [
                    "Técnicas de Secretariado II",
                    "Ofimática Avanzada",
                    "Contabilidad Básica",
                    "Legislación Laboral",
                    "Comunicación Empresarial",
                    "Protocolo y Etiqueta",
                    "Inglés Técnico II",
                ],
            },
            {
                "anio": "Tercer Año",
                "materias": [
                    "Gestión Ejecutiva",
                    "Administración de Recursos Humanos",
                    "Marketing y Atención al Cliente",
                    "Organización de Eventos",
                    "Gestión Documental Digital",
                    "Ética Profesional",
                    "Proyecto de Grado",
                ],
            },
        ],
        "icono": "briefcase",
        "color_principal": "#7c3aed",
        "color_suave": "#f5f3ff",
        "imagen_archivo": "secretariado.png",
        "iconos_animados": [
            _icono_orbital_config("calendar-clock", 55.0, 0.25, PERSPECTIVA_DEFECTO, 0, 18.0, 0.0, "#7c3aed", True),
            _icono_orbital_config("mail", 70.0, 0.15, PERSPECTIVA_DEFECTO, 90, 24.0, 3.0, "#db2777"),
            _icono_orbital_config("users", 62.0, 0.30, PERSPECTIVA_DEFECTO, 180, 21.0, 6.0, "#0891b2"),
            _icono_orbital_config("file-text", 85.0, 0.20, PERSPECTIVA_DEFECTO, 270, 27.0, 9.0, "#ea580c"),
        ],
    },

    # ------------------------------------------------------------------
    # Carrera 3 — Comercio Internacional
    # ------------------------------------------------------------------
    {
        "id": 3,
        "nombre": "Comercio Internacional y Administración Aduanera",
        "nombre_corto": "Comercio Int.",
        "duracion": "3 Años",
        "lema": "Comercio exterior, aduanas y logística global",
        "descripcion": (
            "El Técnico Superior en Comercio Internacional y Administración Aduanera "
            "es un profesional capacitado para gestionar operaciones de importación y "
            "exportación, trámites aduaneros, logística internacional y negociaciones "
            "comerciales."
        ),
        "perfil_profesional": [
            "Gestión de trámites de importación y exportación.",
            "Aplicación de normativa aduanera nacional e internacional.",
            "Coordinación de logística y transporte internacional.",
            "Negociación en mercados internacionales.",
            "Manejo de tratados comerciales y regímenes aduaneros.",
        ],
        "campo_laboral": [
            "Agencias despachantes de aduana.",
            "Empresas importadoras y exportadoras.",
            "Operadores logísticos y de transporte internacional.",
            "Instituciones aduaneras y comerciales.",
        ],
        "plan_estudios": [
            {
                "anio": "Primer Año",
                "materias": [
                    "Introducción al Comercio Internacional",
                    "Legislación Aduanera I",
                    "Documentación Comercial",
                    "Contabilidad Básica",
                    "Ofimática Aplicada",
                    "Comunicación y Redacción",
                    "Inglés Técnico I",
                ],
            },
            {
                "anio": "Segundo Año",
                "materias": [
                    "Regímenes Aduaneros",
                    "Legislación Aduanera II",
                    "Logística Internacional",
                    "Marketing Internacional",
                    "Medios de Pago Internacionales",
                    "Estadística Aplicada",
                    "Inglés Técnico II",
                ],
            },
            {
                "anio": "Tercer Año",
                "materias": [
                    "Gestión Aduanera",
                    "Tratados y Acuerdos Comerciales",
                    "Transporte Internacional",
                    "Negociación Internacional",
                    "Sistemas Informáticos Aduaneros (SIDUNEA)",
                    "Ética Profesional",
                    "Proyecto de Grado",
                ],
            },
        ],
        "icono": "globe",
        "color_principal": "#ea580c",
        "color_suave": "#fff7ed",
        "imagen_archivo": "comercio.png",
        "iconos_animados": [
            _icono_orbital_config("ship", 55.0, 0.25, PERSPECTIVA_DEFECTO, 0, 18.0, 0.0, "#ea580c", True),
            _icono_orbital_config("package", 70.0, 0.15, PERSPECTIVA_DEFECTO, 90, 24.0, 3.0, "#0891b2"),
            _icono_orbital_config("file-text", 62.0, 0.30, PERSPECTIVA_DEFECTO, 180, 21.0, 6.0, "#7c3aed"),
            _icono_orbital_config("truck", 85.0, 0.20, PERSPECTIVA_DEFECTO, 270, 27.0, 9.0, "#16a34a"),
        ],
    },

    # ------------------------------------------------------------------
    # Carrera 4 — Electrónica
    # ------------------------------------------------------------------
    {
        "id": 4,
        "nombre": "Electrónica",
        "nombre_corto": "Electrónica",
        "duracion": "3 Años",
        "lema": "Circuitos, automatización y sistemas electrónicos",
        "descripcion": (
            "El Técnico Superior en Electrónica es un profesional capacitado para "
            "diseñar, instalar, mantener y reparar circuitos electrónicos, sistemas "
            "de control, telecomunicaciones y automatización industrial."
        ),
        "perfil_profesional": [
            "Diseño y montaje de circuitos electrónicos.",
            "Instalación y mantenimiento de sistemas de telecomunicación.",
            "Programación de microcontroladores y automatización.",
            "Reparación de equipos electrónicos industriales y domésticos.",
            "Aplicación de normas de seguridad eléctrica.",
        ],
        "campo_laboral": [
            "Empresas de electrónica y telecomunicaciones.",
            "Industria de automatización y control.",
            "Servicios técnicos especializados.",
            "Emprendimientos independientes de reparación e instalación.",
        ],
        "plan_estudios": [
            {
                "anio": "Primer Año",
                "materias": [
                    "Electricidad Básica",
                    "Matemática Aplicada",
                    "Física Aplicada",
                    "Dibujo Electrónico",
                    "Componentes Electrónicos",
                    "Ofimática Aplicada",
                    "Inglés Técnico I",
                ],
            },
            {
                "anio": "Segundo Año",
                "materias": [
                    "Electrónica Analógica",
                    "Electrónica Digital",
                    "Instrumentación y Medición",
                    "Circuitos Impresos",
                    "Sistemas de Audio y Video",
                    "Seguridad Eléctrica",
                    "Inglés Técnico II",
                ],
            },
            {
                "anio": "Tercer Año",
                "materias": [
                    "Microcontroladores",
                    "Automatización Industrial",
                    "Telecomunicaciones",
                    "Sistemas de Control",
                    "Mantenimiento de Equipos Electrónicos",
                    "Ética Profesional",
                    "Proyecto de Grado",
                ],
            },
        ],
        "icono": "zap",
        "color_principal": "#16a34a",
        "color_suave": "#f0fdf4",
        "imagen_archivo": "electronica.png",
        "iconos_animados": [
            _icono_orbital_config("circuit-board", 55.0, 0.25, PERSPECTIVA_DEFECTO, 0, 18.0, 0.0, "#16a34a", True),
            _icono_orbital_config("cpu", 70.0, 0.15, PERSPECTIVA_DEFECTO, 90, 24.0, 3.0, "#2563eb"),
            _icono_orbital_config("radio", 62.0, 0.30, PERSPECTIVA_DEFECTO, 180, 21.0, 6.0, "#ea580c"),
            _icono_orbital_config("plug-zap", 85.0, 0.20, PERSPECTIVA_DEFECTO, 270, 27.0, 9.0, "#7c3aed"),
        ],
    },
]