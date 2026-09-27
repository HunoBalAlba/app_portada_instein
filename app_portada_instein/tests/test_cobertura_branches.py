"""
Tests específicos para cubrir las dos ramas de salida del bucle
de Newton-Raphson en `resolver.py`:

    Rama A: `break` (convergencia) → salta al return.
    Rama B: agotamiento del `for` (sin break) → cae al return.

Coverage marca estas dos salidas como ramas distintas, por lo que
ambas deben ejecutarse para alcanzar el 100%.
"""

from __future__ import annotations

import math

import pytest

from app_portada_instein.dominio.kepler import resolver_kepler


# ======================================================================
# Rama A: salida por CONVERGENCIA (`break`)
# ======================================================================


class TestRamaConvergencia:
    """Fuerza que el bucle salga por `break`, no por agotamiento."""

    def test_convergencia_rapida_con_max_iteraciones_alto(self) -> None:
        """Con `max_iteraciones` alto, el bucle sale por `break`."""
        E = resolver_kepler(math.pi, 0.3, max_iteraciones=50)
        residual = E - 0.3 * math.sin(E) - math.pi
        assert abs(residual) < 1e-10

    def test_convergencia_con_valores_aleatorios(self) -> None:
        """Múltiples combinaciones (M, e) con max_iteraciones=100."""
        casos = [
            (0.1, 0.05),
            (0.5, 0.1),
            (1.0, 0.2),
            (2.0, 0.3),
            (3.0, 0.4),
            (4.0, 0.5),
            (-1.0, 0.2),
            (-2.5, 0.35),
        ]
        for M, e in casos:
            E = resolver_kepler(M, e, max_iteraciones=100)
            residual = E - e * math.sin(E) - M
            assert abs(residual) < 1e-9, f"Falló con M={M}, e={e}"

    def test_convergencia_con_tolerancia_grande(self) -> None:
        """Con tolerancia grande, la convergencia es inmediata."""
        E = resolver_kepler(
            anomalia_media=0.5,
            excentricidad=0.1,
            max_iteraciones=50,
            tolerancia=1e-1,
        )
        assert abs(E - 0.5) < 0.5

    def test_convergencia_con_tolerancia_estricta(self) -> None:
        """Con tolerancia muy estricta, debe converger eventualmente."""
        E = resolver_kepler(
            anomalia_media=1.2,
            excentricidad=0.4,
            max_iteraciones=100,
            tolerancia=1e-15,
        )
        residual = E - 0.4 * math.sin(E) - 1.2
        assert abs(residual) < 1e-12

    @pytest.mark.parametrize("M", [0.01, 0.5, 1.5, 2.5, 3.0, 5.0])
    @pytest.mark.parametrize("e", [0.01, 0.1, 0.3, 0.5, 0.7])
    def test_grid_convergencia(self, M: float, e: float) -> None:
        """Grid exhaustivo: 30 combinaciones con max_iteraciones=100."""
        E = resolver_kepler(M, e, max_iteraciones=100)
        residual = E - e * math.sin(E) - M
        assert abs(residual) < 1e-9


# ======================================================================
# Rama B: salida por AGOTAMIENTO del `for` (sin break)
# ======================================================================


class TestRamaAgotamiento:
    """
    Fuerza que el bucle `for` termine por agotamiento sin `break`.

    Cálculo verificado para M=2.0, e=0.9, max_iteraciones=1:
        M_norm = 2.0
        E_0    = 2.0
        f      = 2.0 - 0.9·sin(2.0) - 2.0 = -0.818
        f'     = 1 - 0.9·cos(2.0) = 1.374
        delta  = -0.595   (≥ 1e-10, NO break)
        → for agota → rama 86->104 ✅
    """

    def test_agotamiento_m_2_e_09(self) -> None:
        """EL test que cubre la rama 86->104."""
        E = resolver_kepler(
            anomalia_media=2.0,
            excentricidad=0.9,
            max_iteraciones=1,
        )
        assert math.isfinite(E)
        # No convergió (residual grande).
        residual = E - 0.9 * math.sin(E) - 2.0
        assert abs(residual) > 1e-3

    @pytest.mark.parametrize(
        "M, e, max_iter",
        [
            (2.0, 0.9, 1),  # delta ≈ -0.595 → no break
            (1.0, 0.8, 1),  # delta ≈ -0.5 → no break
            (0.5, 0.9, 1),  # delta ≈ -0.3 → no break
            (-1.5, 0.8, 1),
            (3.0, 0.95, 1),
            (5.0, 0.7, 2),
        ],
    )
    def test_grid_agotamiento(self, M: float, e: float, max_iter: int) -> None:
        """Grid de casos que agotan el for sin break."""
        E = resolver_kepler(M, e, max_iteraciones=max_iter)
        assert math.isfinite(E)

    def test_agotamiento_con_tolerancia_imposible(self) -> None:
        """Con tolerancia < precisión de máquina, NUNCA hay break."""
        E = resolver_kepler(
            anomalia_media=1.0,
            excentricidad=0.5,
            max_iteraciones=8,
            tolerancia=1e-300,
        )
        assert math.isfinite(E)

    def test_agotamiento_varios_ciclos(self) -> None:
        """Múltiples llamadas que agotan el for."""
        for M in [0.3, 0.7, 1.3, 2.7, 4.1, 5.5]:
            E = resolver_kepler(
                anomalia_media=M,
                excentricidad=0.85,
                max_iteraciones=1,
            )
            assert math.isfinite(E)


# ======================================================================
# Casos límite
# ======================================================================


class TestCasosLimite:
    """Casos límite y de robustez numérica."""

    def test_anomalia_muy_grande(self) -> None:
        assert math.isfinite(resolver_kepler(1000 * math.pi, 0.3))

    def test_anomalia_muy_negativa(self) -> None:
        assert math.isfinite(resolver_kepler(-1000 * math.pi, 0.3))

    def test_excentricidad_maxima(self) -> None:
        E = resolver_kepler(math.pi, 0.99, max_iteraciones=50)
        residual = E - 0.99 * math.sin(E) - math.pi
        assert abs(residual) < 1e-8

    def test_excentricidad_cero(self) -> None:
        assert resolver_kepler(123.456, 0.0) == 123.456
