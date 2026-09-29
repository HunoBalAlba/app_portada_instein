"""
Constantes compartidas del explorador de carrera.
"""

# ======================================================================
# Layout
# ======================================================================

# Ancho máximo del buscador.
ANCHO_MAXIMO_BUSCADOR = "48rem"

# Padding inferior del grid de carreras.
PADDING_INFERIOR_GRID = "0 auto 3rem auto"

# Padding del contenedor del explorador.
from app_portada_instein.infraestructura.constantes_visuales import PADDING_LATERAL

PADDING_EXPLORADOR = f"2rem {PADDING_LATERAL}"

# Tamaño del botón flotante del panel.
TAMANO_BOTON_FLOTANTE = "3.5rem"

# Tamaño del icono en botones de opción.
TAMANO_ICONO_OPCION = 22

# Tamaño del icono del estado vacío.
TAMANO_ICONO_ESTADO_VACIO = 48


# ======================================================================
# Opciones del explorador
# ======================================================================

# Tuplas (icono, etiqueta, id_seccion) de las 5 opciones del explorador.
OPCIONES_EXPLORADOR: list[tuple[str, str, str]] = [
    ("info", "Información", "info"),
    ("book-open", "Plan", "plan"),
    ("user-check", "Perfil", "perfil"),
    ("briefcase", "Campo", "campo"),
    ("help-circle", "FAQ", "faq"),
]


__all__ = [
    "ANCHO_MAXIMO_BUSCADOR",
    "OPCIONES_EXPLORADOR",
    "PADDING_EXPLORADOR",
    "PADDING_INFERIOR_GRID",
    "TAMANO_BOTON_FLOTANTE",
    "TAMANO_ICONO_ESTADO_VACIO",
    "TAMANO_ICONO_OPCION",
]