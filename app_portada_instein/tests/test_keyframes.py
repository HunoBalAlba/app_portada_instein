"""
Tests del generador de keyframes CSS.

Nota sobre precisión numérica:
    Los valores `0.000` y `-0.000` son iguales en coma flotante
    (`-0.0 == 0.0` en Python), pero al formatear con `f"{x:.3f}"` se
    producen strings distintos. El test `test_cierre_ciclo` normaliza
    estos valores antes de comparar.
"""

from __future__ import annotations

import re

import pytest

from app_portada_instein.dominio.kepler import (
    DefinicionKeyframe,
    generar_keyframes_css,
    generar_pasos_orbita,
)


# ======================================================================
# Helpers
# ======================================================================

_PATRON_TRANSLATE = re.compile(r"translate\(([-\d.]+)rem,\s*([-\d.]+)rem\)")
_PATRON_SCALE = re.compile(r"scale\(([\d.]+)\)")


def _normalizar_transform(transform: str) -> str:
    """
    Normaliza un `transform` CSS para comparación robusta.

    Reemplaza `-0.000rem` por `0.000rem` y colapsa espacios múltiples.
    """
    normalizado = transform.replace("-0.000", "0.000")
    return re.sub(r"\s+", " ", normalizado).strip()


def _extraer_translate(transform: str) -> tuple[float, float]:
    """Extrae los valores (x, y) del `translate(xrem, yrem)`."""
    match = _PATRON_TRANSLATE.search(transform)
    if match is None:
        raise AssertionError(f"No se encontró translate en: {transform!r}")
    return float(match.group(1)), float(match.group(2))


def _extraer_scale(transform: str) -> float:
    """Extrae el valor de `scale(s)`."""
    match = _PATRON_SCALE.search(transform)
    if match is None:
        raise AssertionError(f"No se encontró scale en: {transform!r}")
    return float(match.group(1))


# ======================================================================
# TestGenerarPasos
# ======================================================================


class TestGenerarPasos:
    """Verifica la estructura del dict de pasos."""

    def test_num_pasos_correcto(self) -> None:
        pasos = generar_pasos_orbita(
            semieje_mayor=50.0,
            excentricidad=0.2,
            factor_perspectiva=0.5,
            angulo_inicial_grados=0.0,
            num_pasos=12,
        )
        # 12 intervalos → 13 pasos (0% … 100%).
        assert len(pasos) == 13

    def test_claves_porcentaje(self) -> None:
        pasos = generar_pasos_orbita(
            semieje_mayor=50.0,
            excentricidad=0.2,
            factor_perspectiva=0.5,
            angulo_inicial_grados=0.0,
            num_pasos=10,
        )
        assert "0%" in pasos
        assert "50%" in pasos
        assert "100%" in pasos

    def test_estructura_step(self) -> None:
        pasos = generar_pasos_orbita(
            semieje_mayor=50.0,
            excentricidad=0.2,
            factor_perspectiva=0.5,
            angulo_inicial_grados=0.0,
            num_pasos=4,
        )
        for step in pasos.values():
            assert "transform" in step
            assert "opacity" in step
            assert "translate(-50%, -50%)" in step["transform"]
            assert "scale(" in step["transform"]

    def test_opacidad_en_rango(self) -> None:
        pasos = generar_pasos_orbita(
            semieje_mayor=85.0,
            excentricidad=0.3,
            factor_perspectiva=0.5,
            angulo_inicial_grados=0.0,
            num_pasos=60,
        )
        for step in pasos.values():
            op = float(step["opacity"])
            assert 0.45 <= op <= 1.0

    def test_escala_en_rango(self) -> None:
        pasos = generar_pasos_orbita(
            semieje_mayor=62.0,
            excentricidad=0.3,
            factor_perspectiva=0.5,
            angulo_inicial_grados=0.0,
            num_pasos=60,
        )
        for step in pasos.values():
            escala = _extraer_scale(step["transform"])
            assert 0.55 <= escala <= 1.2

    def test_cierre_ciclo(self) -> None:
        """
        El paso 100% debe coincidir con 0% (órbita cerrada).

        Normalizamos `-0.000rem` → `0.000rem` porque en coma flotante
        `sin(2π) ≈ -2.45e-16`, lo que produce un "-0.000" al formatear.
        Geométricamente son idénticos.
        """
        pasos = generar_pasos_orbita(
            semieje_mayor=55.0,
            excentricidad=0.25,
            factor_perspectiva=0.5,
            angulo_inicial_grados=0.0,
            num_pasos=60,
        )
        t0 = _normalizar_transform(pasos["0%"]["transform"])
        t100 = _normalizar_transform(pasos["100%"]["transform"])
        assert t0 == t100, f"{t0!r} != {t100!r}"

    def test_cierre_ciclo_por_componentes(self) -> None:
        """
        Alternativa robusta: comparar translate y scale por separado,
        con tolerancia absoluta.
        """
        pasos = generar_pasos_orbita(
            semieje_mayor=55.0,
            excentricidad=0.25,
            factor_perspectiva=0.5,
            angulo_inicial_grados=0.0,
            num_pasos=60,
        )
        x0, y0 = _extraer_translate(pasos["0%"]["transform"])
        x100, y100 = _extraer_translate(pasos["100%"]["transform"])
        s0 = _extraer_scale(pasos["0%"]["transform"])
        s100 = _extraer_scale(pasos["100%"]["transform"])

        assert x0 == pytest.approx(x100, abs=1e-6)
        assert y0 == pytest.approx(y100, abs=1e-6)
        assert s0 == pytest.approx(s100, abs=1e-6)


# ======================================================================
# TestErrores
# ======================================================================


class TestErrores:
    def test_num_pasos_uno(self) -> None:
        with pytest.raises(ValueError):
            generar_pasos_orbita(
                semieje_mayor=50.0,
                excentricidad=0.2,
                factor_perspectiva=0.5,
                angulo_inicial_grados=0.0,
                num_pasos=1,
            )

    def test_semieje_cero(self) -> None:
        with pytest.raises(ValueError):
            generar_pasos_orbita(
                semieje_mayor=0.0,
                excentricidad=0.2,
                factor_perspectiva=0.5,
                angulo_inicial_grados=0.0,
                num_pasos=10,
            )

    def test_semieje_negativo(self) -> None:
        with pytest.raises(ValueError):
            generar_pasos_orbita(
                semieje_mayor=-10.0,
                excentricidad=0.2,
                factor_perspectiva=0.5,
                angulo_inicial_grados=0.0,
                num_pasos=10,
            )

    def test_factor_perspectiva_fuera_de_rango(self) -> None:
        with pytest.raises(ValueError):
            generar_pasos_orbita(
                semieje_mayor=50.0,
                excentricidad=0.2,
                factor_perspectiva=1.5,
                angulo_inicial_grados=0.0,
                num_pasos=10,
            )


# ======================================================================
# TestGenerarKeyframesCSS
# ======================================================================


class TestGenerarKeyframesCSS:
    def test_estructura_css(self) -> None:
        defs: list[DefinicionKeyframe] = [
            {
                "nombre": "orbita_0_55",
                "pasos": {"0%": {"transform": "translate(0, 0)", "opacity": "1"}},
            },
            {
                "nombre": "orbita_90_70",
                "pasos": {"0%": {"transform": "translate(0, 0)", "opacity": "0.5"}},
            },
        ]
        css = generar_keyframes_css(defs)
        assert "@keyframes orbita_0_55" in css
        assert "@keyframes orbita_90_70" in css
        assert css["@keyframes orbita_0_55"]["0%"]["opacity"] == "1"

    def test_lista_vacia(self) -> None:
        assert generar_keyframes_css([]) == {}


# ======================================================================
# TestIntegracionConCatalogo
# ======================================================================


class TestIntegracionConCatalogo:
    """Simula el uso real con parámetros del catálogo."""

    def test_orbitas_estandar(self, orbitas_estandar: list[dict]) -> None:
        """
        Verifica que la API acepta el desempaquetado `**orbita`.

        Este test depende de que las claves de la fixture coincidan con
        los nombres de los parámetros de `generar_pasos_orbita`
        (ver `conftest.py`).
        """
        for orbita in orbitas_estandar:
            pasos = generar_pasos_orbita(**orbita, num_pasos=30)
            assert len(pasos) == 31
            for step in pasos.values():
                assert "translate(-50%, -50%)" in step["transform"]

    def test_orbitas_degeneradas(self, orbitas_degeneradas: list[dict]) -> None:
        """Órbitas con parámetros límite deben funcionar sin excepción."""
        for orbita in orbitas_degeneradas:
            pasos = generar_pasos_orbita(**orbita, num_pasos=10)
            assert len(pasos) == 11

    def test_todas_las_orbitas_diferentes(self) -> None:
        """Cada configuración debe producir un keyframe único."""
        configuraciones = [
            (55.0, 0.25, 0.5, 0),
            (70.0, 0.15, 0.5, 90),
            (62.0, 0.30, 0.5, 180),
            (85.0, 0.20, 0.5, 270),
        ]
        resultados = []
        for a, e, p, ang in configuraciones:
            pasos = generar_pasos_orbita(
                semieje_mayor=a,
                excentricidad=e,
                factor_perspectiva=p,
                angulo_inicial_grados=ang,
                num_pasos=10,
            )
            firma = str(sorted(pasos.keys())) + pasos["50%"]["transform"]
            resultados.append(firma)
        assert len(set(resultados)) == len(resultados)
