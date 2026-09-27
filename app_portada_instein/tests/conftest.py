"""
Fixtures compartidas para los tests del motor kepleriano.

Convención: las fixtures devuelven parámetros con los nombres exactos
que aceptan las funciones del módulo `dominio.kepler`, para permitir
`generar_pasos_orbita(**orbita)`.
"""

from __future__ import annotations

import pytest


# ======================================================================
# Fixtures numéricas
# ======================================================================

@pytest.fixture
def excentricidades_tipicas() -> list[float]:
    """Excentricidades usadas en el catálogo real de carreras."""
    return [0.15, 0.20, 0.25, 0.30]


@pytest.fixture
def excentricidades_amplias() -> list[float]:
    """Rango amplio de excentricidades para tests de robustez."""
    return [0.0, 0.1, 0.3, 0.5, 0.7, 0.9]


@pytest.fixture
def angulos_todos() -> list[float]:
    """Ángulos cardinales para tests de rotación."""
    return [0.0, 90.0, 180.0, 270.0, 360.0, -90.0]


# ======================================================================
# Fixtures de órbitas (parámetros con nombres exactos a la API)
# ======================================================================

@pytest.fixture
def orbitas_estandar() -> list[dict]:
    """
    Órbitas con parámetros similares a las del catálogo real.

    ⚠️ IMPORTANTE: los nombres de las claves DEBEN coincidir con los
    parámetros de `generar_pasos_orbita` para que funcione el
    desempaquetado `generar_pasos_orbita(**orbita)`.

    Parámetros esperados:
        - semieje_mayor (float)
        - excentricidad (float)
        - factor_perspectiva (float)
        - angulo_inicial_grados (float)  ← antes era `angulo_inicial`
    """
    return [
        {
            "semieje_mayor": 55.0,
            "excentricidad": 0.25,
            "factor_perspectiva": 0.5,
            "angulo_inicial_grados": 0,
        },
        {
            "semieje_mayor": 70.0,
            "excentricidad": 0.15,
            "factor_perspectiva": 0.5,
            "angulo_inicial_grados": 90,
        },
        {
            "semieje_mayor": 62.0,
            "excentricidad": 0.30,
            "factor_perspectiva": 0.5,
            "angulo_inicial_grados": 180,
        },
        {
            "semieje_mayor": 85.0,
            "excentricidad": 0.20,
            "factor_perspectiva": 0.5,
            "angulo_inicial_grados": 270,
        },
    ]


@pytest.fixture
def orbitas_degeneradas() -> list[dict]:
    """Órbitas con parámetros límite."""
    return [
        # Órbita circular perfecta.
        {
            "semieje_mayor": 50.0,
            "excentricidad": 0.0,
            "factor_perspectiva": 1.0,
            "angulo_inicial_grados": 0,
        },
        # Órbita muy excéntrica.
        {
            "semieje_mayor": 80.0,
            "excentricidad": 0.9,
            "factor_perspectiva": 0.5,
            "angulo_inicial_grados": 45,
        },
        # Perspectiva extrema (casi plana).
        {
            "semieje_mayor": 60.0,
            "excentricidad": 0.3,
            "factor_perspectiva": 0.05,
            "angulo_inicial_grados": 120,
        },
    ]