"""
theme.py — Sistema de temas para la app de hábitos
Estética: Minimalista / Clean

USO BÁSICO:
    from theme import DARK_THEME, LIGHT_THEME, apply_theme

    def main(page: ft.Page):
        apply_theme(page, LIGHT_THEME)   # o DARK_THEME

        t = LIGHT_THEME
        c = t.colors
        sp = t.spacing

        ft.Container(
            bgcolor=c.surface,
            border_radius=sp.radius_md,
            padding=sp.md,
            content=ft.Text("Hábito", color=c.text_primary),
        )
"""

import flet as ft
from dataclasses import dataclass


# ══════════════════════════════════════════════════════════════
#  1. PALETAS DE COLOR
# ══════════════════════════════════════════════════════════════

@dataclass(frozen=True)
class ColorPalette:
    # ── Fondos ────────────────────────────────────────────────
    bg: str           # Fondo raíz de la app
    surface: str      # Cards, paneles, bottom sheets
    surface_alt: str  # Inputs, chips, items de lista (nivel 3)

    # ── Acento ────────────────────────────────────────────────
    accent: str        # Color de acción principal
    accent_soft: str   # Versión tenue para fondos de badge/chip
    accent_on: str     # Texto/icono encima del acento

    # ── Texto ─────────────────────────────────────────────────
    text_primary: str    # Títulos, labels principales
    text_secondary: str  # Subtítulos, metadatos
    text_disabled: str   # Placeholders, elementos inactivos
    text_inverse: str    # Texto sobre fondos de acento

    # ── Bordes & divisores ────────────────────────────────────
    border: str    # Bordes de cards e inputs
    divider: str   # Líneas separadoras sutiles

    # ── Semánticos ────────────────────────────────────────────
    success: str
    success_soft: str
    warning: str
    warning_soft: str
    error: str
    error_soft: str


# ── LIGHT ─────────────────────────────────────────────────────
# Blanco roto con grises cálidos y verde salvia como acento.
# Transmite calma, claridad y enfoque.
LIGHT = ColorPalette(
    bg="#F7F7F5",
    surface="#FFFFFF",
    surface_alt="#F0F0EE",

    accent="#3D7A5E",        # Verde salvia oscuro
    accent_soft="#E8F2ED",   # Verde muy tenue
    accent_on="#FFFFFF",

    text_primary="#1A1A1A",
    text_secondary="#6B6B6B",
    text_disabled="#ADADAD",
    text_inverse="#FFFFFF",

    border="#E4E4E2",
    divider="#EFEFED",

    success="#3D7A5E",
    success_soft="#E8F2ED",
    warning="#B45309",
    warning_soft="#FEF3C7",
    error="#C0392B",
    error_soft="#FDECEA",
)

# ── DARK ──────────────────────────────────────────────────────
# Gris carbón profundo (no negro puro). Mismo acento verde
# adaptado para contraste alto sin ser agresivo.
DARK = ColorPalette(
    bg="#141414",
    surface="#1E1E1E",
    surface_alt="#282828",

    accent="#5AA882",        # Verde salvia más luminoso en oscuro
    accent_soft="#1A3329",
    accent_on="#FFFFFF",

    text_primary="#F0F0EE",
    text_secondary="#888888",
    text_disabled="#4A4A4A",
    text_inverse="#141414",

    border="#2C2C2C",
    divider="#242424",

    success="#5AA882",
    success_soft="#1A3329",
    warning="#D97706",
    warning_soft="#2D1F06",
    error="#E55C4A",
    error_soft="#2D100D",
)


# ══════════════════════════════════════════════════════════════
#  2. TIPOGRAFÍA
# ══════════════════════════════════════════════════════════════

@dataclass(frozen=True)
class Typography:
    family: str       
    family_mono: str  

    # Escala de tamaños (sp)
    size_xs: int     # etiquetas micro, badges
    size_sm: int     # texto de apoyo
    size_base: int   # cuerpo de texto
    size_md: int     # labels destacados, subtítulos
    size_lg: int     # títulos de sección
    size_xl: int     # títulos de pantalla
    size_2xl: int    # números grandes (streaks, %)

    # Pesos semánticos
    regular: ft.FontWeight
    medium: ft.FontWeight
    semibold: ft.FontWeight
    bold: ft.FontWeight

    # Altura de línea (line height multiplier)
    line_height_tight: float    # títulos
    line_height_normal: float   # cuerpo
    line_height_relaxed: float  # texto largo


TYPOGRAPHY = Typography(
    family="DM Sans",       # Fuente principal sans-serif
    family_mono="DM Mono",  # Monoespaciada para números/stats

    size_xs=11,
    size_sm=13,
    size_base=15,
    size_md=17,
    size_lg=20,
    size_xl=26,
    size_2xl=34,

    regular=ft.FontWeight.NORMAL,
    medium=ft.FontWeight.W_500,
    semibold=ft.FontWeight.W_600,
    bold=ft.FontWeight.W_700,

    line_height_tight=1.2,
    line_height_normal=1.5,
    line_height_relaxed=1.7,
)


# ══════════════════════════════════════════════════════════════
#  3. ESPACIADO & RADIOS
# ══════════════════════════════════════════════════════════════

@dataclass(frozen=True)
class Spacing:
    # Escala de espacio (dp) — base 4
    xs: int     # 4
    sm: int     # 8
    md: int     # 16
    lg: int     # 24
    xl: int     # 32
    xxl: int    # 48
    xxxl: int   # 64

    # Radios de borde — minimalista: moderados, nada excesivo
    radius_xs: int    # 4   — badges, tags inline
    radius_sm: int    # 8   — chips, botones pequeños
    radius_md: int    # 12  — cards, inputs
    radius_lg: int    # 16  — modales, bottom sheets
    radius_full: int  # 999 — píldoras, avatares

    # Alturas estándar de componentes
    input_height: int    # 48
    button_height: int   # 44
    bar_height: int      # 56 — bottom nav bar
    app_bar_height: int  # 60


SPACING = Spacing(
    xs=4,
    sm=8,
    md=16,
    lg=24,
    xl=32,
    xxl=48,
    xxxl=64,

    radius_xs=4,
    radius_sm=8,
    radius_md=12,
    radius_lg=16,
    radius_full=999,

    input_height=48,
    button_height=44,
    bar_height=56,
    app_bar_height=60,
)


# ══════════════════════════════════════════════════════════════
#  4. SOMBRAS
# ══════════════════════════════════════════════════════════════

@dataclass(frozen=True)
class ShadowSet:
    none: list               # Sin sombra
    xs: list[ft.BoxShadow]   # Separación mínima (focus states)
    sm: list[ft.BoxShadow]   # Cards en reposo
    md: list[ft.BoxShadow]   # Cards elevadas, dropdowns
    lg: list[ft.BoxShadow]   # Modales, bottom sheets


SHADOWS_LIGHT = ShadowSet(
    none=[],
    xs=[ft.BoxShadow(blur_radius=4,  spread_radius=0, color="#00000008", offset=ft.Offset(0, 1))],
    sm=[ft.BoxShadow(blur_radius=8,  spread_radius=0, color="#0000000D", offset=ft.Offset(0, 2))],
    md=[ft.BoxShadow(blur_radius=16, spread_radius=0, color="#00000012", offset=ft.Offset(0, 4))],
    lg=[ft.BoxShadow(blur_radius=32, spread_radius=0, color="#00000018", offset=ft.Offset(0, 8))],
)

SHADOWS_DARK = ShadowSet(
    none=[],
    xs=[ft.BoxShadow(blur_radius=4,  spread_radius=0, color="#00000030", offset=ft.Offset(0, 1))],
    sm=[ft.BoxShadow(blur_radius=8,  spread_radius=0, color="#00000040", offset=ft.Offset(0, 2))],
    md=[ft.BoxShadow(blur_radius=16, spread_radius=0, color="#00000055", offset=ft.Offset(0, 4))],
    lg=[ft.BoxShadow(blur_radius=32, spread_radius=0, color="#00000070", offset=ft.Offset(0, 8))],
)


# ══════════════════════════════════════════════════════════════
#  5. TEMA COMPLETO
# ══════════════════════════════════════════════════════════════

@dataclass(frozen=True)
class AppTheme:
    """
    Objeto raíz que aglutina todos los tokens de diseño.
    Úsalo como fuente única de verdad en cada vista.
    """
    colors: ColorPalette
    typography: Typography
    spacing: Spacing
    shadows: ShadowSet
    is_dark: bool

    # Aliases cortos para vistas
    @property
    def c(self) -> ColorPalette:
        """t.c.accent, t.c.surface ..."""
        return self.colors

    @property
    def ty(self) -> Typography:
        """t.ty.size_lg, t.ty.semibold ..."""
        return self.typography

    @property
    def sp(self) -> Spacing:
        """t.sp.md, t.sp.radius_md ..."""
        return self.spacing

    @property
    def sh(self) -> ShadowSet:
        """t.sh.sm, t.sh.lg ..."""
        return self.shadows


LIGHT_THEME = AppTheme(
    colors=LIGHT,
    typography=TYPOGRAPHY,
    spacing=SPACING,
    shadows=SHADOWS_LIGHT,
    is_dark=False,
)

DARK_THEME = AppTheme(
    colors=DARK,
    typography=TYPOGRAPHY,
    spacing=SPACING,
    shadows=SHADOWS_DARK,
    is_dark=True,
)


# ══════════════════════════════════════════════════════════════
#  6. HELPERS
# ══════════════════════════════════════════════════════════════

def get_flet_theme(app_theme: AppTheme) -> ft.Theme:
    """
    Genera el ft.Theme nativo de Flet a partir de un AppTheme.
    Asígnalo a page.theme y/o page.dark_theme.
    """
    c = app_theme.colors
    ty = app_theme.typography

    color_scheme = ft.ColorScheme(
        primary=c.accent,
        on_primary=c.accent_on,
        primary_container=c.accent_soft,
        on_primary_container=c.accent,
        secondary=c.accent,
        on_secondary=c.accent_on,
        secondary_container=c.accent_soft,
        background=c.bg,
        on_background=c.text_primary,
        surface=c.surface,
        on_surface=c.text_primary,
        surface_variant=c.surface_alt,
        on_surface_variant=c.text_secondary,
        error=c.error,
        on_error=c.accent_on,
        error_container=c.error_soft,
        outline=c.border,
        outline_variant=c.divider,
    )

    text_theme = ft.TextTheme(
        # Números grandes: streaks, porcentajes
        display_large=ft.TextStyle(
            size=ty.size_2xl,
            weight=ty.bold,
            font_family=ty.family_mono,
        ),
        # Títulos de pantalla
        display_medium=ft.TextStyle(
            size=ty.size_xl,
            weight=ty.bold,
            font_family=ty.family,
        ),
        # Títulos de sección
        headline_medium=ft.TextStyle(
            size=ty.size_lg,
            weight=ty.semibold,
            font_family=ty.family,
        ),
        # Labels destacados
        title_large=ft.TextStyle(
            size=ty.size_md,
            weight=ty.semibold,
            font_family=ty.family,
        ),
        title_medium=ft.TextStyle(
            size=ty.size_base,
            weight=ty.medium,
            font_family=ty.family,
        ),
        # Cuerpo
        body_large=ft.TextStyle(
            size=ty.size_base,
            weight=ty.regular,
            font_family=ty.family,
        ),
        body_medium=ft.TextStyle(
            size=ty.size_sm,
            weight=ty.regular,
            font_family=ty.family,
        ),
        # Etiquetas micro
        label_small=ft.TextStyle(
            size=ty.size_xs,
            weight=ty.medium,
            font_family=ty.family,
        ),
    )

    return ft.Theme(
        color_scheme=color_scheme,
        text_theme=text_theme,
        font_family=ty.family,
        use_material3=True,
        visual_density=ft.ThemeVisualDensity.COMFORTABLE,
    )

def get_flet_theme(app_theme: AppTheme) -> ft.Theme:
    c = app_theme.colors
    ty = app_theme.typography

    color_scheme = ft.ColorScheme(
        primary=c.accent,
        on_primary=c.accent_on,
        primary_container=c.accent_soft,
        on_primary_container=c.accent,

        secondary=c.accent,
        on_secondary=c.accent_on,
        secondary_container=c.accent_soft,

        surface=c.surface,
        on_surface=c.text_primary,
        on_surface_variant=c.text_secondary,

        error=c.error,
        on_error=c.accent_on,
        error_container=c.error_soft,

        outline=c.border,
        outline_variant=c.divider,
    )

    text_theme = ft.TextTheme(
        display_large=ft.TextStyle(
            size=ty.size_2xl,
            weight=ty.bold,
            font_family=ty.family_mono,
        ),
        display_medium=ft.TextStyle(
            size=ty.size_xl,
            weight=ty.bold,
            font_family=ty.family,
        ),
        headline_medium=ft.TextStyle(
            size=ty.size_lg,
            weight=ty.semibold,
            font_family=ty.family,
        ),
        title_large=ft.TextStyle(
            size=ty.size_md,
            weight=ty.semibold,
            font_family=ty.family,
        ),
        title_medium=ft.TextStyle(
            size=ty.size_base,
            weight=ty.medium,
            font_family=ty.family,
        ),
        body_large=ft.TextStyle(
            size=ty.size_base,
            weight=ty.regular,
            font_family=ty.family,
        ),
        body_medium=ft.TextStyle(
            size=ty.size_sm,
            weight=ty.regular,
            font_family=ty.family,
        ),
        label_small=ft.TextStyle(
            size=ty.size_xs,
            weight=ty.medium,
            font_family=ty.family,
        ),
    )

    return ft.Theme(
        color_scheme=color_scheme,
        text_theme=text_theme,
        font_family=ty.family,
        use_material3=True,
        canvas_color=c.bg,
        card_bgcolor=c.surface,
    )

def apply_theme(page: ft.Page, app_theme: AppTheme) -> None:
    """
    Aplica el tema completo a ft.Page de una sola llamada.
    Registra las fuentes, asigna theme y dark_theme,
    y establece el modo activo.

    Ejemplo:
        def main(page: ft.Page):
            apply_theme(page, LIGHT_THEME)
    """
    page.fonts = {
        "DM Sans": "https://fonts.gstatic.com/s/dmsans/v15/rP2tp2ywxg089UriI5-g4vlH9VoD8CmcqZG40F9JadbnoEwAkJxhTmf3ZGMZpg.woff2",
        "DM Mono":  "https://fonts.gstatic.com/s/dmmono/v14/aFTR7PB1QTsUX8KYth-QAKqbYqE.woff2",
    }
    page.theme = get_flet_theme(LIGHT_THEME)
    page.dark_theme = get_flet_theme(DARK_THEME)
    page.theme_mode = ft.ThemeMode.DARK if app_theme.is_dark else ft.ThemeMode.LIGHT
    page.bgcolor = app_theme.colors.bg
    page.padding = 0
    page.update()

def apply_theme(page: ft.Page, app_theme: AppTheme) -> None:
    page.fonts = {
        "DM Sans": "https://fonts.gstatic.com/s/dmsans/v15/rP2tp2ywxg089UriI5-g4vlH9VoD8CmcqZG40F9JadbnoEwAkJxhTmf3ZGMZpg.woff2",
        "DM Mono": "https://fonts.gstatic.com/s/dmmono/v14/aFTR7PB1QTsUX8KYth-QAKqbYqE.woff2",
    }

    page.theme = get_flet_theme(LIGHT_THEME)
    page.dark_theme = get_flet_theme(DARK_THEME)
    page.theme_mode = ft.ThemeMode.DARK if app_theme.is_dark else ft.ThemeMode.LIGHT
    page.bgcolor = app_theme.colors.bg
    page.padding = 0
    page.update()


def toggle_theme(page: ft.Page, current: AppTheme) -> AppTheme:
    """
    Alterna entre modo claro y oscuro. Devuelve el nuevo AppTheme.

    Ejemplo:
        active_theme = LIGHT_THEME

        def on_toggle(e):
            nonlocal active_theme
            active_theme = toggle_theme(page, active_theme)
            page.update()
    """
    next_theme = DARK_THEME if not current.is_dark else LIGHT_THEME
    page.theme_mode = ft.ThemeMode.DARK if next_theme.is_dark else ft.ThemeMode.LIGHT
    page.bgcolor = next_theme.colors.bg
    page.update()
    return next_theme


# ══════════════════════════════════════════════════════════════
#  7. RECETARIO DE COMPONENTES
#     Snippets listos para copiar en tus vistas.
# ══════════════════════════════════════════════════════════════
#
#  ── Card de hábito ──────────────────────────────────────────
#
#  def habit_card(label: str, done: bool, t: AppTheme) -> ft.Container:
#      c, sp, sh = t.c, t.sp, t.sh
#      return ft.Container(
#          bgcolor=c.surface,
#          border_radius=sp.radius_md,
#          padding=ft.padding.symmetric(horizontal=sp.md, vertical=sp.sm + sp.xs),
#          shadow=sh.sm,
#          border=ft.border.all(1, c.accent if done else c.border),
#          content=ft.Row([
#              ft.Icon(
#                  ft.icons.CHECK_CIRCLE if done else ft.icons.RADIO_BUTTON_UNCHECKED,
#                  color=c.accent if done else c.text_disabled,
#                  size=22,
#              ),
#              ft.Text(
#                  label,
#                  size=t.ty.size_base,
#                  weight=t.ty.medium,
#                  color=c.text_primary if not done else c.text_secondary,
#              ),
#          ], spacing=sp.sm),
#      )
#
#  ── Botón primario ──────────────────────────────────────────
#
#  ft.ElevatedButton(
#      text="Añadir hábito",
#      style=ft.ButtonStyle(
#          bgcolor={
#              ft.ControlState.DEFAULT: c.accent,
#              ft.ControlState.HOVERED: c.accent_soft,
#          },
#          color=c.accent_on,
#          shape=ft.RoundedRectangleBorder(radius=sp.radius_sm),
#          elevation={"default": 0},
#          padding=ft.padding.symmetric(horizontal=sp.md, vertical=sp.sm),
#      ),
#  )
#
#  ── Badge de racha ───────────────────────────────────────────
#
#  ft.Container(
#      bgcolor=c.accent_soft,
#      border_radius=sp.radius_full,
#      padding=ft.padding.symmetric(horizontal=sp.sm, vertical=sp.xs),
#      content=ft.Text(
#          "🔥 7 días",
#          size=t.ty.size_xs,
#          weight=t.ty.semibold,
#          color=c.accent,
#      ),
#  )
#
#  ── Divider ──────────────────────────────────────────────────
#
#  ft.Divider(height=1, color=c.divider)
#
#  ── Input de texto ───────────────────────────────────────────
#
#  ft.TextField(
#      hint_text="Nombre del hábito",
#      hint_style=ft.TextStyle(color=c.text_disabled),
#      text_style=ft.TextStyle(color=c.text_primary, size=t.ty.size_base),
#      bgcolor=c.surface_alt,
#      border_color=c.border,
#      focused_border_color=c.accent,
#      border_radius=sp.radius_md,
#      height=sp.input_height,
#      content_padding=ft.padding.symmetric(horizontal=sp.md, vertical=sp.sm),
#  )