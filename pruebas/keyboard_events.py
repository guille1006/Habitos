import flet as ft
from flet import Page, Text, KeyboardEvent, Button, Row

def main(page: Page) -> None:
    page.title = "Keyboard"
    page.spacing = 30 
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"

    # Creando las vistas del texto 
    key: Text = Text(value="key", size=10)
    shift: Text = Text(value="Shift", color="red")
    ctrl: Text = Text(value="Ctrl", color="black")

    # Manejo de keyboard events
    def on_keyboard(e: KeyboardEvent) -> None:
        key.value = e.key 
        shift.visible = e.shift 
        ctrl.visible = e.ctrl 
        print(e.data)
        page.update()

    page.on_keyboard_event = on_keyboard 
    page.add(Row(controls=[key, shift, ctrl]))
if __name__ == "__main__":
    ft.run(main, view=ft.AppView.WEB_BROWSER)