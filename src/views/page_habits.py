# ══════════════════════════════════════════════════════════════
#  VISTA 1 — HÁBITOS
# ══════════════════════════════════════════════════════════════
import flet as ft
from datetime import date
from ..utils.theme import LIGHT_THEME, DARK_THEME, AppTheme, apply_theme, toggle_theme

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

