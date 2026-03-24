import flet as ft

class HabitCard(ft.Container):
    def __init__(
        self,
        name: str,
        icon: str,
        streak: int,
        frequency: str,
        reminder_time: str | None,
        color: str = ft.Colors.BLUE,
        completed: bool = False,
        on_complete=None,
        on_edit=None,
    ):
        super().__init__(...)
        self.name = name
        self.icon = icon
        self.streak = streak
        self.frequency = frequency
        self.reminder_time = reminder_time
        self.color = color
        self.completed = completed
        self.on_complete = on_complete
        self.on_edit = on_edit

        self._drag_offset = 0.0
        self._SWIPE_THRESHOLD = 80      # px para confirmar completado
        self._EDIT_THRESHOLD = -60      # px para revelar editar

    # ── Drag handlers ──────────────────────────────────────────

    def _on_drag_update(self, e: ft.DragUpdateEvent):
        # Limita el arrastre: derecha hasta 120px, izquierda hasta -80px
        self._drag_offset += e.local_delta.x
        self._drag_offset = max(-80, min(120, self._drag_offset))
        self._card_container.offset = ft.Offset(
            self._drag_offset / 400, 0
        )
        self._update_background_hint()
        self.gesture.update()

    def _on_drag_end(self, e: ft.DragEndEvent):
        if self._drag_offset >= self._SWIPE_THRESHOLD:
            print("Completado")
        elif self._drag_offset <= self._EDIT_THRESHOLD:
            print("Editar")

        # Vuelve a la posición original
        self._drag_offset = 0.0
        self._card_container.offset = ft.Offset(0, 0)
        self._bg_right.opacity = 0
        self._bg_left.opacity = 0
        self.gesture.update()

    def _update_background_hint(self):
        # Fondo verde al deslizar derecha
        self._bg_right.opacity = min(1.0, self._drag_offset / self._SWIPE_THRESHOLD) if self._drag_offset > 0 else 0
        # Fondo naranja al deslizar izquierda
        self._bg_left.opacity = min(1.0, abs(self._drag_offset) / abs(self._EDIT_THRESHOLD)) if self._drag_offset < 0 else 0

    # ── Build ──────────────────────────────────────────────────
    def build(self):
        # Fondo que aparece al deslizar a la derecha (completar)
        self._bg_right = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(ft.Icons.CHECK_CIRCLE_ROUNDED, color=ft.Colors.WHITE, size=28),
                    ft.Text("Completado", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                ],
                spacing=8,
            ),
            bgcolor=ft.Colors.GREEN_400,
            border_radius=16,
            padding=ft.Padding.symmetric(horizontal=20),
            alignment=ft.Alignment(-1, 0),
            opacity=0,
            animate_opacity=150,
        )

        # Fondo que aparece al deslizar a la izquierda (editar)
        self._bg_left = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Text("Editar", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                    ft.Icon(ft.Icons.EDIT_ROUNDED, color=ft.Colors.WHITE, size=28),
                ],
                spacing=8,
                alignment=ft.MainAxisAlignment.END,
            ),
            bgcolor=ft.Colors.ORANGE_400,
            border_radius=16,
            padding=ft.Padding.symmetric(horizontal=20),
            alignment=ft.Alignment(1, 0),
            opacity=0,
            animate_opacity=150,
        )
        # Contenido principal de la tarjeta
        icon_container = ft.Container(
            content=ft.Text(self.icon, size=28),
            bgcolor=ft.Colors.with_opacity(0.15, self.color),
            border_radius=12,
            width=52,
            height=52,
            alignment=ft.Alignment(0, 0),
        )

        streak_badge = ft.Row(
            controls=[
                ft.Icon(ft.Icons.LOCAL_FIRE_DEPARTMENT_ROUNDED, color=ft.Colors.ORANGE_400, size=14),
                ft.Text(f"{self.streak} días", size=12, color=ft.Colors.SECONDARY),
            ],
            spacing=2,
        )

        frequency_badge = ft.Container(
            content=ft.Text(self.frequency, size=11, color=self.color, weight=ft.FontWeight.W_500),
            bgcolor=ft.Colors.with_opacity(0.12, self.color),
            border_radius=20,
            padding=ft.Padding.symmetric(horizontal=8, vertical=2),
        )

        reminder_row = ft.Row(
            controls=[
                ft.Icon(ft.Icons.NOTIFICATIONS_NONE_ROUNDED, size=12, color=ft.Colors.SECONDARY),
                ft.Text(self.reminder_time, size=11, color=ft.Colors.SECONDARY),
            ],
            spacing=4,
            visible=self.reminder_time is not None,
        )

        info_column = ft.Column(
            controls=[
                ft.Text(
                    self.name,
                    size=15,
                    weight=ft.FontWeight.W_600,
                    color=ft.Colors.ON_SURFACE,
                ),
                ft.Row(controls=[streak_badge, frequency_badge], spacing=8),
                reminder_row,
            ],
            spacing=4,
            expand=True,
        )

        check_icon = ft.Icon(
            ft.Icons.CHECK_CIRCLE_ROUNDED if self.completed else ft.Icons.RADIO_BUTTON_UNCHECKED_ROUNDED,
            color=self.color if self.completed else ft.Colors.with_opacity(0.3, ft.Colors.ON_SURFACE),
            size=26
        )

        card_content = ft.Container(
            content=ft.Row(
                controls=[icon_container, info_column, check_icon],
                spacing=14,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor=ft.Colors.with_opacity(0.05 if self.completed else 0, ft.Colors.ON_SURFACE)
            if self.completed
            else ft.Colors.SURFACE,
            border_radius=16,
            padding=ft.Padding.symmetric(horizontal=16, vertical=14),
            border=ft.Border.all(
                1,
                ft.Colors.with_opacity(0.3, self.color) if self.completed else ft.Colors.with_opacity(0.08, ft.Colors.ON_SURFACE),
            ),
            animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT)
        )

        self._card_container = ft.Container(
            content=card_content,
            offset=ft.Offset(0, 0),
            animate_offset=ft.Animation(300, ft.AnimationCurve.EASE_OUT)
        )

        self.gesture = ft.GestureDetector(
            content=self._card_container,
            on_horizontal_drag_update=self._on_drag_update,
            on_horizontal_drag_end=self._on_drag_end
        )

        return ft.Stack(
            controls=[self._bg_right, self._bg_left, self.gesture],
            height=84,
        )