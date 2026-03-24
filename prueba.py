import flet as ft

class HabitCard(ft.Container):
    def __init__(
        self,
        color: str = ft.Colors.BLUE,
        completed: bool = False,
        on_complete=None,
        on_edit=None,
    ):
        super().__init__(...)
        self.color = color
        self.completed = completed
        self.on_complete = on_complete
        self.on_edit = on_edit

        self._drag_offset = 0.0
        self._SWIPE_THRESHOLD = 80      # px para confirmar completado
        self._EDIT_THRESHOLD = -60      # px para revelar editar

    # ── Drag handlers ──────────────────────────────────────────
    def _on_drag_update(self, e: ft.DragUpdateEvent):
        self._drag_offset += e.global_delta.x
        self._drag_offset = max(-80, min(120, self._drag_offset))
        self._card_container.offset = ft.Offset(
            self._drag_offset / 400, 0
        )
        self._update_background_hint()
        self.update()

    def _update_background_hint(self):
        # Fondo verde al deslizar derecha
        self._bg_right.opacity = min(1.0, self._drag_offset / self._SWIPE_THRESHOLD) if self._drag_offset > 0 else 0
        # Fondo naranja al deslizar izquierda
        self._bg_left.opacity = min(1.0, abs(self._drag_offset) / abs(self._EDIT_THRESHOLD)) if self._drag_offset < 0 else 0

    def _on_drag_end(self, e: ft.DragEndEvent):
        if self._drag_offset >= self._SWIPE_THRESHOLD:
            self._mark_complete()
        elif self._drag_offset <= self._EDIT_THRESHOLD:
            self._show_edit()

        # Vuelve a la posición original
        self._drag_offset = 0.0
        self._card_container.offset = ft.Offset(0, 0)
        self._bg_right.opacity = 0
        self._bg_left.opacity = 0
        self.update()
    
    # ── Build ──────────────────────────────────────────────────
    def build(self):
def main(page: ft.Page) -> None:
    page.title = "Keyboard"
    page.spacing = 30 
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"
    page.bgcolor = "white"