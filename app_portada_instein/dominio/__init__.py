"""
Capa de dominio.

Contiene el estado global de la aplicación pública. Es la única
fuente de verdad para la navegación, la carrera activa y el plan
de estudios visible.
"""

from .estado_institucional import EstadoInstitucional


__all__ = ["EstadoInstitucional"]
