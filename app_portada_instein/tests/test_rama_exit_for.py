"""
Test "asesino" para cubrir AMBAS ramas de salida del bucle for
en `resolver.py`:

    - Rama A: break por convergencia (86->return).
    - Rama B: agotamiento natural del for (for->return).

Cubre la rama 86->104 reportada por coverage.
"""

from __future__ import annotations

import math

import pytest

from app_portada_instein.dominio.kepler import resolver_kepler


# ======================================================================
# Fuerza la salida por BREAK (convergencia)
# ======================================================================

class TestExitPorBreak:
    """Salida del `for` por `break` (convergencia)."""

    def test_break_en_primera_iteracion(self) -> None:
        """
        Con tolerancia grande y M pequeño, delta es pequeño
        en la primera iteración → break inmediato.
        """
        E = resolver_kepler(
            anomalia_media=1e-6,
            excentricidad=0.5,
            max_iteraciones=50,
            tolerancia=1.0,
        )
        assert math.isfinite(E)

    def test_break_iteracion_media(self) -> None:
        """
        Con M=0.5, e=0.3 y tolerancia=0.1, converge rápido
        y hace break antes de agotar.
        """
        E = resolver_kepler(
            anomalia_media=0.5,
            excentricidad=0.3,
            max_iteraciones=50,
            tolerancia=0.1,
        )
        assert math.isfinite(E)


# ======================================================================
# Fuerza la salida por AGOTAMIENTO del for (sin break)
# ======================================================================

class TestExitPorAgotamiento:
    """
    Salida del `for` por agotamiento natural (sin `break`).

    Esta es la rama 86->104 reportada por coverage.
    """

    def test_agotamiento_garantizado_max_iter_1(self) -> None:
        """
        Con max_iteraciones=1 y un delta grande, el for agota.

        Verificación manual (M=1.0, e=0.9, max_iter=1):
            E_0    = 1.0
            f      = 1.0 - 0.9·sin(1.0) - 1.0 ≈ -0.757
            f'     = 1 - 0.9·cos(1.0) ≈ 0.514
            delta  = -0.757 / 0.514 ≈ -1.474
            |delta| ≥ 1e-10 → NO break ✅ → for agota ✅
        """
        E = resolver_kepler(
            anomalia_media=1.0,
            excentricidad=0.9,
            max_iteraciones=1,
        )
        assert math.isfinite(E)
        # Confirmamos que NO convergió.
        residual = E - 0.9 * math.sin(E) - 1.0
        assert abs(residual) > 0.1

    @pytest.mark.parametrize(
        "M, e",
        [
            (1.0, 0.9),
            (1.5, 0.85),
            (2.0, 0.9),
            (2.5, 0.95),
            (3.0, 0.9),
            (0.5, 0.95),
            (0.8, 0.85),
            (-1.0, 0.9),
            (-2.0, 0.85),
            (-3.0, 0.95),
        ],
    )
    def test_agotamiento_grid_garantizado(self, M: float, e: float) -> None:
        """
        Grid exhaustivo con max_iter=1 y e alta.
        Todos estos casos agotan el for sin break.
        """
        E = resolver_kepler(M, e, max_iteraciones=1)
        assert math.isfinite(E)

    def test_agotamiento_con_tolerancia_minuscula(self) -> None:
        """
        Con tolerancia < precisión de máquina, NUNCA hay break.

        Verificación: con tol=1e-300, incluso deltas de orden 1e-15
        (precisión de float64) NO satisfacen |delta| < 1e-300.
        Por tanto, el for SIEMPRE agota.
        """
        E = resolver_kepler(
            anomalia_media=1.5,
            excentricidad=0.5,
            max_iteraciones=100,
            tolerancia=1e-300,
        )
        assert math.isfinite(E)

    def test_agotamiento_con_max_iter_insuficiente(self) -> None:
        """
        Con M grande y max_iteraciones=1, el algoritmo NO puede
        converger en una sola iteración.

        Verificación manual (M=10.0, e=0.9, max_iter=1):
            M_norm = 10.0 - 2π ≈ 3.7168
            E_0    = 3.7168
            f      = 3.7168 - 0.9·sin(3.7168) - 3.7168
                   ≈ -0.9·(-0.5427) = 0.4884
            f'     = 1 - 0.9·cos(3.7168)
                   = 1 - 0.9·(-0.8399) = 1.7559
            delta  = 0.4884 / 1.7559 ≈ 0.2782
            |delta| ≥ 1e-10 → NO break ✅ → for agota ✅
        """
        E = resolver_kepler(
            anomalia_media=10.0,
            excentricidad=0.9,
            max_iteraciones=1,
        )
        assert math.isfinite(E)
        # Verificamos que NO convergió del todo con 1 iteración.
        M_norm = 10.0 - 2 * math.pi
        residual = E - 0.9 * math.sin(E) - M_norm
        assert abs(residual) > 1e-3

    def test_convergencia_cuadratica_con_dos_iteraciones(self) -> None:
        """
        Con M=3.0, e=0.99, max_iteraciones=2, Newton-Raphson
        converge cuadráticamente y alcanza precisión de máquina
        en 2 iteraciones.

        Este test documenta el comportamiento REAL (no el que
        erróneamente asumí antes).
        """
        E = resolver_kepler(
            anomalia_media=3.0,
            excentricidad=0.99,
            max_iteraciones=2,
        )
        residual = E - 0.99 * math.sin(E) - 3.0
        # Newton-Raphson converge cuadráticamente: con 2 iteraciones
        # alcanza precisión de máquina incluso con e=0.99.
        assert abs(residual) < 1e-6
        assert math.isfinite(E)


# ======================================================================
# Verificación empírica del flujo de control
# ======================================================================

class TestVerificacionFlujo:
    """Verifica empíricamente que ambas ramas se ejecutan."""

    def test_ambas_ramas_se_ejecutan(self) -> None:
        """
        Ejecuta un caso que hace break y otro que agota,
        confirmando que ambos flujos son alcanzables.
        """
        # Caso 1: break garantizado (tolerancia laxa).
        E_break = resolver_kepler(
            anomalia_media=0.5,
            excentricidad=0.3,
            max_iteraciones=50,
            tolerancia=0.1,
        )
        residual_break = E_break - 0.3 * math.sin(E_break) - 0.5
        assert abs(residual_break) < 0.1  # Convergió.

        # Caso 2: agotamiento garantizado (max_iter=1, e alta).
        E_agota = resolver_kepler(
            anomalia_media=1.0,
            excentricidad=0.9,
            max_iteraciones=1,
        )
        residual_agota = E_agota - 0.9 * math.sin(E_agota) - 1.0
        assert abs(residual_agota) > 0.1  # NO convergió.

        # Los dos resultados son distintos.
        assert E_break != E_agota