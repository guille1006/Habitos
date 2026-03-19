import flet as ft 
from flet import TextField

def main(page: ft.Page) -> None:
    page.title = "Hábitos"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.theme_mode = "dark"

    text_number: TextField = TextField(value="0", text_align=ft.TextAlign.RIGHT, width=100)

    def decrement(e: ft.ControlEvent) -> None:
        text_number.value = str(int(text_number.value) - 1)
        page.update()

    def increment(e: ft.ControlEvent) -> None:
        text_number.value = str(int(text_number.value) + 1)
        page.update()

    page.add(
        ft.Row(
            [ft.IconButton(ft.Icons.REMOVE, on_click=decrement), 
             text_number, 
             ft.IconButton(ft.Icons.ADD, on_click=increment)
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
    )

if __name__ == "__main__":
    ft.run(target=main, view=ft.AppView.WEB_BROWSER)