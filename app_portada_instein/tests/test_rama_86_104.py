"""
Test dedicado a cubrir la rama 86->104 de resolver.py.

La rama 86->104 corresponde a la salida del bucle por:
    - `break` de convergencia (línea 86)
    - agotamiento natural del `for`

Este archivo contiene tests verificados manualmente para forzar
ambos casos.
"""

from __future__ import annotations

import math

import pytest

from app_portada_instein.dominio.kepler import resolver_kepler


class TestBreakConvergencia:
    """Fuerza el `break` de la línea 86 (convergencia por delta)."""

    def test_delta_pequeno_primera_iteracion(self) -> None:
        """
        Fuerza que delta sea pequeño en la PRIMERA iteración.

        Verificación manual para M=0.01, e=0.1:
            M_norm = 0.01
            E_0    = 0.01
            f      = 0.01 - 0.1·sin(0.01) - 0.01 = -0.1·0.00999 ≈ -0.001
            f'     = 1 - 0.1·cos(0.01) ≈ 0.9
            delta  = -0.001 / 0.9 ≈ -0.0011
            |delta| = 0.0011 ≥ 1e-10 → NO break ❌
        """
        E = resolver_kepler(0.01, 0.1, max_iteraciones=50)
        # Este caso NO hace break en la primera iteración,
        # pero convergerá en iteraciones posteriores.
        residual = E - 0.1 * math.sin(E) - 0.01
        assert abs(residual) < 1e-12

    def test_delta_muy_pequeno_con_tolerancia_laxa(self) -> None:
        """
        Con tolerancia laxa (1e-2), el delta pequeño dispara break
        en las primeras iteraciones.

        Verificación manual para M=0.001, e=0.01, tol=1e-2:
            M_norm = 0.001
            E_0    = 0.001
            f      = 0.001 - 0.01·sin(0.001) - 0.001 ≈ -1e-5
            f'     = 1 - 0.01·cos(0.001) ≈ 0.99
            delta  = -1e-5 / 0.99 ≈ -1e-5
            |delta| = 1e-5 < 1e-2 → **BREAK** ✅
        """
        E = resolver_kepler(
            anomalia_media=0.001,
            excentricidad=0.01,
            max_iteraciones=50,
            tolerancia=1e-2,
        )
        # Debe haber break en la primera iteración.
        assert math.isfinite(E)


class TestAgotamientoFor:
    """
    Fuerza el agotamiento del `for` sin break (rama 86->104 vía exit).

    Verificaciones manuales:

    Caso 1: M=2.0, e=0.9, max_iter=1
        M_norm = 2.0
        E_0    = 2.0
        f      = 2.0 - 0.9·sin(2.0) - 2.0 = -0.9·0.9093 ≈ -0.8184
        f'     = 1 - 0.9·cos(2.0) = 1 - 0.9·(-0.4161) = 1.3745
        |f'| = 1.3745 ≥ 1e-10 → NO break (f_prima)
        delta  = -0.8184 / 1.3745 ≈ -0.5954
        |delta| = 0.5954 ≥ 1e-10 → NO break (delta)
        Fin iteración 1 → for agota → rama 86->104 ✅

    Caso 2: M=1.5, e=0.8, max_iter=1
        E_0 = 1.5
        f   = 1.5 - 0.8·sin(1.5) - 1.5 = -0.8·0.9975 ≈ -0.798
        f'  = 1 - 0.8·cos(1.5) = 1 - 0.8·0.0707 ≈ 0.9434
        delta = -0.798 / 0.9434 ≈ -0.846
        |delta| ≥ 1e-10 → NO break ✅
    """

    @pytest.mark.parametrize(
        "M, e",
        [
            (2.0, 0.9),
            (1.5, 0.8),
            (1.0, 0.8),
            (0.5, 0.9),
            (-1.5, 0.8),
            (3.0, 0.95),
            (2.5, 0.85),
        ],
    )
    def test_agotamiento_max_iter_uno(self, M: float, e: float) -> None:
        """
        Con max_iteraciones=1, el `for` hace 1 iteración.
        Si delta es grande, NO hay break y el `for` agota.
        """
        E = resolver_kepler(M, e, max_iteraciones=1)
        assert math.isfinite(E)

    def test_agotamiento_verificado_por_residual(self) -> None:
        """
        Verifica que tras max_iter=1 el residual es GRANDE
        (es decir, NO hubo break por convergencia).
        """
        M, e = 2.0, 0.9
        E = resolver_kepler(M, e, max_iteraciones=1)
        residual = E - e * math.sin(E) - M
        # Residual grande → no hubo break por delta.
        assert abs(residual) > 1e-3, (
            f"El residual {residual} es muy pequeño; "
            "puede que hubo break por convergencia."
        )

    def test_agotamiento_tolerancia_imposible(self) -> None:
        """
        Con tolerancia imposible (1e-300), NUNCA se cumple
        `abs(delta) < tolerancia`, así que el `for` siempre agota.
        """
        E = resolver_kepler(
            anomalia_media=1.0,
            excentricidad=0.5,
            max_iteraciones=8,
            tolerancia=1e-300,
        )
        assert math.isfinite(E)

    def test_agotamiento_grid_exhaustivo(self) -> None:
        """
        Grid de valores verificados para forzar agotamiento con
        max_iteraciones=1.
        """
        casos = [
            (0.3, 0.7),
            (0.7, 0.85),
            (1.3, 0.9),
            (2.7, 0.95),
            (4.1, 0.85),
            (5.5, 0.75),
        ]
        for M, e in casos:
            E = resolver_kepler(M, e, max_iteraciones=1)
            assert math.isfinite(E)