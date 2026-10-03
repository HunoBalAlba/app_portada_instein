"""
Estado global de la aplicación pública del instituto.

Centraliza:
- El catálogo de carreras.
- La carrera destacada en el home.
- El estado del explorador (sección activa + búsqueda + año seleccionado).
- La visibilidad del panel flotante de selección.
- El filtro activo en la página de carreras.
- El carrusel de carreras destacadas.

Nota técnica: PATH PARAMS y RUTA
--------------------------------
- Los PATH PARAMS se obtienen con `self.router.page.params` (dict).
- La RUTA ACTUAL se obtiene con `self.router.url.path` (str).
- `carrera_id` viene como string; se convierte a int con try/except.
- Si no es convertible, se devuelve `-1` para detectar IDs inválidos.

Nota técnica: TIPADO DE VARS REACTIVAS CON `rx.foreach`
--------------------------------------------------------
Reflex necesita que las `@rx.var` que se usan como fuente de
`rx.foreach` tengan un **tipo de retorno preciso**. Si devuelven
`dict` genérico, los campos internos se infieren como `Any` y
`rx.foreach` falla con:

    ForeachVarError: Could not foreach over var of type Any

Por eso:

- `carrera_seleccionada` **siempre devuelve un `Carrera` válido**
  (fallback a `carreras[0]` si el id es inválido). Esto garantiza el
  tipado que `rx.foreach` necesita.
- La **validez real** del id se comprueba por separado con
  `carrera_es_valida` (bool), que NO se usa en `foreach`.
- El `on_load` de la vista usa `carrera_es_valida` para decidir si
  redirige a `/404`. Así, si el id es inválido, la vista ni siquiera
  se renderiza.
- Las listas de `TypedDict` (`list[Carrera]`, `list[PlanAnual]`,
  `list[PreguntaFrecuente]`) evitan el `ForeachVarError` porque el
  tipo interno se infiere correctamente.

Nota técnica: COLORES ADAPTATIVOS
---------------------------------
Los colores adaptativos (light/dark) NO se exponen como `@rx.var`
porque `rx.color_mode_cond()` devuelve un `Var` reactivo del frontend,
no un `str` serializable.

⚠️ NOTA: Como el proyecto decidió unificar el acento bajo un único
azul marino (`AZUL_MARINO_NEON`), los iconos flotantes de esta State
también lo usan directamente en lugar de `carrera["color_principal"]`.

Nota técnica: @rx.var SIN ARGUMENTOS
------------------------------------
En Reflex 0.9.x, un `@rx.var` NO puede recibir argumentos (más allá de
`self`). Los helpers que necesitan argumentos (como `_carrera_por_id`)
deben ser **métodos normales de Python**, no decorados.

Nota técnica: @rx.var(cache=True)
---------------------------------
Las `@rx.var` que dependen de otras vars y solo cambian cuando el
catálogo cambia pueden cachearse con `@rx.var(cache=True)`. Esto evita
recalcular la var en cada render del componente que la consume.

Aplicado a: `carreras_destacadas_con_etiquetas` (depende solo de
`self.carreras`).

Nota técnica: CARRUSEL AUTOMÁTICO (FIX FUGA DE MEMORIA)
-------------------------------------------------------
El auto-avance del carrusel **NO se implementa con una tarea en
background de Python** (`while True` + `@rx.event(background=True)`)
porque eso causaba una fuga de memoria:

- La tarea nunca se detenía al salir de `/carreras` (Reflex no expone
  `on_unmount` de página).
- Cada navegación a `/carreras` añadía una tarea infinita nueva.

**Solución**: el auto-avance vive en el **cliente** mediante
`rx.moment(interval=5000)`, que dispara el evento
`siguiente_carrusel` cada 5 segundos. El navegador cancela el
intervalo automáticamente al desmontar el componente (salir de la
página).

Ventajas:
- 1 intervalo por página activa (no acumulativo).
- 0% CPU del servidor (el timer vive en el navegador).
- Cancelación automática al navegar fuera.

Este State solo expone los eventos `siguiente_carrusel`,
`anterior_carrusel` e `ir_a_banner`, que son disparados desde el
componente `hero_carreras` (flechas, dots y el `rx.moment`).
"""

from __future__ import annotations

import random
from typing import TypedDict

import reflex as rx

from app_portada_instein.datos.catalogo_carreras import (
    CATALOGO_CARRERAS,
    PALETA_COLORES,
)
from app_portada_instein.datos.modelos_carrera import (
    Carrera,
    CarreraConEtiqueta,
    PlanAnual,
    PreguntaFrecuente,
)
from app_portada_instein.infraestructura.constantes_visuales import (
    AZUL_MARINO_NEON,
)


# ======================================================================
# Tipos locales
# ======================================================================


class OpcionAnio(TypedDict):
    """
    Opción de año para el `rx.segmented_control` del plan de estudios.

    Attributes:
        etiqueta: Texto visible (ej: "Primer Año").
        valor: Valor único que se pasa al `on_change` (ej: "0", "1").
    """

    etiqueta: str
    valor: str


# ======================================================================
# Constantes del módulo
# ======================================================================

# --- Iconos flotantes del detalle ---
CANTIDAD_ICONOS_FONDO: int = 30
SEMILLA_ICONOS_FONDO: int = 42
TAMANOS_ICONOS_FONDO: list[int] = [16, 20, 24, 28, 32, 40]

# --- Etiquetas cíclicas del carrusel ---
ETIQUETAS_CARRUSEL: list[str] = [
    "Inscripciones abiertas",
    "Cupos limitados",
    "Últimos lugares",
    "Alta demanda",
    "Nuevo plan 2026",
]

# --- Carrusel automático ---
SEGUNDOS_ENTRE_BANNERS: int = 5
"""Segundos entre cada avance automático del carrusel (usado por el
`rx.moment(interval=...)` del componente `hero_carreras`)."""

# --- Secciones válidas del explorador y del detalle ---
SECCIONES_EXPLORADOR_VALIDAS: frozenset[str] = frozenset(
    {"info", "plan", "perfil", "campo", "faq"}
)
"""Secciones válidas del explorador del home."""

SECCIONES_DETALLE_VALIDAS: frozenset[str] = frozenset(
    {"info", "plan", "perfil"}
)
"""Secciones válidas de la vista de detalle de carrera."""

# --- Filtros válidos de la lista de carreras ---
FILTROS_VALIDOS: frozenset[str] = frozenset({
    "demanda_alta",
    "puntuacion_top",
    "mas_inscritos",
    "mas_graduados",
})
"""Claves de filtros válidos para `carreras_filtradas_y_ordenadas`."""

# --- Órdenes válidos de la lista de carreras ---
ORDENES_VALIDAS: frozenset[str] = frozenset({
    "puntuacion_desc",
    "inscritos_desc",
    "graduados_desc",
    "empleabilidad_desc",
    "salario_desc",
})
"""Claves de ordenamiento válidos para `carreras_filtradas_y_ordenadas`."""


# ======================================================================
# Estado
# ======================================================================


class EstadoInstitucional(rx.State):
    """Estado central de la aplicación pública."""

    # ==================================================================
    # ESTADO PERSISTENTE
    # ==================================================================

    # --- Catálogo ---
    carreras: list[Carrera] = CATALOGO_CARRERAS
    """Catálogo de carreras. Puede ser modificado por
    `aleatorizar_colores_carreras`."""

    # --- Home: carrera destacada y explorador ---
    id_carrera_destacada: int = 0
    seccion_explorador_activa: str = "info"
    indice_anio_explorador: int = 0
    texto_busqueda_carrera: str = ""
    mostrar_panel_flotante: bool = False

    # --- Detalle: sección y año ---
    indice_anio_seleccionado: int = 0
    seccion_detalle_activa: str = "info"

    # --- Filtros y ordenamiento de la lista ---
    filtro_activo: str = "demanda_alta"
    orden_activo: str = "puntuacion_desc"

    # --- Carrusel ---
    indice_carrusel: int = 0

    # ==================================================================
    # HELPERS INTERNOS (métodos normales, NO decorados con @rx.var)
    # ==================================================================

    def _carrera_por_id(self, id_carrera: int) -> Carrera:
        """
        Busca una carrera por su `id` en el catálogo actual.

        Si no se encuentra, devuelve la primera del catálogo como
        fallback seguro (para garantizar que `carrera_seleccionada`
        SIEMPRE devuelva un `Carrera` con tipado correcto).

        ⚠️ NO está decorado con `@rx.var` porque tiene argumentos.
        """
        if id_carrera < 0:
            return self.carreras[0]
        for carrera in self.carreras:
            if carrera["id"] == id_carrera:
                return carrera
        return self.carreras[0]

    def _carrera_existe(self, id_carrera: int) -> bool:
        """
        Devuelve True si el id corresponde a una carrera del catálogo.

        ⚠️ Este método SÍ detecta inválidos (no tiene fallback). Se usa
        para validar la URL en `redirigir_si_carrera_invalida`.
        """
        if id_carrera < 0:
            return False
        return any(c["id"] == id_carrera for c in self.carreras)

    @staticmethod
    def _plan_anual_seguro(
        plan_estudios: list[PlanAnual],
        indice: int,
    ) -> PlanAnual:
        """
        Devuelve el plan anual en `indice`, con fallback seguro.

        No usa `self` → `@staticmethod` para permitir testearlo sin
        instanciar el State.
        """
        if not plan_estudios:
            return {"anio": "Sin plan", "materias": []}
        if indice < 0 or indice >= len(plan_estudios):
            return plan_estudios[0]
        return plan_estudios[indice]

    @classmethod
    def _materias_del_plan(
        cls,
        plan_estudios: list[PlanAnual],
        indice: int,
    ) -> list[str]:
        """Devuelve las materias del año en `indice`, con fallback seguro."""
        plan = cls._plan_anual_seguro(plan_estudios, indice)
        return plan["materias"]

    # ==================================================================
    # VARIABLES COMPUTADAS: URL
    # ==================================================================

    @rx.var
    def id_carrera_desde_url(self) -> int:
        """
        Extrae el identificador de la carrera desde la URL.

        Si el valor no es convertible a int, devuelve `-1`.
        """
        valor_crudo = self.router.page.params.get("carrera_id", "")
        try:
            return int(valor_crudo)
        except (ValueError, TypeError):
            return -1

    @rx.var
    def ruta_activa_normalizada(self) -> str:
        """Devuelve la ruta actual normalizada."""
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
        """
        Devuelve la carrera activa según la URL actual.

        ⚠️ SIEMPRE devuelve un `Carrera` válido (con fallback a
        `carreras[0]`), porque `rx.foreach` necesita un tipado
        preciso para iterar sobre `carrera["iconos_animados"]`.

        La validez real del id se comprueba con `carrera_es_valida`.
        """
        return self._carrera_por_id(self.id_carrera_desde_url)

    @rx.var
    def carrera_es_valida(self) -> bool:
        """
        Indica si el `carrera_id` de la URL corresponde a una carrera
        real del catálogo.

        Se usa en `redirigir_si_carrera_invalida` para decidir si
        redirigir a `/404`.
        """
        return self._carrera_existe(self.id_carrera_desde_url)

    @rx.var
    def plan_anual_seleccionado(self) -> PlanAnual:
        """Devuelve el año del plan de estudios visible en detalle."""
        carrera = self.carrera_seleccionada
        return self._plan_anual_seguro(
            carrera["plan_estudios"],
            self.indice_anio_seleccionado,
        )

    # ==================================================================
    # VARIABLES COMPUTADAS: HOME / EXPLORADOR
    # ==================================================================

    @rx.var
    def carrera_destacada(self) -> Carrera:
        """Devuelve la carrera destacada en el home."""
        return self._carrera_por_id(self.id_carrera_destacada)

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
        carrera = self.carrera_destacada
        materias: list[str] = []
        for anio in carrera["plan_estudios"]:
            for materia in anio["materias"]:
                materias.append(materia)
        return materias

    @rx.var
    def perfil_carrera_destacada(self) -> list[str]:
        """Devuelve el perfil profesional de la carrera destacada."""
        return self.carrera_destacada["perfil_profesional"]

    @rx.var
    def campo_carrera_destacada(self) -> list[str]:
        """Devuelve el campo laboral de la carrera destacada."""
        return self.carrera_destacada["campo_laboral"]

    @rx.var
    def plan_agrupado_por_anio(self) -> list[PlanAnual]:
        """Devuelve el plan de estudios de la carrera destacada."""
        return self.carrera_destacada["plan_estudios"]

    @rx.var
    def anio_explorador_seleccionado(self) -> PlanAnual:
        """Devuelve el año visible en el explorador del home."""
        carrera = self.carrera_destacada
        return self._plan_anual_seguro(
            carrera["plan_estudios"],
            self.indice_anio_explorador,
        )

    @rx.var
    def materias_anio_explorador(self) -> list[str]:
        """Devuelve las materias del año seleccionado en el explorador."""
        carrera = self.carrera_destacada
        return self._materias_del_plan(
            carrera["plan_estudios"],
            self.indice_anio_explorador,
        )

    @rx.var
    def preguntas_frecuentes_carrera_destacada(
        self,
    ) -> list[PreguntaFrecuente]:
        """Devuelve las preguntas frecuentes de la carrera destacada."""
        return self.carrera_destacada.get("preguntas_frecuentes", [])

    # ==================================================================
    # VARIABLES COMPUTADAS: VISTA DE CARRERAS (columnas)
    # ==================================================================

    @rx.var
    def carreras_columna_1(self) -> list[Carrera]:
        return self.carreras[:2]

    @rx.var
    def carreras_columna_2(self) -> list[Carrera]:
        return self.carreras[2:4]

    @rx.var
    def carreras_columna_3(self) -> list[Carrera]:
        return self.carreras[4:]

    # ==================================================================
    # VARIABLES COMPUTADAS: PLAN DE ESTUDIOS (segmented control)
    # ==================================================================

    @rx.var
    def opciones_anio_plan(self) -> list[OpcionAnio]:
        """Devuelve las opciones de año para el segmented control."""
        carrera = self.carrera_seleccionada
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
        """Devuelve las carreras filtradas y ordenadas según los filtros."""
        carreras = list(self.carreras)

        # --- Filtro ---
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
            "inscritos_desc": (
                lambda c: c["estadisticas"]["estudiantes_inscritos"]
            ),
            "graduados_desc": (
                lambda c: c["estadisticas"]["estudiantes_graduados"]
            ),
            "empleabilidad_desc": (
                lambda c: c["estadisticas"]["tasa_empleabilidad"]
            ),
            "salario_desc": (
                lambda c: c["estadisticas"]["salario_promedio_bs"]
            ),
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
        """
        Devuelve los componentes de iconos flotantes precalculados.

        ✅ REFACTORIZADO: usa `AZUL_MARINO_NEON` en lugar del color
        de la carrera, porque el proyecto unificó el acento bajo un
        único azul marino.
        """
        carrera = self.carrera_seleccionada

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
                    rx.icon(
                        tag=nombre,
                        size=tamano,
                        color=AZUL_MARINO_NEON,
                    ),
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

    @rx.var(cache=True)
    def carreras_destacadas_con_etiquetas(
        self,
    ) -> list[CarreraConEtiqueta]:
        """
        Devuelve TODAS las carreras del catálogo con su etiqueta.

        ✅ CACHEADA con `@rx.var(cache=True)` porque solo depende de
        `self.carreras` (que rara vez cambia). Evita recalcular la
        lista en cada render del carrusel.
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

    @rx.var
    def total_carrusel(self) -> int:
        """
        Cantidad total de items del carrusel.

        Útil para el JS que lo necesita como contador (aunque
        `siguiente_carrusel` ya hace módulo, esto puede servir para
        debug).
        """
        return len(self.carreras_destacadas_con_etiquetas)

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
    # MANEJADORES DE EVENTOS: VALIDACIÓN DE RUTA
    # ==================================================================

    @rx.event
    def redirigir_si_carrera_invalida(self):
        """
        Redirige a `/404` si el `carrera_id` de la URL no existe.

        Añade `?origen=carrera` al query param para que la 404 muestre
        CTAs contextuales ("Ver carreras").
        """
        if not self.carrera_es_valida:
            return rx.redirect("/404?origen=carrera")
        return None

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
    # ⚠️ Ya NO hay `bucle_carrusel`, `iniciar_carrusel_automatico` ni
    #    `detener_carrusel_automatico`. El auto-avance vive en el
    #    componente `hero_carreras` con `rx.moment(interval=...)`.
    # ==================================================================

    @rx.event
    def siguiente_carrusel(self):
        """
        Avanza al siguiente banner del carrusel.

        Este evento es disparado por:
        - El `rx.moment(interval=...)` del componente (cada 5s).
        - La flecha derecha del carrusel (clic manual).
        """
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

    # ==================================================================
    # UTILIDADES
    # ==================================================================

    @rx.event
    def aleatorizar_colores_carreras(self, semilla: int | None = None):
        """Reasigna aleatoriamente la paleta de colores a las carreras."""
        rng = random.Random(semilla)

        cantidad = len(self.carreras)
        paleta_disponible = PALETA_COLORES.copy()

        if len(paleta_disponible) >= cantidad:
            seleccionados = rng.sample(paleta_disponible, cantidad)
        else:
            seleccionados = [
                rng.choice(paleta_disponible) for _ in range(cantidad)
            ]

        rng.shuffle(seleccionados)

        carreras_actualizadas: list[Carrera] = []
        for carrera, colores in zip(self.carreras, seleccionados):
            principal, suave, principal_dark, suave_dark = colores
            nueva_carrera = dict(carrera)
            nueva_carrera["color_principal"] = principal
            nueva_carrera["color_suave"] = suave
            nueva_carrera["color_principal_dark"] = principal_dark
            nueva_carrera["color_suave_dark"] = suave_dark
            carreras_actualizadas.append(nueva_carrera)

        self.carreras = carreras_actualizadas


# ======================================================================
# EXPORTS
# ======================================================================

__all__ = [
    "CANTIDAD_ICONOS_FONDO",
    "ETIQUETAS_CARRUSEL",
    "EstadoInstitucional",
    "FILTROS_VALIDOS",
    "ORDENES_VALIDAS",
    "OpcionAnio",
    "SECCIONES_DETALLE_VALIDAS",
    "SECCIONES_EXPLORADOR_VALIDAS",
    "SEGUNDOS_ENTRE_BANNERS",
    "SEMILLA_ICONOS_FONDO",
    "TAMANOS_ICONOS_FONDO",
]