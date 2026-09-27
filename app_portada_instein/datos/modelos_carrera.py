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


class Carrera(TypedDict):
    """Estructura completa de una carrera técnica ofrecida por el instituto."""

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
    color_principal: str
    color_suave: str

    # --- Imágenes de la carrera ---
    imagen_archivo: str
    """Imagen cuadrada (1:1) para tarjetas y listas."""

    imagen_banner: str
    """Imagen horizontal (16:9) para el carrusel de banners."""

    iconos_animados: list[IconoAnimado]


class CarreraConEtiqueta(TypedDict):
    """Combina una carrera con su etiqueta contextual."""

    carrera: Carrera
    etiqueta: str