import flet as ft
from flet import (TextField,
                  InputBorder,
                  Page,
                  ControlEvent,
                  KeyboardEvent,
                  Row)

class TextEditor():
    def __init__(self) -> None:
        self.text = ""
        self.textfield = TextField(multiline=True,
                                   autofocus=True,
                                   border=InputBorder.NONE,
                                   min_lines=40, 
                                   on_change=self.add_text,
                                   cursor_color="yellow")
        self.save_document = "save.txt"

    def add_text(self, e: KeyboardEvent):
        self.text += e.data 
        self.save_change() # Seria mejor guardarlo cada 5 segundos

    def save_change(self) -> None:
        with open(self.save_document, "w") as f:
            f.write(self.textfield.value)

    def read_text(self) -> str | None:
        try: 
            with open(self.save_document, "r") as f:
                return f.read() 
        except FileNotFoundError:
            self.textfield.hint_text = "Bienvenido"

    def build(self) -> TextField:
        self.textfield.value = self.read_text()
        return self.textfield

def main(page: Page) -> None: 
    page.title = "Notepad"
    page.vertical_alignment = "center"
    page.theme_mode = "dark"
    page.scroll = True 

    text_editor = TextEditor()
    page.add(text_editor.build())

if __name__ == "__main__":
    ft.run(main)
