import math

import flet as ft 
import flet.canvas as cv


class ProgressRing():
    def __init__(self, value: float, size: int = 120, stroke_width: int = 20):
        self.value = value
        self.size = size 
        self.stroke_width = stroke_width
        self.color = ft.Colors.GREEN

    def build(self):
        cx = self.size/2    # Centro x
        cy = self.size/2    # Centro y
        radius = (self.size / 2) - (self.stroke_width / 2)

        start_angle = 0
        progress_angle = self.value * math.pi*2 

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
                        color=ft.Colors.with_opacity(0.9, ft.Colors.ON_SURFACE),
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
                        stroke_cap=ft.StrokeCap.BUTT,
                    ),
                ),
            ],
            width=self.size,
            height=self.size,
        )

        # Texto con el progreso
        percentage_text = ft.Text(
            value=f"{int(self.value * 100)}%",
            size=self.size * 0.22,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.ON_SURFACE,
        )

        return ft.Stack(
            controls=[
                ring,
                percentage_text,
            ],
            width=self.size,
            height=self.size,
            alignment=ft.Alignment.CENTER
        )