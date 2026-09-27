"""
Capa de datos.

Expone el catálogo de carreras y los modelos tipados que describen
su estructura. Esta capa no depende de Reflex ni de la UI.
"""

from .modelos_carrera import Carrera, PlanAnual
from .catalogo_carreras import CATALOGO_CARRERAS, PALETA_COLORES

__all__ = [
    "Carrera",
    "PlanAnual",
    "CATALOGO_CARRERAS",
    "PALETA_COLORES",
]