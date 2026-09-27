"""
Punto de entrada de la aplicación web del Instituto Técnico Integrado
San Antonio de Padua (INSTEIN).

Este módulo genera keyframes CSS y estilos globales que simulan:
- Órbitas keplerianas para los iconos (con perspectiva achatada).
- Líneas de fuga radiales tipo "sistema solar ilustrado".
- Fondo estrellado decorativo (adaptativo a modo claro/oscuro).
"""

import math

import reflex as rx

from app_portada_instein.vistas import (
    vista_inicio,
    vista_carreras,
    vista_detalle_carrera,
    vista_contacto,
)


# ======================================================================
# Constantes de conversión
# ======================================================================

# El contenedor orbital mide 32rem de ancho (ver widgets_home.py).
# Como el `translate` en CSS con `%` es relativo al propio elemento
# (no al padre), necesitamos convertir los semiejes a unidades absolutas.
ANCHO_CONTENEDOR_REM = 32.0
FACTOR_CONVERSION_REM = ANCHO_CONTENEDOR_REM / 100.0


# ======================================================================
# Motor físico: resolución de las leyes de Kepler
# ======================================================================

def _resolver_kepler(anomalia_media: float, excentricidad: float) -> float:
    """
    Resuelve la Ecuación de Kepler: M = E - e·sin(E).

    Usa el método de Newton-Raphson para encontrar la anomalía
    excéntrica E dada la anomalía media M.
    """
    E = anomalia_media

    for _ in range(8):
        f = E - excentricidad * math.sin(E) - anomalia_media
        f_prima = 1 - excentricidad * math.cos(E)
        if abs(f_prima) < 1e-10:
            break
        E = E - f / f_prima

    return E


def _posicion_en_orbita(
    anomalia_media: float,
    semieje_mayor: float,
    excentricidad: float,
) -> tuple[float, float]:
    """
    Calcula la posición (x, y) en la órbita elíptica (Sol en el foco).

    Args:
        anomalia_media: M en radianes (0 a 2π).
        semieje_mayor: a (radio horizontal).
        excentricidad: e (0 = círculo).

    Returns:
        Tupla (x, y) en coordenadas de pantalla.
    """
    semieje_menor = semieje_mayor * math.sqrt(1 - excentricidad ** 2)
    E = _resolver_kepler(anomalia_media, excentricidad)

    x = semieje_mayor * (math.cos(E) - excentricidad)
    y = semieje_menor * math.sin(E)

    return x, y


# ======================================================================
# Generador de keyframes CSS para cada icono
# ======================================================================

def _generar_keyframes_orbitales() -> dict:
    """
    Genera las @keyframes CSS para cada icono, con:
    - Trayectoria kepleriana (Sol en el foco).
    - Perspectiva achatada (eje Y multiplicado por factor_perspectiva).
    - Escala y opacidad según posición vertical (efecto 3D).
    - Conversión de unidades: los semiejes están en % del contenedor,
      pero el `translate` de CSS se aplica en `rem` absolutos.
    """
    estilos: dict = {
        # --- Animación de la imagen central (Sol) ---
        "@keyframes pulso_central": {
            "0%, 100%": {"transform": "translate(-50%, -50%) scale(1)"},
            "50%": {"transform": "translate(-50%, -50%) scale(1.05)"},
        },
        # --- Animación sutil de las estrellas de fondo ---
        "@keyframes flotar_estrella": {
            "0%, 100%": {"opacity": "0.4"},
            "50%": {"opacity": "1"},
        },
    }

    from app_portada_instein.datos.catalogo_carreras import CATALOGO_CARRERAS

    # Recolectamos cada configuración única de icono.
    iconos_vistos: dict[str, dict] = {}
    for carrera in CATALOGO_CARRERAS:
        for icono in carrera["iconos_animados"]:
            clave = icono["keyframe_orbita"]
            if clave not in iconos_vistos:
                iconos_vistos[clave] = icono

    NUM_PASOS = 60  # 60 pasos = cada 6° → órbita muy suave

    for sufijo, icono in iconos_vistos.items():
        a = icono["semieje_mayor"]
        e = icono["excentricidad"]
        perspectiva = icono["factor_perspectiva"]
        angulo_inicial = math.radians(icono["angulo_inicial"])

        keyframes_orbita: dict = {}

        for paso in range(NUM_PASOS + 1):
            fraccion = paso / NUM_PASOS
            M = 2 * math.pi * fraccion

            # Posición kepleriana (Sol en el foco) en % del contenedor
            x_elipse_pct, y_elipse_pct = _posicion_en_orbita(M, a, e)

            # Aplicamos perspectiva: el eje Y se aplasta
            y_perspectiva_pct = y_elipse_pct * perspectiva

            # Aplicamos el ángulo inicial rotando la elipse completa
            x_rot_pct = (
                x_elipse_pct * math.cos(angulo_inicial)
                - y_perspectiva_pct * math.sin(angulo_inicial)
            )
            y_rot_pct = (
                x_elipse_pct * math.sin(angulo_inicial)
                + y_perspectiva_pct * math.cos(angulo_inicial)
            )

            # Conversión clave: de % a rem absolutos.
            x_rem = x_rot_pct * FACTOR_CONVERSION_REM
            y_rem = y_rot_pct * FACTOR_CONVERSION_REM

            # Escala y opacidad según la posición vertical
            y_norm = y_rot_pct / max(a, 0.01)
            escala = 0.85 + y_norm * 0.35
            opacidad = 0.65 + y_norm * 0.35

            escala = max(0.55, min(1.2, escala))
            opacidad = max(0.45, min(1.0, opacidad))

            porcentaje = f"{int(fraccion * 100)}%"

            keyframes_orbita[porcentaje] = {
                "transform": (
                    f"translate(-50%, -50%) "
                    f"translate({x_rem:.3f}rem, {y_rem:.3f}rem) "
                    f"scale({escala:.2f})"
                ),
                "opacity": f"{opacidad:.2f}",
            }

        estilos[f"@keyframes {sufijo}"] = keyframes_orbita

    return estilos


ESTILOS_GLOBALES = _generar_keyframes_orbitales()


app = rx.App(
    theme=rx.theme(
        appearance="light",
        accent_color="blue",
        radius="medium",
    ),
    style=ESTILOS_GLOBALES,
)