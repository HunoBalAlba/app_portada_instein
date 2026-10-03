"""
Catálogo estático de carreras ofrecidas por el instituto.

Cada carrera define 4 iconos animados con órbitas elípticas keplerianas
achatadas verticalmente (perspectiva 3D tipo "disco visto de lado").

Los semiejes mayores están calibrados para que las órbitas se alejen
visiblemente del centro y cada icono tenga su propia trayectoria.

Sistema de color
----------------
Cada carrera expone 4 colores adaptativos al color_mode:

- `color_principal` / `color_suave`          → light mode
- `color_principal_dark` / `color_suave_dark` → dark mode

Los hex de dark mode son variantes más luminosas del color de marca
para garantizar contraste sobre fondos oscuros (`gray-1` de Radix).

Nota técnica: NOMBRES DE ICONOS LUCIDE
--------------------------------------
Todos los nombres siguen el formato **kebab-case** oficial de Lucide
(https://lucide.dev/icons), que es el recomendado por Reflex:

    ✅ code-xml       ❌ code_xml
    ✅ chart-line     ❌ chart_line
    ✅ calendar-clock ❌ calendar_clock
    ✅ file-text      ❌ file_text
    ✅ circuit-board  ❌ circuit_board
    ✅ plug-zap       ❌ plug_zap

Reflex normalmente tolera snake_case, pero kebab-case evita sorpresas
si en el futuro actualizas la versión de Lucide.

Nota técnica: TURNOS
--------------------
Los turnos disponibles del instituto se definen en `modelos_carrera`:

    - "Mañana"  → horario estándar de mañana.
    - "Tarde"   → horario estándar de tarde.
    - "Noche"   → 19:00 - 22:00 (para quienes trabajan).
    - "Sábado"  → 08:00 - 14:00 (intensivo, para quienes no pueden
                   asistir entre semana).

`TURNOS_DISPONIBLES` se re-exporta desde aquí por conveniencia, pero
la fuente de verdad es `modelos_carrera.TURNOS_VALIDOS`.

Nota técnica: PALETA_COLORES
----------------------------
La constante `PALETA_COLORES` se mantiene porque
`EstadoInstitucional.aleatorizar_colores_carreras` la usa para asignar
colores aleatorios al catálogo (útil para prototipado y demos).

⚠️ Si el proyecto decide usar **un solo acento global** (ej: azul
marino `#3b5bdb`) para todas las carreras, `PALETA_COLORES` puede
eliminarse y los campos `color_principal`, `color_suave`,
`color_principal_dark`, `color_suave_dark` de cada carrera pueden
apuntar todos al mismo valor, o directamente reemplazarse por los
tokens de `constantes_visuales.py`.
"""

from __future__ import annotations

from app_portada_instein.datos.modelos_carrera import (
    Carrera,
    IconoAnimado,
    Turno,
    TURNOS_VALIDOS,
)


# ======================================================================
# Re-export de constantes de dominio
# ======================================================================
# `TURNOS_DISPONIBLES` se mantiene como alias retrocompatible de
# `TURNOS_VALIDOS`. La fuente de verdad vive en `modelos_carrera`.
# ----------------------------------------------------------------------

TURNOS_DISPONIBLES: tuple[Turno, ...] = TURNOS_VALIDOS
"""Alias retrocompatible de `TURNOS_VALIDOS`.

⚠️ La fuente de verdad es `modelos_carrera.TURNOS_VALIDOS`.
"""

MODALIDAD_PRESENCIAL: str = "Presencial"
"""Valor por defecto del campo `modalidad` de cada carrera."""


# ======================================================================
# Paleta de colores disponibles para asignación aleatoria
# ======================================================================
# Tuplas (color_principal, color_suave, color_principal_dark, color_suave_dark)
# ----------------------------------------------------------------------

PALETA_COLORES: list[tuple[str, str, str, str]] = [
    ("#2563eb", "#eff6ff", "#60a5fa", "#1e3a8a"),  # blue
    ("#0891b2", "#ecfeff", "#22d3ee", "#164e63"),  # cyan
    ("#7c3aed", "#f5f3ff", "#a78bfa", "#4c1d95"),  # violet
    ("#ea580c", "#fff7ed", "#fb923c", "#7c2d12"),  # orange
    ("#16a34a", "#f0fdf4", "#4ade80", "#14532d"),  # green
    ("#db2777", "#fdf2f8", "#f472b6", "#831843"),  # pink
    ("#0d9488", "#f0fdfa", "#2dd4bf", "#134e4a"),  # teal
    ("#d97706", "#fffbeb", "#fbbf24", "#78350f"),  # amber
    ("#4f46e5", "#eef2ff", "#818cf8", "#312e81"),  # indigo
    ("#dc2626", "#fef2f2", "#f87171", "#7f1d1d"),  # red
    ("#059669", "#ecfdf5", "#34d399", "#064e3b"),  # emerald
    ("#9333ea", "#faf5ff", "#c084fc", "#581c87"),  # purple
]
"""Paleta de 12 colores para asignación aleatoria a carreras.

Cada tupla contiene:
    (color_principal, color_suave, color_principal_dark, color_suave_dark)
"""


# ======================================================================
# Iconos Lucide usados en el catálogo
# ======================================================================
# Lista consolidada de todos los iconos Lucide que aparecen en
# `CATALOGO_CARRERAS` (tanto en `icono`, `iconos_animados` como en
# `caracteristicas`). Útil para validar contra la versión instalada de
# Lucide o para documentar los requisitos del proyecto.
# ----------------------------------------------------------------------

ICONOS_LUCIDE_DISPONIBLES: frozenset[str] = frozenset({
    # Iconos principales de cada carrera
    "cpu", "calculator", "briefcase", "globe", "zap",
    # Iconos orbitales
    "code-xml", "database", "wifi", "terminal",
    "receipt", "coins", "chart-line", "wallet",
    "calendar-clock", "mail", "users", "file-text",
    "ship", "package", "truck",
    "circuit-board", "radio", "plug-zap",
    # Iconos de características
    "award", "code-2", "languages", "file-check",
})
"""Conjunto de iconos Lucide usados en este catálogo."""


# ======================================================================
# Helper de construcción de iconos orbitales
# ======================================================================


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
    Construye un `IconoAnimado` con los parámetros orbitales de su elipse.

    Args:
        nombre: Identificador del icono Lucide en **kebab-case**
            (ej: "code-xml", "chart-line").
        semieje_mayor: Radio horizontal de la elipse en % del contenedor.
        excentricidad: Excentricidad orbital (0 = círculo).
        factor_perspectiva: Aplanamiento vertical (0.5 = disco de lado).
        angulo_inicial: Ángulo inicial en grados.
        periodo: Duración de una vuelta completa en segundos.
        desfase_temporal: Retraso inicial en segundos.
        color: Color hex del icono.
        tiene_anillos: Si debe dibujarse con anillos tipo Saturno.

    Returns:
        Diccionario `IconoAnimado` listo para renderizar.
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
PERSPECTIVA_DEFECTO: float = 0.5
"""Factor de aplanamiento vertical por defecto para las órbitas."""


# ======================================================================
# Catálogo de carreras
# ======================================================================

CATALOGO_CARRERAS: list[Carrera] = [
    # ------------------------------------------------------------------
    # Carrera 0 — Sistemas Informáticos
    # Turnos: Mañana · Tarde · Noche · Sábado
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
        "preguntas_frecuentes": [
            {
                "pregunta": "¿Necesito saber programar antes de entrar?",
                "respuesta": (
                    "No, empezamos desde cero. En el primer año aprenderás "
                    "lógica de programación y fundamentos de informática."
                ),
            },
            {
                "pregunta": "¿Qué lenguajes de programación voy a aprender?",
                "respuesta": (
                    "Python, JavaScript, SQL y fundamentos de Java. Además, "
                    "HTML/CSS para desarrollo web y frameworks modernos."
                ),
            },
            {
                "pregunta": "¿Puedo trabajar mientras estudio?",
                "respuesta": (
                    "Sí, ofrecemos turno nocturno (19:00-22:00) y turno de "
                    "sábados (09:00-14:30) especialmente diseñados para "
                    "estudiantes que trabajan."
                ),
            },
            {
                "pregunta": "¿Qué equipos necesito tener?",
                "respuesta": (
                    "Contamos con laboratorios equipados. Si quieres practicar "
                    "en casa, una laptop básica con 8GB de RAM es suficiente."
                ),
            },
            {
                "pregunta": "¿Qué salidas laborales tengo al egresar?",
                "respuesta": (
                    "Desarrollador junior, soporte técnico, administrador de "
                    "redes, tester QA, analista de sistemas y más."
                ),
            },
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
        # --- Colores light ---
        "color_principal": "#2563eb",
        "color_suave": "#eff6ff",
        # --- Colores dark ---
        "color_principal_dark": "#60a5fa",
        "color_suave_dark": "#1e3a8a",
        # --- Recursos ---
        "imagen_archivo": "sistemas.png",
        "imagen_banner": "sistemas_banner.avif",
        "iconos_animados": [
            _icono_orbital_config(
                "code-xml", 55.0, 0.25, PERSPECTIVA_DEFECTO,
                0, 18.0, 0.0, "#2563eb", True,
            ),
            _icono_orbital_config(
                "database", 70.0, 0.15, PERSPECTIVA_DEFECTO,
                90, 24.0, 3.0, "#0891b2",
            ),
            _icono_orbital_config(
                "wifi", 62.0, 0.30, PERSPECTIVA_DEFECTO,
                180, 21.0, 6.0, "#7c3aed",
            ),
            _icono_orbital_config(
                "terminal", 85.0, 0.20, PERSPECTIVA_DEFECTO,
                270, 27.0, 9.0, "#ea580c",
            ),
        ],
        "estadisticas": {
            "demanda_laboral": "alta",
            "puntuacion": 4.8,
            "estudiantes_inscritos": 87,
            "estudiantes_graduados": 234,
            "tasa_empleabilidad": 95,
            "salario_promedio_bs": 4500,
        },
        "caracteristicas": [
            {
                "icono": "cpu",
                "etiqueta": "Laboratorios equipados",
                "descripcion": "20 PCs con hardware moderno",
            },
            {
                "icono": "award",
                "etiqueta": "Certificación Cisco",
                "descripcion": "Preparación para CCNA",
            },
            {
                "icono": "code-2",
                "etiqueta": "Proyecto real",
                "descripcion": "Desarrollo con clientes reales",
            },
            {
                "icono": "briefcase",
                "etiqueta": "Pasantías",
                "descripcion": "Convenios con 15+ empresas de TI",
            },
        ],
        "modalidad": "Presencial",
        "turnos": ["Mañana", "Tarde", "Noche", "Sábado"],
        "cupos_disponibles": 30,
    },
    # ------------------------------------------------------------------
    # Carrera 1 — Contaduría General
    # Turnos: Mañana · Noche · Sábado
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
        "preguntas_frecuentes": [
            {
                "pregunta": "¿Necesito conocimientos previos de contabilidad?",
                "respuesta": (
                    "No, comenzamos desde contabilidad básica. Solo se requiere "
                    "manejo de matemática básica y ganas de aprender."
                ),
            },
            {
                "pregunta": "¿Qué software contable voy a aprender?",
                "respuesta": (
                    "Aprenderás sistemas contables computarizados, manejo de "
                    "hojas de cálculo y software tributario boliviano."
                ),
            },
            {
                "pregunta": "¿Puedo firmar balances al egresar?",
                "respuesta": (
                    "Como Técnico Superior puedes llevar contabilidad de empresas, "
                    "aunque la firma oficial de balances requiere título profesional "
                    "universitario."
                ),
            },
            {
                "pregunta": "¿La carrera incluye práctica tributaria?",
                "respuesta": (
                    "Sí, en segundo y tercer año trabajarás con casos reales de "
                    "declaraciones de impuestos y normativa vigente."
                ),
            },
            {
                "pregunta": "¿Qué salidas laborales tengo al egresar?",
                "respuesta": (
                    "Auxiliar contable, asistente tributario, contador de "
                    "microempresas, analista de costos y más."
                ),
            },
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
        # --- Colores light ---
        "color_principal": "#0891b2",
        "color_suave": "#ecfeff",
        # --- Colores dark ---
        "color_principal_dark": "#22d3ee",
        "color_suave_dark": "#164e63",
        # --- Recursos ---
        "imagen_archivo": "contaduria.png",
        "imagen_banner": "contaduria_banner.avif",
        "iconos_animados": [
            _icono_orbital_config(
                "receipt", 55.0, 0.25, PERSPECTIVA_DEFECTO,
                0, 18.0, 0.0, "#0891b2", True,
            ),
            _icono_orbital_config(
                "coins", 70.0, 0.15, PERSPECTIVA_DEFECTO,
                90, 24.0, 3.0, "#16a34a",
            ),
            _icono_orbital_config(
                "chart-line", 62.0, 0.30, PERSPECTIVA_DEFECTO,
                180, 21.0, 6.0, "#ea580c",
            ),
            _icono_orbital_config(
                "wallet", 85.0, 0.20, PERSPECTIVA_DEFECTO,
                270, 27.0, 9.0, "#7c3aed",
            ),
        ],
        "estadisticas": {
            "demanda_laboral": "alta",
            "puntuacion": 4.7,
            "estudiantes_inscritos": 72,
            "estudiantes_graduados": 198,
            "tasa_empleabilidad": 92,
            "salario_promedio_bs": 4200,
        },
        "caracteristicas": [
            {
                "icono": "calculator",
                "etiqueta": "Software contable",
                "descripcion": "SIAT, SICON, hojas de cálculo",
            },
            {
                "icono": "award",
                "etiqueta": "Auxiliar tributario",
                "descripcion": "Preparación en impuestos",
            },
            {
                "icono": "file-text",
                "etiqueta": "Declaraciones reales",
                "descripcion": "Práctica con empresas",
            },
        ],
        "modalidad": "Presencial",
        "turnos": ["Mañana", "Noche", "Sábado"],
        "cupos_disponibles": 25,
    },
    # ------------------------------------------------------------------
    # Carrera 2 — Secretariado Ejecutivo
    # Turnos: Mañana · Tarde · Sábado
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
        "preguntas_frecuentes": [
            {
                "pregunta": "¿Qué habilidades voy a desarrollar?",
                "respuesta": (
                    "Redacción ejecutiva, manejo de agendas, organización de eventos, "
                    "atención al cliente y herramientas ofimáticas avanzadas."
                ),
            },
            {
                "pregunta": "¿Se enseña inglés?",
                "respuesta": (
                    "Sí, Inglés Técnico I y II en los dos primeros años, "
                    "enfocado a comunicación empresarial y protocolo."
                ),
            },
            {
                "pregunta": "¿Qué software aprenderé?",
                "respuesta": (
                    "Word, Excel avanzado, PowerPoint, herramientas de gestión "
                    "documental y sistemas de gestión ejecutiva."
                ),
            },
            {
                "pregunta": "¿Puedo trabajar en empresas grandes?",
                "respuesta": (
                    "Sí, el perfil está diseñado para trabajar en gerencias, "
                    "direcciones ejecutivas y atención al cliente en empresas "
                    "e instituciones."
                ),
            },
            {
                "pregunta": "¿Qué salidas laborales tengo al egresar?",
                "respuesta": (
                    "Secretaria ejecutiva, asistente administrativa, recepcionista "
                    "bilingüe, coordinadora de eventos y más."
                ),
            },
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
        # --- Colores light ---
        "color_principal": "#7c3aed",
        "color_suave": "#f5f3ff",
        # --- Colores dark ---
        "color_principal_dark": "#a78bfa",
        "color_suave_dark": "#4c1d95",
        # --- Recursos ---
        "imagen_archivo": "secretariado.png",
        "imagen_banner": "secretariado_banner.avif",
        "iconos_animados": [
            _icono_orbital_config(
                "calendar-clock", 55.0, 0.25, PERSPECTIVA_DEFECTO,
                0, 18.0, 0.0, "#7c3aed", True,
            ),
            _icono_orbital_config(
                "mail", 70.0, 0.15, PERSPECTIVA_DEFECTO,
                90, 24.0, 3.0, "#db2777",
            ),
            _icono_orbital_config(
                "users", 62.0, 0.30, PERSPECTIVA_DEFECTO,
                180, 21.0, 6.0, "#0891b2",
            ),
            _icono_orbital_config(
                "file-text", 85.0, 0.20, PERSPECTIVA_DEFECTO,
                270, 27.0, 9.0, "#ea580c",
            ),
        ],
        "estadisticas": {
            "demanda_laboral": "media",
            "puntuacion": 4.6,
            "estudiantes_inscritos": 45,
            "estudiantes_graduados": 156,
            "tasa_empleabilidad": 88,
            "salario_promedio_bs": 3500,
        },
        "caracteristicas": [
            {
                "icono": "languages",
                "etiqueta": "Inglés técnico",
                "descripcion": "2 niveles conversacionales",
            },
            {
                "icono": "users",
                "etiqueta": "Protocolo empresarial",
                "descripcion": "Etiqueta y eventos",
            },
            {
                "icono": "briefcase",
                "etiqueta": "Atención al cliente",
                "descripcion": "Prácticas con clientes reales",
            },
        ],
        "modalidad": "Presencial",
        "turnos": ["Mañana", "Tarde", "Sábado"],
        "cupos_disponibles": 20,
    },
    # ------------------------------------------------------------------
    # Carrera 3 — Comercio Internacional
    # Turnos: Mañana · Noche · Sábado
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
        "preguntas_frecuentes": [
            {
                "pregunta": "¿Qué es el SIDUNEA?",
                "respuesta": (
                    "Es el Sistema Informático Aduanero usado en Bolivia y varios "
                    "países de la región. Aprenderás a usarlo en tercer año."
                ),
            },
            {
                "pregunta": "¿Se enseña normativa aduanera?",
                "respuesta": (
                    "Sí, Legislación Aduanera I y II cubren toda la normativa "
                    "vigente boliviana y tratados internacionales."
                ),
            },
            {
                "pregunta": "¿Puedo trabajar en agencias despachantes?",
                "respuesta": (
                    "Sí, es una de las principales salidas. También en "
                    "importadoras, exportadoras y operadores logísticos."
                ),
            },
            {
                "pregunta": "¿Qué idiomas se enseñan?",
                "respuesta": (
                    "Inglés Técnico I y II enfocado a comercio exterior. "
                    "Se recomienda inglés básico previo pero no es obligatorio."
                ),
            },
            {
                "pregunta": "¿Qué salidas laborales tengo al egresar?",
                "respuesta": (
                    "Auxiliar de despachante, asistente de comercio exterior, "
                    "operador logístico, analista de importaciones y más."
                ),
            },
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
        # --- Colores light ---
        "color_principal": "#ea580c",
        "color_suave": "#fff7ed",
        # --- Colores dark ---
        "color_principal_dark": "#fb923c",
        "color_suave_dark": "#7c2d12",
        # --- Recursos ---
        "imagen_archivo": "comercio.png",
        "imagen_banner": "comercio_banner.avif",
        "iconos_animados": [
            _icono_orbital_config(
                "ship", 55.0, 0.25, PERSPECTIVA_DEFECTO,
                0, 18.0, 0.0, "#ea580c", True,
            ),
            _icono_orbital_config(
                "package", 70.0, 0.15, PERSPECTIVA_DEFECTO,
                90, 24.0, 3.0, "#0891b2",
            ),
            _icono_orbital_config(
                "file-text", 62.0, 0.30, PERSPECTIVA_DEFECTO,
                180, 21.0, 6.0, "#7c3aed",
            ),
            _icono_orbital_config(
                "truck", 85.0, 0.20, PERSPECTIVA_DEFECTO,
                270, 27.0, 9.0, "#16a34a",
            ),
        ],
        "estadisticas": {
            "demanda_laboral": "alta",
            "puntuacion": 4.9,
            "estudiantes_inscritos": 58,
            "estudiantes_graduados": 145,
            "tasa_empleabilidad": 94,
            "salario_promedio_bs": 5000,
        },
        "caracteristicas": [
            {
                "icono": "globe",
                "etiqueta": "SIDUNEA",
                "descripcion": "Sistema aduanero oficial",
            },
            {
                "icono": "ship",
                "etiqueta": "Logística global",
                "descripcion": "Importación y exportación",
            },
            {
                "icono": "file-check",
                "etiqueta": "Tratados comerciales",
                "descripcion": "MERCOSUR, CAN",
            },
        ],
        "modalidad": "Presencial",
        "turnos": ["Mañana", "Noche", "Sábado"],
        "cupos_disponibles": 25,
    },
    # ------------------------------------------------------------------
    # Carrera 4 — Electrónica
    # Turnos: Mañana · Tarde · Noche · Sábado
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
        "preguntas_frecuentes": [
            {
                "pregunta": "¿Qué equipos voy a usar en los laboratorios?",
                "respuesta": (
                    "Osciloscopios, multímetros, generadores de señales, estaciones "
                    "de soldadura y microcontroladores PIC/Arduino/ESP32."
                ),
            },
            {
                "pregunta": "¿Se enseña programación de microcontroladores?",
                "respuesta": (
                    "Sí, en tercer año. Trabajarás con Arduino, PIC y ESP32 "
                    "para proyectos de automatización y domótica."
                ),
            },
            {
                "pregunta": "¿Puedo reparar equipos electrónicos al egresar?",
                "respuesta": (
                    "Sí, tendrás todas las competencias para reparar equipos "
                    "domésticos, industriales y de telecomunicaciones."
                ),
            },
            {
                "pregunta": "¿La carrera incluye automatización industrial?",
                "respuesta": (
                    "Sí, es parte del tercer año. Aprenderás PLCs, sensores "
                    "y sistemas de control industrial."
                ),
            },
            {
                "pregunta": "¿Qué salidas laborales tengo al egresar?",
                "respuesta": (
                    "Técnico electrónico, mantenedor industrial, instalador de "
                    "telecomunicaciones y emprendedor de servicios técnicos."
                ),
            },
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
        # --- Colores light ---
        "color_principal": "#16a34a",
        "color_suave": "#f0fdf4",
        # --- Colores dark ---
        "color_principal_dark": "#4ade80",
        "color_suave_dark": "#14532d",
        # --- Recursos ---
        "imagen_archivo": "electronica.png",
        "imagen_banner": "electronica_banner.avif",
        "iconos_animados": [
            _icono_orbital_config(
                "circuit-board", 55.0, 0.25, PERSPECTIVA_DEFECTO,
                0, 18.0, 0.0, "#16a34a", True,
            ),
            _icono_orbital_config(
                "cpu", 70.0, 0.15, PERSPECTIVA_DEFECTO,
                90, 24.0, 3.0, "#2563eb",
            ),
            _icono_orbital_config(
                "radio", 62.0, 0.30, PERSPECTIVA_DEFECTO,
                180, 21.0, 6.0, "#ea580c",
            ),
            _icono_orbital_config(
                "plug-zap", 85.0, 0.20, PERSPECTIVA_DEFECTO,
                270, 27.0, 9.0, "#7c3aed",
            ),
        ],
        "estadisticas": {
            "demanda_laboral": "alta",
            "puntuacion": 4.7,
            "estudiantes_inscritos": 52,
            "estudiantes_graduados": 178,
            "tasa_empleabilidad": 91,
            "salario_promedio_bs": 4800,
        },
        "caracteristicas": [
            {
                "icono": "circuit-board",
                "etiqueta": "PLC y automatización",
                "descripcion": "Siemens, Schneider",
            },
            {
                "icono": "cpu",
                "etiqueta": "Microcontroladores",
                "descripcion": "Arduino, PIC, ESP32",
            },
            {
                "icono": "zap",
                "etiqueta": "Energía solar",
                "descripcion": "Instalación fotovoltaica",
            },
        ],
        "modalidad": "Presencial",
        "turnos": ["Mañana", "Tarde", "Noche", "Sábado"],
        "cupos_disponibles": 30,
    },
]


# ======================================================================
# Helper de acceso: paleta por ID de carrera
# ======================================================================


def paleta_por_id_carrera(
    carrera_id: int,
) -> tuple[str, str, str, str] | None:
    """
    Devuelve la tupla de colores (principal, suave, principal_dark,
    suave_dark) de la carrera indicada.

    Útil para el `aleatorizar_colores_carreras` del State, o para
    cualquier consumidor que necesite acceso rápido a los colores de
    una carrera sin iterar sobre el catálogo.

    Args:
        carrera_id: ID de la carrera (0-4).

    Returns:
        Tupla de colores, o `None` si el ID no existe.
    """
    for carrera in CATALOGO_CARRERAS:
        if carrera["id"] == carrera_id:
            return (
                carrera["color_principal"],
                carrera["color_suave"],
                carrera["color_principal_dark"],
                carrera["color_suave_dark"],
            )
    return None


# ======================================================================
# EXPORTS
# ======================================================================

__all__ = [
    "CATALOGO_CARRERAS",
    "ICONOS_LUCIDE_DISPONIBLES",
    "MODALIDAD_PRESENCIAL",
    "PALETA_COLORES",
    "PERSPECTIVA_DEFECTO",
    "TURNOS_DISPONIBLES",
    # Re-exportados desde modelos_carrera para conveniencia
    "TURNOS_VALIDOS",
    "Turno",
    "paleta_por_id_carrera",
]