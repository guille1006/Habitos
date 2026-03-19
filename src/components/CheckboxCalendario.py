import flet as ft 
from flet import Page, Row, Column, Checkbox, Container 

import calendar
from datetime import datetime
from typing import List


class CheckboxCalendario():
    def __init__(self, current_day: List) -> None:
        self.current_day = datetime(*current_day)
        self.calendar_month = calendar.monthcalendar(self.current_day.year, self.current_day.month)

        self.colors = {True: "blue", False: "white"}

        self.row_weeks = []
        for week in self.calendar_month:
            controls_week = [
                Container(
                    content=ft.Text(str(day)),
                    width=40,
                    height=40,
                    border=ft.border.all(1, "black"),
                    on_click=self.on_click_action,
                    data=False,
                    bgcolor=self.colors[False]
                ) if day != 0 else Container(width=40, height=40)
                for day in week
            ]
            self.row_weeks.append(Row(controls=controls_week,
                             spacing = 5))  
        self.day_value = {}
        self.day_ticked()
        

    def on_click_action(self, e) -> None:
        e.control.data = not e.control.data
        self.modificar_color(e)
        self.day_ticked()
        e.control.update()

    def modificar_color(self, e) -> None:
        e.control.bgcolor = self.colors[e.control.data]

    def build(self) -> Container:
                  
        return Container(content=Column(controls=self.row_weeks),
                         border=ft.Border.all(2, "black"),  # grosor y color
                         padding=10,  # opcional, para que no quede pegado 
                         width = 350,
                         expand=False
                         )

    def day_ticked(self) -> None:
        for week in self.row_weeks:
            for day in week.controls:
                if hasattr(day, "content") and hasattr(day.content, "value"):
                    self.day_value[day.content.value] = day.data

        print(self.day_value)