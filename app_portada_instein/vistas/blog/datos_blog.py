"""
Datos estáticos del Blog Institucional.

Contiene:
- `CATEGORIAS`: lista de categorías del blog con metadatos visuales
  (icono, color, etiqueta).
- `POSTS`: lista completa de posts del blog. Cada post incluye:
  - id, titulo, extracto, contenido (cuerpo completo del artículo)
  - categoria, autor, fecha, minutos_lectura, destacado
  - imagen (nombre del archivo en assets/blog/)

Todos los datos son listas de `TypedDict`, lo que da:
- Autocompletado real en el IDE.
- Verificación de tipos con mypy/pyright.
- Compatibilidad total con `rx.foreach` y `rx.match` de Reflex
  (evita `ForeachVarError: Could not foreach over var of type Any`).

Cómo agregar un post nuevo:
    POSTS.append(Post(
        id=13,
        titulo="...",
        extracto="...",
        contenido="...",
        categoria="tecnologia",       # clave de CategoriaId
        autor="...",
        fecha="...",
        minutos_lectura=5,
        destacado=False,
        imagen="nombre_archivo.webp", # archivo en assets/blog/
    ))

Cómo cambiar el post destacado:
    - Marca `destacado=True` en el post deseado.
    - Asegúrate de que solo UN post tenga `destacado=True`.

Imágenes:
    Los archivos viven en `assets/blog/` (o `public/blog/` según tu
    configuración) y se referencian como `/blog/nombre_archivo.webp`.
"""

from __future__ import annotations

from typing import Literal, TypedDict


# ======================================================================
# Tipos
# ======================================================================

CategoriaId = Literal[
    "todas",
    "tecnologia",
    "contaduria",
    "empleabilidad",
    "institucional",
    "estudiantes",
    "tutoriales",
]
"""Identificadores válidos de categoría.

`Literal` restringe el tipo a estos strings exactos. El IDE y mypy
te avisarán si escribes mal un ID (ej: "tecnologiaa").
"""

ColorScheme = Literal[
    "gray",
    "blue",
    "violet",
    "green",
    "crimson",
    "orange",
    "cyan",
]
"""Nombres de color scheme de Radix Themes usados por las categorías."""


class Categoria(TypedDict):
    """Metadatos visuales de una categoría del blog."""

    valor: CategoriaId
    etiqueta: str
    icono: str
    color: ColorScheme


class Post(TypedDict):
    """Estructura completa de un post del blog."""

    id: int
    titulo: str
    extracto: str
    contenido: str
    categoria: CategoriaId
    autor: str
    fecha: str
    minutos_lectura: int
    destacado: bool
    imagen: str


# ======================================================================
# Categorías
# ======================================================================

CATEGORIAS: list[Categoria] = [
    {
        "valor": "todas",
        "etiqueta": "Todas",
        "icono": "list",
        "color": "gray",
    },
    {
        "valor": "tecnologia",
        "etiqueta": "Tecnología",
        "icono": "cpu",
        "color": "blue",
    },
    {
        "valor": "contaduria",
        "etiqueta": "Contaduría",
        "icono": "calculator",
        "color": "violet",
    },
    {
        "valor": "empleabilidad",
        "etiqueta": "Empleabilidad",
        "icono": "trending-up",
        "color": "green",
    },
    {
        "valor": "institucional",
        "etiqueta": "Institucional",
        "icono": "landmark",
        "color": "crimson",
    },
    {
        "valor": "estudiantes",
        "etiqueta": "Estudiantes",
        "icono": "graduation-cap",
        "color": "orange",
    },
    {
        "valor": "tutoriales",
        "etiqueta": "Tutoriales",
        "icono": "book-open",
        "color": "cyan",
    },
]


# ======================================================================
# Posts del blog
# ======================================================================

POSTS: list[Post] = [
    # ==================================================================
    # POST DESTACADO
    # ==================================================================
    {
        "id": 0,
        "titulo": "Cómo la IA está transformando la formación técnica en Bolivia",
        "extracto": (
            "Las herramientas de inteligencia artificial están cambiando "
            "la forma en que los estudiantes técnicos aprenden, practican "
            "y se preparan para el mundo laboral."
        ),
        "contenido": (
            "La inteligencia artificial (IA) dejó de ser una promesa "
            "futurista para convertirse en una realidad cotidiana en las "
            "aulas técnicas de Bolivia. Desde asistentes de código hasta "
            "plataformas adaptativas de aprendizaje, la IA está "
            "redefiniendo cómo se enseña y cómo se aprende.\n\n"
            "En INSTEIN, por ejemplo, los estudiantes de Sistemas ya "
            "utilizan herramientas de IA para revisar su código, generar "
            "pruebas automatizadas y documentar proyectos. Los docentes "
            "usan IA para personalizar el ritmo de aprendizaje de cada "
            "estudiante y detectar dificultades antes de que se "
            "conviertan en problemas mayores.\n\n"
            "Sin embargo, este cambio también trae desafíos: ¿cómo "
            "garantizar que los estudiantes no dependan ciegamente de "
            "la IA? ¿Cómo evaluar el pensamiento crítico cuando la "
            "respuesta está a un clic? Estas son las preguntas que "
            "estamos respondiendo con nuevas metodologías que combinan "
            "lo mejor de la tecnología con la formación humana."
        ),
        "categoria": "tecnologia",
        "autor": "Equipo INSTEIN",
        "fecha": "15 de abril, 2026",
        "minutos_lectura": 8,
        "destacado": True,
        "imagen": "ia_formacion_tecnica.webp",
    },
    # ==================================================================
    # POSTS REGULARES
    # ==================================================================
    {
        "id": 1,
        "titulo": "5 habilidades técnicas que todo programador junior debe dominar",
        "extracto": (
            "Desde control de versiones hasta testing automatizado, estas "
            "son las competencias que te harán destacar en tu primer "
            "empleo como desarrollador."
        ),
        "contenido": (
            "El mercado laboral técnico en Bolivia es cada vez más "
            "competitivo. Para destacar como programador junior, no "
            "basta con saber un lenguaje: necesitas dominar un conjunto "
            "de habilidades transversales.\n\n"
            "1. Control de versiones con Git: saber trabajar con ramas, "
            "resolver conflictos y hacer pull requests es indispensable.\n\n"
            "2. Testing automatizado: escribir pruebas unitarias y de "
            "integración te diferencia del 90% de los juniors.\n\n"
            "3. Lectura de código ajeno: saber navegar un repositorio "
            "existente es más importante que crear uno desde cero.\n\n"
            "4. Manejo de la terminal: no todo se resuelve con el IDE.\n\n"
            "5. Inglés técnico: la documentación está en inglés. No "
            "necesitas ser fluido, pero sí leer con soltura.\n\n"
            "En INSTEIN trabajamos estas 5 habilidades desde el primer "
            "semestre, integradas en proyectos reales."
        ),
        "categoria": "tecnologia",
        "autor": "Prof. Juan Pérez",
        "fecha": "10 de abril, 2026",
        "minutos_lectura": 6,
        "destacado": False,
        "imagen": "habilidades_programador.webp",
    },
    {
        "id": 2,
        "titulo": "Guía completa para inscribirte en el turno nocturno",
        "extracto": (
            "¿Trabajas y quieres estudiar? Te explicamos paso a paso cómo "
            "matricularte en el turno nocturno y aprovechar al máximo "
            "esta modalidad."
        ),
        "contenido": (
            "El turno nocturno fue diseñado específicamente para "
            "personas que trabajan durante el día pero quieren "
            "estudiar una carrera técnica. En INSTEIN, este turno "
            "funciona de 19:00 a 22:00, de lunes a viernes.\n\n"
            "Paso 1: elige tu carrera. Puedes ver la oferta completa "
            "en nuestra página de carreras.\n\n"
            "Paso 2: reúne los documentos. Diploma de bachiller, "
            "carnet de identidad, 2 fotos tamaño carnet.\n\n"
            "Paso 3: contáctanos por WhatsApp o visítanos. Te "
            "guiaremos paso a paso.\n\n"
            "Paso 4: agenda una entrevista breve. Coordinamos un "
            "horario compatible con tu trabajo.\n\n"
            "Paso 5: ¡comienza clases el siguiente lunes! El proceso "
            "completo toma menos de 24 horas."
        ),
        "categoria": "institucional",
        "autor": "Admisiones INSTEIN",
        "fecha": "08 de abril, 2026",
        "minutos_lectura": 4,
        "destacado": False,
        "imagen": "turno_nocturno.webp",
    },
    {
        "id": 3,
        "titulo": "Contabilidad digital: herramientas que debes conocer en 2026",
        "extracto": (
            "SIAT, SICON, hojas de cálculo avanzadas y software en la "
            "nube. Estas son las herramientas que todo técnico contable "
            "debe manejar este año."
        ),
        "contenido": (
            "La contabilidad tradicional dejó de ser un ejercicio de "
            "papel y lápiz. Hoy, el técnico contable boliviano debe "
            "manejar un ecosistema de herramientas digitales.\n\n"
            "SIAT (Sistema Integrado de Administración Tributaria): "
            "esencial para la facturación electrónica y el cumplimiento "
            "de obligaciones con el Servicio de Impuestos Nacionales.\n\n"
            "SICON: sistema contable ampliamente usado en Bolivia para "
            "el registro de operaciones y la generación de estados "
            "financieros.\n\n"
            "Excel avanzado: tablas dinámicas, fórmulas complejas y "
            "automatización con macros. Sigue siendo la herramienta más "
            "usada en pymes.\n\n"
            "Software en la nube: plataformas como QuickBooks o "
            "Contabilidad en la Nube están ganando terreno.\n\n"
            "En INSTEIN enseñamos todas estas herramientas desde el "
            "primer año, con casos reales."
        ),
        "categoria": "contaduria",
        "autor": "Prof. María González",
        "fecha": "05 de abril, 2026",
        "minutos_lectura": 7,
        "destacado": False,
        "imagen": "contabilidad_digital.webp",
    },
    {
        "id": 4,
        "titulo": "Cómo prepararte para tu primera entrevista técnica",
        "extracto": (
            "La entrevista técnica puede ser intimidante. Aquí te damos "
            "las estrategias y recursos que usan nuestros egresados para "
            "conseguir empleo en su área."
        ),
        "contenido": (
            "La primera entrevista técnica es un momento decisivo. "
            "Muchos candidatos con excelentes habilidades técnicas "
            "fallan por no saber comunicarse.\n\n"
            "Antes de la entrevista: investiga la empresa, repasa los "
            "fundamentos de tu área, prepara 3 ejemplos de proyectos "
            "que hayas hecho (con problemas, soluciones y resultados).\n\n"
            "Durante la entrevista: piensa en voz alta. Los "
            "entrevistadores quieren entender cómo razonas, no solo si "
            "llegas a la respuesta. Si no sabes algo, dilo con "
            "honestidad y propón cómo lo resolverías.\n\n"
            "Después: envía un correo de agradecimiento. Es un detalle "
            "que muchos candidatos olvidan y que marca la diferencia.\n\n"
            "En INSTEIN organizamos simulacros de entrevista para "
            "preparar a nuestros egresados."
        ),
        "categoria": "empleabilidad",
        "autor": "Equipo INSTEIN",
        "fecha": "02 de abril, 2026",
        "minutos_lectura": 5,
        "destacado": False,
        "imagen": "entrevista_tecnica.webp",
    },
    {
        "id": 5,
        "titulo": "Electrónica aplicada: proyecto de domótica para principiantes",
        "extracto": (
            "Tutorial paso a paso para construir un sistema básico de "
            "domótica con Arduino, sensores y relés."
        ),
        "contenido": (
            "La domótica es la automatización de una vivienda. En este "
            "tutorial construiremos un sistema básico que enciende y "
            "apaga luces según la luz ambiental.\n\n"
            "Materiales: Arduino UNO, sensor LDR, módulo de relé, "
            "resistencia de 10kΩ, cables, protoboard, LED de prueba.\n\n"
            "Esquema: el LDR va conectado a una entrada analógica del "
            "Arduino. El relé se conecta a una salida digital.\n\n"
            "Código: leemos el valor del LDR, si la luz es baja, "
            "activamos el relé; si es alta, lo desactivamos.\n\n"
            "Aplicaciones: control de iluminación exterior, riego "
            "automático, ventilación inteligente.\n\n"
            "Este proyecto es ideal para estudiantes de segundo año de "
            "Electrónica y se presenta en la feria de innovación."
        ),
        "categoria": "tutoriales",
        "autor": "Prof. Carlos Rojas",
        "fecha": "28 de marzo, 2026",
        "minutos_lectura": 10,
        "destacado": False,
        "imagen": "proyecto_domotica.webp",
    },
    {
        "id": 6,
        "titulo": "Cómo elegir tu carrera técnica según tus intereses",
        "extracto": (
            "¿Sistemas, Contaduría, Secretariado, Comercio o Electrónica? "
            "Te ayudamos a tomar una decisión informada."
        ),
        "contenido": (
            "Elegir una carrera técnica es una decisión que marcará los "
            "próximos 3 años de tu vida. Aquí te damos una guía práctica.\n\n"
            "Pregúntate: ¿qué actividades disfruto hacer? Si te gusta "
            "resolver problemas lógicos, Sistemas. Si te gustan los "
            "números y las finanzas, Contaduría. Si te gusta organizar "
            "y comunicarte, Secretariado.\n\n"
            "Piensa en tu futuro: ¿qué carreras tienen más demanda en "
            "tu ciudad? ¿Cuáles pagan mejor? ¿Cuáles te permiten "
            "trabajar remoto?\n\n"
            "Conversa con profesionales: habla con personas que ya "
            "trabajen en cada área para conocer la realidad del día a "
            "día.\n\n"
            "Visítanos: en INSTEIN ofrecemos charlas de orientación "
            "vocacional gratuitas. Solo tienes que agendar una cita."
        ),
        "categoria": "estudiantes",
        "autor": "Orientación Vocacional",
        "fecha": "25 de marzo, 2026",
        "minutos_lectura": 6,
        "destacado": False,
        "imagen": "elegir_carrera.webp",
    },
    {
        "id": 7,
        "titulo": "Casos de éxito: egresados que emprendieron en Bolivia",
        "extracto": (
            "Conoce las historias de 3 egresados de INSTEIN que hoy "
            "lideran sus propios emprendimientos técnicos."
        ),
        "contenido": (
            "Nuestros egresados no solo trabajan en empresas: muchos "
            "crean sus propios emprendimientos. Estas son sus historias.\n\n"
            "Carlos (Sistemas, 2022): fundó una agencia de desarrollo "
            "web en Santa Cruz. Hoy tiene 5 empleados y clientes en 3 "
            "países.\n\n"
            "María (Contaduría, 2021): abrió su propio estudio "
            "contable. Atiende a 40 pymes y acaba de contratar a su "
            "primera asistente.\n\n"
            "José (Electrónica, 2023): creó un servicio técnico "
            "especializado en domótica. Ha instalado sistemas en más "
            "de 50 viviendas.\n\n"
            "Estos casos demuestran que la formación técnica abre "
            "puertas no solo al empleo, sino también al emprendimiento."
        ),
        "categoria": "empleabilidad",
        "autor": "Equipo INSTEIN",
        "fecha": "20 de marzo, 2026",
        "minutos_lectura": 8,
        "destacado": False,
        "imagen": "egresados_emprendedores.webp",
    },
    {
        "id": 8,
        "titulo": "Comercio internacional: oportunidades para técnicos en 2026",
        "extracto": (
            "El comercio exterior boliviano está en expansión. "
            "Analizamos las oportunidades laborales para técnicos."
        ),
        "contenido": (
            "Bolivia está ampliando sus relaciones comerciales con "
            "varios países de la región. Esto genera una demanda "
            "creciente de técnicos en comercio internacional.\n\n"
            "Oportunidades concretas: auxiliares de despachantes de "
            "aduana, asistentes en agencias de carga internacional, "
            "analistas de importaciones y exportaciones.\n\n"
            "Habilidades clave: manejo de SIDUNEA (sistema aduanero), "
            "conocimiento de tratados comerciales (MERCOSUR, CAN), "
            "inglés técnico.\n\n"
            "Sectores en crecimiento: agroindustria, minería, "
            "textiles y tecnología.\n\n"
            "En INSTEIN formamos técnicos capaces de insertarse "
            "inmediatamente en este mercado."
        ),
        "categoria": "empleabilidad",
        "autor": "Prof. Ana Vargas",
        "fecha": "18 de marzo, 2026",
        "minutos_lectura": 7,
        "destacado": False,
        "imagen": "comercio_internacional.webp",
    },
    {
        "id": 9,
        "titulo": "Secretariado ejecutivo: habilidades blandas que marcan la diferencia",
        "extracto": (
            "Más allá de la ofimática, el éxito como secretaria ejecutiva "
            "depende de habilidades como comunicación y organización."
        ),
        "contenido": (
            "El secretariado ejecutivo es una carrera técnico-profesional "
            "que combina tecnología con habilidades humanas. Aquí te "
            "contamos las habilidades blandas más valoradas.\n\n"
            "Comunicación asertiva: saber transmitir información sin "
            "perder profesionalismo. Tanto por escrito como oralmente.\n\n"
            "Organización impecable: manejo de agendas, reuniones, "
            "documentos y prioridades. La secretaria es el pilar "
            "operativo de una gerencia.\n\n"
            "Discreción: manejar información confidencial con ética.\n\n"
            "Protocolo empresarial: saber cómo comportarse en reuniones, "
            "eventos y comunicaciones formales.\n\n"
            "En INSTEIN reforzamos estas habilidades desde el primer "
            "semestre con talleres prácticos."
        ),
        "categoria": "estudiantes",
        "autor": "Prof. Laura Méndez",
        "fecha": "15 de marzo, 2026",
        "minutos_lectura": 5,
        "destacado": False,
        "imagen": "secretariado_ejecutivo.webp",
    },
    {
        "id": 10,
        "titulo": "Cómo aprovechar las ferias de innovación del instituto",
        "extracto": (
            "Las ferias internas son una oportunidad única para mostrar "
            "tu talento, ganar becas y conectar con empresas."
        ),
        "contenido": (
            "Dos veces al año, INSTEIN organiza ferias de innovación. "
            "Estas ferias no son solo exhibiciones: son competencias "
            "reales con premios reales.\n\n"
            "Cómo prepararte: forma un equipo de hasta 3 personas, "
            "elige un área de innovación (Sistemas, Electrónica, "
            "Contaduría, Comercio, Secretariado) y desarrolla un "
            "proyecto.\n\n"
            "Qué se evalúa: originalidad, impacto, viabilidad técnica, "
            "calidad de la presentación.\n\n"
            "Qué puedes ganar: becas del 30%, 50% o 100% de la "
            "mensualidad, dependiendo del puntaje obtenido (90-93, "
            "94-97, 98-100 puntos).\n\n"
            "Cómo aprovechar al máximo: documenta todo el proceso, "
            "prepara una presentación de 10 minutos, y practica con "
            "tus docentes mentores."
        ),
        "categoria": "institucional",
        "autor": "Equipo INSTEIN",
        "fecha": "12 de marzo, 2026",
        "minutos_lectura": 6,
        "destacado": False,
        "imagen": "feria_innovacion.webp",
    },
    {
        "id": 11,
        "titulo": "Tutorial: crear tu primer sitio web con HTML y CSS",
        "extracto": (
            "Guía completa desde cero para crear un sitio web responsive "
            "usando solo HTML y CSS."
        ),
        "contenido": (
            "Este tutorial te guiará paso a paso para crear un sitio "
            "web básico pero funcional usando HTML y CSS.\n\n"
            "Paso 1: crea la estructura HTML. Una página con "
            "`<header>`, `<main>`, `<section>` y `<footer>`.\n\n"
            "Paso 2: aplica estilos con CSS. Fuentes, colores, "
            "espaciado y layout con Flexbox.\n\n"
            "Paso 3: hazlo responsive. Usa media queries para adaptar "
            "el layout a móviles y tablets.\n\n"
            "Paso 4: publica tu sitio. Puedes usar GitHub Pages o "
            "Netlify gratis.\n\n"
            "Recursos recomendados: MDN Web Docs, CSS-Tricks, "
            "Frontend Mentor.\n\n"
            "Este proyecto es parte del primer semestre de Sistemas "
            "Informáticos."
        ),
        "categoria": "tutoriales",
        "autor": "Prof. Juan Pérez",
        "fecha": "08 de marzo, 2026",
        "minutos_lectura": 12,
        "destacado": False,
        "imagen": "primer_sitio_web.webp",
    },
    {
        "id": 12,
        "titulo": "La importancia de la ética profesional en el mundo técnico",
        "extracto": (
            "Los técnicos toman decisiones todos los días que impactan a "
            "las personas y las empresas."
        ),
        "contenido": (
            "La ética profesional no es un tema abstracto: es lo que "
            "define cómo actúas cuando nadie te está mirando.\n\n"
            "En Sistemas, por ejemplo, un programador puede acceder a "
            "datos sensibles de usuarios. ¿Los usa solo para lo que se "
            "le autorizó?\n\n"
            "En Contaduría, un técnico puede recibir presión para "
            "falsificar balances. ¿Cómo responde?\n\n"
            "En Electrónica, un técnico puede detectar una falla "
            "grave en un equipo. ¿La reporta o la ignora?\n\n"
            "En INSTEIN abordamos la ética desde el primer año, con "
            "casos prácticos y reflexiones. Formamos técnicos "
            "competentes, pero sobre todo, íntegros."
        ),
        "categoria": "institucional",
        "autor": "Dirección Académica",
        "fecha": "05 de marzo, 2026",
        "minutos_lectura": 5,
        "destacado": False,
        "imagen": "etica_profesional.webp",
    },
]


# ======================================================================
# Helpers de búsqueda
# ======================================================================


def obtener_post(post_id: int) -> Post | None:
    """
    Busca un post por su `id` en el catálogo estático.

    Args:
        post_id: ID del post a buscar.

    Returns:
        El post encontrado, o `None` si no existe.
    """
    for post in POSTS:
        if post["id"] == post_id:
            return post
    return None


def obtener_post_destacado() -> Post:
    """
    Devuelve el primer post con `destacado=True`.

    Returns:
        El post destacado, o `POSTS[0]` si ninguno está marcado.
    """
    for post in POSTS:
        if post["destacado"]:
            return post
    return POSTS[0]


# ======================================================================
# EXPORTS
# ======================================================================

__all__ = [
    "CATEGORIAS",
    "POSTS",
    "Categoria",
    "CategoriaId",
    "ColorScheme",
    "Post",
    "obtener_post",
    "obtener_post_destacado",
]