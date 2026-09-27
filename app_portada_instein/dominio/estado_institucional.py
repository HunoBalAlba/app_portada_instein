"""
Estado global de la aplicación pública del instituto.

Esta clase centraliza:
- El catálogo de carreras disponibles.
- La selección de carrera activa (leída desde la URL).
- El estado de la sección de detalle activa.
- El estado de la carrera destacada en el home.
"""

import random

import reflex as rx

from ..datos.catalogo_carreras import CATALOGO_CARRERAS, PALETA_COLORES
from ..datos.modelos_carrera import Carrera, PlanAnual


class EstadoInstitucional(rx.State):
    """Estado central de la aplicación pública."""

    # --- Catálogo de carreras ---
    carreras: list[Carrera] = CATALOGO_CARRERAS

    # --- Estado del home (carrera destacada) ---
    id_carrera_destacada: int = 0

    # --- Estado de la vista de detalle ---
    indice_anio_seleccionado: int = 0
    seccion_detalle_activa: str = "info"  # Valores: "info" | "plan" | "perfil"

    # ------------------------------------------------------------------
    # Variables computadas (reactivas) derivadas de la URL y del estado
    # ------------------------------------------------------------------

    @rx.var
    def id_carrera_desde_url(self) -> int:
        """
        Extrae el identificador de la carrera desde la URL.
        Ej: /carrera/3  →  3
        """
        valor_crudo = self.router.page.params.get("carrera_id", "0")
        try:
            return int(valor_crudo)
        except (ValueError, TypeError):
            return 0

    @rx.var
    def carrera_seleccionada(self) -> Carrera:
        """Devuelve la carrera activa según la URL actual."""
        return self._buscar_carrera_por_id(self.id_carrera_desde_url)

    @rx.var
    def plan_anual_seleccionado(self) -> PlanAnual:
        """Devuelve el año del plan de estudios actualmente visible."""
        carrera = self._buscar_carrera_por_id(self.id_carrera_desde_url)
        if self.indice_anio_seleccionado >= len(carrera["plan_estudios"]):
            return carrera["plan_estudios"][0]
        return carrera["plan_estudios"][self.indice_anio_seleccionado]

    @rx.var
    def carrera_destacada(self) -> Carrera:
        """Devuelve la carrera destacada en el home."""
        return self._buscar_carrera_por_id(self.id_carrera_destacada)

    @rx.var
    def url_detalle_carrera_destacada(self) -> str:
        """Construye la URL de detalle para la carrera destacada."""
        return f"/carrera/{self.id_carrera_destacada}"

    # ------------------------------------------------------------------
    # Métodos internos
    # ------------------------------------------------------------------

    def _buscar_carrera_por_id(self, id_carrera: int) -> Carrera:
        """Busca una carrera por su id; si no existe devuelve la primera."""
        for carrera in self.carreras:
            if carrera["id"] == id_carrera:
                return carrera
        return self.carreras[0]

    # ------------------------------------------------------------------
    # Manejadores de eventos
    # ------------------------------------------------------------------

    @rx.event
    def seleccionar_anio(self, indice: int):
        """Cambia el año visible del plan de estudios."""
        self.indice_anio_seleccionado = indice

    @rx.event
    def seleccionar_seccion_detalle(self, seccion: str):
        """Cambia la sección activa dentro de la vista de detalle."""
        self.seccion_detalle_activa = seccion

    @rx.event
    def seleccionar_carrera_destacada(self, id_carrera: int):
        """Cambia la carrera destacada en el home."""
        self.id_carrera_destacada = id_carrera

    @rx.event
    def aleatorizar_colores_carreras(self):
        """Reasigna aleatoriamente la paleta de colores a las carreras."""
        cantidad = len(self.carreras)
        paleta_disponible = PALETA_COLORES.copy()

        if len(paleta_disponible) >= cantidad:
            seleccionados = random.sample(paleta_disponible, cantidad)
        else:
            seleccionados = [
                random.choice(paleta_disponible) for _ in range(cantidad)
            ]

        random.shuffle(seleccionados)

        carreras_actualizadas: list[Carrera] = []
        for carrera, (color, color_suave) in zip(self.carreras, seleccionados):
            nueva_carrera = dict(carrera)
            nueva_carrera["color_principal"] = color
            nueva_carrera["color_suave"] = color_suave
            carreras_actualizadas.append(nueva_carrera)

        self.carreras = carreras_actualizadas