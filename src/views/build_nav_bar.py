# ══════════════════════════════════════════════════════════════
#  BARRA INFERIOR PERSONALIZADA
# ══════════════════════════════════════════════════════════════

import flet as ft  
from ..utils.theme import LIGHT_THEME, DARK_THEME, AppTheme, apply_theme, toggle_theme


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
