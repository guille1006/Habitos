import flet as ft
from dataclasses import dataclass

from ..utils.theme import apply_theme, LIGHT_THEME


@dataclass
class HabitData:
    name: str
    icon: str
    streak: int
    frequency: str
    reminder_time: str | None = None
    completed: bool = False


class HabitCard(ft.Container):
    def __init__(
        self,
        habit: HabitData,
        theme: ft.Theme,
        on_complete=None,
        on_edit=None,
    ):
        super().__init__()

        self.habit = habit
        self.app_theme = theme

        self.t = theme
        self.c = theme.c
        self.sp = theme.sp
        self.ty = theme.ty

        self.on_complete = on_complete
        self.on_edit = on_edit

        self._drag_offset = 0.0
        self._SWIPE_THRESHOLD = 80
        self._EDIT_THRESHOLD = -60

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

    # ── Background Creation ────────────────────────────────────
    def _bg_card(self, 
                 text: str, 
                 color: ft.Colors, 
                 icon: ft.Icons, 
                 alignment: ft.Alignment) -> ft.Container:
        """
        Funcion que devuleve el fondo de las cartas
        """
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(icon, # Icono
                            color=self.c.text_primary, 
                            size=self.ty.size_md),
                    ft.Text(text, # Texto
                            color=self.c.text_primary,
                            font_family=self.ty.family,
                            size=self.ty.size_base,
                            weight=self.ty.bold),
                ],
                spacing=self.sp.md,
                alignment=alignment
            ),
            expand=True,
            alignment=ft.Alignment(0,0),
            bgcolor=color,      # Aqui pongo el color del fondo
            border_radius= self.sp.radius_md,
            padding=ft.Padding.symmetric(horizontal=20),
            opacity=0,
            animate_opacity=150,
        )
    # ── Build ──────────────────────────────────────────────────
    def build(self):
        # Fondo que aparece al deslizar a la derecha (completar)
        self._bg_right = self._bg_card(text="Completado",
                                       color=ft.Colors.GREEN,
                                       icon=ft.Icons.CHECK_CIRCLE_OUTLINE_ROUNDED,
                                       alignment=ft.MainAxisAlignment.START)
        
        # Fondo que aparece al deslizar a la izquierda (editar)
        self._bg_left = self._bg_card(text="Editar",
                                       color=ft.Colors.YELLOW,
                                       icon=ft.Icons.EDIT_ROUNDED,
                                       alignment=ft.MainAxisAlignment.END)

        
        card_content = ft.Container(
            expand=True,
            alignment=ft.Alignment.CENTER,
            content=ft.Text(
                self.habit.name,
                weight=ft.FontWeight.W_600,
                color=ft.Colors.ON_SURFACE,
            ),
            bgcolor=ft.Colors.with_opacity(0.05 if self.habit.completed else 0, ft.Colors.ON_SURFACE)
            if self.habit.completed
            else ft.Colors.SURFACE,
            border_radius=16,
            padding=ft.Padding.symmetric(horizontal=16, vertical=14),
            border=ft.Border.all(
                1,
                ft.Colors.with_opacity(0.3, self.c.accent)
                if self.habit.completed
                else ft.Colors.with_opacity(0.08, ft.Colors.ON_SURFACE),
            ),
            animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
        )

        self._card_container = ft.Container(
            expand=True,
            content=card_content,
            offset=ft.Offset(0, 0),
            animate_offset=ft.Animation(300, ft.AnimationCurve.EASE_OUT)
        )

        self.gesture = ft.GestureDetector(
            expand=True,
            content=self._card_container,
            on_horizontal_drag_update=self._on_drag_update,
            on_horizontal_drag_end=self._on_drag_end,
            # mouse_cursor=ft.MouseCursor.MOVE
        )

        return ft.Stack(
            controls=[self._bg_right, self._bg_left, self.gesture],
            height=50,
        )
    

if __name__ == "__main__":
    def main(page: ft.Page) -> None:
        apply_theme(page=page, app_theme=LIGHT_THEME)

        habit_data = HabitData(name="Leer 30 minutos",
        icon="📚",
        streak=7,
        frequency="Diario",
        reminder_time="21:00",
        completed=False)

        card = HabitCard(
        habit=habit_data,
        theme=LIGHT_THEME,
        on_complete=lambda: print("completado"),
        on_edit=lambda: print("editar"),
        )

        page.add(card.build())

    ft.run(main)

"""
Para un futuro poner mas contenido a la carta:
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
            bgcolor=self.c.bg,
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
"""
