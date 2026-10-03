"""
Modelos de datos (tipados) que describen la estructura de una carrera
técnica y su plan de estudios anual.

Estos `TypedDict` son el **contrato tipado** entre:

- La capa de datos (`catalogo_carreras.py`) → los produce.
- La capa de dominio (`estado_institucional.py`) → los expone como
  `@rx.var`.
- La capa de presentación (`componentes/`, `vistas/`) → los consume.

Nota técnica: `TypedDict` y `rx.foreach`
----------------------------------------
Reflex necesita tipos **precisos** para `rx.foreach`. Si un campo se
tipa como `dict` genérico, sus subcampos se infieren como `Any` y
`rx.foreach` falla con:

    ForeachVarError: Could not foreach over var of type Any

Por eso todos los modelos usan `TypedDict` con tipos concretos, y las
listas anidadas (`list[PlanAnual]`, `list[IconoAnimado]`) tienen su
propio `TypedDict` en lugar de `list[dict]`.

Nota técnica: `Literal` para enums
----------------------------------
Campos como `demanda_laboral` ("alta" | "media" | "baja") o
`modalidad` ("Presencial" | "Semipresencial" | "Virtual") se tipan
con `Literal` en lugar de `str`. Esto:

- Detecta typos en tiempo de escritura (IDE/mypy).
- Documenta los valores válidos directamente en el tipo.
- No afecta el runtime (es solo un hint de tipo).

Nota técnica: TURNOS DISPONIBLES
--------------------------------
El instituto ofrece 4 turnos:

- **Mañana**   → turno estándar de mañana (horario habitual).
- **Tarde**    → turno estándar de tarde (horario habitual).
- **Noche**    → turno nocturno (19:00 - 22:00), pensado para
                 estudiantes que trabajan durante el día.
- **Sábado**   → turno intensivo de sábados (09:00 - 14:30), pensado
                 para estudiantes que no pueden asistir entre semana.

Los turnos se tipan con `Literal` para que el IDE avise si escribes
un valor no válido en `catalogo_carreras.py`.
"""

from __future__ import annotations

from typing import Literal, TypedDict


# ======================================================================
# Alias de tipos básicos
# ======================================================================

ColorHex = str
"""Color en formato hexadecimal `#RRGGBB` (ej: "#2563eb")."""

DemandaLaboral = Literal["alta", "media", "baja"]
"""Nivel de demanda laboral de una carrera.

- `"alta"`  → alta empleabilidad, muchos puestos disponibles.
- `"media"` → demanda moderada.
- `"baja"`  → poca demanda en el mercado actual.
"""

Modalidad = Literal["Presencial", "Semipresencial", "Virtual"]
"""Modalidad de cursado de la carrera."""

Turno = Literal["Mañana", "Tarde", "Noche", "Sábado"]
"""Turno de cursado de la carrera.

El instituto ofrece 4 turnos:

- `"Mañana"`  → turno estándar de mañana.
- `"Tarde"`   → turno estándar de tarde.
- `"Noche"`   → turno nocturno (19:00 - 22:00), ideal para quienes trabajan.
- `"Sábado"`  → turno intensivo de sábados (09:00 - 14:30), ideal para
                quienes no pueden asistir entre semana.

⚠️ La tilde de `"Sábado"` es intencional: el nombre se muestra tal cual
en la UI (`turnos: ["Mañana", "Sábado"]`). Si se necesitara un
identificador sin tilde para URLs o keys, se añadiría un campo aparte
(ej: `turno_id: "sabado"`).
"""


# ======================================================================
# Constantes de turnos (referencia rápida)
# ======================================================================

TURNOS_VALIDOS: tuple[Turno, ...] = ("Mañana", "Tarde", "Noche", "Sábado")
"""Tupla con todos los turnos válidos.

Útil para:

- Validar el campo `turnos` de cada carrera (subset check).
- Iterar sobre opciones en la UI (filtros, selects, pills).
- Generar documentación / tests.
"""

HORARIOS_TURNO: dict[Turno, str] = {
    "Mañana": "08:30 - 12:30",
    "Tarde": "14:30 - 18:30",
    "Noche": "19:00 - 22:00",
    "Sábado": "09:00 - 14:30",
}
"""Horario aproximado de cada turno (para mostrar en la UI)."""


# ======================================================================
# Modelos anidados
# ======================================================================


class PlanAnual(TypedDict):
    """
    Representa un año del plan de estudios con su lista de materias.

    Ejemplo:
        {
            "anio": "Primer Año",
            "materias": [
                "Introducción a la Informática",
                "Matemática Aplicada",
                ...
            ],
        }
    """

    anio: str
    """Etiqueta del año (ej: "Primer Año", "Segundo Año")."""

    materias: list[str]
    """Lista de materias del año, en orden de cursado."""


class PreguntaFrecuente(TypedDict):
    """
    Representa una pregunta frecuente específica de una carrera con su
    respuesta.

    Ejemplo:
        {
            "pregunta": "¿Necesito saber programar antes de entrar?",
            "respuesta": "No, empezamos desde cero...",
        }
    """

    pregunta: str
    respuesta: str


class IconoAnimado(TypedDict):
    """
    Icono que orbita alrededor de la imagen principal de la carrera.

    Los parámetros describen una órbita elíptica kepleriana con
    achatamiento vertical (perspectiva 3D tipo "disco visto de lado").

    Ejemplo:
        {
            "nombre": "code-xml",
            "semieje_mayor": 55.0,
            "excentricidad": 0.25,
            "factor_perspectiva": 0.5,
            "angulo_inicial": 0,
            "periodo": 18.0,
            "desfase_temporal": 0.0,
            "color": "#2563eb",
            "tiene_anillos": True,
            "keyframe_orbita": "orbita_0_550",
        }
    """

    nombre: str
    """Nombre del icono de Lucide (kebab-case recomendado)."""

    semieje_mayor: float
    """Radio horizontal de la elipse, en % del contenedor (0-100)."""

    excentricidad: float
    """Excentricidad orbital (0.0 = círculo, 1.0 = muy elíptica)."""

    factor_perspectiva: float
    """Aplanamiento vertical (0.5 = disco de lado, 1.0 = sin aplanar)."""

    angulo_inicial: int
    """Ángulo inicial de la órbita, en grados (0-359)."""

    periodo: float
    """Duración de una vuelta completa, en segundos."""

    desfase_temporal: float
    """Retraso inicial de la animación, en segundos."""

    color: ColorHex
    """Color hex del icono orbital."""

    tiene_anillos: bool
    """Si el icono debe llevar anillos tipo Saturno."""

    keyframe_orbita: str
    """Nombre del `@keyframes` CSS generado para esta órbita."""


class EstadisticasCarrera(TypedDict):
    """
    Métricas cuantitativas de una carrera, usadas en las tarjetas del
    listado y en el panel de filtros.

    Ejemplo:
        {
            "demanda_laboral": "alta",
            "puntuacion": 4.8,
            "estudiantes_inscritos": 87,
            "estudiantes_graduados": 234,
            "tasa_empleabilidad": 95,
            "salario_promedio_bs": 4500,
        }
    """

    demanda_laboral: DemandaLaboral
    """Nivel de demanda: `"alta"`, `"media"` o `"baja"`."""

    puntuacion: float
    """Puntuación promedio de la carrera (0.0 - 5.0)."""

    estudiantes_inscritos: int
    """Estudiantes inscritos actualmente."""

    estudiantes_graduados: int
    """Egresados históricos de la carrera."""

    tasa_empleabilidad: int
    """Porcentaje de empleabilidad (0-100)."""

    salario_promedio_bs: int
    """Salario promedio en bolivianos."""


class CaracteristicaCarrera(TypedDict):
    """
    Característica específica de una carrera (badge informativo con
    icono + etiqueta + descripción corta).

    Ejemplo:
        {
            "icono": "cpu",
            "etiqueta": "Laboratorios equipados",
            "descripcion": "20 PCs con hardware moderno",
        }
    """

    icono: str
    etiqueta: str
    descripcion: str


# ======================================================================
# Modelo principal: Carrera
# ======================================================================


class Carrera(TypedDict):
    """
    Estructura completa de una carrera técnica ofrecida por el instituto.

    Sistema de color (light + dark)
    -------------------------------
    Cada carrera expone 4 colores para adaptarse al `color_mode`:

    **Light mode:**
        - `color_principal`: color de marca (hex, ej: "#2563eb").
        - `color_suave`: tinte de fondo suave (hex, ej: "#eff6ff").

    **Dark mode:**
        - `color_principal_dark`: versión del color de marca ajustada
          para fondos oscuros (más luminosa, ej: "#60a5fa").
        - `color_suave_dark`: tinte de fondo suave para dark mode
          (hex oscuro con matiz de marca, ej: "#1e3a8a").

    ⚠️ IMPORTANTE: Si el proyecto decide usar **un solo acento global**
    (ej: azul marino `#3b5bdb`) para todas las carreras, los 4 campos
    de color pueden quedar con el mismo valor, o eliminarse y usar
    directamente los tokens de `constantes_visuales.py`.
    """

    # --- Identificación ---
    id: int
    """Identificador único de la carrera (usado en la URL `/carrera/{id}`)."""

    nombre: str
    """Nombre completo de la carrera."""

    nombre_corto: str
    """Nombre abreviado para tarjetas y menús."""

    duracion: str
    """Duración como texto (ej: "3 Años")."""

    lema: str
    """Frase corta que resume la carrera."""

    descripcion: str
    """Descripción larga de 1-2 párrafos."""

    # --- Contenido académico ---
    perfil_profesional: list[str]
    """Habilidades y competencias que el egresado desarrollará."""

    campo_laboral: list[str]
    """Dónde puede trabajar el egresado."""

    preguntas_frecuentes: list[PreguntaFrecuente]
    """FAQ específicas de la carrera."""

    plan_estudios: list[PlanAnual]
    """Materias agrupadas por año."""

    # --- Icono principal ---
    icono: str
    """Nombre del icono de Lucide que representa la carrera."""

    # --- Colores light mode ---
    color_principal: ColorHex
    """Color de marca principal en light mode."""

    color_suave: ColorHex
    """Tinte de fondo suave en light mode."""

    # --- Colores dark mode ---
    color_principal_dark: ColorHex
    """Color de marca principal en dark mode (más luminoso)."""

    color_suave_dark: ColorHex
    """Tinte de fondo suave en dark mode."""

    # --- Recursos multimedia ---
    imagen_archivo: str
    """Nombre del archivo de imagen principal en `assets/`."""

    imagen_banner: str
    """Nombre del archivo de imagen banner (16:9) en `assets/`."""

    iconos_animados: list[IconoAnimado]
    """Iconos que orbitan alrededor de la imagen principal."""

    # --- Métricas y características ---
    estadisticas: EstadisticasCarrera
    """Métricas cuantitativas de la carrera."""

    caracteristicas: list[CaracteristicaCarrera]
    """Características destacadas (badges informativos)."""

    modalidad: Modalidad
    """Modalidad de cursado."""

    turnos: list[Turno]
    """Turnos disponibles para esta carrera.

    Valores válidos: `"Mañana"`, `"Tarde"`, `"Noche"`, `"Sábado"`.

    Ejemplo: `["Mañana", "Noche", "Sábado"]`.

    El turno `"Sábado"` corresponde a clases intensivas de 08:00 a
    14:00, pensadas para estudiantes que no pueden asistir entre
    semana.
    """

    cupos_disponibles: int
    """Cupos disponibles para la próxima gestión."""


# ======================================================================
# Modelo derivado: Carrera con etiqueta
# ======================================================================


class CarreraConEtiqueta(TypedDict):
    """
    Combina una carrera con su etiqueta contextual del carrusel.

    Usado por `EstadoInstitucional.carreras_destacadas_con_etiquetas`
    para el carrusel del hero de `/carreras`.

    Ejemplo:
        {
            "carrera": { ...Carrera completa... },
            "etiqueta": "Inscripciones abiertas",
        }
    """

    carrera: Carrera
    etiqueta: str
    """Etiqueta contextual (ej: "Inscripciones abiertas", "Cupos limitados")."""


# ======================================================================
# EXPORTS
# ======================================================================

__all__ = [
    # --- Alias de tipos ---
    "ColorHex",
    "DemandaLaboral",
    "Modalidad",
    "Turno",
    # --- Constantes ---
    "HORARIOS_TURNO",
    "TURNOS_VALIDOS",
    # --- Modelos anidados ---
    "CaracteristicaCarrera",
    "EstadisticasCarrera",
    "IconoAnimado",
    "PlanAnual",
    "PreguntaFrecuente",
    # --- Modelos principales ---
    "Carrera",
    "CarreraConEtiqueta",
]