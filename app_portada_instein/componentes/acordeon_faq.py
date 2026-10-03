"""
Acordeón de preguntas frecuentes — componente único reutilizable.

Reemplaza las 5 implementaciones duplicadas que existían en:

- `componentes/preguntas_frecuentes.py`      → FAQ del home
- `vistas/vista_detalle_carrera.py`          → FAQ de la carrera
- `vistas/vista_becas.py`                    → FAQ del programa de becas
- `vistas/vista_admision.py`                 → FAQ de admisión
- `componentes/explorador/contenido.py`      → FAQ del explorador

Ventajas de unificar
--------------------
- 1 sola implementación del acordeón → 1 sola corrección de bugs.
- 1 solo `EstadoAcordeonFaq` → menos superficie de error.
- Estilos consistentes en toda la app.
- Personalizable por props (variante, icono, color de acento).

Nota técnica: TIPADO CON `TypedDict`
------------------------------------
`ItemFaq` es un `TypedDict` (no `rx.Base`), consistente con el resto
del proyecto (`Post`, `Carrera`, `PreguntaFrecuente`).

Esto permite:
- Autocompletado real en el IDE.
- Compatibilidad total con `rx.foreach` sin ForeachVarError.
- No depender de APIs internas de Reflex.

⚠️ Los items estáticos se construyen con dicts literales:

    {"pregunta": "¿...?", "respuesta": "..."}

NO con `ItemFaq(pregunta=..., respuesta=...)`.

Nota técnica: `items` ACEPTA ESTÁTICO O `Var`
---------------------------------------------
`acordeon_faq(items=...)` acepta DOS formas:

1. **Lista estática** (`list[ItemFaq]`):
       PREGUNTAS_BECA = [
           {"pregunta": "¿...?", "respuesta": "..."},
           ...
       ]
       acordeon_faq(items=PREGUNTAS_BECA, ...)

   → Cada `item` en el `rx.foreach` es un `dict` real.

2. **Var reactiva** (`rx.Var`):
       acordeon_faq(
           items=carrera_seleccionada["preguntas_frecuentes"],
           ...
       )

   → Cada `item` en el `rx.foreach` es un `Var` reactivo.

En AMBOS casos, el acceso con corchetes `item["pregunta"]` funciona:

- Para `dict` estático → devuelve el `str` directamente.
- Para `Var` reactivo → devuelve un `Var` que apunta al campo.

⚠️ NO se puede iterar el `Var` en Python puro (lanzaría
`VarTypeError`). Por eso el `rx.foreach` interno del acordeón se
encarga de iterar en el frontend.

Nota técnica: VARIOS ACORDEONES EN LA MISMA PÁGINA
--------------------------------------------------
Cada vez que uses `acordeon_faq(...)`, se usa el MISMO `EstadoAcordeonFaq`.
Esto significa que si tienes 2 acordeones en la misma página, al abrir
una pregunta del primero se cerraría la del segundo (porque comparten
`indice_abierto`).

⚠️ En la práctica, cada página tiene UN solo acordeón, así que no es
un problema real. Si en el futuro necesitas múltiples acordeones
independientes en la misma página, se puede crear una subclase de
State por instancia.

Nota técnica: VARIANTES
-----------------------
El componente soporta dos variantes visuales:

- `"light"`: fondo claro (`COLOR_FONDO_CARTA`), borde de acento,
  texto oscuro. Ideal para páginas de contenido (carreras, becas,
  admisión, explorador).

- `"neon"`: glassmorphism adaptativo (light/dark), borde azul marino,
  texto adaptativo. Ideal para el home.

Ambas variantes respetan el `color_mode` del usuario.
"""

from __future__ import annotations

from typing import TypedDict

import reflex as rx

from app_portada_instein.infraestructura.constantes_visuales import (
    AZUL_MARINO_NEON,
    BORDE_HOME_AZUL,
    BORDE_HOME_MEDIO,
    BORDE_HOME_SUAVE,
    COLOR_BORDE_SUAVE,
    COLOR_FONDO_CARTA,
    COLOR_FONDO_SUAVE,
    COLOR_TEXTO_CUERPO,
    COLOR_TEXTO_PRINCIPAL,
    COLOR_TEXTO_SECUNDARIO,
    FONDO_AZUL_MUY_SUAVE,
    FONDO_AZUL_SUAVE,
    FONDO_HOME_CARD_ADAPTATIVO,
    RADIO_MEDIO,
    TEXTO_HOME_MAS_SUAVE,
    TEXTO_HOME_PRINCIPAL,
    TEXTO_HOME_SUAVE,
)


# ======================================================================
# Tipos
# ======================================================================


class ItemFaq(TypedDict):
    """
    Item individual de FAQ (pregunta + respuesta).

    Se usa `TypedDict` (no `rx.Base`) para mantener consistencia con
    el resto del proyecto (`Post`, `Carrera`, `PreguntaFrecuente`) y
    garantizar compatibilidad con `rx.foreach`.

    Ejemplo:
        {
            "pregunta": "¿Qué es el INSTEIN?",
            "respuesta": "Es una institución...",
        }
    """

    pregunta: str
    respuesta: str


# ======================================================================
# Estado del acordeón
# ======================================================================


class EstadoAcordeonFaq(rx.State):
    """
    Estado del acordeón de FAQ compartido por toda la app.

    `indice_abierto = -1` significa que ninguno está abierto.
    Solo una pregunta puede estar abierta a la vez.
    """

    indice_abierto: int = -1

    @rx.event
    def alternar(self, indice: int):
        """Abre o cierra una pregunta del acordeón."""
        if self.indice_abierto == indice:
            self.indice_abierto = -1
        else:
            self.indice_abierto = indice


# ======================================================================
# Configuración por variante
# ======================================================================


def _config_variante(variante: str) -> dict:
    """
    Devuelve la configuración visual del acordeón según la variante.

    Args:
        variante: `"light"` o `"neon"`.

    Returns:
        Dict con claves de estilo (fondo, bordes, colores de texto).
    """
    if variante == "neon":
        return {
            "fondo_card": FONDO_HOME_CARD_ADAPTATIVO,
            "fondo_card_abierta": FONDO_AZUL_MUY_SUAVE,
            "fondo_icono_abierto": FONDO_AZUL_SUAVE,
            "borde_card": BORDE_HOME_SUAVE,
            "borde_hover": BORDE_HOME_MEDIO,
            "borde_abierto": BORDE_HOME_AZUL,
            "color_texto": TEXTO_HOME_PRINCIPAL,
            "color_texto_secundario": TEXTO_HOME_MAS_SUAVE,
            "color_texto_cuerpo": TEXTO_HOME_SUAVE,
            "con_blur": True,
        }
    # light (default)
    return {
        "fondo_card": COLOR_FONDO_CARTA,
        "fondo_card_abierta": COLOR_FONDO_CARTA,
        "fondo_icono_abierto": FONDO_AZUL_SUAVE,
        "borde_card": COLOR_BORDE_SUAVE,
        "borde_hover": COLOR_BORDE_SUAVE,
        "borde_abierto": AZUL_MARINO_NEON,
        "color_texto": COLOR_TEXTO_PRINCIPAL,
        "color_texto_secundario": COLOR_TEXTO_SECUNDARIO,
        "color_texto_cuerpo": COLOR_TEXTO_CUERPO,
        "con_blur": False,
    }


# ======================================================================
# Item individual
# ======================================================================


def _item_acordeon(
    item: ItemFaq | rx.Var,
    indice: int,
    *,
    icono: str,
    color_acento: str,
    radio_item: str,
    fondo_card,
    fondo_card_abierta,
    fondo_icono_abierto,
    borde_card,
    borde_hover,
    borde_abierto,
    color_texto,
    color_texto_secundario,
    color_texto_cuerpo,
    con_blur: bool,
    tamano_texto_pregunta: str,
    tamano_texto_respuesta: str,
    padding_cabecera: str,
    padding_respuesta: str,
) -> rx.Component:
    """
    Item individual del acordeón.

    Args:
        item: `ItemFaq` (dict estático) O `rx.Var` (que apunta a un
            dict con `pregunta` y `respuesta`). En ambos casos, el
            acceso `item["pregunta"]` / `item["respuesta"]` funciona
            gracias a la magia de Reflex.
        indice: Índice del item (para el acordeón).
        icono: Nombre del icono Lucide (a la izquierda). Pasa `""`
            para ocultarlo.
        color_acento: Color del acento cuando el item está abierto.
        radio_item: Border-radius de cada item.
        fondo_card, fondo_card_abierta, fondo_icono_abierto: Fondos
            para los diferentes estados.
        borde_card, borde_hover, borde_abierto: Bordes para los
            diferentes estados.
        color_texto, color_texto_secundario, color_texto_cuerpo:
            Colores de texto.
        con_blur: Si `True`, aplica `backdrop_filter`.
        tamano_texto_pregunta, tamano_texto_respuesta: Tamaños de fuente.
        padding_cabecera, padding_respuesta: Paddings internos.
    """
    esta_abierta = EstadoAcordeonFaq.indice_abierto == indice

    # --- Icono indicador (opcional) ---
    tiene_icono = icono != ""

    icono_componente = rx.cond(
        tiene_icono,
        rx.box(
            rx.icon(
                icono,
                size=16,
                color=rx.cond(
                    esta_abierta,
                    color_acento,
                    color_texto_secundario,
                ),
            ),
            padding="0.5rem",
            border_radius=RADIO_MEDIO,
            background=rx.cond(
                esta_abierta,
                fondo_icono_abierto,
                COLOR_FONDO_SUAVE,
            ),
            display="flex",
            align_items="center",
            justify_content="center",
            flex_shrink="0",
            transition="all 0.2s",
        ),
        rx.fragment(),
    )

    # Padding de la respuesta (con o sin sangría del icono)
    padding_respuesta_final = rx.cond(
        tiene_icono,
        padding_respuesta,
        "0 1.25rem 1.25rem 1.25rem",
    )

    return rx.box(
        # ==========================================================
        # Cabecera clicable
        # ==========================================================
        rx.box(
            rx.flex(
                icono_componente,
                rx.text(
                    item["pregunta"],
                    font_size=tamano_texto_pregunta,
                    font_weight="700",
                    color=color_texto,
                    flex="1",
                    line_height="1.4",
                ),
                rx.icon(
                    "chevron-down",
                    size=20,
                    color=rx.cond(
                        esta_abierta,
                        color_acento,
                        color_texto_secundario,
                    ),
                    transform=rx.cond(
                        esta_abierta,
                        "rotate(180deg)",
                        "rotate(0deg)",
                    ),
                    transition=(
                        "transform 0.3s cubic-bezier(0.4, 0, 0.2, 1), "
                        "color 0.2s"
                    ),
                    flex_shrink="0",
                ),
                align="center",
                gap="0.75rem",
                width="100%",
            ),
            on_click=lambda: EstadoAcordeonFaq.alternar(indice),
            cursor="pointer",
            padding=padding_cabecera,
            role="button",
            tab_index=0,
            width="100%",
        ),
        # ==========================================================
        # Respuesta colapsable
        # ==========================================================
        rx.cond(
            esta_abierta,
            rx.box(
                rx.text(
                    item["respuesta"],
                    font_size=tamano_texto_respuesta,
                    line_height="1.7",
                    color=color_texto_cuerpo,
                ),
                padding=padding_respuesta_final,
            ),
            rx.fragment(),
        ),
        # ==========================================================
        # Estilos base
        # ==========================================================
        width="100%",
        border=rx.cond(
            esta_abierta,
            f"1px solid {borde_abierto}",
            f"1px solid {borde_card}",
        ),
        border_radius=radio_item,
        background=rx.cond(
            esta_abierta,
            fondo_card_abierta,
            fondo_card,
        ),
        backdrop_filter="blur(12px)" if con_blur else "none",
        transition="all 0.2s",
        overflow="hidden",
        _hover={
            "border_color": rx.cond(
                esta_abierta,
                borde_abierto,
                borde_hover,
            ),
        },
    )


# ======================================================================
# Acordeón completo
# ======================================================================


def acordeon_faq(
    items: list[ItemFaq] | rx.Var,
    *,
    variante: str = "light",
    icono: str = "help-circle",
    color_acento: str = AZUL_MARINO_NEON,
    radio_item: str = RADIO_MEDIO,
    tamano_texto_pregunta: str = "0.9375rem",
    tamano_texto_respuesta: str = "0.875rem",
    padding_cabecera: str = "1.125rem 1.25rem",
    padding_respuesta: str = "0 1.25rem 1.25rem 3.5rem",
    max_width: str | None = None,
) -> rx.Component:
    """
    Acordeón de preguntas frecuentes reutilizable.

    Args:
        items: Lista estática (`list[ItemFaq]`) O `Var` reactiva que
            apunta a una lista de dicts con `pregunta` y `respuesta`.

            - Estático: `PREGUNTAS_BECA` (constante de módulo).
            - Reactivo: `carrera_seleccionada["preguntas_frecuentes"]`.

        variante: `"light"` (por defecto) o `"neon"`.
        icono: Nombre del icono Lucide a la izquierda. Pasa `""`
            para ocultarlo.
        color_acento: Color del acento (hex o Var).
        radio_item: Border-radius de cada item.
        tamano_texto_pregunta: Tamaño de la pregunta.
        tamano_texto_respuesta: Tamaño de la respuesta.
        padding_cabecera: Padding interno de la cabecera.
        padding_respuesta: Padding de la respuesta (con sangría).
        max_width: Ancho máximo del contenedor. Si es `None`, usa
            el 100% del contenedor padre.

    Returns:
        Componente `rx.vstack` con la lista de preguntas en acordeón.

    Ejemplo (estático):
        from app_portada_instein.componentes.acordeon_faq import (
            acordeon_faq,
        )

        acordeon_faq(
            items=[
                {"pregunta": "¿...?", "respuesta": "..."},
                {"pregunta": "¿...?", "respuesta": "..."},
            ],
            variante="neon",
            icono="circle-help",
        )

    Ejemplo (reactivo):
        acordeon_faq(
            items=EstadoInstitucional.carrera_seleccionada[
                "preguntas_frecuentes"
            ],
            variante="light",
            icono="circle-help",
        )
    """
    config = _config_variante(variante)

    props_estilo = dict(
        icono=icono,
        color_acento=color_acento,
        radio_item=radio_item,
        fondo_card=config["fondo_card"],
        fondo_card_abierta=config["fondo_card_abierta"],
        fondo_icono_abierto=config["fondo_icono_abierto"],
        borde_card=config["borde_card"],
        borde_hover=config["borde_hover"],
        borde_abierto=config["borde_abierto"],
        color_texto=config["color_texto"],
        color_texto_secundario=config["color_texto_secundario"],
        color_texto_cuerpo=config["color_texto_cuerpo"],
        con_blur=config["con_blur"],
        tamano_texto_pregunta=tamano_texto_pregunta,
        tamano_texto_respuesta=tamano_texto_respuesta,
        padding_cabecera=padding_cabecera,
        padding_respuesta=padding_respuesta,
    )

    contenedor = rx.vstack(
        rx.foreach(
            items,
            lambda item, idx: _item_acordeon(
                item,
                idx,
                **props_estilo,
            ),
        ),
        spacing="3",
        width="100%",
    )

    if max_width is not None:
        return rx.box(
            contenedor,
            width="100%",
            max_width=max_width,
            margin="0 auto",
        )
    return contenedor


__all__ = [
    "EstadoAcordeonFaq",
    "ItemFaq",
    "acordeon_faq",
]