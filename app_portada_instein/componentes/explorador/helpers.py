"""
Helpers de color adaptativo del explorador.
"""

import reflex as rx

from app_portada_instein.dominio.estado_institucional import EstadoInstitucional
from app_portada_instein.infraestructura.constantes_visuales import (
    color_carrera_adaptativo,
    color_suave_carrera_adaptativo,
)


def color_carrera(carrera: dict) -> rx.Var:
    """Color principal de la carrera adaptado al color_mode."""
    return color_carrera_adaptativo(carrera)


def color_suave_carrera(carrera: dict) -> rx.Var:
    """Color suave de la carrera adaptado al color_mode."""
    return color_suave_carrera_adaptativo(carrera)


def color_carrera_destacada() -> rx.Var:
    """Color principal de la carrera destacada (la del home)."""
    return color_carrera(EstadoInstitucional.carrera_destacada)


def color_suave_carrera_destacada() -> rx.Var:
    """Color suave de la carrera destacada (la del home)."""
    return color_suave_carrera(EstadoInstitucional.carrera_destacada)


__all__ = [
    "color_carrera",
    "color_carrera_destacada",
    "color_suave_carrera",
    "color_suave_carrera_destacada",
]