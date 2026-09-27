"""
Test de regresión: verifica que las páginas se registran correctamente.

Este test detecta un bug común en Reflex: si olvidas importar los
módulos de vistas en el punto de entrada (`app_portada_instein.py`),
los decoradores `@rx.page(...)` no se ejecutan y la app arranca
SIN rutas (home en blanco).
"""

from __future__ import annotations

import reflex as rx

from app_portada_instein.app_portada_instein import app


class TestRegistroDePaginas:
    """Verifica que todas las rutas esperadas están registradas."""

    def test_app_esta_registrada(self) -> None:
        """La app debe ser una instancia de rx.App."""
        assert isinstance(app, rx.App)

    def test_hay_paginas_registradas(self) -> None:
        """La app debe tener al menos 4 páginas registradas."""
        rutas = list(app.pages.keys())
        assert len(rutas) >= 4, (
            f"Se esperaban al menos 4 páginas, se encontraron {len(rutas)}: "
            f"{rutas}. ¿Olvidaste importar `from app_portada_instein.vistas "
            f"import ...` en app_portada_instein.py?"
        )

    def test_ruta_raiz_registrada(self) -> None:
        """La ruta raíz '/' debe existir."""
        rutas = list(app.pages.keys())
        assert "/" in rutas, (
            f"La ruta raíz '/' no está registrada. Rutas: {rutas}. "
            f"¿Olvidaste importar `vista_inicio`?"
        )

    def test_ruta_carreras_registrada(self) -> None:
        """La ruta '/carreras' debe existir."""
        assert "/carreras" in app.pages, (
            f"La ruta '/carreras' no está registrada. "
            f"¿Olvidaste importar `vista_carreras`?"
        )

    def test_ruta_detalle_carrera_registrada(self) -> None:
        """La ruta dinámica '/carrera/[carrera_id]' debe existir."""
        rutas = list(app.pages.keys())
        assert any("/carrera" in r for r in rutas), (
            f"La ruta de detalle de carrera no está registrada. Rutas: {rutas}"
        )

    def test_ruta_contacto_registrada(self) -> None:
        """La ruta '/contacto' debe existir."""
        assert "/contacto" in app.pages, (
            f"La ruta '/contacto' no está registrada. "
            f"¿Olvidaste importar `vista_contacto`?"
        )

    def test_app_tiene_tema_configurado(self) -> None:
        """La app debe tener un tema configurado."""
        assert app.theme is not None