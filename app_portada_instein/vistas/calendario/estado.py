"""
Estado de los filtros del Calendario Académico.
"""

import reflex as rx

from .datos import PROXIMOS_EVENTOS


# ======================================================================
# Orden de meses para ordenamiento por fecha
# ======================================================================

ORDEN_MESES: dict[str, int] = {
    "ENERO": 1,
    "FEBRERO": 2,
    "MARZO": 3,
    "ABRIL": 4,
    "MAYO": 5,
    "JUNIO": 6,
    "JULIO": 7,
    "AGOSTO": 8,
    "SEPTIEMBRE": 9,
    "OCTUBRE": 10,
    "NOVIEMBRE": 11,
    "DICIEMBRE": 12,
}


class EstadoCalendario(rx.State):
    """
    Estado de filtros y ordenamiento del calendario académico.

    Atributos:
        filtro_carrera: Clave de la carrera seleccionada (ej: "sistemas",
            "todas").
        filtro_tipo: Clave del tipo de evento (ej: "taller", "todos").
        orden_activo: Clave de ordenamiento (ej: "fecha_asc").
        texto_busqueda: Texto de búsqueda por título o descripción.
    """

    filtro_carrera: str = "todas"
    filtro_tipo: str = "todos"
    orden_activo: str = "fecha_asc"
    texto_busqueda: str = ""

    # ==================================================================
    # Eventos computados
    # ==================================================================

    @rx.var
    def eventos_filtrados(self) -> list[dict]:
        """
        Devuelve los eventos filtrados y ordenados según los filtros
        activos.
        """
        eventos = list(PROXIMOS_EVENTOS)

        # --- Filtro por carrera ---
        if self.filtro_carrera != "todas":
            eventos = [
                e for e in eventos
                if e.get("carrera", "institucional") == self.filtro_carrera
            ]

        # --- Filtro por tipo ---
        if self.filtro_tipo != "todos":
            eventos = [
                e for e in eventos
                if e["tipo"] == self.filtro_tipo
            ]

        # --- Filtro por búsqueda de texto ---
        if self.texto_busqueda:
            busqueda = self.texto_busqueda.lower()
            eventos = [
                e for e in eventos
                if busqueda in e["titulo"].lower()
                or busqueda in e["descripcion"].lower()
                or busqueda in e["lugar"].lower()
            ]

        # --- Ordenamiento ---
        if self.orden_activo == "fecha_asc":
            eventos = sorted(
                eventos,
                key=lambda e: (
                    ORDEN_MESES.get(e["mes"], 99),
                    int(e["dia"]) if e["dia"].isdigit() else 0,
                ),
            )
        elif self.orden_activo == "fecha_desc":
            eventos = sorted(
                eventos,
                key=lambda e: (
                    ORDEN_MESES.get(e["mes"], 99),
                    int(e["dia"]) if e["dia"].isdigit() else 0,
                ),
                reverse=True,
            )
        elif self.orden_activo == "tipo_asc":
            eventos = sorted(
                eventos,
                key=lambda e: (e["tipo"], e["titulo"]),
            )

        return eventos

    @rx.var
    def hay_resultados(self) -> bool:
        """Indica si hay eventos que coincidan con los filtros."""
        return len(self.eventos_filtrados) > 0

    @rx.var
    def contador_resultados(self) -> str:
        """Texto con el número de resultados."""
        return str(len(self.eventos_filtrados))

    @rx.var
    def hay_filtros_activos(self) -> bool:
        """Indica si hay algún filtro activo (distinto de los defaults)."""
        return (
            self.filtro_carrera != "todas"
            or self.filtro_tipo != "todos"
            or self.orden_activo != "fecha_asc"
            or self.texto_busqueda != ""
        )

    # ==================================================================
    # Event handlers
    # ==================================================================

    @rx.event
    def cambiar_filtro_carrera(self, valor: str):
        """Cambia el filtro de carrera."""
        self.filtro_carrera = valor

    @rx.event
    def cambiar_filtro_tipo(self, valor: str):
        """Cambia el filtro de tipo de evento."""
        self.filtro_tipo = valor

    @rx.event
    def cambiar_orden(self, valor: str):
        """Cambia el ordenamiento activo."""
        self.orden_activo = valor

    @rx.event
    def actualizar_busqueda(self, texto: str):
        """Actualiza el texto de búsqueda."""
        self.texto_busqueda = texto

    @rx.event
    def limpiar_filtros(self):
        """Restablece todos los filtros a sus valores por defecto."""
        self.filtro_carrera = "todas"
        self.filtro_tipo = "todos"
        self.orden_activo = "fecha_asc"
        self.texto_busqueda = ""


__all__ = ["EstadoCalendario", "ORDEN_MESES"]