"""
Modelos de datos (tipados) que describen la estructura de una carrera
y su plan de estudios anual.
"""

from typing import TypedDict


class PlanAnual(TypedDict):
    """Representa un año del plan de estudios con su lista de materias."""

    anio: str
    materias: list[str]


class IconoAnimado(TypedDict):
    """
    Icono que orbita alrededor de la imagen central siguiendo las leyes
    de Kepler, con una elipse aplastada para simular perspectiva 3D
    (vista de disco inclinado, como en la ilustración del sistema solar).

    La trayectoria se precalcula en el backend y se convierte en keyframes
    CSS. El icono NUNCA rota sobre su propio eje.
    """

    nombre: str
    """Identificador del icono Lucide (ej: "cpu", "database")."""

    semieje_mayor: float
    """Radio horizontal de la elipse (en % del contenedor)."""

    excentricidad: float
    """Excentricidad orbital (0 = círculo, 0.5 = elipse marcada)."""

    factor_perspectiva: float
    """Factor de aplanamiento vertical (0.5 = disco visto de lado)."""

    angulo_inicial: int
    """Ángulo inicial en grados para distribuir los iconos."""

    periodo: float
    """Duración en segundos de una vuelta completa."""

    desfase_temporal: float
    """Retraso inicial en segundos para desincronizar los iconos."""

    color: str
    """Color del icono en formato hexadecimal."""

    tiene_anillos: bool
    """Si el icono debe dibujarse con anillos (estilo Saturno)."""

    keyframe_orbita: str
    """Nombre del keyframe CSS de la trayectoria orbital."""


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
    plan_estudios: list[PlanAnual]
    icono: str
    color_principal: str
    color_suave: str
    imagen_archivo: str
    iconos_animados: list[IconoAnimado]