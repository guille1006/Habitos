import flet as ft

from ..models.habit_data import HabitData
from ..utils.theme import AppTheme, apply_theme, LIGHT_THEME


# ══════════════════════════════════════════════════════════════
#  EMOJIS PREDEFINIDOS
# ══════════════════════════════════════════════════════════════

HABIT_EMOJIS = [
    "📚", "🏃", "💧", "🧘", "✍️", "🎯", "💪", "🥗",
    "😴", "🎨", "🎵", "🧹", "💊", "🌿", "🧠", "☀️",
    "🚴", "🍎", "📝", "🛁", "🙏", "💻", "📵", "❤️",
]


# ══════════════════════════════════════════════════════════════
#  DIALOG
# ══════════════════════════════════════════════════════════════

class EditHabitDialog(ft.AlertDialog):
    """
    AlertDialog para editar un HabitData existente.

    USO:
        def on_edit(habit: HabitData):
            dialog = EditHabitDialog(
                page=page,
                habit=habit,
                theme=LIGHT_THEME,
                on_save=lambda updated: print(updated),
            )
            dialog.open_dialog()
    """

    def __init__(
        self,
        page: ft.Page,
        habit: HabitData,
        theme: AppTheme,
        on_save=None,           # callback(HabitData) → se llama al guardar
    ):
        super().__init__()

        self._page       = page
        self.habit      = habit

        self.t          = theme
        self.c          = theme.c
        self.sp         = theme.sp
        self.ty         = theme.ty

        self.on_save    = on_save

        # Estado interno del formulario
        self._selected_icon = habit.icon
        self._reminder_text = habit.reminder_time or ""

        # Construye el contenido y configura el AlertDialog
        self._build_dialog()

    # ──────────────────────────────────────────────────────────
    #  CONSTRUCCIÓN
    # ──────────────────────────────────────────────────────────

    def _build_dialog(self):
        c  = self.c
        sp = self.sp
        ty = self.ty

        # ── Campo nombre ──────────────────────────────────────
        self._name_field = ft.TextField(
            value=self.habit.name,
            # label="Nombre del hábito",
            label_style=ft.TextStyle(color=c.text_secondary, size=ty.size_sm),
            text_style=ft.TextStyle(color=c.text_primary, size=ty.size_base),
            bgcolor=c.surface_alt,
            border_color=c.border,
            focused_border_color=c.accent,
            border_radius=sp.radius_md,
            height=sp.input_height,
            content_padding=ft.Padding.symmetric(horizontal=sp.md, vertical=sp.sm),
            cursor_color=c.accent,
        )

        # ── Grid de emojis ────────────────────────────────────
        self._emoji_grid = self._build_emoji_grid()

        # ── Campo recordatorio ────────────────────────────────
        self._reminder_field = ft.TextField(
            value=self._reminder_text,
            label="(HH:MM)",
            label_style=ft.TextStyle(color=c.text_secondary, size=ty.size_sm),
            text_style=ft.TextStyle(color=c.text_primary, size=ty.size_base),
            hint_text="Ej: 08:30",
            hint_style=ft.TextStyle(color=c.text_disabled, size=ty.size_sm),
            bgcolor=c.surface_alt,
            border_color=c.border,
            focused_border_color=c.accent,
            border_radius=sp.radius_md,
            height=sp.input_height,
            content_padding=ft.Padding.symmetric(horizontal=sp.md, vertical=sp.sm),
            cursor_color=c.accent,
            suffix=ft.IconButton(
                icon=ft.Icons.ACCESS_TIME_ROUNDED,
                icon_color=c.text_secondary,
                icon_size=18,
                on_click=self._open_time_picker,
                tooltip="Seleccionar hora",
            ),
        )

        # ── Errores ───────────────────────────────────────────
        self._error_text = ft.Text(
            "",
            color=c.error,
            size=ty.size_xs,
            visible=False,
        )

        # ── Contenido completo del dialog ─────────────────────
        dialog_content = ft.Container(
            width=360,
            content=ft.Column(
                controls=[
                    # Nombre
                    self._section_label("Nombre"),
                    self._name_field,

                    ft.Container(height=sp.sm),  # separador

                    # Icono
                    self._section_label("Icono"),
                    self._emoji_grid,

                    ft.Container(height=sp.sm),  # separador

                    # Recordatorio
                    self._section_label("Recordatorio"),
                    self._reminder_field,

                    # Error
                    self._error_text,
                ],
                spacing=sp.xs,
                tight=True,
                scroll=ft.ScrollMode.AUTO,
            ),
            padding=ft.Padding.only(top=sp.xs),
        )

        # ── Configura el AlertDialog ──────────────────────────
        self.modal            = True
        self.bgcolor          = c.surface
        self.shape            = ft.RoundedRectangleBorder(radius=sp.radius_lg)
        self.title            = self._build_title()
        self.content          = dialog_content
        self.actions          = self._build_actions()
        self.actions_alignment = ft.MainAxisAlignment.END

    # ──────────────────────────────────────────────────────────
    #  SUB-CONSTRUCTORES
    # ──────────────────────────────────────────────────────────

    def _section_label(self, text: str) -> ft.Text:
        return ft.Text(
            text,
            size=self.ty.size_xs,
            weight=self.ty.semibold,
            color=self.c.text_secondary,
        )

    def _build_title(self) -> ft.Row:
        c, sp, ty = self.c, self.sp, self.ty
        return ft.Row(
            controls=[
                ft.Container(
                    content=ft.Text(self.habit.icon, size=22),
                    bgcolor=ft.Colors.with_opacity(0.12, c.accent),
                    border_radius=sp.radius_sm,
                    width=40,
                    height=40,
                    alignment=ft.Alignment.CENTER,
                ),
                ft.Text(
                    "Editar hábito",
                    size=ty.size_md,
                    weight=ty.semibold,
                    color=c.text_primary,
                ),
            ],
            spacing=sp.sm,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def _build_emoji_grid(self) -> ft.Container:
        c, sp = self.c, self.sp

        self._emoji_buttons = {}  # guardamos referencia a cada botón

        grid = ft.GridView(
            runs_count=8,
            max_extent=40,
            spacing=sp.xs,
            run_spacing=sp.xs,
            height=104,
        )

        for emoji in HABIT_EMOJIS:
            is_selected = emoji == self._selected_icon
            btn = ft.Container(
                content=ft.Text(emoji, size=20),
                width=36,
                height=36,
                border_radius=sp.radius_sm,
                alignment=ft.Alignment.CENTER,
                bgcolor=ft.Colors.with_opacity(0.15, c.accent) if is_selected else c.surface_alt,
                border=ft.Border.all(
                    1.5 if is_selected else 0,
                    c.accent if is_selected else "transparent",
                ),
                on_click=lambda e, em=emoji: self._select_emoji(em),
                animate=ft.Animation(150, ft.AnimationCurve.EASE_OUT),
            )
            self._emoji_buttons[emoji] = btn
            grid.controls.append(btn)

        return ft.Container(
            content=grid,
            bgcolor=c.surface_alt,
            border_radius=sp.radius_md,
            border=ft.Border.all(1, c.border),
            padding=sp.sm,
        )

    def _build_actions(self) -> list:
        c, sp, ty = self.c, self.sp, self.ty

        cancel_btn = ft.TextButton(
            content="Cancelar",
            style=ft.ButtonStyle(
                color=c.text_secondary,
                overlay_color=ft.Colors.with_opacity(0.06, c.text_secondary),
            ),
            on_click=self._on_cancel,
        )

        save_btn = ft.Button(
            content="Guardar",
            style=ft.ButtonStyle(
                bgcolor={
                    ft.ControlState.DEFAULT: c.accent,
                    ft.ControlState.HOVERED: c.accent_soft,
                },
                color=c.accent_on,
                shape=ft.RoundedRectangleBorder(radius=sp.radius_sm),
                elevation={"default": 0},
                padding=ft.Padding.symmetric(horizontal=sp.md, vertical=sp.sm),
            ),
            on_click=self._on_save,
        )

        return [cancel_btn, save_btn]

    # ──────────────────────────────────────────────────────────
    #  INTERACCIONES
    # ──────────────────────────────────────────────────────────

    def _select_emoji(self, emoji: str):
        """Actualiza el emoji seleccionado y refresca el grid."""
        c, sp = self.c, self.sp

        # Deselecciona el anterior
        if self._selected_icon in self._emoji_buttons:
            prev = self._emoji_buttons[self._selected_icon]
            prev.bgcolor = c.surface_alt
            prev.border  = ft.Border.all(0, "transparent")
            prev.update()

        # Selecciona el nuevo
        self._selected_icon = emoji
        curr = self._emoji_buttons[emoji]
        curr.bgcolor = ft.Colors.with_opacity(0.15, c.accent)
        curr.border  = ft.Border.all(1.5, c.accent)
        curr.update()

    def _open_time_picker(self, e):
        """Abre el TimePicker nativo de Flet."""
        picker = ft.TimePicker(
            confirm_text="Confirmar",
            cancel_text="Cancelar",
            help_text="Hora del recordatorio",
            on_change=self._on_time_selected,
        )
        self._page.overlay.append(picker)
        picker.open = True
        self._page.update()

    def _on_time_selected(self, e: ft.DatePicker):
        """Rellena el campo con la hora seleccionada."""
        if e.control.value:
            t = e.control.value
            formatted = f"{t.hour:02d}:{t.minute:02d}"
            self._reminder_field.value = formatted
            self._reminder_text = formatted
            self._reminder_field.update()

    def _validate(self) -> bool:
        """Devuelve True si el formulario es válido."""
        name = self._name_field.value.strip()

        if not name:
            self._show_error("El nombre no puede estar vacío.")
            return False

        reminder = self._reminder_field.value.strip()
        if reminder:
            parts = reminder.split(":")
            valid_format = (
                len(parts) == 2
                and parts[0].isdigit()
                and parts[1].isdigit()
                and 0 <= int(parts[0]) <= 23
                and 0 <= int(parts[1]) <= 59
            )
            if not valid_format:
                self._show_error("Formato de hora inválido. Usa HH:MM.")
                return False

        self._hide_error()
        return True

    def _show_error(self, msg: str):
        self._error_text.value   = msg
        self._error_text.visible = True
        self._error_text.update()

    def _hide_error(self):
        self._error_text.visible = False
        self._error_text.update()

    def _on_save(self, e):
        if not self._validate():
            return

        reminder = self._reminder_field.value.strip() or None

        updated = HabitData(
            name=self._name_field.value.strip(),
            icon=self._selected_icon,
            streak=self.habit.streak,        # streak no se edita aquí
            frequency=self.habit.frequency,  # frequency no se edita aquí
            reminder_time=reminder,
            completed=self.habit.completed,
        )

        self.open = False
        self._page.update()

        if self.on_save:
            self.on_save(updated)

    def _on_cancel(self, e):
        self.open = False
        self._page.update()

    # ──────────────────────────────────────────────────────────
    #  API PÚBLICA
    # ──────────────────────────────────────────────────────────

    def open_dialog(self):
        """Añade el dialog al overlay y lo abre."""
        if self not in self._page.overlay:
            self._page.overlay.append(self)
        self.open = True
        self._page.update()

if __name__ == "__main__":
    def main(page: ft.Page):
        page.title = "Preview — EditHabitDialog"
        page.window.width = 420
        page.window.height = 720
    
        apply_theme(page, LIGHT_THEME)
    
        t = LIGHT_THEME
        c = t.c
        sp = t.sp
        ty = t.ty
    
        # ── Hábito de prueba ──────────────────────────────────────
        habit = HabitData(
            name="Leer 30 minutos",
            icon="📚",
            streak=7,
            frequency="Diario",
            reminder_time="21:00",
            completed=False,
        )
    
        # ── Texto de resultado (muestra el HabitData guardado) ────
        result_text = ft.Text(
            "Pulsa el botón para abrir el dialog.",
            size=ty.size_sm,
            color=c.text_secondary,
            text_align=ft.TextAlign.CENTER,
        )
    
        # ── Callback: se ejecuta al pulsar "Guardar" ──────────────
        def on_save(updated: HabitData):
            result_text.value = (
                f"✅ Guardado\n"
                f"Nombre: {updated.name}\n"
                f"Icono:  {updated.icon}\n"
                f"Hora:   {updated.reminder_time or '—'}"
            )
            result_text.color = c.success
            result_text.update()
    
        # ── Callback: abre el dialog ──────────────────────────────
        def open_dialog(e):
            dialog = EditHabitDialog(
                page=page,
                habit=habit,
                theme=t,
                on_save=on_save,
            )
            dialog.open_dialog()
    
        # ── UI de la pantalla de preview ──────────────────────────
        page.add(
            ft.Container(
                expand=True,
                alignment=ft.Alignment.CENTER,
                bgcolor=c.bg,
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=sp.lg,
                    controls=[
                        # Icono decorativo
                        ft.Container(
                            content=ft.Text("📚", size=40),
                            bgcolor=ft.Colors.with_opacity(0.12, c.accent),
                            border_radius=sp.radius_lg,
                            width=72,
                            height=72,
                            alignment=ft.Alignment.CENTER,
                        ),
    
                        # Título
                        ft.Text(
                            "EditHabitDialog",
                            size=ty.size_lg,
                            weight=ty.semibold,
                            color=c.text_primary,
                        ),
    
                        # Subtítulo
                        ft.Text(
                            "Preview del componente",
                            size=ty.size_sm,
                            color=c.text_secondary,
                        ),
    
                        # Botón que abre el dialog
                        ft.Button(
                            content="Abrir dialog de edición",
                            on_click=open_dialog,
                            style=ft.ButtonStyle(
                                bgcolor={
                                    ft.ControlState.DEFAULT: c.accent,
                                    ft.ControlState.HOVERED: c.accent_soft,
                                },
                                color=c.accent_on,
                                shape=ft.RoundedRectangleBorder(radius=sp.radius_sm),
                                elevation={"default": 0},
                                padding=ft.Padding.symmetric(
                                    horizontal=sp.lg, vertical=sp.sm + sp.xs
                                ),
                            ),
                        ),
    
                        # Resultado tras guardar
                        ft.Container(
                            content=result_text,
                            bgcolor=c.surface,
                            border_radius=sp.radius_md,
                            padding=sp.md,
                            border=ft.Border.all(1, c.border),
                            width=260,
                            visible=True,
                        ),
                    ],
                ),
            )
        )
    
    
    ft.run(main)