# ══════════════════════════════════════════════════════════════
#  VISTA 2 — ESTADÍSTICAS
# ══════════════════════════════════════════════════════════════
import flet as ft
from datetime import date
from ..utils.theme import LIGHT_THEME, DARK_THEME, AppTheme, apply_theme, toggle_theme

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

