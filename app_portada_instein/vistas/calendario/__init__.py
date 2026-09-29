"""
Paquete de la vista del Calendario Académico.

API pública:
- `vista_calendario()`: la página completa registrada con `@rx.page`.

Uso desde `app_portada_instein.py`:
    from app_portada_instein.vistas.calendario import vista_calendario
"""

from .vista import vista_calendario

__all__ = ["vista_calendario"]