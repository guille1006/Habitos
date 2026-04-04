# ══════════════════════════════════════════════════════════════
#  VISTA 3 — PERFIL
# ══════════════════════════════════════════════════════════════

import flet as ft
from datetime import date
from ..utils.theme import LIGHT_THEME, DARK_THEME, AppTheme, apply_theme, toggle_theme

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
