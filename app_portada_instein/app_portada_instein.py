"""
Punto de entrada de la aplicación web del INSTEIN.

Este módulo:
- Registra todas las páginas de la aplicación.
- Configura el tema global (light/dark, accent, radius).
- Fusiona las keyframes CSS de estilos personalizados y del motor kepleriano.
- Carga las fuentes Inter y JetBrains Mono desde Google Fonts + un
  stylesheet personalizado que aplica las fuentes a etiquetas HTML.

El motor kepleriano vive en `dominio.kepler` y es agnóstico a Reflex.
"""

import reflex as rx

from app_portada_instein.datos.catalogo_carreras import CATALOGO_CARRERAS
from app_portada_instein.dominio.kepler import (
    DefinicionKeyframe,
    generar_keyframes_css,
    generar_pasos_orbita,
)
from app_portada_instein.infraestructura.constantes_visuales import (
    ESTILO_BASE,
    ESTILOS_GLOBALES_CSS,
    FUENTE_PRINCIPAL,
    HOJAS_DE_ESTILO_BASE,
)


# ======================================================================
# ⚠️ IMPORT CRÍTICO: REGISTRA LAS PÁGINAS
# ======================================================================
# Este import NO se usa directamente, pero es OBLIGATORIO porque al
# importar los módulos de vistas se ejecutan sus decoradores
# `@rx.page(...)`, que registran las rutas en la app de Reflex.
#
# Si comentas o eliminas este import, la app arranca SIN páginas y
# verás una pantalla en blanco en http://localhost:3000
# ======================================================================
from app_portada_instein.vistas import (  # noqa: F401
    vista_admision,
    vista_becas,
    vista_calendario,
    vista_carreras,
    vista_contacto,
    vista_detalle_carrera,
    vista_faq,
    vista_inicio,
    vista_sobre_nosotros,
)


# ======================================================================
# Keyframes de UI (independientes del motor kepleriano)
# ======================================================================

KEYFRAMES_UI: dict = {
    "@keyframes pulso_central": {
        "0%, 100%": {"transform": "translate(-50%, -50%) scale(1)"},
        "50%": {"transform": "translate(-50%, -50%) scale(1.05)"},
    },
    "@keyframes flotar_estrella": {
        "0%, 100%": {"opacity": "0.4"},
        "50%": {"opacity": "1"},
    },
    "@keyframes pulso_verde": {
        "0%, 100%": {"opacity": "1", "transform": "scale(1)"},
        "50%": {"opacity": "0.6", "transform": "scale(1.15)"},
    },
    "@keyframes flotar_icono_particula": {
        "0%, 100%": {
            "transform": "translateY(0) rotate(var(--rotacion, 0deg))",
            "opacity": "0.15",
        },
        "25%": {
            "transform": "translateY(-8px) rotate(var(--rotacion, 0deg))",
            "opacity": "0.25",
        },
        "50%": {
            "transform": "translateY(-15px) rotate(var(--rotacion, 0deg))",
            "opacity": "0.35",
        },
        "75%": {
            "transform": "translateY(-8px) rotate(var(--rotacion, 0deg))",
            "opacity": "0.25",
        },
    },
    "@keyframes flotar_cristal": {
        "0%, 100%": {"transform": "translateY(0) rotate(0deg)"},
        "50%": {"transform": "translateY(-30px) rotate(8deg)"},
    },
    "@keyframes deslizar_linea": {
        "0%": {"transform": "translateX(-100%)", "opacity": "0"},
        "50%": {"opacity": "0.6"},
        "100%": {"transform": "translateX(100%)", "opacity": "0"},
    },
    "@keyframes deslizar_desde_abajo": {
        "from": {"transform": "translateY(20px)", "opacity": "0"},
        "to": {"transform": "translateY(0)", "opacity": "1"},
    },
}


# ======================================================================
# Keyframes de órbitas keplerianas (delegadas al motor)
# ======================================================================


def _iconos_unicos_por_keyframe() -> dict[str, dict]:
    """Recopila los iconos animados únicos de todas las carreras."""
    vistos: dict[str, dict] = {}
    for carrera in CATALOGO_CARRERAS:
        for icono in carrera["iconos_animados"]:
            clave = icono["keyframe_orbita"]
            if clave not in vistos:
                vistos[clave] = icono
    return vistos


def _generar_keyframes_orbitales() -> dict:
    """Genera los @keyframes de todas las órbitas keplerianas."""
    definiciones: list[DefinicionKeyframe] = []

    for sufijo, icono in _iconos_unicos_por_keyframe().items():
        pasos = generar_pasos_orbita(
            semieje_mayor=icono["semieje_mayor"],
            excentricidad=icono["excentricidad"],
            factor_perspectiva=icono["factor_perspectiva"],
            angulo_inicial_grados=icono["angulo_inicial"],
        )
        definiciones.append({"nombre": sufijo, "pasos": pasos})

    return generar_keyframes_css(definiciones)


# ======================================================================
# Fusión de estilos globales
# ======================================================================

ESTILOS_GLOBALES: dict = {
    **KEYFRAMES_UI,
    **_generar_keyframes_orbitales(),
    **ESTILOS_GLOBALES_CSS,   # ← ✅ Restaurado
    **ESTILO_BASE,            # ← ✅ Restaurado
}


# ======================================================================
# Configuración de la aplicación
# ======================================================================

app = rx.App(
    theme=rx.theme(
        appearance="light",
        accent_color="crimson",
        radius="medium",
        font_family=FUENTE_PRINCIPAL,   # ← ✅ Restaurado
    ),
    style=ESTILOS_GLOBALES,
    stylesheets=[
        *HOJAS_DE_ESTILO_BASE,          # ← ✅ Restaurado
        "/styles/global.css",
    ],
)