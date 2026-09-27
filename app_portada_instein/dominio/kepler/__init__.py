"""
Motor kepleriano puro para Reflex.

Este paquete NO depende de Reflex. Expone funciones puras y tipadas
para calcular órbitas elípticas y generar sus @keyframes CSS.

Uso típico desde `app_portada_instein.py`:

    from app_portada_instein.dominio.kepler import (
        generar_pasos_orbita,
        generar_keyframes_css,
        DefinicionKeyframe,
    )

    def _generar_keyframes_proyecto() -> dict:
        definiciones = []
        for icono in iconos_unicos:
            sufijo = icono["keyframe_orbita"]
            pasos = generar_pasos_orbita(
                semieje_mayor=icono["semieje_mayor"],
                excentricidad=icono["excentricidad"],
                factor_perspectiva=icono["factor_perspectiva"],
                angulo_inicial_grados=icono["angulo_inicial"],
            )
            definiciones.append({"nombre": sufijo, "pasos": pasos})
        return generar_keyframes_css(definiciones)
"""

from .constantes import (
    ANCHO_CONTENEDOR_REM,
    ESCALA_BASE,
    ESCALA_MAXIMA,
    ESCALA_MINIMA,
    ESCALA_VARIACION,
    EXCENTRICIDAD_MAXIMA,
    EXCENTRICIDAD_MINIMA,
    FACTOR_CONVERSION_REM,
    MAX_ITERACIONES_KEPLER,
    NUM_PASOS_KEYFRAMES,
    OPACIDAD_BASE,
    OPACIDAD_MAXIMA,
    OPACIDAD_MINIMA,
    OPACIDAD_VARIACION,
    TOLERANCIA_KEPLER,
)
from .keyframes import (
    DefinicionKeyframe,
    KeyframeStep,
    generar_keyframes_css,
    generar_pasos_orbita,
)
from .perspectiva import (
    CoordenadaPerspectiva,
    aplicar_perspectiva_y_rotacion,
    convertir_a_rem,
)
from .posicion import (
    PosicionOrbital,
    calcular_posicion_orbital,
)
from .resolver import (
    ErrorKepler,
    resolver_kepler,
)


__all__ = [
    # Constantes
    "ANCHO_CONTENEDOR_REM",
    "ESCALA_BASE",
    "ESCALA_MAXIMA",
    "ESCALA_MINIMA",
    "ESCALA_VARIACION",
    "EXCENTRICIDAD_MAXIMA",
    "EXCENTRICIDAD_MINIMA",
    "FACTOR_CONVERSION_REM",
    "MAX_ITERACIONES_KEPLER",
    "NUM_PASOS_KEYFRAMES",
    "OPACIDAD_BASE",
    "OPACIDAD_MAXIMA",
    "OPACIDAD_MINIMA",
    "OPACIDAD_VARIACION",
    "TOLERANCIA_KEPLER",
    "CoordenadaPerspectiva",
    "DefinicionKeyframe",
    "ErrorKepler",
    "KeyframeStep",
    "PosicionOrbital",
    # Perspectiva
    "aplicar_perspectiva_y_rotacion",
    # Posición
    "calcular_posicion_orbital",
    "convertir_a_rem",
    "generar_keyframes_css",
    # Keyframes
    "generar_pasos_orbita",
    # Resolver
    "resolver_kepler",
]
