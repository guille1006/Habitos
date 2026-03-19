import math

import flet as ft 
from flet import Page, Row, Column, Checkbox, Container
import flet.canvas as cv

import calendar
from datetime import datetime
from typing import List


class ProgressRing():
    def __init__(self, value: float, size: int = 120, stroke_width: int = 10):
        self.value = value
        self.size = size 
        self.stroke_width = stroke_width
        self.color = ft.Colors.GREEN

    def build(self):
        cx = self.size/2
        cy = self.size/2
        radius = (self.size / 2) - (self.stroke_width / 2)

        start_angle = math.pi/2
        progress_angle = math.pi 

        ring = cv.Canvas(
            shapes=[
                # Arco de fondo
                cv.Arc(
                    x = cx - radius,
                    y = cy - radius,
                    width = radius * 2,
                    height = radius * 2,
                    sweep_angle = 2 * math.pi,
                    paint = ft.Paint(
                        color=ft.Colors.with_opacity(0.15, ft.Colors.ON_SURFACE),
                        stroke_width=self.stroke_width,
                        style=ft.PaintingStyle.STROKE,
                        stroke_cap=ft.StrokeCap.ROUND,
                    ),
                ),
                # Arco de progreso
                cv.Arc(
                    x=cx - radius,
                    y=cy - radius,
                    width=radius * 2,
                    height=radius * 2,
                    start_angle=start_angle,
                    sweep_angle=progress_angle,
                    paint=ft.Paint(
                        color=self.color,
                        stroke_width=self.stroke_width,
                        style=ft.PaintingStyle.STROKE,
                        stroke_cap=ft.StrokeCap.ROUND,
                    ),
                ),
            ],
            width=self.size,
            height=self.size,
        )

        percentage_text = ft.Text(
            value=f"{int(self.value * 100)}%",
            size=self.size * 0.22,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.ON_SURFACE,
        )

        return ft.Stack(
            controls=[
                ring,
                ft.Container(
                    content=percentage_text,
                    width=self.size,
                    height=self.size,
                    alignment="center",
                ),
            ],
            width=self.size,
            height=self.size,
        )




def main(page: Page) -> None:
    page.title = "Keyboard"
    page.spacing = 30 
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"

    calendario = ProgressRing(value=0.7, size=120)
    page.add(calendario.build())

if __name__ == "__main__":
    ft.run(main, view=ft.AppView.WEB_BROWSER)

