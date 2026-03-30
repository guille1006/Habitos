import flet as ft
from src.utils.theme import LIGHT_THEME, apply_theme
from src.components.HabitCard import HabitCard


def main(page: ft.Page):
    apply_theme(page, LIGHT_THEME)

    card = HabitCard(
        name="Leer 30 minutos",
        icon="📚",
        streak=7,
        frequency="Diario",
        reminder_time="21:00",
        theme=LIGHT_THEME,       # ← aquí
        completed=False,
        on_complete=lambda: print("completado"),
        on_edit=lambda: print("editar"),
    )

    page.add(card)

if __name__ == "__main__":
    ft.run(main, view=ft.AppView.WEB_BROWSER)

