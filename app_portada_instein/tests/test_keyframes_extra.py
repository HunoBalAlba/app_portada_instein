"""
Tests adicionales para el generador de keyframes.

Este archivo agrupa tests enfocados en cobertura de ramas límite
(los "clamps" de escala y opacidad) y validaciones específicas
de `keyframes.py`.
"""

from __future__ import annotations

import re

import pytest

from app_portada_instein.dominio.kepler import (
    ESCALA_MAXIMA,
    ESCALA_MINIMA,
    generar_pasos_orbita,
)


# ======================================================================
# Helpers de parsing (autocontenidos)
# ======================================================================

_PATRON_SCALE = re.compile(r"scale\(([\d.]+)\)")
_PATRON_TRANSLATE = re.compile(
    r"translate\(([-\d.]+)rem,\s*([-\d.]+)rem\)"
)


def _extraer_scale(transform: str) -> float:
    """Extrae el valor numérico de `scale(s)` en un transform CSS."""
    match = _PATRON_SCALE.search(transform)
    if match is None:
        raise AssertionError(f"No se encontró scale en: {transform!r}")
    return float(match.group(1))


def _extraer_opacidad(step: dict) -> float:
    """Extrae la opacidad como float de un step de keyframe."""
    return float(step["opacity"])


# ======================================================================
# TestCoberturaCompleta — clamps de escala y opacidad
# ======================================================================

class TestCoberturaCompleta:
    """
    Tests diseñados para alcanzar el 100% de cobertura en las
    ramas de `max()`/`min()` de `_calcular_escala_opacidad`.
    """

    def test_escala_tope_superior(self) -> None:
        """Forzar `y_norm ≈ +1` para tocar el clamp superior."""
        pasos = generar_pasos_orbita(
            semieje_mayor=50.0,
            excentricidad=0.0,
            factor_perspectiva=1.0,
            angulo_inicial_grados=0.0,
            num_pasos=4,
        )
        escala = _extraer_scale(pasos["25%"]["transform"])
        assert escala == pytest.approx(ESCALA_MAXIMA, abs=1e-6)
        assert escala == 1.2

    def test_escala_tope_inferior(self) -> None:
        """Forzar `y_norm ≈ -1` para tocar el clamp inferior."""
        pasos = generar_pasos_orbita(
            semieje_mayor=50.0,
            excentricidad=0.0,
            factor_perspectiva=1.0,
            angulo_inicial_grados=0.0,
            num_pasos=4,
        )
        escala = _extraer_scale(pasos["75%"]["transform"])
        assert escala == pytest.approx(ESCALA_MINIMA, abs=1e-6)
        assert escala == 0.55

    def test_opacidad_tope_superior(self) -> None:
        """Forzar `y_norm ≈ +1` para tocar el clamp superior de opacidad."""
        pasos = generar_pasos_orbita(
            semieje_mayor=50.0,
            excentricidad=0.0,
            factor_perspectiva=1.0,
            angulo_inicial_grados=0.0,
            num_pasos=4,
        )
        opacidad = _extraer_opacidad(pasos["25%"])
        assert opacidad == pytest.approx(1.0, abs=1e-6)

    def test_opacidad_tope_inferior(self) -> None:
        """Forzar `y_norm ≈ -1` para tocar el clamp inferior de opacidad."""
        pasos = generar_pasos_orbita(
            semieje_mayor=50.0,
            excentricidad=0.0,
            factor_perspectiva=1.0,
            angulo_inicial_grados=0.0,
            num_pasos=4,
        )
        opacidad = _extraer_opacidad(pasos["75%"])
        assert opacidad == pytest.approx(0.45, abs=1e-6)

    def test_escala_en_punto_medio(self) -> None:
        """En f=0 o f=0.5, la escala queda en un valor intermedio."""
        pasos = generar_pasos_orbita(
            semieje_mayor=50.0,
            excentricidad=0.0,
            factor_perspectiva=1.0,
            angulo_inicial_grados=0.0,
            num_pasos=4,
        )
        escala_0 = _extraer_scale(pasos["0%"]["transform"])
        escala_50 = _extraer_scale(pasos["50%"]["transform"])
        assert escala_0 == pytest.approx(0.85, abs=1e-6)
        assert escala_50 == pytest.approx(0.85, abs=1e-6)


# ======================================================================
# TestCoberturaPerspectiva
# ======================================================================

class TestCoberturaPerspectiva:
    """Tests que ejercitan ramas de `perspectiva.py`."""

    def test_factor_perspectiva_minimo_valido(self) -> None:
        """`factor_perspectiva` muy pequeño (pero > 0) es válido."""
        pasos = generar_pasos_orbita(
            semieje_mayor=50.0,
            excentricidad=0.3,
            factor_perspectiva=0.01,
            angulo_inicial_grados=45.0,
            num_pasos=8,
        )
        assert len(pasos) == 9


# ======================================================================
# TestCoberturaPosicion
# ======================================================================

class TestCoberturaPosicion:
    """Tests que ejercitan ramas de `posicion.py`."""

    def test_semieje_mayor_muy_pequeno(self) -> None:
        """Un semieje muy pequeño debe seguir siendo válido."""
        pasos = generar_pasos_orbita(
            semieje_mayor=0.001,
            excentricidad=0.1,
            factor_perspectiva=0.5,
            angulo_inicial_grados=0.0,
            num_pasos=4,
        )
        assert len(pasos) == 5

    def test_excentricidad_cero_y_angulo_cero(self) -> None:
        """Caso borde: e=0 y ángulo=0 (identidad tras perspectiva)."""
        pasos = generar_pasos_orbita(
            semieje_mayor=50.0,
            excentricidad=0.0,
            factor_perspectiva=0.5,
            angulo_inicial_grados=0.0,
            num_pasos=4,
        )
        match = _PATRON_TRANSLATE.search(pasos["0%"]["transform"])
        assert match is not None
        x0, y0 = match.groups()
        assert float(x0) == pytest.approx(16.0, abs=1e-3)
        assert float(y0) == pytest.approx(0.0, abs=1e-6)


# ======================================================================
# TestCoberturaResolver
# ======================================================================

class TestCoberturaResolver:
    """Tests que ejercitan ramas de `resolver.py` desde keyframes."""

    def test_max_iteraciones_insuficientes(self) -> None:
        """Con muy pocas iteraciones, no debe fallar."""
        pasos = generar_pasos_orbita(
            semieje_mayor=50.0,
            excentricidad=0.9,
            factor_perspectiva=0.5,
            angulo_inicial_grados=0.0,
            num_pasos=4,
        )
        assert len(pasos) == 5

    def test_excentricidad_extrema(self) -> None:
        """Excentricidad cercana al límite superior (0.99)."""
        pasos = generar_pasos_orbita(
            semieje_mayor=80.0,
            excentricidad=0.99,
            factor_perspectiva=0.5,
            angulo_inicial_grados=90.0,
            num_pasos=10,
        )
        assert len(pasos) == 11


# ======================================================================
# TestValidacionesKeyframes — cobertura de líneas 109 y 112
# ======================================================================

class TestValidacionesKeyframes:
    """
    Tests que ejecutan las validaciones dentro de `generar_pasos_orbita`.

    Cubre las líneas 109 (validación `num_pasos`) y 112 (validación
    `semieje_mayor`), que ya tienen su test principal en
    `test_keyframes.py` pero se refuerzan aquí.
    """

    def test_num_pasos_cero(self) -> None:
        """num_pasos=0 debe fallar (cobertura línea 109)."""
        with pytest.raises(ValueError, match="num_pasos"):
            generar_pasos_orbita(
                semieje_mayor=50.0,
                excentricidad=0.2,
                factor_perspectiva=0.5,
                angulo_inicial_grados=0.0,
                num_pasos=0,
            )

    def test_num_pasos_negativo(self) -> None:
        """num_pasos negativo debe fallar."""
        with pytest.raises(ValueError, match="num_pasos"):
            generar_pasos_orbita(
                semieje_mayor=50.0,
                excentricidad=0.2,
                factor_perspectiva=0.5,
                angulo_inicial_grados=0.0,
                num_pasos=-5,
            )

    def test_semieje_mayor_cero_cobertura(self) -> None:
        """semieje_mayor=0 debe fallar (cobertura línea 112)."""
        with pytest.raises(ValueError, match="semieje_mayor"):
            generar_pasos_orbita(
                semieje_mayor=0.0,
                excentricidad=0.2,
                factor_perspectiva=0.5,
                angulo_inicial_grados=0.0,
                num_pasos=10,
            )

    def test_semieje_mayor_negativo_cobertura(self) -> None:
        """semieje_mayor negativo debe fallar."""
        with pytest.raises(ValueError, match="semieje_mayor"):
            generar_pasos_orbita(
                semieje_mayor=-1.0,
                excentricidad=0.2,
                factor_perspectiva=0.5,
                angulo_inicial_grados=0.0,
                num_pasos=10,
            )

    def test_factor_conversion_rem_personalizado(self) -> None:
        """Un factor de conversión distinto debe reflejarse en el output."""
        pasos = generar_pasos_orbita(
            semieje_mayor=50.0,
            excentricidad=0.0,
            factor_perspectiva=1.0,
            angulo_inicial_grados=0.0,
            num_pasos=4,
            factor_conversion_rem=1.0,  # 1 rem por unidad de %
        )
        match = _PATRON_TRANSLATE.search(pasos["0%"]["transform"])
        assert match is not None
        x0, _ = match.groups()
        # Con factor=1.0 y a=50, x = 50 rem.
        assert float(x0) == pytest.approx(50.0, abs=1e-3)