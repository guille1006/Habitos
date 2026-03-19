import flet as ft
from flet import TextField, Checkbox, ElevatedButton, Text, Row, Column, ControlEvent

def main(page:ft.Page) -> None:
    # Aspectos principales de la pagina
    page.title = "Login"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.theme_mode = "dark"

    # Definimos los elementos
    text_username: TextField = TextField(label="Username", text_align=ft.TextAlign.LEFT, width=200)
    text_password: TextField = TextField(label="Password", text_align=ft.TextAlign.LEFT, width=200, password=True)
    checkbox_signup: Checkbox = Checkbox(label="I agree to stuff", value=False)
    button_submit: ft.Button = ft.Button(
                                    "Sign up",
                                    style=ft.ButtonStyle(
                                        bgcolor=ft.Colors.BLUE,
                                        color=ft.Colors.WHITE,
                                        elevation=5
                                    )
                                )

    def validate(e: ControlEvent) -> None:
        button_submit.disabled = not all([text_username.value, text_password.value, checkbox_signup.value])
        page.update() 

    def submit(e: ControlEvent) -> None:
        print(text_username.value)
        print(text_password.value)

        page.clean()
        page.add(
            Row(
                controls=[Text(value="Buenos dias",color="black")]
            )
        )

    text_username.on_change = validate
    text_password.on_change = validate 
    checkbox_signup.on_change = validate 
    button_submit.on_click = submit

    page.add(
        Column([
            text_username,
            text_password,
            checkbox_signup,
            button_submit
        ])
    )
if __name__ == "__main__":
    ft.run(main, view=ft.AppView.WEB_BROWSER)