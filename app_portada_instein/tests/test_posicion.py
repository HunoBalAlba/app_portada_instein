"""Tests de la posición orbital."""

import math

import pytest

from app_portada_instein.dominio.kepler import (
    ErrorKepler,
    calcular_posicion_orbital,
)


class TestOrbitaCircular:
    """Con e = 0, la posición es (a·cos(M), a·sin(M))."""

    @pytest.mark.parametrize(
        "M, x_esperado, y_esperado",
        [
            (0.0, 50.0, 0.0),
            (math.pi / 2, 0.0, 50.0),
            (math.pi, -50.0, 0.0),
            (3 * math.pi / 2, 0.0, -50.0),
        ],
    )
    def test_posiciones_cardinales(
        self, M: float, x_esperado: float, y_esperado: float
    ) -> None:
        p = calcular_posicion_orbital(M, 50.0, 0.0)
        assert p.x == pytest.approx(x_esperado, abs=1e-9)
        assert p.y == pytest.approx(y_esperado, abs=1e-9)


class TestOrbitaElíptica:
    """El foco está en el origen."""

    @pytest.mark.parametrize("e", [0.1, 0.25, 0.5, 0.75])
    @pytest.mark.parametrize("a", [50.0, 62.0, 85.0])
    def test_periastro_y_apoastro(self, a: float, e: float) -> None:
        # En M = 0, el cuerpo está en el periastro: x = a·(1 - e).
        p_peri = calcular_posicion_orbital(0.0, a, e)
        assert p_peri.x == pytest.approx(a * (1 - e), abs=1e-9)
        assert p_peri.y == pytest.approx(0.0, abs=1e-9)

        # En M = π, está en el apoastro: x = -a·(1 + e).
        p_apo = calcular_posicion_orbital(math.pi, a, e)
        assert p_apo.x == pytest.approx(-a * (1 + e), abs=1e-9)

    def test_semieje_menor(self) -> None:
        a, e = 100.0, 0.6
        p = calcular_posicion_orbital(1.0, a, e)
        assert p.semieje_menor == pytest.approx(a * math.sqrt(1 - e ** 2))

    def test_anomalia_excentrica_devuelta(self) -> None:
        p = calcular_posicion_orbital(1.0, 50.0, 0.3)
        # E debe satisfacer la ecuación de Kepler.
        residual = p.anomalia_excentrica - 0.3 * math.sin(
            p.anomalia_excentrica
        ) - 1.0
        assert abs(residual) < 1e-9


class TestInvariantes:
    """El cuerpo siempre está dentro de la elipse."""

    @pytest.mark.parametrize("e", [0.0, 0.3, 0.7])
    def test_dentro_de_la_elipse(self, e: float) -> None:
        a = 60.0
        b = a * math.sqrt(1 - e ** 2)
        # Distancia al foco (origen)
        for i in range(36):
            M = i * math.pi / 18
            p = calcular_posicion_orbital(M, a, e)
            # r = a(1 - e·cos(E)) debe estar entre a(1-e) y a(1+e).
            r = math.hypot(p.x, p.y)
            assert a * (1 - e) - 1e-9 <= r <= a * (1 + e) + 1e-9


class TestErrores:
    def test_semieje_mayor_cero(self) -> None:
        with pytest.raises(ErrorKepler):
            calcular_posicion_orbital(1.0, 0.0, 0.3)

    def test_semieje_mayor_negativo(self) -> None:
        with pytest.raises(ErrorKepler):
            calcular_posicion_orbital(1.0, -10.0, 0.3)

    def test_excentricidad_invalida(self) -> None:
        with pytest.raises(ErrorKepler):
            calcular_posicion_orbital(1.0, 50.0, 1.5)