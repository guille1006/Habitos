import flet as ft 

class MovingItem():
    def __init__(
            self,
            parent_width: float,
            parent_height: float,
            color: str = ft.Colors.BLUE        
            ) -> None:
        self.x = 0.0
        self.y = 0.0 
        self._color = color 
        self._square: ft.Container | None = None
        self._parent_width = parent_width
        self._parent_height = parent_height

    def on_drag_update(self, e: ft.DragUpdateEvent) -> None:
        self.x += e.local_delta.x /self._parent_width
        self.y += e.local_delta.y /self._parent_height
        e.control.offset = ft.Offset(self.x, self.y)
        e.control.update()


    def build(self) -> ft.GestureDetector:
        self._square = ft.Container(
            width=30,
            height=10,
            bgcolor=self._color,
            border_radius=16,
            offset=ft.Offset(0, 0),                          # posición inicial
            animate_offset=ft.Animation(duration=0, curve=ft.AnimationCurve.LINEAR)  # suaviza
        )

        gesture = ft.GestureDetector(
            mouse_cursor=ft.MouseCursor.MOVE,
            content=self._square,
            on_pan_update=self.on_drag_update,  # pan captura x e y simultáneo
        )

        return gesture
    
        
def main(page: ft.Page) -> None:
    page.title = "Keyboard"
    page.spacing = 30 
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"
    page.bgcolor = "white"
    page.width = 500
    page.height = 400


    calendario = MovingItem(parent_width=300,
                            parent_height=200)
    contenedor = ft.Container(
        width=300,
        height=200,
        border=ft.Border.all(1, ft.Colors.RED),
        border_radius=10,
        bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
        content=calendario.build()
    )
    page.add(contenedor)

if __name__ == "__main__":
    ft.run(main, view=ft.AppView.WEB_BROWSER)

