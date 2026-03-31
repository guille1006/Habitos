"""
login.py — Página de login para la app de hábitos

USO:
    ft.app(target=main)
    
    O integrado en tu router:
    from login import LoginPage
    LoginPage(page, theme, on_login=lambda: navigate_to_home())
"""

import flet as ft
from ..utils.theme import (
    LIGHT_THEME, DARK_THEME, AppTheme,
    apply_theme, toggle_theme,
)


# ══════════════════════════════════════════════════════════════
#  COMPONENTES AUXILIARES
# ══════════════════════════════════════════════════════════════

def build_logo(t: AppTheme) -> ft.Control:
    """Logotipo + nombre de la app."""
    c, sp, ty = t.c, t.sp, t.ty
    return ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=sp.sm,
        controls=[
            ft.Container(
                width=56,
                height=56,
                border_radius=sp.radius_md,
                bgcolor=c.accent,
                content=ft.Icon(
                    ft.Icons.LOOP_ROUNDED,
                    color=c.accent_on,
                    size=28,
                ),
            ),
            ft.Text(
                "Habitly",
                size=ty.size_xl,
                weight=ty.bold,
                font_family=ty.family,
                color=c.text_primary,
            ),
            ft.Text(
                "Construye hábitos que duran",
                size=ty.size_sm,
                weight=ty.regular,
                font_family=ty.family,
                color=c.text_secondary,
            ),
        ],
    )


def build_divider_with_text(label: str, t: AppTheme) -> ft.Control:
    c, sp, ty = t.c, t.sp, t.ty
    line = ft.Container(
        height=1,
        bgcolor=c.divider,
        expand=True,
    )
    return ft.Row(
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=sp.sm,
        controls=[
            line,
            ft.Text(
                label,
                size=ty.size_xs,
                color=c.text_disabled,
                font_family=ty.family,
            ),
            line,
        ],
    )


def build_social_button(
    icon: str,
    label: str,
    t: AppTheme,
    on_click=None,
) -> ft.Control:
    c, sp, ty = t.c, t.sp, t.ty
    return ft.Container(
        height=sp.button_height,
        border_radius=sp.radius_md,
        border=ft.Border.all(1, c.border),
        bgcolor=c.surface,
        ink=True,
        on_click=on_click,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=sp.sm,
            controls=[
                ft.Icon(icon, color=c.text_secondary, size=18),
                ft.Text(
                    label,
                    size=ty.size_sm,
                    weight=ty.medium,
                    color=c.text_primary,
                    font_family=ty.family,
                ),
            ],
        ),
    )


# ══════════════════════════════════════════════════════════════
#  PÁGINA PRINCIPAL
# ══════════════════════════════════════════════════════════════

class LoginPage:
    def __init__(
        self,
        page: ft.Page,
        theme: AppTheme,
        on_login=None,
        on_register=None,
    ):
        self._page = page
        self.theme = theme
        self.on_login = on_login
        self.on_register = on_register

        self._email_field = None
        self._password_field = None
        self._error_text = None
        self._login_btn = None
        self._loading = False

        apply_theme(page, theme)
        page.on_resized = self._on_resize
        self._render()

    # ── Render ───────────────────────────────────────────────

    def _render(self):
        self._page.controls.clear()
        self._page.add(self._build_scaffold())
        self._page.update()

    def _build_scaffold(self) -> ft.Control:
        t = self.theme
        c, sp = t.c, t.sp

        return ft.Stack(
            expand=True,
            controls=[
                # Fondo decorativo
                ft.Container(
                    expand=True,
                    bgcolor=c.bg,
                    content=ft.Stack(
                        controls=[
                            # Blob de color superior
                            ft.Container(
                                width=300,
                                height=300,
                                border_radius=999,
                                bgcolor=c.accent_soft,
                                top=-80,
                                right=-80,
                            ),
                            # Blob inferior
                            ft.Container(
                                width=200,
                                height=200,
                                border_radius=999,
                                bgcolor=c.surface_alt,
                                bottom=-60,
                                left=-60,
                            ),
                        ],
                    ),
                ),
                # Contenido centrado
                ft.Container(
                    expand=True,
                    alignment=ft.Alignment.CENTER,
                    padding=ft.Padding.symmetric(horizontal=sp.lg),
                    content=ft.Column(
                        scroll=ft.ScrollMode.AUTO,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=0,
                        controls=[
                            ft.Container(height=sp.xxxl),  # top spacer
                            self._build_card(),
                            ft.Container(height=sp.lg),
                            self._build_footer(),
                            ft.Container(height=sp.xxxl),  # bottom spacer
                        ],
                    ),
                ),
                # Botón de tema (esquina superior derecha)
                ft.Container(
                    top=sp.lg,
                    right=sp.lg,
                    content=self._build_theme_toggle(),
                ),
            ],
        )

    def _build_card(self) -> ft.Control:
        t = self.theme
        c, sp, sh, ty = t.c, t.sp, t.sh, t.ty

        # ── Campos ───────────────────────────────────────────
        self._email_field = ft.TextField(
            hint_text="correo@ejemplo.com",
            hint_style=ft.TextStyle(color=c.text_disabled, font_family=ty.family),
            text_style=ft.TextStyle(color=c.text_primary, size=ty.size_base, font_family=ty.family),
            bgcolor=c.surface_alt,
            border_color=c.border,
            focused_border_color=c.accent,
            border_radius=sp.radius_md,
            height=sp.input_height,
            content_padding=ft.Padding.symmetric(horizontal=sp.md, vertical=0),
            keyboard_type=ft.KeyboardType.EMAIL,
            on_submit=lambda e: self._password_field.focus(),
            prefix_icon=ft.Icons.MAIL_OUTLINE_ROUNDED,
        )

        self._password_field = ft.TextField(
            hint_text="Contraseña",
            hint_style=ft.TextStyle(color=c.text_disabled, font_family=ty.family),
            text_style=ft.TextStyle(color=c.text_primary, size=ty.size_base, font_family=ty.family),
            bgcolor=c.surface_alt,
            border_color=c.border,
            focused_border_color=c.accent,
            border_radius=sp.radius_md,
            height=sp.input_height,
            content_padding=ft.Padding.symmetric(horizontal=sp.md, vertical=0),
            password=True,
            can_reveal_password=True,
            on_submit=lambda e: self._handle_login(e),
            prefix_icon=ft.Icons.LOCK_OUTLINE_ROUNDED,
        )

        # ── Error ─────────────────────────────────────────────
        self._error_text = ft.Text(
            "",
            size=ty.size_xs,
            color=c.error,
            font_family=ty.family,
            visible=False,
        )

        # ── Botón principal ───────────────────────────────────
        self._login_btn = ft.Container(
            height=sp.button_height,
            border_radius=sp.radius_md,
            bgcolor=c.accent,
            ink=True,
            on_click=self._handle_login,
            shadow=sh.sm,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=sp.sm,
                controls=[
                    ft.Text(
                        "Iniciar sesión",
                        size=ty.size_base,
                        weight=ty.semibold,
                        color=c.accent_on,
                        font_family=ty.family,
                    ),
                ],
            ),
        )

        # ── Card completa ─────────────────────────────────────
        return ft.Container(
            width=400,
            bgcolor=c.surface,
            border_radius=sp.radius_lg,
            border=ft.Border.all(1, c.border),
            shadow=sh.md,
            padding=ft.Padding.all(sp.xl),
            content=ft.Column(
                spacing=0,
                controls=[
                    # Logo
                    build_logo(t),
                    ft.Container(height=sp.xl),

                    # Etiqueta email
                    ft.Text(
                        "Correo electrónico",
                        size=ty.size_sm,
                        weight=ty.medium,
                        color=c.text_secondary,
                        font_family=ty.family,
                    ),
                    ft.Container(height=sp.xs),
                    self._email_field,
                    ft.Container(height=sp.md),

                    # Etiqueta contraseña + "Olvidé"
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Text(
                                "Contraseña",
                                size=ty.size_sm,
                                weight=ty.medium,
                                color=c.text_secondary,
                                font_family=ty.family,
                            ),
                            ft.TextButton(
                                "¿Olvidaste tu contraseña?",
                                style=ft.ButtonStyle(
                                    color={ft.ControlState.DEFAULT: c.accent},
                                    padding=ft.Padding.all(0),
                                    overlay_color=ft.Colors.TRANSPARENT,
                                ),
                                on_click=self._handle_forgot,
                            ),
                        ],
                    ),
                    ft.Container(height=sp.xs),
                    self._password_field,
                    ft.Container(height=sp.xs),

                    # Error message
                    self._error_text,
                    ft.Container(height=sp.md),

                    # Botón login
                    self._login_btn,
                    ft.Container(height=sp.lg),

                    # Divisor "o continúa con"
                    build_divider_with_text("o continúa con", t),
                    ft.Container(height=sp.md),

                    # Botones sociales
                    ft.Row(
                        spacing=sp.sm,
                        controls=[
                            ft.Container(
                                expand=True,
                                content=build_social_button(
                                    ft.Icons.G_MOBILEDATA_ROUNDED,
                                    "Google",
                                    t,
                                    on_click=self._handle_google,
                                ),
                            ),
                            ft.Container(
                                expand=True,
                                content=build_social_button(
                                    ft.Icons.APPLE,
                                    "Apple",
                                    t,
                                    on_click=self._handle_apple,
                                ),
                            ),
                        ],
                    ),
                ],
            ),
        )

    def _build_footer(self) -> ft.Control:
        t = self.theme
        c, ty = t.c, t.ty
        return ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Text(
                    "¿No tienes cuenta?",
                    size=ty.size_sm,
                    color=c.text_secondary,
                    font_family=ty.family,
                ),
                ft.TextButton(
                    "Regístrate gratis",
                    style=ft.ButtonStyle(
                        color={ft.ControlState.DEFAULT: c.accent},
                        padding=ft.Padding.only(left=4),
                        overlay_color=ft.Colors.TRANSPARENT,
                    ),
                    on_click=self._handle_register,
                ),
            ],
        )

    def _build_theme_toggle(self) -> ft.Control:
        t = self.theme
        c, sp = t.c, t.sp
        icon = ft.Icons.DARK_MODE_OUTLINED if not t.is_dark else ft.Icons.LIGHT_MODE_OUTLINED
        return ft.IconButton(
            icon=icon,
            icon_color=c.text_secondary,
            icon_size=20,
            style=ft.ButtonStyle(
                bgcolor={ft.ControlState.DEFAULT: c.surface},
                shape=ft.RoundedRectangleBorder(radius=sp.radius_sm),
                side={ft.ControlState.DEFAULT: ft.BorderSide(1, c.border)},
                overlay_color=c.surface_alt,
                padding=ft.Padding.all(sp.sm),
            ),
            on_click=self._handle_toggle_theme,
        )

    # ── Handlers ─────────────────────────────────────────────

    def _handle_login(self, e):
        """Valida y simula el login."""
        email = self._email_field.value.strip() if self._email_field.value else ""
        password = self._password_field.value.strip() if self._password_field.value else ""

        # Validación básica
        if not email or "@" not in email:
            self._show_error("Introduce un correo válido.")
            return
        if len(password) < 6:
            self._show_error("La contraseña debe tener al menos 6 caracteres.")
            return

        self._hide_error()
        self._set_loading(True)

        # Aquí iría tu lógica de autenticación real.
        # Por ahora simulamos con un callback.
        if self.on_login:
            self.on_login(email, password)
        else:
            # Demo: muestra un snackbar de éxito
            self._page.snack_bar = ft.SnackBar(
                content=ft.Text(f"¡Bienvenido, {email}!"),
                bgcolor=self.theme.c.success,
            )
            self._page.snack_bar.open = True
            self._page.update()

        self._set_loading(False)

    def _handle_forgot(self, e):
        self._page.snack_bar = ft.SnackBar(
            content=ft.Text("Se envió un enlace de recuperación."),
            bgcolor=self.theme.c.warning,
        )
        self._page.snack_bar.open = True
        self._page.update()

    def _handle_register(self, e):
        if self.on_register:
            self.on_register()

    def _handle_google(self, e):
        self._page.snack_bar = ft.SnackBar(
            content=ft.Text("Login con Google — pendiente de integración."),
        )
        self._page.snack_bar.open = True
        self._page.update()

    def _handle_apple(self, e):
        self._page.snack_bar = ft.SnackBar(
            content=ft.Text("Login con Apple — pendiente de integración."),
        )
        self._page.snack_bar.open = True
        self._page.update()

    def _handle_toggle_theme(self, e):
        self.theme = toggle_theme(self._page, self.theme)
        self._render()

    def _on_resize(self, e):
        self._page.update()

    # ── Helpers de estado ────────────────────────────────────

    def _show_error(self, msg: str):
        if self._error_text:
            self._error_text.value = msg
            self._error_text.visible = True
            self._page.update()

    def _hide_error(self):
        if self._error_text:
            self._error_text.visible = False
            self._page.update()

    def _set_loading(self, loading: bool):
        self._loading = loading
        t = self.theme
        if self._login_btn:
            if loading:
                self._login_btn.content = ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[ft.ProgressRing(width=18, height=18, color=t.c.accent_on, stroke_width=2)],
                )
            else:
                self._login_btn.content = ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.Text(
                            "Iniciar sesión",
                            size=t.ty.size_base,
                            weight=t.ty.semibold,
                            color=t.c.accent_on,
                            font_family=t.ty.family,
                        ),
                    ],
                )
            self._page.update()


# ══════════════════════════════════════════════════════════════
#  ENTRY POINT (prueba standalone)
# ══════════════════════════════════════════════════════════════

def main(page: ft.Page):
    page.title = "Habitly — Login"
    page.window_width = 480
    page.window_height = 780
    page.window_resizable = True

    LoginPage(
        page=page,
        theme=LIGHT_THEME,
        on_login=lambda email, pw: print(f"Login: {email}"),
        on_register=lambda: print("Ir a registro"),
    )


if __name__ == "__main__":
    ft.run(main)