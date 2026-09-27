"""Tests de la Ecuación de Kepler."""

import math

import pytest

from app_portada_instein.dominio.kepler import (
    ErrorKepler,
    resolver_kepler,
)


class TestOrbitaCircular:
    """Con e = 0, la solución es trivial: E = M."""

    @pytest.mark.parametrize("M", [0.0, math.pi / 2, math.pi, 3 * math.pi / 2])
    def test_E_igual_a_M(self, M: float) -> None:
        assert resolver_kepler(M, 0.0) == M

    def test_M_negativo(self) -> None:
        assert resolver_kepler(-1.5, 0.0) == -1.5


class TestConvergencia:
    """La ecuación debe satisfacerse con precisión de máquina."""

    @pytest.mark.parametrize("M", [0.0, 1.0, math.pi, 4.5, -2.0])
    @pytest.mark.parametrize("e", [0.1, 0.3, 0.5, 0.7, 0.9])
    def test_ecuacion_satisfecha(self, M: float, e: float) -> None:
        E = resolver_kepler(M, e)
        residual = E - e * math.sin(E) - M
        assert abs(residual) < 1e-9, f"Residual {residual} para M={M}, e={e}"

    def test_converge_en_pocas_iteraciones(self) -> None:
        # Con e = 0.5 y M = π, Newton-Raphson converge en ~4 iteraciones.
        E = resolver_kepler(math.pi, 0.5, max_iteraciones=8)
        residual = E - 0.5 * math.sin(E) - math.pi
        assert abs(residual) < 1e-10


class TestPeriodicidad:
    """E(M + 2πk) = E(M) + 2πk."""

    @pytest.mark.parametrize("k", [-2, -1, 1, 2, 5])
    @pytest.mark.parametrize("M", [0.3, 1.2, math.pi, 5.0])
    @pytest.mark.parametrize("e", [0.2, 0.5])
    def test_periodicidad(self, M: float, e: float, k: int) -> None:
        E1 = resolver_kepler(M, e)
        E2 = resolver_kepler(M + 2 * math.pi * k, e)
        assert E2 == pytest.approx(E1 + 2 * math.pi * k, abs=1e-9)


class TestSimetria:
    """E(-M) = -E(M) por ser la función impar."""

    @pytest.mark.parametrize("M", [0.5, 1.5, 3.0])
    @pytest.mark.parametrize("e", [0.1, 0.3, 0.6])
    def test_impar(self, M: float, e: float) -> None:
        assert resolver_kepler(-M, e) == pytest.approx(
            -resolver_kepler(M, e), abs=1e-9
        )


class TestErrores:
    """Validación de entrada."""

    def test_excentricidad_negativa(self) -> None:
        with pytest.raises(ErrorKepler):
            resolver_kepler(1.0, -0.1)

    def test_excentricidad_uno(self) -> None:
        with pytest.raises(ErrorKepler):
            resolver_kepler(1.0, 1.0)

    def test_excentricidad_excesiva(self) -> None:
        with pytest.raises(ErrorKepler):
            resolver_kepler(1.0, 1.5)


class TestRendimiento:
    """Sanity check de velocidad (no debe ser lento)."""

    def test_1000_resoluciones_rapidas(self) -> None:
        import time

        inicio = time.perf_counter()
        for i in range(1000):
            resolver_kepler(i * 0.01, 0.3)
        duracion = time.perf_counter() - inicio
        assert duracion < 0.5, f"Demasiado lento: {duracion:.3f}s"