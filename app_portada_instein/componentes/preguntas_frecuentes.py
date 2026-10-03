# app_portada_instein/componentes/preguntas_frecuentes.py

"""
Sección de preguntas frecuentes del home — estilo Neon adaptativo.

✅ REFACTORIZADO: ahora usa el componente genérico `acordeon_faq`
   con variante `"neon"`. El estado del acordeón vive en
   `EstadoAcordeonFaq` (compartido por toda la app).

Antes tenía su propio `EstadoPreguntasFrecuentes` y su propia
implementación del acordeón. Ahora delega en `componentes/acordeon_faq.py`.

Sistema de color (UX)
---------------------
✅ ADAPTATIVO: todos los colores respetan el color_mode del usuario.

- Card cerrada: `FONDO_HOME_CARD_ADAPTATIVO` con glassmorphism.
- Card abierta: `FONDO_AZUL_MUY_SUAVE` + borde azul (`BORDE_HOME_AZUL`).
- Chevron abierto: azul marino neon + rotación 180°.
- Textos: `TEXTO_HOME_PRINCIPAL` / `TEXTO_HOME_MAS_SUAVE` / `TEXTO_HOME_SUAVE`.
- Bordes: `BORDE_HOME_AZUL` / `BORDE_HOME_MEDIO` / `BORDE_HOME_SUAVE`.

⚠️ El encabezado (número + título) se renderiza desde
`vista_inicio.py` con `separador_numerado`, por eso este componente
solo renderiza la lista de preguntas.
"""

from __future__ import annotations

import reflex as rx

from app_portada_instein.componentes.acordeon_faq import (
    ItemFaq,
    acordeon_faq,
)


# ======================================================================
# Constantes locales
# ======================================================================

ANCHO_MAXIMO_LISTA = "56rem"


# ======================================================================
# Estructura de preguntas frecuentes
# ======================================================================

PREGUNTAS_FRECUENTES: list[ItemFaq] = [
    ItemFaq(
        pregunta="¿Qué es el INSTEIN?",
        respuesta=(
            "El Instituto Técnico Integrado San Antonio de Padua (INSTEIN) "
            "es una institución educativa de nivel técnico superior "
            "autorizada por Resolución Ministerial R.M. 0871/2016. "
            "Ofrecemos formación técnica de excelencia en 5 carreras."
        ),
    ),
    ItemFaq(
        pregunta="¿Cómo puedo inscribirme a una carrera?",
        respuesta=(
            "Puedes inscribirte presencialmente en nuestras oficinas "
            "ubicadas en la Galería FLOR DE ORO (1er piso), o contactarnos "
            "por WhatsApp al 71282993. El proceso incluye la presentación "
            "de documentos personales y el pago de la matrícula."
        ),
    ),
    ItemFaq(
        pregunta="¿Cuánto duran las carreras?",
        respuesta=(
            "Todas nuestras carreras tienen una duración de 3 años "
            "(6 semestres). Al finalizar, los estudiantes obtienen el "
            "título de Técnico Superior en Provisión Nacional."
        ),
    ),
    ItemFaq(
        pregunta="¿Cuáles son los requisitos de admisión?",
        respuesta=(
            "Los requisitos son: fotocopia del diploma de bachiller, "
            "fotocopia del carnet de identidad, 2 fotografías tamaño "
            "carnet, y el pago de la matrícula y primera mensualidad."
        ),
    ),
    ItemFaq(
        pregunta="¿Qué horarios ofrecen?",
        respuesta=(
            "Ofrecemos turnos de mañana (08:30 - 12:30) y tarde "
            "(14:30 - 18:30). Algunas carreras también tienen turno "
            "nocturno (19:00 - 22:00) para estudiantes que trabajan."
        ),
    ),
    ItemFaq(
        pregunta="¿Los títulos son válidos para trabajar?",
        respuesta=(
            "Sí, nuestros títulos son emitidos por el Ministerio de "
            "Educación con validez nacional. Están registrados en el "
            "sistema educativo boliviano y son reconocidos por "
            "empleadores."
        ),
    ),
]


# ======================================================================
# Sección completa de preguntas frecuentes
# ======================================================================


def seccion_preguntas_frecuentes() -> rx.Component:
    """
    Sección completa con la lista de preguntas frecuentes del home.

    El encabezado (número + título) se renderiza desde `vista_inicio.py`
    con `separador_numerado`. Este componente SOLO renderiza la lista.

    ✅ REFACTORIZADO: delega en `acordeon_faq` con variante `"neon"`
    (glassmorphism adaptativo) y sin icono lateral (el home tiene
    tipografía más grande, no necesita icono).
    """
    return rx.box(
        acordeon_faq(
            items=PREGUNTAS_FRECUENTES,
            variante="neon",
            icono="",  # Sin icono lateral
            tamano_texto_pregunta="1.0625rem",
            tamano_texto_respuesta="0.9375rem",
            padding_cabecera="1.25rem 1.5rem",
            padding_respuesta="0 1.5rem 1.5rem 1.5rem",
            max_width=ANCHO_MAXIMO_LISTA,
        ),
        width="100%",
        padding="0 1.5rem 4rem 1.5rem",
    )


__all__ = [
    "PREGUNTAS_FRECUENTES",
    "seccion_preguntas_frecuentes",
]