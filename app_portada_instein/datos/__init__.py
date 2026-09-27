"""
Capa de datos.

Expone el catálogo de carreras y los modelos tipados que describen
su estructura. Esta capa no depende de Reflex ni de la UI.
"""

from .catalogo_carreras import CATALOGO_CARRERAS, PALETA_COLORES
from .modelos_carrera import Carrera, PlanAnual


__all__ = [
    "CATALOGO_CARRERAS",
    "PALETA_COLORES",
    "Carrera",
    "PlanAnual",
]
