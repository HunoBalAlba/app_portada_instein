# app_portada_instein/vistas/vista_inicio.py

"""
Vista de la página de inicio (ruta "/") — estilo Neon adaptativo.

✅ SOLO componentes oficiales de Reflex:
   https://reflex.dev/docs/library/

✅ SEMÁNTICA HTML5 sin `rx.el.*`:
   - `rx.section` para secciones numeradas.
   - `rx.heading(as_="h1"|"h2"|"h3")` para jerarquía correcta.
   - `role` + `aria-label` en `rx.box` cuando aporte accesibilidad.

✅ ESTRUCTURA:
   1. Barra de navegación sticky (role="banner").
   2. Hero principal (h1).
   3. Multimedia institucional (section).
   4. Sección 01 — Estadísticas (section, h2).
   5. Sección 02 — ¿Por qué INSTEIN? (section, h2).
   6. Sección 03 — Preguntas frecuentes (section, h2).
   7. Banner CTA final (article semántico).
   8. Footer institucional (role="contentinfo").
   9. Banner de cookies (RGPD).

✅ SEO:
   - @rx.page con title, description, image.
   - JSON-LD con datos estructurados.

✅ ACCESIBILIDAD WCAG 2.1 AA:
   - role="banner", role="main", role="contentinfo".
   - aria-label en secciones.
   - aria-hidden en elementos decorativos.

✅ LEGAL / RGPD:
   - Banner de cookies con consentimiento explícito.
"""

import reflex as rx

from app_portada_instein.componentes.banner_cookies import banner_cookies
from app_portada_instein.componentes.banner_cta_final import banner_cta_final
from app_portada_instein.componentes.barra_navegacion import (
    barra_navegacion_superior,
)
from app_portada_instein.componentes.estadisticas_instituto import (
    seccion_estadisticas,
)
from app_portada_instein.componentes.hero_principal import hero_principal
from app_portada_instein.componentes.multimedia_institucional import (
    seccion_multimedia_institucional,
)
from app_portada_instein.componentes.pie_pagina import pie_pagina_institucional
from app_portada_instein.componentes.por_que_instein import (
    seccion_por_que_instein,
)
from app_portada_instein.componentes.preguntas_frecuentes import (
    seccion_preguntas_frecuentes,
)
from app_portada_instein.infraestructura.constantes_visuales import (
    AZUL_MARINO_NEON,
    FONDO_HOME,
    NOMBRE_INSTITUTO,
    PADDING_LATERAL,
    TEXTO_HOME_MAS_SUAVE,
    TEXTO_HOME_PRINCIPAL,
)


# ======================================================================
# Constantes locales
# ======================================================================

ANCHO_MAXIMO_CONTENIDO = "72rem"
MAX_WIDTH_CONTENIDO = "100%"
PADDING_INFERIOR_CONTENIDO = "6rem"
PADDING_BANNER_CTA = f"0 {PADDING_LATERAL} 6rem {PADDING_LATERAL}"
PADDING_SEPARADOR_X = "1.5rem"


# ======================================================================
# SEO
# ======================================================================

DESCRIPCION_SEO = (
    "INSTEIN · Instituto Técnico Integrado San Antonio de Padua. "
    "Formación técnica de excelencia con títulos de Provisión Nacional. "
    "5 carreras, equipamiento moderno y docentes especializados."
)

URL_BASE = "https://instein.edu.bo"
IMAGEN_OG = f"{URL_BASE}/og_image.png"


# ======================================================================
# Separador numerado (estilo Neon: "01 — TÍTULO")
# ======================================================================


def separador_numerado(
    numero: str,
    etiqueta: str,
    titulo: str,
    subtitulo: str | None = None,
) -> rx.Component:
    """
    Separador de sección con número grande estilo Neon.

    ✅ SEO: el título es un `<h2>` (vía `as_="h2"`).
    ✅ ACCESIBILIDAD: número decorativo con `aria_hidden`.

    Args:
        numero: "01", "02", "03".
        etiqueta: texto pequeño en mayúsculas.
        titulo: título grande de la sección (se renderiza como `<h2>`).
        subtitulo: texto descriptivo opcional.

    Returns:
        Componente con el número grande a la izquierda y el
        bloque título/subtítulo a la derecha.
    """
    return rx.flex(
        # ─── Número grande a la izquierda (decorativo) ───────────
        rx.text(
            numero,
            font_size=["4rem", "5rem", "6rem"],
            font_weight="900",
            color=AZUL_MARINO_NEON,
            line_height="1",
            letter_spacing="-0.05em",
            font_family="JetBrains Mono",
            opacity="0.4",
            flex_shrink="0",
            aria_hidden="true",
        ),
        # ─── Contenido a la derecha ──────────────────────────────
        rx.vstack(
            rx.text(
                etiqueta,
                font_size="0.75rem",
                font_weight="700",
                color=AZUL_MARINO_NEON,
                letter_spacing="0.15em",
                text_transform="uppercase",
            ),
            # ✅ SEO: `<h2>` para títulos de sección
            rx.heading(
                titulo,
                as_="h2",
                size="8",
                font_weight="900",
                color=TEXTO_HOME_PRINCIPAL,
                letter_spacing="-0.03em",
                line_height="1.1",
                max_width="52rem",
            ),
            rx.cond(
                subtitulo,
                rx.text(
                    subtitulo,
                    font_size="1.125rem",
                    color=TEXTO_HOME_MAS_SUAVE,
                    line_height="1.6",
                    max_width="42rem",
                    margin_top="0.75rem",
                ),
            ),
            spacing="2",
            align="start",
        ),
        gap=["1rem", "2rem", "3rem"],
        align="start",
        width="100%",
        margin_bottom="3rem",
    )


# ======================================================================
# Sección semántica numerada
# ======================================================================


def _seccion_numerada(
    numero: str,
    etiqueta: str,
    titulo: str,
    subtitulo: str,
    contenido: rx.Component,
    id_seccion: str,
) -> rx.Component:
    """
    Envuelve un separador numerado + su contenido en un
    componente `<section>` (usando `rx.section` oficial de Reflex).

    ✅ SEO: `rx.section` renderiza `<section>` HTML5.
    ✅ ACCESIBILIDAD: `aria_label` con el título de la sección.

    Args:
        numero, etiqueta, titulo, subtitulo: parámetros del separador.
        contenido: componente a renderizar debajo del separador.
        id_seccion: ID único para anclar la sección.

    Returns:
        Componente `<section>` con el separador + contenido centrado.
    """
    return rx.section(
        rx.box(
            separador_numerado(numero, etiqueta, titulo, subtitulo),
            padding=f"4rem {PADDING_SEPARADOR_X} 0 {PADDING_SEPARADOR_X}",
            max_width=ANCHO_MAXIMO_CONTENIDO,
            margin="0 auto",
        ),
        contenido,
        width="100%",
        id=id_seccion,
        aria_label=f"Sección {numero}: {titulo}",
    )


# ======================================================================
# Vista
# ======================================================================


@rx.page(
    route="/",
    title=f"Inicio | {NOMBRE_INSTITUTO}",
    description=DESCRIPCION_SEO,
    image=IMAGEN_OG,
)
def vista_inicio() -> rx.Component:
    """
    Página principal de bienvenida — estilo Neon adaptativo.

    ✅ ESTRUCTURA SEMÁNTICA con componentes oficiales de Reflex:
       - `rx.box(role="banner")`    → barra de navegación.
       - `rx.box(role="main")`      → contenido principal.
       - `rx.section`               → cada sección numerada.
       - `rx.box(role="contentinfo")` → footer.

    ✅ JERARQUÍA DE ENCABEZADOS:
       - `<h1>` único en el hero.
       - `<h2>` en cada sección.
       - `<h3>` en cada card.

    ✅ SEO:
       - Metadatos en `@rx.page`.
       - JSON-LD con datos estructurados.

    ✅ ACCESIBILIDAD WCAG 2.1 AA:
       - Roles ARIA en contenedores principales.
       - `aria-label` en secciones.
       - `aria_hidden` en elementos decorativos.

    ✅ RESPONSIVE MOBILE-FIRST:
       - Breakpoints `initial` = móvil.

    Returns:
        Layout completo de la página de inicio.
    """
    return rx.box(
        # =============================================================
        # SEO: JSON-LD con datos estructurados (schema.org)
        # =============================================================
        rx.script(
            """
            {
              "@context": "https://schema.org",
              "@type": "EducationalOrganization",
              "name": "INSTEIN - Instituto Técnico Integrado San Antonio de Padua",
              "url": "https://instein.edu.bo",
              "logo": "https://instein.edu.bo/logo.png",
              "description": "Formación técnica de excelencia con títulos de Provisión Nacional.",
              "address": {
                "@type": "PostalAddress",
                "streetAddress": "Calle Jorge Carrasco entre 3 y 4, Galería FLOR DE ORO 1er piso",
                "addressLocality": "Santa Cruz de la Sierra",
                "addressCountry": "BO"
              },
              "contactPoint": {
                "@type": "ContactPoint",
                "telephone": "+59171282993",
                "contactType": "Admissions"
              }
            }
            """,
            type="application/ld+json",
        ),
        rx.vstack(
            # =============================================================
            # 1. HEADER — Barra de navegación (sticky)
            # =============================================================
            # ✅ SEMÁNTICA: `role="banner"` en rx.box
            rx.box(
                barra_navegacion_superior(),
                width="100%",
                role="banner",
                aria_label="Navegación principal",
            ),
            # =============================================================
            # 2. MAIN — Contenido principal
            # =============================================================
            # ✅ SEMÁNTICA: `role="main"` en rx.box
            rx.box(
                # -----------------------------------------------------
                # 2.1 HERO PRINCIPAL
                # -----------------------------------------------------
                # ✅ SEMÁNTICA: `<article>` con aria-label
                rx.box(
                    hero_principal(),
                    width="100%",
                    role="article",
                    aria_label="Presentación principal",
                ),
                # -----------------------------------------------------
                # 2.2 MULTIMEDIA INSTITUCIONAL (section)
                # -----------------------------------------------------
                rx.section(
                    seccion_multimedia_institucional(),
                    width="100%",
                    id="multimedia",
                    aria_label="Video institucional y redes sociales",
                ),
                # -----------------------------------------------------
                # 2.3 SECCIÓN 01 — Estadísticas
                # -----------------------------------------------------
                _seccion_numerada(
                    numero="01",
                    etiqueta="Métricas institucionales",
                    titulo="15 años formando técnicos de excelencia",
                    subtitulo=(
                        "Cifras que respaldan nuestro compromiso con la "
                        "formación técnica superior."
                    ),
                    contenido=seccion_estadisticas(),
                    id_seccion="estadisticas",
                ),
                # -----------------------------------------------------
                # 2.4 SECCIÓN 02 — ¿Por qué INSTEIN?
                # -----------------------------------------------------
                _seccion_numerada(
                    numero="02",
                    etiqueta="Nuestra propuesta",
                    titulo="Formación que transforma",
                    subtitulo=(
                        "Todo lo que necesitas para convertirte en un "
                        "profesional técnico de excelencia."
                    ),
                    contenido=seccion_por_que_instein(),
                    id_seccion="por-que-instein",
                ),
                # -----------------------------------------------------
                # 2.5 SECCIÓN 03 — Preguntas frecuentes
                # -----------------------------------------------------
                _seccion_numerada(
                    numero="03",
                    etiqueta="Resolvemos tus dudas",
                    titulo="¿Tienes preguntas?",
                    subtitulo=(
                        "Las respuestas a las dudas más comunes de "
                        "nuestros estudiantes."
                    ),
                    contenido=seccion_preguntas_frecuentes(),
                    id_seccion="faq",
                ),
                # -----------------------------------------------------
                # 2.6 BANNER CTA FINAL (article)
                # -----------------------------------------------------
                rx.box(
                    rx.box(
                        banner_cta_final(),
                        padding=PADDING_BANNER_CTA,
                        width="100%",
                        display="flex",
                        justify_content="center",
                    ),
                    width="100%",
                    role="article",
                    aria_label="Llamado a la acción",
                ),
                # -----------------------------------------------------
                # Contenedor principal
                # -----------------------------------------------------
                padding_bottom=PADDING_INFERIOR_CONTENIDO,
                max_width=MAX_WIDTH_CONTENIDO,
                width="100%",
                role="main",
            ),
            # =============================================================
            # 3. FOOTER — Pie de página
            # =============================================================
            # ✅ SEMÁNTICA: `role="contentinfo"` en rx.box
            rx.box(
                pie_pagina_institucional(),
                width="100%",
                role="contentinfo",
                aria_label="Información del sitio",
            ),
            # =============================================================
            # 4. BANNER DE COOKIES (RGPD)
            # =============================================================
            # ✅ LEGAL: banner de consentimiento de cookies.
            banner_cookies(),
            # =============================================================
            # Layout del contenedor raíz
            # =============================================================
            align="center",
            min_height="100vh",
            width="100%",
            spacing="0",
            background=FONDO_HOME,
        ),
        width="100%",
        background=FONDO_HOME,
        lang="es",
    )


__all__ = ["vista_inicio", "separador_numerado"]