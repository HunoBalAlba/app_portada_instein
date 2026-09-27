"""Tests de la transformación de perspectiva y rotación."""

import math

import pytest

from app_portada_instein.dominio.kepler import (
    aplicar_perspectiva_y_rotacion,
    convertir_a_rem,
)


class TestSinTransformacion:
    """Sin aplanamiento ni rotación, la coordenada es idéntica."""

    def test_identidad(self) -> None:
        c = aplicar_perspectiva_y_rotacion(3.0, 4.0, 1.0, 0.0)
        assert c.x == pytest.approx(3.0)
        assert c.y == pytest.approx(4.0)
        assert c.y_perspectiva == pytest.approx(4.0)


class TestAplanamiento:
    """El factor de perspectiva solo afecta a Y."""

    @pytest.mark.parametrize("factor", [0.5, 0.7, 0.9])
    def test_solo_afecta_y(self, factor: float) -> None:
        c = aplicar_perspectiva_y_rotacion(10.0, 8.0, factor, 0.0)
        assert c.x == pytest.approx(10.0)
        assert c.y == pytest.approx(8.0 * factor)
        assert c.y_perspectiva == pytest.approx(8.0 * factor)


class TestRotacion:
    """Rotaciones cardinales."""

    def test_rotacion_90(self) -> None:
        c = aplicar_perspectiva_y_rotacion(1.0, 0.0, 1.0, 90.0)
        assert c.x == pytest.approx(0.0, abs=1e-9)
        assert c.y == pytest.approx(1.0, abs=1e-9)

    def test_rotacion_180(self) -> None:
        c = aplicar_perspectiva_y_rotacion(1.0, 0.0, 1.0, 180.0)
        assert c.x == pytest.approx(-1.0, abs=1e-9)
        assert c.y == pytest.approx(0.0, abs=1e-9)

    def test_rotacion_360_igual_a_0(self) -> None:
        c0 = aplicar_perspectiva_y_rotacion(3.0, 4.0, 0.5, 0.0)
        c360 = aplicar_perspectiva_y_rotacion(3.0, 4.0, 0.5, 360.0)
        assert c0.x == pytest.approx(c360.x)
        assert c0.y == pytest.approx(c360.y)


class TestInvarianteRotacion:
    """La rotación preserva la norma euclídea."""

    @pytest.mark.parametrize("angulo", [0.0, 30.0, 90.0, 180.0, 270.0, -45.0])
    def test_norma_preservada(self, angulo: float) -> None:
        x, y = 5.0, 3.0
        c = aplicar_perspectiva_y_rotacion(x, y, 1.0, angulo)
        assert math.hypot(c.x, c.y) == pytest.approx(math.hypot(x, y))


class TestErrores:
    def test_factor_cero(self) -> None:
        with pytest.raises(ValueError):
            aplicar_perspectiva_y_rotacion(1.0, 1.0, 0.0, 0.0)

    def test_factor_mayor_que_uno(self) -> None:
        with pytest.raises(ValueError):
            aplicar_perspectiva_y_rotacion(1.0, 1.0, 1.5, 0.0)


class TestConversionRem:
    def test_factor_estandar(self) -> None:
        # 0.32 rem por unidad de %
        assert convertir_a_rem(100.0, 0.32) == pytest.approx(32.0)

    def test_cero(self) -> None:
        assert convertir_a_rem(0.0, 0.32) == 0.0

    def test_negativo(self) -> None:
        assert convertir_a_rem(-50.0, 0.32) == pytest.approx(-16.0)
