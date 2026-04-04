"""
home.py — Página principal con barra de navegación inferior

Secciones: Hoy · Hábitos · Estadísticas · Perfil

USO:
    ft.app(target=main)

    O desde tu router:
        from home import HomePage
        HomePage(page, theme=LIGHT_THEME)
"""

import flet as ft
from datetime import date
from ..utils.theme import LIGHT_THEME, DARK_THEME, AppTheme, apply_theme, toggle_theme


# ══════════════════════════════════════════════════════════════
#  DATOS DE EJEMPLO
# ══════════════════════════════════════════════════════════════

SAMPLE_HABITS = [
    {"id": 1, "name": "Meditación",      "icon": ft.Icons.SELF_IMPROVEMENT_ROUNDED,  "streak": 12, "done": True,  "category": "Mente"},
    {"id": 2, "name": "Leer 20 min",     "icon": ft.Icons.MENU_BOOK_ROUNDED,          "streak": 7,  "done": True,  "category": "Mente"},
    {"id": 3, "name": "Beber 2L agua",   "icon": ft.Icons.WATER_DROP_OUTLINED,        "streak": 4,  "done": False, "category": "Salud"},
    {"id": 4, "name": "Ejercicio",        "icon": ft.Icons.FITNESS_CENTER_ROUNDED,     "streak": 21, "done": False, "category": "Salud"},
    {"id": 5, "name": "Sin redes 1h",    "icon": ft.Icons.PHONE_ANDROID_OUTLINED,     "streak": 2,  "done": False, "category": "Foco"},
    {"id": 6, "name": "Diario personal", "icon": ft.Icons.EDIT_NOTE_ROUNDED,          "streak": 9,  "done": True,  "category": "Mente"},
]

ALL_HABITS = [
    {"id": 1, "name": "Meditación",      "icon": ft.Icons.SELF_IMPROVEMENT_ROUNDED,  "streak": 12, "category": "Mente",  "freq": "Diario"},
    {"id": 2, "name": "Leer 20 min",     "icon": ft.Icons.MENU_BOOK_ROUNDED,          "streak": 7,  "category": "Mente",  "freq": "Diario"},
    {"id": 3, "name": "Beber 2L agua",   "icon": ft.Icons.WATER_DROP_OUTLINED,        "streak": 4,  "category": "Salud",  "freq": "Diario"},
    {"id": 4, "name": "Ejercicio",        "icon": ft.Icons.FITNESS_CENTER_ROUNDED,     "streak": 21, "category": "Salud",  "freq": "Lun/Mié/Vie"},
    {"id": 5, "name": "Sin redes 1h",    "icon": ft.Icons.PHONE_ANDROID_OUTLINED,     "streak": 2,  "category": "Foco",   "freq": "Diario"},
    {"id": 6, "name": "Diario personal", "icon": ft.Icons.EDIT_NOTE_ROUNDED,          "streak": 9,  "category": "Mente",  "freq": "Diario"},
    {"id": 7, "name": "Caminar 30 min",  "icon": ft.Icons.DIRECTIONS_WALK_ROUNDED,    "streak": 0,  "category": "Salud",  "freq": "Mar/Jue"},
    {"id": 8, "name": "Sin cafeína",     "icon": ft.Icons.FREE_BREAKFAST_OUTLINED,    "streak": 3,  "category": "Salud",  "freq": "Fines de semana"},
]

WEEK_DATA = [62, 85, 50, 100, 75, 33, 90]
WEEK_LABELS = ["L", "M", "X", "J", "V", "S", "D"]

CATEGORY_COLORS = {
    "Mente": "#3D7A5E",
    "Salud": "#2E86AB",
    "Foco":  "#B45309",
}


# ══════════════════════════════════════════════════════════════
#  BARRA INFERIOR PERSONALIZADA
# ══════════════════════════════════════════════════════════════

NAV_ITEMS = [
    {"label": "Hoy",          "icon": ft.Icons.TODAY_OUTLINED,        "icon_active": ft.Icons.TODAY_ROUNDED},
    {"label": "Hábitos",      "icon": ft.Icons.CHECKLIST_OUTLINED,    "icon_active": ft.Icons.CHECKLIST_ROUNDED},
    {"label": "Estadísticas", "icon": ft.Icons.BAR_CHART_OUTLINED,    "icon_active": ft.Icons.BAR_CHART_ROUNDED},
    {"label": "Perfil",       "icon": ft.Icons.PERSON_OUTLINE_ROUNDED,"icon_active": ft.Icons.PERSON_ROUNDED},
]


def build_nav_bar(t: AppTheme, active: int, on_change) -> ft.Control:
    c, sp, ty = t.c, t.sp, t.ty

    items = []
    for i, nav in enumerate(NAV_ITEMS):
        is_active = i == active
        items.append(
            ft.GestureDetector(
                on_tap=lambda e, idx=i: on_change(idx),
                content=ft.Container(
                    expand=True,
                    height=sp.bar_height,
                    alignment=ft.Alignment.CENTER,
                    content=ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=2,
                        controls=[
                            ft.Container(
                                width=40,
                                height=28,
                                border_radius=sp.radius_full,
                                bgcolor=c.accent_soft if is_active else ft.Colors.TRANSPARENT,
                                alignment=ft.Alignment.CENTER,
                                animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
                                content=ft.Icon(
                                    nav["icon_active"] if is_active else nav["icon"],
                                    color=c.accent if is_active else c.text_disabled,
                                    size=20,
                                ),
                            ),
                            ft.Text(
                                nav["label"],
                                size=ty.size_xs,
                                weight=ty.semibold if is_active else ty.regular,
                                color=c.accent if is_active else c.text_disabled,
                                font_family=ty.family,
                            ),
                        ],
                    ),
                ),
            )
        )

    return ft.Container(
        bgcolor=c.surface,
        border=ft.Border.only(top=ft.BorderSide(1, c.border)),
        content=ft.Row(
            spacing=0,
            controls=items,
        ),
    )


# ══════════════════════════════════════════════════════════════
#  VISTA 0 — HOY
# ══════════════════════════════════════════════════════════════

def build_view_hoy(t: AppTheme, habits: list, on_toggle) -> ft.Control:
    c, sp, ty, sh = t.c, t.sp, t.ty, t.sh

    done_count = sum(1 for h in habits if h["done"])
    total = len(habits)
    progress = done_count / total if total else 0

    today_str = date.today().strftime("%A, %d de %B").capitalize()

    # ── Header ───────────────────────────────────────────────
    header = ft.Container(
        padding=ft.Padding.only(left=sp.lg, right=sp.lg, top=sp.lg, bottom=sp.md),
        content=ft.Column(
            spacing=sp.md,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                    controls=[
                        ft.Column(
                            spacing=2,
                            controls=[
                                ft.Text(
                                    "Buenos días 👋",
                                    size=ty.size_xl,
                                    weight=ty.bold,
                                    color=c.text_primary,
                                    font_family=ty.family,
                                ),
                                ft.Text(
                                    today_str,
                                    size=ty.size_sm,
                                    color=c.text_secondary,
                                    font_family=ty.family,
                                ),
                            ],
                        ),
                        # Badge racha
                        ft.Container(
                            bgcolor=c.accent_soft,
                            border_radius=sp.radius_full,
                            padding=ft.Padding.symmetric(horizontal=sp.sm, vertical=sp.xs),
                            content=ft.Row(
                                spacing=4,
                                tight=True,
                                controls=[
                                    ft.Text("🔥", size=14),
                                    ft.Text(
                                        "21 días",
                                        size=ty.size_xs,
                                        weight=ty.semibold,
                                        color=c.accent,
                                        font_family=ty.family,
                                    ),
                                ],
                            ),
                        ),
                    ],
                ),

                # Tarjeta de progreso
                ft.Container(
                    bgcolor=c.accent,
                    border_radius=sp.radius_md,
                    padding=ft.Padding.all(sp.md),
                    shadow=sh.sm,
                    content=ft.Column(
                        spacing=sp.sm,
                        controls=[
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Text(
                                        "Progreso de hoy",
                                        size=ty.size_sm,
                                        color=c.accent_on,
                                        font_family=ty.family,
                                        opacity=0.85,
                                    ),
                                    ft.Text(
                                        f"{done_count}/{total}",
                                        size=ty.size_md,
                                        weight=ty.bold,
                                        color=c.accent_on,
                                        font_family=ty.family_mono,
                                    ),
                                ],
                            ),
                            ft.ProgressBar(
                                value=progress,
                                bgcolor=ft.Colors.with_opacity(0.25, c.accent_on),
                                color=c.accent_on,
                                border_radius=sp.radius_full,
                                height=6,
                            ),
                            ft.Text(
                                f"¡Vas muy bien! Te quedan {total - done_count} hábitos." if done_count < total
                                else "¡Completaste todos tus hábitos hoy! 🎉",
                                size=ty.size_xs,
                                color=c.accent_on,
                                font_family=ty.family,
                                opacity=0.85,
                            ),
                        ],
                    ),
                ),
            ],
        ),
    )

    # ── Lista de hábitos ─────────────────────────────────────
    habit_cards = []
    for h in habits:
        habit_cards.append(_build_habit_row(h, t, on_toggle))

    pending = [h for h in habits if not h["done"]]
    done    = [h for h in habits if h["done"]]

    list_content = ft.Column(
        spacing=0,
        controls=[
            ft.Container(
                padding=ft.Padding.only(left=sp.lg, right=sp.lg, bottom=sp.sm),
                content=ft.Text(
                    "Pendientes",
                    size=ty.size_sm,
                    weight=ty.semibold,
                    color=c.text_secondary,
                    font_family=ty.family,
                ),
            ),
            *[ft.Container(
                padding=ft.Padding.symmetric(horizontal=sp.lg, vertical=sp.xs),
                content=_build_habit_row(h, t, on_toggle),
            ) for h in pending],

            ft.Container(height=sp.md),

            ft.Container(
                padding=ft.Padding.only(left=sp.lg, right=sp.lg, bottom=sp.sm),
                content=ft.Text(
                    "Completados",
                    size=ty.size_sm,
                    weight=ty.semibold,
                    color=c.text_secondary,
                    font_family=ty.family,
                ),
            ),
            *[ft.Container(
                padding=ft.Padding.symmetric(horizontal=sp.lg, vertical=sp.xs),
                content=_build_habit_row(h, t, on_toggle),
            ) for h in done],

            ft.Container(height=sp.xl),
        ],
    )

    return ft.Column(
        expand=True,
        scroll=ft.ScrollMode.AUTO,
        spacing=0,
        controls=[header, list_content],
    )


def _build_habit_row(h: dict, t: AppTheme, on_toggle) -> ft.Control:
    c, sp, ty, sh = t.c, t.sp, t.ty, t.sh
    done = h["done"]

    return ft.Container(
        bgcolor=c.surface,
        border_radius=sp.radius_md,
        border=ft.Border.all(1, c.accent if done else c.border),
        shadow=sh.xs,
        padding=ft.Padding.symmetric(horizontal=sp.md, vertical=sp.sm + sp.xs),
        on_click=lambda e, hid=h["id"]: on_toggle(hid),
        ink=True,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Row(
                    spacing=sp.sm,
                    controls=[
                        ft.Container(
                            width=36,
                            height=36,
                            border_radius=sp.radius_sm,
                            bgcolor=c.accent_soft if done else c.surface_alt,
                            alignment=ft.Alignment.CENTER,
                            content=ft.Icon(
                                h["icon"],
                                color=c.accent if done else c.text_secondary,
                                size=18,
                            ),
                        ),
                        ft.Column(
                            spacing=2,
                            controls=[
                                ft.Text(
                                    h["name"],
                                    size=ty.size_base,
                                    weight=ty.medium,
                                    color=c.text_secondary if done else c.text_primary,
                                    font_family=ty.family,
                                ),
                                ft.Row(
                                    spacing=4,
                                    tight=True,
                                    controls=[
                                        ft.Icon(ft.Icons.LOCAL_FIRE_DEPARTMENT_ROUNDED, size=12, color=c.accent if h["streak"] > 0 else c.text_disabled),
                                        ft.Text(
                                            f"{h['streak']} días",
                                            size=ty.size_xs,
                                            color=c.accent if h["streak"] > 0 else c.text_disabled,
                                            font_family=ty.family,
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
                ft.Icon(
                    ft.Icons.CHECK_CIRCLE_ROUNDED if done else ft.Icons.RADIO_BUTTON_UNCHECKED_ROUNDED,
                    color=c.accent if done else c.text_disabled,
                    size=22,
                ),
            ],
        ),
    )


# ══════════════════════════════════════════════════════════════
#  VISTA 1 — HÁBITOS
# ══════════════════════════════════════════════════════════════

def build_view_habitos(t: AppTheme) -> ft.Control:
    c, sp, ty, sh = t.c, t.sp, t.ty, t.sh

    categories = sorted(set(h["category"] for h in ALL_HABITS))

    cat_chips = ft.Row(
        scroll=ft.ScrollMode.AUTO,
        spacing=sp.sm,
        controls=[
            ft.Container(
                bgcolor=c.accent_soft,
                border_radius=sp.radius_full,
                padding=ft.Padding.symmetric(horizontal=sp.md, vertical=sp.xs),
                content=ft.Text("Todos", size=ty.size_xs, weight=ty.semibold, color=c.accent, font_family=ty.family),
            ),
            *[
                ft.Container(
                    bgcolor=c.surface_alt,
                    border_radius=sp.radius_full,
                    border=ft.Border.all(1, c.border),
                    padding=ft.Padding.symmetric(horizontal=sp.md, vertical=sp.xs),
                    content=ft.Text(cat, size=ty.size_xs, color=c.text_secondary, font_family=ty.family),
                )
                for cat in categories
            ],
        ],
    )

    rows = []
    for h in ALL_HABITS:
        cat_color = CATEGORY_COLORS.get(h["category"], c.accent)
        rows.append(
            ft.Container(
                bgcolor=c.surface,
                border_radius=sp.radius_md,
                border=ft.Border.all(1, c.border),
                shadow=sh.xs,
                padding=ft.Padding.symmetric(horizontal=sp.md, vertical=sp.sm + sp.xs),
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Row(
                            spacing=sp.sm,
                            controls=[
                                ft.Container(
                                    width=38,
                                    height=38,
                                    border_radius=sp.radius_sm,
                                    bgcolor=ft.Colors.with_opacity(0.12, cat_color),
                                    alignment=ft.Alignment.CENTER,
                                    content=ft.Icon(h["icon"], color=cat_color, size=18),
                                ),
                                ft.Column(
                                    spacing=2,
                                    controls=[
                                        ft.Text(h["name"], size=ty.size_base, weight=ty.medium, color=c.text_primary, font_family=ty.family),
                                        ft.Row(
                                            spacing=sp.sm,
                                            tight=True,
                                            controls=[
                                                ft.Container(
                                                    bgcolor=ft.Colors.with_opacity(0.10, cat_color),
                                                    border_radius=sp.radius_full,
                                                    padding=ft.Padding.symmetric(horizontal=6, vertical=2),
                                                    content=ft.Text(h["category"], size=ty.size_xs, color=cat_color, font_family=ty.family),
                                                ),
                                                ft.Text("·", size=ty.size_xs, color=c.text_disabled),
                                                ft.Text(h["freq"], size=ty.size_xs, color=c.text_secondary, font_family=ty.family),
                                            ],
                                        ),
                                    ],
                                ),
                            ],
                        ),
                        ft.Row(
                            spacing=4,
                            tight=True,
                            controls=[
                                ft.Icon(ft.Icons.LOCAL_FIRE_DEPARTMENT_ROUNDED, size=14, color=c.accent if h["streak"] > 0 else c.text_disabled),
                                ft.Text(
                                    str(h["streak"]),
                                    size=ty.size_sm,
                                    weight=ty.semibold,
                                    color=c.accent if h["streak"] > 0 else c.text_disabled,
                                    font_family=ty.family_mono,
                                ),
                            ],
                        ),
                    ],
                ),
            )
        )

    return ft.Column(
        expand=True,
        scroll=ft.ScrollMode.AUTO,
        spacing=0,
        controls=[
            # Header
            ft.Container(
                padding=ft.Padding.only(left=sp.lg, right=sp.lg, top=sp.lg, bottom=sp.md),
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Text("Mis hábitos", size=ty.size_xl, weight=ty.bold, color=c.text_primary, font_family=ty.family),
                        ft.Container(
                            width=36,
                            height=36,
                            border_radius=sp.radius_sm,
                            bgcolor=c.accent,
                            alignment=ft.Alignment.CENTER,
                            content=ft.Icon(ft.Icons.ADD_ROUNDED, color=c.accent_on, size=20),
                            ink=True,
                        ),
                    ],
                ),
            ),
            # Chips
            ft.Container(
                padding=ft.Padding.only(left=sp.lg, right=sp.lg, bottom=sp.md),
                content=cat_chips,
            ),
            # Lista
            ft.Container(
                padding=ft.Padding.symmetric(horizontal=sp.lg),
                content=ft.Column(spacing=sp.sm, controls=rows),
            ),
            ft.Container(height=sp.xl),
        ],
    )


# ══════════════════════════════════════════════════════════════
#  VISTA 2 — ESTADÍSTICAS
# ══════════════════════════════════════════════════════════════

def build_view_estadisticas(t: AppTheme) -> ft.Control:
    c, sp, ty, sh = t.c, t.sp, t.ty, t.sh

    # ── Tarjetas de resumen ──────────────────────────────────
    def stat_card(value: str, label: str, icon, color: str) -> ft.Control:
        return ft.Container(
            expand=True,
            bgcolor=c.surface,
            border_radius=sp.radius_md,
            border=ft.Border.all(1, c.border),
            shadow=sh.xs,
            padding=ft.Padding.all(sp.md),
            content=ft.Column(
                spacing=sp.xs,
                controls=[
                    ft.Icon(icon, color=color, size=20),
                    ft.Text(value, size=ty.size_2xl, weight=ty.bold, color=c.text_primary, font_family=ty.family_mono),
                    ft.Text(label, size=ty.size_xs, color=c.text_secondary, font_family=ty.family),
                ],
            ),
        )

    summary_row = ft.Row(
        spacing=sp.sm,
        controls=[
            stat_card("21", "Mejor racha", ft.Icons.LOCAL_FIRE_DEPARTMENT_ROUNDED, "#E55C4A"),
            stat_card("87%", "Esta semana",  ft.Icons.TRENDING_UP_ROUNDED,            c.accent),
            stat_card("6",   "Hábitos activos", ft.Icons.CHECKLIST_ROUNDED,           "#2E86AB"),
        ],
    )

    # ── Gráfica de barras semanal (Canvas) ───────────────────
    max_val = max(WEEK_DATA)
    bar_height = 120

    bars = []
    for i, (val, label) in enumerate(zip(WEEK_DATA, WEEK_LABELS)):
        is_today = i == date.today().weekday()
        fill = val / max_val
        bars.append(
            ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=sp.xs,
                controls=[
                    ft.Text(
                        f"{val}%",
                        size=ty.size_xs,
                        color=c.accent if is_today else c.text_disabled,
                        font_family=ty.family_mono,
                    ),
                    ft.Stack(
                        width=28,
                        height=bar_height,
                        controls=[
                            # Fondo
                            ft.Container(
                                width=28,
                                height=bar_height,
                                border_radius=sp.radius_xs,
                                bgcolor=c.surface_alt,
                                bottom=0,
                            ),
                            # Relleno
                            ft.Container(
                                width=28,
                                height=int(bar_height * fill),
                                border_radius=sp.radius_xs,
                                bgcolor=c.accent if is_today else ft.Colors.with_opacity(0.45, c.accent),
                                bottom=0,
                                alignment=ft.Alignment.BOTTOM_CENTER,
                            ),
                        ],
                    ),
                    ft.Text(
                        label,
                        size=ty.size_xs,
                        weight=ty.semibold if is_today else ty.regular,
                        color=c.accent if is_today else c.text_secondary,
                        font_family=ty.family,
                    ),
                ],
            )
        )

    chart_card = ft.Container(
        bgcolor=c.surface,
        border_radius=sp.radius_md,
        border=ft.Border.all(1, c.border),
        shadow=sh.xs,
        padding=ft.Padding.all(sp.md),
        content=ft.Column(
            spacing=sp.md,
            controls=[
                ft.Text("Completados esta semana", size=ty.size_md, weight=ty.semibold, color=c.text_primary, font_family=ty.family),
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=bars,
                ),
            ],
        ),
    )

    # ── Top hábitos por racha ────────────────────────────────
    sorted_habits = sorted(ALL_HABITS, key=lambda h: h["streak"], reverse=True)[:4]

    top_rows = []
    for i, h in enumerate(sorted_habits):
        top_rows.append(
            ft.Container(
                padding=ft.Padding.symmetric(vertical=sp.sm),
                border=ft.Border.only(bottom=ft.BorderSide(1, c.divider)) if i < 3 else None,
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Row(
                            spacing=sp.sm,
                            controls=[
                                ft.Text(
                                    f"{i+1}",
                                    size=ty.size_sm,
                                    weight=ty.bold,
                                    color=c.text_disabled,
                                    font_family=ty.family_mono,
                                    width=16,
                                ),
                                ft.Icon(h["icon"], color=c.accent, size=16),
                                ft.Text(h["name"], size=ty.size_base, color=c.text_primary, font_family=ty.family),
                            ],
                        ),
                        ft.Row(
                            spacing=4,
                            tight=True,
                            controls=[
                                ft.Icon(ft.Icons.LOCAL_FIRE_DEPARTMENT_ROUNDED, size=14, color=c.accent),
                                ft.Text(f"{h['streak']}d", size=ty.size_sm, weight=ty.semibold, color=c.accent, font_family=ty.family_mono),
                            ],
                        ),
                    ],
                ),
            )
        )

    top_card = ft.Container(
        bgcolor=c.surface,
        border_radius=sp.radius_md,
        border=ft.Border.all(1, c.border),
        shadow=sh.xs,
        padding=ft.Padding.all(sp.md),
        content=ft.Column(
            spacing=0,
            controls=[
                ft.Text("🏆 Top rachas", size=ty.size_md, weight=ty.semibold, color=c.text_primary, font_family=ty.family),
                ft.Container(height=sp.sm),
                *top_rows,
            ],
        ),
    )

    return ft.Column(
        expand=True,
        scroll=ft.ScrollMode.AUTO,
        spacing=0,
        controls=[
            ft.Container(
                padding=ft.Padding.only(left=sp.lg, right=sp.lg, top=sp.lg, bottom=sp.md),
                content=ft.Text("Estadísticas", size=ty.size_xl, weight=ty.bold, color=c.text_primary, font_family=ty.family),
            ),
            ft.Container(
                padding=ft.Padding.symmetric(horizontal=sp.lg),
                content=ft.Column(
                    spacing=sp.md,
                    controls=[summary_row, chart_card, top_card],
                ),
            ),
            ft.Container(height=sp.xl),
        ],
    )


# ══════════════════════════════════════════════════════════════
#  VISTA 3 — PERFIL
# ══════════════════════════════════════════════════════════════

def build_view_perfil(t: AppTheme, on_toggle_theme, on_logout) -> ft.Control:
    c, sp, ty, sh = t.c, t.sp, t.ty, t.sh

    def menu_item(icon, label: str, trailing=None, on_click=None, danger=False) -> ft.Control:
        color = c.error if danger else c.text_primary
        return ft.Container(
            bgcolor=c.surface,
            border_radius=sp.radius_md,
            border=ft.Border.all(1, c.border),
            padding=ft.Padding.symmetric(horizontal=sp.md, vertical=sp.md),
            ink=True,
            on_click=on_click,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Row(
                        spacing=sp.sm,
                        controls=[
                            ft.Icon(icon, color=c.error if danger else c.text_secondary, size=18),
                            ft.Text(label, size=ty.size_base, color=color, font_family=ty.family),
                        ],
                    ),
                    trailing or ft.Icon(ft.Icons.CHEVRON_RIGHT_ROUNDED, color=c.text_disabled, size=18),
                ],
            ),
        )

    theme_switch = ft.Switch(
        value=t.is_dark,
        active_color=c.accent,
        on_change=lambda e: on_toggle_theme(),
    )

    return ft.Column(
        expand=True,
        scroll=ft.ScrollMode.AUTO,
        spacing=0,
        controls=[
            # Avatar + nombre
            ft.Container(
                padding=ft.Padding.only(left=sp.lg, right=sp.lg, top=sp.xl, bottom=sp.lg),
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=sp.sm,
                    controls=[
                        ft.Container(
                            width=72,
                            height=72,
                            border_radius=sp.radius_full,
                            bgcolor=c.accent_soft,
                            border=ft.Border.all(2, c.accent),
                            alignment=ft.Alignment.CENTER,
                            content=ft.Text("AM", size=ty.size_lg, weight=ty.bold, color=c.accent, font_family=ty.family),
                        ),
                        ft.Text("Alejandro M.", size=ty.size_lg, weight=ty.bold, color=c.text_primary, font_family=ty.family),
                        ft.Text("alejandro@mail.com", size=ty.size_sm, color=c.text_secondary, font_family=ty.family),
                        # Badge nivel
                        ft.Container(
                            bgcolor=c.accent_soft,
                            border_radius=sp.radius_full,
                            padding=ft.Padding.symmetric(horizontal=sp.md, vertical=sp.xs),
                            content=ft.Text("⚡ Nivel 5 — Constante", size=ty.size_xs, weight=ty.semibold, color=c.accent, font_family=ty.family),
                        ),
                    ],
                ),
            ),

            # Menú de opciones
            ft.Container(
                padding=ft.Padding.symmetric(horizontal=sp.lg),
                content=ft.Column(
                    spacing=sp.sm,
                    controls=[
                        ft.Text("Cuenta", size=ty.size_xs, weight=ty.semibold, color=c.text_secondary, font_family=ty.family),
                        menu_item(ft.Icons.PERSON_OUTLINE_ROUNDED,   "Editar perfil"),
                        menu_item(ft.Icons.NOTIFICATIONS_NONE_ROUNDED, "Notificaciones"),
                        menu_item(ft.Icons.LOCK_OUTLINE_ROUNDED,     "Privacidad"),

                        ft.Container(height=sp.xs),
                        ft.Text("Preferencias", size=ty.size_xs, weight=ty.semibold, color=c.text_secondary, font_family=ty.family),
                        menu_item(
                            ft.Icons.DARK_MODE_OUTLINED if not t.is_dark else ft.Icons.LIGHT_MODE_OUTLINED,
                            "Modo oscuro",
                            trailing=theme_switch,
                            on_click=lambda e: on_toggle_theme(),
                        ),
                        menu_item(ft.Icons.LANGUAGE_ROUNDED, "Idioma"),
                        menu_item(ft.Icons.HELP_OUTLINE_ROUNDED, "Ayuda y soporte"),

                        ft.Container(height=sp.xs),
                        menu_item(ft.Icons.LOGOUT_ROUNDED, "Cerrar sesión", on_click=lambda e: on_logout(), danger=True),
                        ft.Container(height=sp.xl),
                    ],
                ),
            ),
        ],
    )


# ══════════════════════════════════════════════════════════════
#  HOME PAGE
# ══════════════════════════════════════════════════════════════

class HomePage:
    def __init__(self, page: ft.Page, theme: AppTheme = LIGHT_THEME, on_logout=None):
        self.page = page
        self.theme = theme
        self.on_logout = on_logout
        self._active_tab = 0
        self._habits = [dict(h) for h in SAMPLE_HABITS]

        apply_theme(page, theme)
        self._render()

    # ── Render ───────────────────────────────────────────────

    def _render(self):
        self.page.controls.clear()
        self.page.add(self._build_scaffold())
        self.page.update()

    def _build_scaffold(self) -> ft.Control:
        t = self.theme
        c, sp = t.c, t.sp

        body = self._build_body()
        nav  = build_nav_bar(t, self._active_tab, self._on_nav_change)

        return ft.Column(
            expand=True,
            spacing=0,
            controls=[
                ft.Container(expand=True, content=body),
                nav,
            ],
        )

    def _build_body(self) -> ft.Control:
        t = self.theme
        if self._active_tab == 0:
            return build_view_hoy(t, self._habits, self._on_habit_toggle)
        elif self._active_tab == 1:
            return build_view_habitos(t)
        elif self._active_tab == 2:
            return build_view_estadisticas(t)
        else:
            return build_view_perfil(t, self._on_toggle_theme, self._on_logout)

    # ── Handlers ─────────────────────────────────────────────

    def _on_nav_change(self, idx: int):
        self._active_tab = idx
        self._render()

    def _on_habit_toggle(self, habit_id: int):
        for h in self._habits:
            if h["id"] == habit_id:
                h["done"] = not h["done"]
                break
        self._render()

    def _on_toggle_theme(self):
        self.theme = toggle_theme(self.page, self.theme)
        self._render()

    def _on_logout(self):
        if self.on_logout:
            self.on_logout()
        else:
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("Sesión cerrada."),
            )
            self.page.snack_bar.open = True
            self.page.update()


# ══════════════════════════════════════════════════════════════
#  ENTRY POINT
# ══════════════════════════════════════════════════════════════

def main(page: ft.Page):
    page.title = "Habitly"
    page.window_width = 420
    page.window_height = 820
    page.window_resizable = True

    HomePage(page=page, theme=LIGHT_THEME)


if __name__ == "__main__":
    ft.app(target=main)