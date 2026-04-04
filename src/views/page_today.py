# ══════════════════════════════════════════════════════════════
#  VISTA 0 — HOY
# ══════════════════════════════════════════════════════════════

import flet as ft
from datetime import date
from ..utils.theme import LIGHT_THEME, DARK_THEME, AppTheme, apply_theme, toggle_theme


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

