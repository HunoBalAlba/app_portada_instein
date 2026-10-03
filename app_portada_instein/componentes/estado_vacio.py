"""
Estado vacío — componente único reutilizable.

Reemplaza las 3 implementaciones duplicadas que existían en:

- `vistas/vista_carreras.py`              → `_estado_vacio()`
- `vistas/blog/card_post.py`              → `estado_vacio()`
- `componentes/explorador/buscador.py`    → `_estado_vacio_busqueda()`

Ventajas de unificar
--------------------
- 1 sola implementación del estado vacío → 1 sola corrección de bugs.
- Estilos consistentes en toda la app.
- Personalizable por props (icono, tamaño, acciones).

Nota técnica: VARIANTES DE USO
------------------------------
El componente soporta 3 casos de uso típicos:

1. **Con acción primaria** (`boton_accion`):
   Estado vacío con un botón para reintentar / limpiar filtros.
   Usado en: `vista_carreras`, `blog/card_post`, `explorador/buscador`.

2. **Con acción secundaria** (`boton_secundario`):
   Dos botones apilados (ej: "Volver" + "Ver carreras").
   Usado en: 404, páginas de error.

3. **Sin acciones**:
   Solo icono + título + mensaje.
   Usado en: secciones que no requieren acción.

Nota técnica: VARIANTES DE ESTILO
---------------------------------
El componente soporta 2 variantes visuales:

- `"light"`: fondo claro (`COLOR_FONDO_CARTA`), ideal para páginas de
  contenido.

- `"neon"`: glassmorphism adaptativo, ideal para el home / explorador.

Ambas variantes respetan el `color_mode` del usuario.

Nota técnica: `mensaje` ACEPTA STR O COMPONENT
---------------------------------------------
El parámetro `mensaje` acepta DOS formas:

1. **`str`** (caso simple):
       estado_vacio(
           titulo="No hay resultados",
           mensaje="Prueba ajustando los filtros.",
           ...
       )

   → El componente lo envuelve automáticamente en un `rx.text` con
     el estilo del estado vacío.

2. **`rx.Component`** (caso enriquecido):
       estado_vacio(
           titulo="No hay resultados",
           mensaje=rx.text(
               "No hay resultados para ",
               rx.text.span(f'"{termino}"', color=AZUL_MARINO_NEON),
               ". Intenta otro término.",
           ),
           ...
       )

   → El componente usa el Component tal cual (permite spans, negritas,
     enlaces, etc.).

Esto permite mostrar el término buscado con estilo (como en
`explorador/buscador.py`) sin perder la simplicidad del API.
"""

from __future__ import annotations

from typing import Callable

import reflex as rx

from app_portada_instein.infraestructura.constantes_visuales import (
    AZUL_MARINO_NEON,
    BORDE_HOME_AZUL,
    BORDE_HOME_SUAVE,
    COLOR_ACENTO_SOLIDO,
    COLOR_ACENTO_TEXTO,
    COLOR_BORDE_SUAVE,
    COLOR_FONDO_SUAVE,
    COLOR_TEXTO_APAGADO,
    COLOR_TEXTO_PRINCIPAL,
    COLOR_TEXTO_SECUNDARIO,
    FONDO_AZUL_SUAVE,
    FONDO_HOME_CARD_ADAPTATIVO,
    RADIO_EXTRA_GRANDE,
    RADIO_PASTILLA,
    TEXTO_HOME_MAS_SUAVE,
    TEXTO_HOME_PRINCIPAL,
)


# ======================================================================
# Configuración por variante
# ======================================================================


def _config_variante(variante: str) -> dict:
    """
    Devuelve la configuración visual del estado vacío según la variante.

    Args:
        variante: `"light"` o `"neon"`.

    Returns:
        Dict con claves de estilo (fondo, bordes, colores de texto).
    """
    if variante == "neon":
        return {
            "fondo_icono": FONDO_AZUL_SUAVE,
            "borde_icono": BORDE_HOME_AZUL,
            "fondo_card": FONDO_HOME_CARD_ADAPTATIVO,
            "borde_card": BORDE_HOME_SUAVE,
            "color_texto": TEXTO_HOME_PRINCIPAL,
            "color_texto_secundario": TEXTO_HOME_MAS_SUAVE,
            "color_icono": AZUL_MARINO_NEON,
            "con_blur": True,
        }
    # light (default)
    return {
        "fondo_icono": COLOR_FONDO_SUAVE,
        "borde_icono": COLOR_BORDE_SUAVE,
        "fondo_card": "transparent",
        "borde_card": "none",
        "color_texto": COLOR_TEXTO_PRINCIPAL,
        "color_texto_secundario": COLOR_TEXTO_SECUNDARIO,
        "color_icono": COLOR_TEXTO_APAGADO,
        "con_blur": False,
    }


# ======================================================================
# Helpers internos
# ======================================================================


def _mensaje_componente(
    mensaje: str | rx.Component,
    color_secundario,
) -> rx.Component:
    """
    Construye el bloque de mensaje del estado vacío.

    Si `mensaje` es `str`, lo envuelve en un `rx.text` con el estilo
    estándar. Si es un `rx.Component`, lo devuelve tal cual.

    Args:
        mensaje: `str` o `rx.Component`.
        color_secundario: Color del texto secundario (Var adaptativa).

    Returns:
        Componente listo para renderizar.
    """
    if isinstance(mensaje, str):
        return rx.text(
            mensaje,
            font_size="0.875rem",
            color=color_secundario,
            text_align="center",
            max_width="32rem",
            line_height="1.6",
        )
    return mensaje


def _boton_accion_primaria(
    etiqueta: str,
    icono: str,
    on_click: Callable | None,
    href: str | None,
    color_scheme: str,
) -> rx.Component:
    """
    Botón de acción primaria (solid).

    Args:
        etiqueta: Texto del botón.
        icono: Icono de Lucide.
        on_click: Callback a ejecutar (si es acción interna).
        href: URL destino (si es navegación). Tiene prioridad.
        color_scheme: Color de Radix para el botón.

    Returns:
        `rx.link` con apariencia de botón (si `href`) o `rx.button`
        (si `on_click`).
    """
    contenido = (
        rx.icon(icono, size=16),
        rx.text(etiqueta, as_="span", font_weight="700"),
    )

    if href is not None:
        return rx.link(
            *contenido,
            href=href,
            text_decoration="none",
            display="inline-flex",
            align_items="center",
            gap="0.5rem",
            background=COLOR_ACENTO_SOLIDO,
            color="white",
            padding="0.625rem 1.25rem",
            border_radius=RADIO_PASTILLA,
            font_size="0.875rem",
            transition="all 0.2s",
            _hover={
                "transform": "translateY(-2px)",
                "filter": "brightness(1.1)",
            },
        )

    return rx.button(
        *contenido,
        on_click=on_click,
        size="3",
        variant="solid",
        color_scheme=color_scheme,
        cursor="pointer",
        transition="all 0.2s",
        _hover={
            "transform": "translateY(-2px)",
        },
    )


def _boton_accion_secundaria(
    etiqueta: str,
    icono: str,
    href: str,
    color_texto,
    color_borde,
) -> rx.Component:
    """
    Botón de acción secundaria (outline).

    Args:
        etiqueta: Texto del botón.
        icono: Icono de Lucide.
        href: URL destino.
        color_texto: Color del texto (Var adaptativa).
        color_borde: Color del borde (Var adaptativa).

    Returns:
        `rx.link` con apariencia de botón outline.
    """
    return rx.link(
        rx.icon(icono, size=16),
        rx.text(etiqueta, as_="span", font_weight="600"),
        href=href,
        text_decoration="none",
        display="inline-flex",
        align_items="center",
        gap="0.5rem",
        background="transparent",
        color=color_texto,
        padding="0.625rem 1.25rem",
        border_radius=RADIO_PASTILLA,
        font_size="0.875rem",
        border=f"1px solid {color_borde}",
        transition="all 0.2s",
        _hover={
            "transform": "translateY(-2px)",
            "border_color": COLOR_ACENTO_TEXTO,
        },
    )


# ======================================================================
# Estado vacío completo
# ======================================================================


def estado_vacio(
    *,
    titulo: str,
    mensaje: str | rx.Component,
    icono: str = "search-x",
    variante: str = "light",
    tamano_icono: int = 48,
    icono_acento: bool = False,
    boton_accion_etiqueta: str | None = None,
    boton_accion_icono: str = "rotate-ccw",
    boton_accion_on_click: Callable | None = None,
    boton_accion_href: str | None = None,
    boton_accion_color_scheme: str = "crimson",
    boton_secundario_etiqueta: str | None = None,
    boton_secundario_icono: str = "arrow-left",
    boton_secundario_href: str | None = None,
    max_width: str | None = None,
    padding_vertical: str = "4rem",
) -> rx.Component:
    """
    Estado vacío reutilizable (sin resultados, error, etc.).

    Args:
        titulo: Título principal (ej: "No se encontraron carreras").
        mensaje: Mensaje descriptivo. Puede ser:
            - `str` → se envuelve en un `rx.text` con estilo estándar.
            - `rx.Component` → se usa tal cual (permite spans, negritas).
        icono: Nombre del icono Lucide central.
        variante: `"light"` (por defecto) o `"neon"`.
        tamano_icono: Tamaño del icono central en px.
        icono_acento: Si `True`, el icono usa el acento azul marino
            (en lugar de gris apagado).
        boton_accion_etiqueta: Texto del botón primario (o `None`).
        boton_accion_icono: Icono del botón primario.
        boton_accion_on_click: Callback del botón primario.
        boton_accion_href: URL destino del botón primario (prioridad).
        boton_accion_color_scheme: Color de Radix del botón primario.
        boton_secundario_etiqueta: Texto del botón secundario (o `None`).
        boton_secundario_icono: Icono del botón secundario.
        boton_secundario_href: URL destino del botón secundario.
        max_width: Ancho máximo del contenedor. Si es `None`, usa 100%.
        padding_vertical: Padding vertical del contenedor.

    Returns:
        Componente con icono + título + mensaje + acciones opcionales.

    Ejemplo (mensaje simple):
        estado_vacio(
            titulo="No se encontraron carreras",
            mensaje="Prueba ajustando los filtros.",
            icono="search-x",
            boton_accion_etiqueta="Limpiar filtros",
            boton_accion_on_click=EstadoInstitucional.limpiar_filtros,
        )

    Ejemplo (mensaje enriquecido con Component):
        estado_vacio(
            titulo="No se encontraron carreras",
            mensaje=rx.text(
                "No hay resultados para ",
                rx.text.span(f'"{termino}"', color=AZUL_MARINO_NEON),
                ". Intenta con otro término.",
            ),
            variante="neon",
            icono_acento=True,
            boton_accion_etiqueta="Restablecer búsqueda",
            boton_accion_on_click=EstadoInstitucional.limpiar_filtros,
        )

    Ejemplo (404 con 2 botones):
        estado_vacio(
            titulo="Página no encontrada",
            mensaje="Lo sentimos, el recurso que buscas no existe.",
            icono="search-x",
            boton_accion_etiqueta="Volver al inicio",
            boton_accion_icono="home",
            boton_accion_href="/",
            boton_secundario_etiqueta="Ver blog",
            boton_secundario_icono="newspaper",
            boton_secundario_href="/blog",
        )
    """
    config = _config_variante(variante)

    # --- Icono central ---
    color_icono = (
        AZUL_MARINO_NEON if icono_acento else config["color_icono"]
    )

    icono_componente = rx.box(
        rx.icon(
            icono,
            size=tamano_icono,
            color=color_icono,
        ),
        padding="1.5rem",
        border_radius=RADIO_EXTRA_GRANDE,
        background=config["fondo_icono"],
        border=f"1px solid {config['borde_icono']}",
        backdrop_filter="blur(12px)" if config["con_blur"] else "none",
        display="flex",
        align_items="center",
        justify_content="center",
    )

    # --- Bloque de texto (título + mensaje) ---
    texto_componente = rx.vstack(
        rx.heading(
            titulo,
            size="5",
            font_weight="700",
            color=config["color_texto"],
            text_align="center",
        ),
        _mensaje_componente(
            mensaje,
            color_secundario=config["color_texto_secundario"],
        ),
        spacing="2",
        align="center",
    )

    # --- Acciones (opcionales) ---
    acciones: list[rx.Component] = []

    if boton_accion_etiqueta is not None:
        acciones.append(
            _boton_accion_primaria(
                etiqueta=boton_accion_etiqueta,
                icono=boton_accion_icono,
                on_click=boton_accion_on_click,
                href=boton_accion_href,
                color_scheme=boton_accion_color_scheme,
            )
        )

    if boton_secundario_etiqueta is not None and boton_secundario_href:
        acciones.append(
            _boton_accion_secundaria(
                etiqueta=boton_secundario_etiqueta,
                icono=boton_secundario_icono,
                href=boton_secundario_href,
                color_texto=config["color_texto"],
                color_borde=config["borde_icono"],
            )
        )

    contenedor = rx.vstack(
        icono_componente,
        texto_componente,
        *(
            [
                rx.flex(
                    *acciones,
                    gap="0.75rem",
                    flex_wrap="wrap",
                    justify="center",
                )
            ]
            if acciones
            else []
        ),
        spacing="4",
        align="center",
        justify="center",
        padding=f"{padding_vertical} 1.5rem",
        width="100%",
        background=config["fondo_card"],
        border_radius=RADIO_EXTRA_GRANDE,
        border=config["borde_card"],
    )

    if max_width is not None:
        return rx.box(
            contenedor,
            width="100%",
            max_width=max_width,
            margin="0 auto",
        )
    return contenedor


# ======================================================================
# EXPORTS
# ======================================================================

__all__ = ["estado_vacio"]