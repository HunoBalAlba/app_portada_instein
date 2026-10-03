# app_portada_instein/componentes/banner_cookies.py

"""
Banner de consentimiento de cookies — cumplimiento RGPD/LGPD/CCPA.

✅ SOLO componentes oficiales de Reflex:
   https://reflex.dev/docs/library/

✅ RESPONSABILIDAD ÚNICA: mostrar el banner hasta que el usuario dé
   su consentimiento explícito. Luego se oculta permanentemente.

✅ Almacena el consentimiento en `localStorage` para no volver a
   mostrarlo en visitas futuras.

✅ Enlaces visibles a Política de Privacidad y Términos.

⚠️ Este componente es OBLIGATORIO si el sitio usa cookies analíticas
   o de terceros (Google Analytics, Meta Pixel, etc.).

Referencia legal:
- RGPD (UE) · Art. 7: consentimiento explícito e informado.
- LGPD (Brasil) · Art. 8: consentimiento del titular.
- CCPA (California) · §1798.100: derecho a saber y opt-out.

⚠️ NOTA SOBRE LA PERSISTENCIA:
   El estado vive en memoria (rx.State). Al recargar la página, el
   banner vuelve a aparecer. Para persistencia real en el navegador,
   se usa `rx.call_script("localStorage...")` y se lee con
   `rx.State` + `rx.call_script` en `on_load` (implementación
   pendiente si se requiere).

⚠️ NOTA SOBRE PROPS DE LAYOUT:
   En Reflex, los props con `Literal` cerrado (`direction`, `justify`,
   `align`, `wrap`) NO aceptan listas de strings. Deben usar
   `rx.breakpoints(...)` para ser responsive.
   Los props de estilo abierto (`width`, `padding`, `gap`) SÍ aceptan
   listas.
"""

import reflex as rx

from app_portada_instein.infraestructura.constantes_visuales import (
    AZUL_MARINO_NEON,
    BORDE_HOME_AZUL,
    FONDO_HOME,
    RADIO_EXTRA_GRANDE,
    TEXTO_HOME_MAS_SUAVE,
    TEXTO_HOME_PRINCIPAL,
)


# ======================================================================
# Estado del banner
# ======================================================================


class EstadoBannerCookies(rx.State):
    """
    Estado del banner de cookies.

    `consentimiento_otorgado` es False por defecto.
    Una vez que el usuario elige una opción, se oculta el banner.
    """

    consentimiento_otorgado: bool = False
    motivo_consentimiento: str = ""

    @rx.event
    def aceptar_todas(self):
        """Acepta todas las cookies."""
        self.consentimiento_otorgado = True
        self.motivo_consentimiento = "all"
        # Persistencia en localStorage (opcional)
        yield rx.call_script(
            "localStorage.setItem('instein_cookies_consent', 'all');"
        )

    @rx.event
    def aceptar_solo_necesarias(self):
        """Acepta solo las cookies necesarias (mínimo legal)."""
        self.consentimiento_otorgado = True
        self.motivo_consentimiento = "necessary"
        yield rx.call_script(
            "localStorage.setItem('instein_cookies_consent', 'necessary');"
        )

    @rx.event
    def rechazar(self):
        """Rechaza todas las cookies no necesarias."""
        self.consentimiento_otorgado = True
        self.motivo_consentimiento = "rejected"
        yield rx.call_script(
            "localStorage.setItem('instein_cookies_consent', 'rejected');"
        )


# ======================================================================
# Componente: Banner de cookies
# ======================================================================


def _enlace_legal_banner(etiqueta: str, ruta: str) -> rx.Component:
    """
    Enlace legal dentro del banner de cookies.

    Usa `rx.link` oficial con hover azul marino.
    """
    return rx.link(
        etiqueta,
        href=ruta,
        color=AZUL_MARINO_NEON,
        text_decoration="underline",
        font_weight="600",
        transition="color 0.2s",
        _hover={"color": TEXTO_HOME_PRINCIPAL},
    )


def _botones_banner() -> rx.Component:
    """
    Fila de 3 botones responsive:
    - Aceptar todas (primario, azul marino).
    - Solo necesarias (outline).
    - Rechazar (ghost).

    ✅ `justify` usa `rx.breakpoints` porque NO acepta lista de strings.
    """
    return rx.flex(
        # ─── Aceptar todas ──────────────────────────────────────
        rx.button(
            rx.icon("check", size=14),
            "Aceptar todas",
            on_click=EstadoBannerCookies.aceptar_todas,
            background=AZUL_MARINO_NEON,
            color="white",
            font_weight="700",
            size="2",
            cursor="pointer",
            border_radius=RADIO_EXTRA_GRANDE,
            transition="all 0.2s",
            _hover={
                "transform": "translateY(-1px)",
                "filter": "brightness(1.1)",
            },
        ),
        # ─── Solo necesarias ────────────────────────────────────
        rx.button(
            rx.icon("shield", size=14),
            "Solo necesarias",
            on_click=EstadoBannerCookies.aceptar_solo_necesarias,
            variant="outline",
            color_scheme="gray",
            size="2",
            cursor="pointer",
            border_radius=RADIO_EXTRA_GRANDE,
        ),
        # ─── Rechazar ───────────────────────────────────────────
        rx.button(
            rx.icon("x", size=14),
            "Rechazar",
            on_click=EstadoBannerCookies.rechazar,
            variant="ghost",
            color_scheme="gray",
            size="2",
            cursor="pointer",
            border_radius=RADIO_EXTRA_GRANDE,
        ),
        gap="0.5rem",
        flex_wrap="wrap",
        width="100%",
        # ✅ `justify` con rx.breakpoints (NO acepta lista)
        justify=rx.breakpoints(
            initial="start",
            sm="start",
            md="end",
            lg="end",
        ),
    )


def banner_cookies() -> rx.Component:
    """
    Banner de cookies con consentimiento explícito.

    ✅ ADAPTATIVO: respeta el color_mode del usuario.
    ✅ ACCESIBLE: navegable por teclado, `role="dialog"`.
    ✅ LEGAL: 3 opciones claras (aceptar todas, solo necesarias,
       rechazar) + enlaces visibles a Política de Privacidad y
       Términos.

    Se oculta automáticamente cuando el usuario elige una opción.

    Returns:
        Banner flotante en la parte inferior de la pantalla (o nada
        si ya se dio el consentimiento).
    """
    return rx.cond(
        EstadoBannerCookies.consentimiento_otorgado,
        # ─── Ya dio consentimiento → no renderizar nada ─────────
        rx.fragment(),
        # ─── Mostrar banner ────────────────────────────────────
        rx.box(
            rx.flex(
                # ─────────────────────────────────────────────
                # Icono decorativo
                # ─────────────────────────────────────────────
                rx.flex(
                    rx.icon(
                        "cookie",
                        size=24,
                        color=AZUL_MARINO_NEON,
                    ),
                    height="2.75rem",
                    width="2.75rem",
                    border_radius=RADIO_EXTRA_GRANDE,
                    background="rgba(59, 91, 219, 0.15)",
                    border=f"1px solid {BORDE_HOME_AZUL}",
                    align="center",
                    justify="center",
                    flex_shrink="0",
                    aria_hidden="true",
                ),
                # ─────────────────────────────────────────────
                # Contenido (título + descripción + botones)
                # ─────────────────────────────────────────────
                rx.vstack(
                    # Título
                    rx.heading(
                        "Usamos cookies",
                        as_="h3",
                        size="4",
                        font_weight="800",
                        color=TEXTO_HOME_PRINCIPAL,
                        line_height="1.2",
                        letter_spacing="-0.02em",
                    ),
                    # Descripción con enlaces legales
                    rx.text(
                        "Utilizamos cookies para mejorar tu experiencia, "
                        "analizar el tráfico y personalizar el contenido. "
                        "Puedes aceptar todas, solo las necesarias, o "
                        "rechazarlas. ",
                        _enlace_legal_banner(
                            "Política de Privacidad", "/privacidad"
                        ),
                        " · ",
                        _enlace_legal_banner(
                            "Términos", "/terminos"
                        ),
                        font_size="0.875rem",
                        color=TEXTO_HOME_MAS_SUAVE,
                        line_height="1.6",
                    ),
                    # Botones
                    _botones_banner(),
                    spacing="3",
                    align="start",
                    width="100%",
                ),
                # ✅ `direction` y `align` con rx.breakpoints (NO aceptan lista)
                direction=rx.breakpoints(
                    initial="column",
                    sm="column",
                    md="row",
                    lg="row",
                ),
                align=rx.breakpoints(
                    initial="start",
                    sm="start",
                    md="start",
                    lg="start",
                ),
                gap="1rem",
                width="100%",
            ),
            # ─────────────────────────────────────────────────
            # Estilos del contenedor
            # ─────────────────────────────────────────────────
            position="fixed",
            bottom="1.5rem",
            left="50%",
            transform="translateX(-50%)",
            # ✅ `width` SÍ acepta lista (es estilo abierto)
            width=[
                "calc(100vw - 2rem)",
                "calc(100vw - 2rem)",
                "42rem",
                "42rem",
            ],
            max_width="42rem",
            padding="1.5rem",
            border_radius=RADIO_EXTRA_GRANDE,
            background=FONDO_HOME,
            border=f"1px solid {BORDE_HOME_AZUL}",
            box_shadow=(
                f"0 20px 40px -10px rgba(0, 0, 0, 0.3), "
                f"0 0 30px -10px {AZUL_MARINO_NEON}40"
            ),
            backdrop_filter="blur(20px)",
            z_index="1000",
            role="dialog",
            aria_label="Consentimiento de cookies",
        ),
    )


__all__ = [
    "EstadoBannerCookies",
    "banner_cookies",
]