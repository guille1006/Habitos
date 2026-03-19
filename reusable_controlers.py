import flet as ft 
from flet import Text, Row, Page, ControlEvent

class IncrementCounter():
    def __init__(self, text:str, start_number: int=0)-> None:
        self.text = text
        self.counter = start_number
        self.text_number: Text = Text(value=str(self.counter), size=40)

    def increment(self, e: ControlEvent) -> None:
        self.counter = str(int(self.text_number.value) + 1)
        

def main(page: Page) -> None: 
    page.title = 