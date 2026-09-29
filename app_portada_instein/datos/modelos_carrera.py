"""
Modelos de datos (tipados) que describen la estructura de una carrera
y su plan de estudios anual.
"""

from typing import TypedDict


class PlanAnual(TypedDict):
    """Representa un año del plan de estudios con su lista de materias."""
    anio: str
    materias: list[str]


class PreguntaFrecuente(TypedDict):
    """Representa una pregunta frecuente con su respuesta."""
    pregunta: str
    respuesta: str


class IconoAnimado(TypedDict):
    """Icono que orbita alrededor de la imagen principal de la carrera."""
    nombre: str
    semieje_mayor: float
    excentricidad: float
    factor_perspectiva: float
    angulo_inicial: int
    periodo: float
    desfase_temporal: float
    color: str
    tiene_anillos: bool
    keyframe_orbita: str


class EstadisticasCarrera(TypedDict):
    """Métricas cuantitativas de una carrera."""
    demanda_laboral: str  # 'alta' | 'media' | 'baja'
    puntuacion: float
    estudiantes_inscritos: int
    estudiantes_graduados: int
    tasa_empleabilidad: int
    salario_promedio_bs: int


class CaracteristicaCarrera(TypedDict):
    """Característica específica de una carrera (badge informativo)."""
    icono: str
    etiqueta: str
    descripcion: str


class Carrera(TypedDict):
    """
    Estructura completa de una carrera técnica ofrecida por el instituto.

    Sistema de color
    ----------------
    Cada carrera expone 4 colores para adaptarse al color_mode:

    Light mode:
        - `color_principal`: color de marca (hex, ej: "#2563eb").
        - `color_suave`: tinte de fondo suave (hex, ej: "#eff6ff").

    Dark mode:
        - `color_principal_dark`: versión del color de marca ajustada
          para fondos oscuros (más luminosa, ej: "#60a5fa").
        - `color_suave_dark`: tinte de fondo suave para dark mode
          (hex oscuro con matiz de marca, ej: "#1e3a8a").
    """
    id: int
    nombre: str
    nombre_corto: str
    duracion: str
    lema: str
    descripcion: str
    perfil_profesional: list[str]
    campo_laboral: list[str]
    preguntas_frecuentes: list[PreguntaFrecuente]
    plan_estudios: list[PlanAnual]
    icono: str

    # --- Colores light mode ---
    color_principal: str
    color_suave: str

    # --- Colores dark mode ---
    color_principal_dark: str
    color_suave_dark: str

    # --- Recursos ---
    imagen_archivo: str
    imagen_banner: str
    iconos_animados: list[IconoAnimado]

    # --- Nuevos campos ---
    estadisticas: EstadisticasCarrera
    caracteristicas: list[CaracteristicaCarrera]
    modalidad: str
    turnos: list[str]
    cupos_disponibles: int


class CarreraConEtiqueta(TypedDict):
    """Combina una carrera con su etiqueta contextual."""
    carrera: Carrera
    etiqueta: str