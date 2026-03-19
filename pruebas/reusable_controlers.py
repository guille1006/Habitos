import flet as ft 
from flet import Text, Row, Page, ControlEvent, Button

class IncrementCounter:
    def __init__(self, text:str, start_number: int=0)-> None:
        self.text = text
        self.counter = start_number
        self.text_number: Text = Text(value=str(self.counter), size=40)

    def increment(self, e: ControlEvent) -> None:
        self.counter = str(int(self.text_number.value) + 1)
        self.text_number.value = str(self.counter)
        e.control.page.update()  # Actualiza la página
        
    def build(self) -> Row:
        return Row(controls=[Button(self.text, on_click=self.increment), self.text_number])
    

def main(page: Page) -> None: 
    page.title = "App"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.theme_mode = "dark"

    counter = IncrementCounter("Buenas")  # Crear instancia
    page.add(counter.build())      



if __name__ == "__main__":
    ft.run(main, view=ft.AppView.WEB_BROWSER)