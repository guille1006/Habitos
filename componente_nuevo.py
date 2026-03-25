import flet as ft
import threading
import asyncio


def show_toast(page: ft.Page, message: str, duration: int = 10):
    """
    Muestra una ventana flotante que aparece desde abajo y se disipa sola.

    Args:
        page: La instancia de ft.Page
        message: El texto a mostrar en el toast
        duration: Segundos antes de desaparecer (default: 10)
    """

    toast = ft.Container(
        content=ft.Row(
            controls=[
                ft.Icon(ft.Icons.NOTIFICATIONS_ROUNDED, color="#FFFFFF", size=20),
                ft.Text(
                    message,
                    color="#FFFFFF",
                    size=14,
                    weight=ft.FontWeight.W_500,
                    max_lines=2,
                    overflow=ft.TextOverflow.ELLIPSIS,
                    expand=True,
                ),
                ft.IconButton(
                    icon=ft.Icons.CLOSE_ROUNDED,
                    icon_color="#FFFFFF80",
                    icon_size=16,
                    on_click=lambda e: dismiss_toast(),
                    tooltip="Cerrar",
                    style=ft.ButtonStyle(
                        padding=ft.Padding.all(4),
                        overlay_color=ft.Colors.with_opacity(0.1, "#FFFFFF"),
                    ),
                ),
            ],
            spacing=12,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        bgcolor="#1C1C2E",
        border_radius=ft.BorderRadius.all(14),
        padding=ft.Padding.symmetric(horizontal=18, vertical=14),
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=24,
            color=ft.Colors.with_opacity(0.35, "#000000"),
            offset=ft.Offset(0, 8),
        ),
        border=ft.Border.all(1, "#FFFFFF15"),
        width=360,
        opacity=0,
        offset=ft.Offset(0, 0.5),
        animate_opacity=ft.Animation(400, ft.AnimationCurve.EASE_OUT),
    )

    progress_bar = ft.ProgressBar(
        value=1.0,
        color="#6C63FF",
        bgcolor="#FFFFFF15",
        height=3,
        border_radius=ft.BorderRadius.only(bottom_left=14, bottom_right=14),
        width=360,
    )

    overlay = ft.Container(
        content=ft.Container(
            content=ft.Row(
                controls=[
                    ft.Column(controls=[toast, progress_bar], spacing=0, tight=True)
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            padding=ft.Padding.only(bottom=32),
            alignment=ft.Alignment.BOTTOM_CENTER,
            expand=True,
        ),
        expand=True,
    )

    # Animar entrada
    toast.opacity = 1
    toast.offset = ft.Offset(0, 0)
    progress_bar.value = 0
        
    ventana_cerrada = False
    async def dismiss_toast():
        nonlocal ventana_cerrada 

        if ventana_cerrada:
            return 

        ventana_cerrada = True 

        toast.opacity = 0
        toast.offset = ft.Offset(0, 0.5)
        progress_bar.opacity = 0
        
        page.update()

        await asyncio.sleep(0.4)

        if overlay in page.overlay:
            page.overlay.remove(overlay)
            page.update()
        
        
    async def dismiss_por_tiempo():
        await asyncio.sleep(duration)
        await dismiss_toast() 

    async def dismiss_por_cancel(e):
        page.run_task(dismiss_toast)

    
    

    # Asignar el botón de cerrar aquí para capturar dismiss_toast en el closure
    toast.content.controls[2].on_click = dismiss_por_cancel
    page.run_task(dismiss_por_tiempo)

    page.overlay.append(overlay)
    page.update()
    
   
        

# ─── Demo ────────────────────────────────────────────────────────────────────

def main(page: ft.Page):
    page.title = "Toast Flotante"
    page.bgcolor = "#F0EFF4"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def on_toast_largo(e):
        show_toast(page, "¡Operación completada! Los cambios se han guardado.", duration=10)
 
    def on_toast_corto(e):
        show_toast(page, "Archivo eliminado.", duration=4)
 
    page.add(
        ft.Column(
            controls=[
                ft.Text("Demo: Ventana Flotante", size=22, weight=ft.FontWeight.BOLD, color="#1C1C2E"),
                ft.Text("Haz clic para mostrar el toast", size=13, color="#666"),
                ft.Button(
                    "Mostrar Toast (10 seg)",
                    on_click=on_toast_largo,
                    style=ft.ButtonStyle(
                        bgcolor="#6C63FF",
                        color="#FFFFFF",
                        shape=ft.RoundedRectangleBorder(radius=10),
                        padding=ft.Padding.symmetric(horizontal=24, vertical=14),
                    ),
                ),
                ft.Button(
                    "Toast corto (4 seg)",
                    on_click=on_toast_corto,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=10),
                        padding=ft.Padding.symmetric(horizontal=24, vertical=14),
                    ),
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=16,
        )
    )
 


ft.run(main)
