"""
Estado global de la aplicación pública del instituto.

Centraliza:
- El catálogo de carreras.
- La carrera destacada en el home.
- El estado del explorador (sección activa + búsqueda + año seleccionado).
- La visibilidad del panel flotante de selección.
- El filtro activo en la página de carreras.
- El carrusel de carreras destacadas.

Nota técnica
------------
Los PATH PARAMS se obtienen con `self.router.page.params` (dict).
La RUTA ACTUAL se obtiene con `self.router.url.path` (str).

Los colores adaptativos (light/dark) NO se exponen como `@rx.var`
porque `rx.color_mode_cond()` devuelve un `Var` reactivo del frontend,
no un `str` serializable. En su lugar, los componentes usan los helpers
`color_carrera_adaptativo()` y `color_suave_carrera_adaptativo()` de
`constantes_visuales.py`, aplicados directamente sobre el dict de la
carrera.
"""

import asyncio
import random

import reflex as rx

from app_portada_instein.datos.catalogo_carreras import (
    CATALOGO_CARRERAS,
    PALETA_COLORES,
)
from app_portada_instein.datos.modelos_carrera import (
    Carrera,
    CarreraConEtiqueta,
    PlanAnual,
)


# ======================================================================
# Constantes para los iconos flotantes
# ======================================================================

CANTIDAD_ICONOS_FONDO = 30
SEMILLA_ICONOS_FONDO = 42

# Etiquetas cíclicas para el carrusel de banners.
ETIQUETAS_CARRUSEL: list[str] = [
    "Inscripciones abiertas",
    "Cupos limitados",
    "Últimos lugares",
    "Alta demanda",
    "Nuevo plan 2026",
]

# Tamaños permitidos para los iconos flotantes del detalle.
TAMANOS_ICONOS_FONDO: list[int] = [16, 20, 24, 28, 32, 40]


class EstadoInstitucional(rx.State):
    """Estado central de la aplicación pública."""

    # ==================================================================
    # ESTADO PERSISTENTE
    # ==================================================================

    # --- Catálogo de carreras ---
    carreras: list[Carrera] = CATALOGO_CARRERAS

    # --- Estado del home (carrera destacada) ---
    id_carrera_destacada: int = 0

    # --- Estado de la vista de detalle (ruta /carrera/[id]) ---
    indice_anio_seleccionado: int = 0
    seccion_detalle_activa: str = "info"

    # --- Estado del explorador del home ---
    seccion_explorador_activa: str = "info"
    indice_anio_explorador: int = 0
    texto_busqueda_carrera: str = ""
    mostrar_panel_flotante: bool = False

    # --- Estado de la página de carreras ---
    filtro_activo: str = "demanda_alta"
    orden_activo: str = "puntuacion_desc"

    # --- Estado del carrusel ---
    indice_carrusel: int = 0

    # ==================================================================
    # VARIABLES COMPUTADAS: URL
    # ==================================================================

    @rx.var
    def id_carrera_desde_url(self) -> int:
        """
        Extrae el identificador de la carrera desde la URL.

        Usa `self.router.page.params` para acceder a los PATH PARAMS
        (los definidos en la ruta como `/carrera/[carrera_id]`).
        """
        valor_crudo = self.router.page.params.get("carrera_id", "0")
        try:
            return int(valor_crudo)
        except (ValueError, TypeError):
            return 0

    @rx.var
    def ruta_activa_normalizada(self) -> str:
        """
        Devuelve la ruta actual normalizada.

        Normaliza casos especiales:
        - "" (vacío) → "/"
        - "/index" → "/"
        - Cualquier ruta con trailing slash se limpia.
        """
        ruta = self.router.url.path or "/"
        if len(ruta) > 1 and ruta.endswith("/"):
            ruta = ruta.rstrip("/")
        if ruta in ("", "/index"):
            ruta = "/"
        return ruta

    @rx.var
    def url_detalle_carrera_destacada(self) -> str:
        """Construye la URL de detalle para la carrera destacada."""
        return f"/carrera/{self.id_carrera_destacada}"

    # ==================================================================
    # VARIABLES COMPUTADAS: CARRERA SELECCIONADA (DETALLE)
    # ==================================================================

    @rx.var
    def carrera_seleccionada(self) -> Carrera:
        """Devuelve la carrera activa según la URL actual."""
        return self._buscar_carrera_por_id(self.id_carrera_desde_url)

    @rx.var
    def plan_anual_seleccionado(self) -> PlanAnual:
        """Devuelve el año del plan de estudios actualmente visible en detalle."""
        carrera = self._buscar_carrera_por_id(self.id_carrera_desde_url)
        if self.indice_anio_seleccionado >= len(carrera["plan_estudios"]):
            return carrera["plan_estudios"][0]
        return carrera["plan_estudios"][self.indice_anio_seleccionado]

    # ==================================================================
    # VARIABLES COMPUTADAS: HOME / EXPLORADOR
    # ==================================================================

    @rx.var
    def carrera_destacada(self) -> Carrera:
        """Devuelve la carrera destacada en el home."""
        return self._buscar_carrera_por_id(self.id_carrera_destacada)

    @rx.var
    def carreras_filtradas(self) -> list[Carrera]:
        """Filtra el catálogo de carreras según el texto de búsqueda."""
        if not self.texto_busqueda_carrera:
            return self.carreras

        busqueda = self.texto_busqueda_carrera.lower()
        return [
            c
            for c in self.carreras
            if busqueda in c["nombre"].lower()
            or busqueda in c["nombre_corto"].lower()
            or busqueda in c["lema"].lower()
            or busqueda in c["descripcion"].lower()
        ]

    @rx.var
    def hay_resultados_busqueda(self) -> bool:
        """Indica si la búsqueda tiene resultados."""
        return len(self.carreras_filtradas) > 0

    @rx.var
    def materias_carrera_destacada(self) -> list[str]:
        """Devuelve todas las materias aplanadas de la carrera destacada."""
        carrera = self._buscar_carrera_por_id(self.id_carrera_destacada)
        materias: list[str] = []
        for anio in carrera["plan_estudios"]:
            for materia in anio["materias"]:
                materias.append(materia)
        return materias

    @rx.var
    def perfil_carrera_destacada(self) -> list[str]:
        """Devuelve el perfil profesional de la carrera destacada."""
        carrera = self._buscar_carrera_por_id(self.id_carrera_destacada)
        return carrera["perfil_profesional"]

    @rx.var
    def campo_carrera_destacada(self) -> list[str]:
        """Devuelve el campo laboral de la carrera destacada."""
        carrera = self._buscar_carrera_por_id(self.id_carrera_destacada)
        return carrera["campo_laboral"]

    @rx.var
    def plan_agrupado_por_anio(self) -> list[PlanAnual]:
        """Devuelve el plan de estudios de la carrera destacada agrupado por año."""
        carrera = self._buscar_carrera_por_id(self.id_carrera_destacada)
        return carrera["plan_estudios"]

    @rx.var
    def anio_explorador_seleccionado(self) -> PlanAnual:
        """Devuelve el año visible en el explorador del home."""
        carrera = self._buscar_carrera_por_id(self.id_carrera_destacada)
        if self.indice_anio_explorador >= len(carrera["plan_estudios"]):
            return carrera["plan_estudios"][0]
        return carrera["plan_estudios"][self.indice_anio_explorador]

    @rx.var
    def materias_anio_explorador(self) -> list[str]:
        """Devuelve las materias del año seleccionado en el explorador."""
        carrera = self._buscar_carrera_por_id(self.id_carrera_destacada)
        if self.indice_anio_explorador >= len(carrera["plan_estudios"]):
            return carrera["plan_estudios"][0]["materias"]
        return carrera["plan_estudios"][self.indice_anio_explorador]["materias"]

    @rx.var
    def preguntas_frecuentes_carrera_destacada(self) -> list[dict]:
        """Devuelve las preguntas frecuentes de la carrera destacada."""
        carrera = self._buscar_carrera_por_id(self.id_carrera_destacada)
        return carrera.get("preguntas_frecuentes", [])

    # ==================================================================
    # VARIABLES COMPUTADAS: VISTA DE CARRERAS (columnas)
    # ==================================================================

    @rx.var
    def carreras_columna_1(self) -> list[Carrera]:
        """Carreras para la primera columna de las listas de éxitos."""
        return self.carreras[:2]

    @rx.var
    def carreras_columna_2(self) -> list[Carrera]:
        """Carreras para la segunda columna de las listas de éxitos."""
        return self.carreras[2:4]

    @rx.var
    def carreras_columna_3(self) -> list[Carrera]:
        """Carreras para la tercera columna de las listas de éxitos."""
        return self.carreras[4:]

    # ==================================================================
    # VARIABLES COMPUTADAS: PLAN DE ESTUDIOS
    # ==================================================================

    @rx.var
    def opciones_anio_plan(self) -> list[dict]:
        """
        Devuelve las opciones de año para el segmented control.

        Cada opción es un dict con:
        - "etiqueta": nombre del año (ej: "Primer Año").
        - "valor": índice como string (ej: "0", "1", "2").
        """
        carrera = self._buscar_carrera_por_id(self.id_carrera_desde_url)
        return [
            {
                "etiqueta": plan_anual["anio"],
                "valor": str(i),
            }
            for i, plan_anual in enumerate(carrera["plan_estudios"])
        ]

    # ==================================================================
    # VARIABLES COMPUTADAS: FILTROS Y ORDENAMIENTO
    # ==================================================================

    @rx.var
    def carreras_filtradas_y_ordenadas(self) -> list[Carrera]:
        """Devuelve las carreras filtradas y ordenadas según los filtros activos."""
        carreras = list(self.carreras)

        # --- Filtro por métrica ---
        if self.filtro_activo == "demanda_alta":
            carreras = [
                c for c in carreras
                if c["estadisticas"]["demanda_laboral"] == "alta"
            ]
        elif self.filtro_activo == "puntuacion_top":
            carreras = [
                c for c in carreras
                if c["estadisticas"]["puntuacion"] >= 4.7
            ]
        elif self.filtro_activo == "mas_inscritos":
            carreras = sorted(
                carreras,
                key=lambda c: c["estadisticas"]["estudiantes_inscritos"],
                reverse=True,
            )[:3]
        elif self.filtro_activo == "mas_graduados":
            carreras = sorted(
                carreras,
                key=lambda c: c["estadisticas"]["estudiantes_graduados"],
                reverse=True,
            )[:3]

        # --- Ordenamiento ---
        ordenamientos = {
            "puntuacion_desc": lambda c: c["estadisticas"]["puntuacion"],
            "inscritos_desc": lambda c: c["estadisticas"]["estudiantes_inscritos"],
            "graduados_desc": lambda c: c["estadisticas"]["estudiantes_graduados"],
            "empleabilidad_desc": lambda c: c["estadisticas"]["tasa_empleabilidad"],
            "salario_desc": lambda c: c["estadisticas"]["salario_promedio_bs"],
        }

        clave = ordenamientos.get(self.orden_activo)
        if clave is not None:
            carreras = sorted(carreras, key=clave, reverse=True)

        return carreras

    # ==================================================================
    # VARIABLES COMPUTADAS: ICONOS FLOTANTES DEL DETALLE
    # ==================================================================

    @rx.var
    def iconos_flotantes_detalle(self) -> list[rx.Component]:
        """Devuelve los componentes de iconos flotantes precalculados."""
        carrera = self._buscar_carrera_por_id(self.id_carrera_desde_url)
        color_principal = carrera["color_principal"]

        iconos_disponibles: list[str] = [carrera["icono"]]
        for icono_animado in carrera["iconos_animados"]:
            iconos_disponibles.append(icono_animado["nombre"])

        rng = random.Random(SEMILLA_ICONOS_FONDO)
        componentes: list[rx.Component] = []

        for _ in range(CANTIDAD_ICONOS_FONDO):
            nombre = rng.choice(iconos_disponibles)
            x = rng.uniform(0, 100)
            y = rng.uniform(0, 100)
            tamano = rng.choice(TAMANOS_ICONOS_FONDO)
            opacidad = rng.uniform(0.06, 0.15)
            delay = rng.uniform(0, 5)
            duracion = rng.uniform(6, 10)

            componentes.append(
                rx.box(
                    rx.icon(tag=nombre, size=tamano, color=color_principal),
                    position="absolute",
                    left=f"{x}%",
                    top=f"{y}%",
                    opacity=f"{opacidad}",
                    animation=(
                        f"flotar_icono_particula {duracion}s "
                        f"ease-in-out {delay}s infinite"
                    ),
                    pointer_events="none",
                )
            )

        return componentes

    # ==================================================================
    # VARIABLES COMPUTADAS: CARRUSEL
    # ==================================================================

    @rx.var
    def carreras_destacadas_con_etiquetas(self) -> list[CarreraConEtiqueta]:
        """
        Devuelve TODAS las carreras del catálogo con su etiqueta contextual.

        Las etiquetas rotan cíclicamente para no repetirse cuando hay
        más carreras que etiquetas disponibles.
        """
        resultado: list[CarreraConEtiqueta] = []
        for i, carrera in enumerate(self.carreras):
            etiqueta = ETIQUETAS_CARRUSEL[i % len(ETIQUETAS_CARRUSEL)]
            resultado.append(
                {
                    "carrera": carrera,
                    "etiqueta": etiqueta,
                }
            )
        return resultado

    @rx.var
    def item_carrusel_actual(self) -> CarreraConEtiqueta:
        """Devuelve el item actual del carrusel (carrera + etiqueta)."""
        items = self.carreras_destacadas_con_etiquetas
        if not items:
            return {"carrera": self.carreras[0], "etiqueta": "Destacada"}
        if self.indice_carrusel >= len(items):
            return items[0]
        return items[self.indice_carrusel]

    # ==================================================================
    # MÉTODOS INTERNOS
    # ==================================================================

    def _buscar_carrera_por_id(self, id_carrera: int) -> Carrera:
        """Busca una carrera por su id; si no existe devuelve la primera."""
        for carrera in self.carreras:
            if carrera["id"] == id_carrera:
                return carrera
        return self.carreras[0]

    # ==================================================================
    # MANEJADORES DE EVENTOS: DETALLE DE CARRERA
    # ==================================================================

    @rx.event
    def seleccionar_anio(self, indice: int):
        """Cambia el año visible del plan de estudios en el detalle."""
        self.indice_anio_seleccionado = indice

    @rx.event
    def seleccionar_seccion_detalle(self, seccion: str):
        """Cambia la sección activa dentro de la vista de detalle."""
        self.seccion_detalle_activa = seccion

    # ==================================================================
    # MANEJADORES DE EVENTOS: EXPLORADOR DEL HOME
    # ==================================================================

    @rx.event
    def seleccionar_carrera_destacada(self, id_carrera: int):
        """Cambia la carrera destacada en el home y resetea el explorador."""
        self.id_carrera_destacada = id_carrera
        self.seccion_explorador_activa = "info"
        self.indice_anio_explorador = 0
        self.texto_busqueda_carrera = ""
        self.mostrar_panel_flotante = False

    @rx.event
    def seleccionar_seccion_explorador(self, seccion: str):
        """Cambia la sección activa del explorador del home."""
        self.seccion_explorador_activa = seccion

    @rx.event
    def seleccionar_anio_explorador(self, indice: int):
        """Cambia el año visible en el explorador del home."""
        self.indice_anio_explorador = indice

    @rx.event
    def actualizar_busqueda_carrera(self, texto: str):
        """Actualiza el texto de búsqueda de carreras."""
        self.texto_busqueda_carrera = texto

    @rx.event
    def alternar_panel_flotante(self):
        """Muestra u oculta el panel flotante de selección."""
        self.mostrar_panel_flotante = not self.mostrar_panel_flotante

    @rx.event
    def cerrar_panel_flotante(self):
        """Cierra el panel flotante."""
        self.mostrar_panel_flotante = False

    # ==================================================================
    # MANEJADORES DE EVENTOS: FILTROS Y ORDENAMIENTO
    # ==================================================================

    @rx.event
    def cambiar_filtro(self, filtro: str):
        """Cambia el filtro activo de la lista de carreras."""
        self.filtro_activo = filtro

    @rx.event
    def cambiar_orden(self, orden: str):
        """Cambia el ordenamiento activo de la lista de carreras."""
        self.orden_activo = orden

    # ==================================================================
    # MANEJADORES DE EVENTOS: CARRUSEL
    # ==================================================================

    @rx.event
    def siguiente_carrusel(self):
        """Avanza al siguiente banner del carrusel."""
        total = len(self.carreras_destacadas_con_etiquetas)
        if total > 0:
            self.indice_carrusel = (self.indice_carrusel + 1) % total

    @rx.event
    def anterior_carrusel(self):
        """Retrocede al banner anterior del carrusel."""
        total = len(self.carreras_destacadas_con_etiquetas)
        if total > 0:
            self.indice_carrusel = (self.indice_carrusel - 1) % total

    @rx.event
    def ir_a_banner(self, indice: int):
        """Salta a un banner específico del carrusel."""
        self.indice_carrusel = indice

    @rx.event(background=True)
    async def auto_avanzar_carrusel(self):
        """Avanza el carrusel automáticamente cada 5 segundos."""
        while True:
            await asyncio.sleep(5)
            async with self:
                self.siguiente_carrusel()

    # ==================================================================
    # UTILIDADES
    # ==================================================================

    @rx.event
    def aleatorizar_colores_carreras(self):
        """
        Reasigna aleatoriamente la paleta de colores a las carreras.

        Cada elemento de `PALETA_COLORES` es una tupla de 4 colores:
        `(principal_light, suave_light, principal_dark, suave_dark)`.
        """
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
        for carrera, colores in zip(self.carreras, seleccionados, strict=False):
            principal, suave, principal_dark, suave_dark = colores
            nueva_carrera = dict(carrera)
            nueva_carrera["color_principal"] = principal
            nueva_carrera["color_suave"] = suave
            nueva_carrera["color_principal_dark"] = principal_dark
            nueva_carrera["color_suave_dark"] = suave_dark
            carreras_actualizadas.append(nueva_carrera)

        self.carreras = carreras_actualizadas


__all__ = ["EstadoInstitucional"]