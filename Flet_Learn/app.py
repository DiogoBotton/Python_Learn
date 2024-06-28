import flet as ft

def Main(page: ft.Page):
    page.title = "Cadastro de Usuários"
    page.bgcolor = "ccc"
    inputs = ft.Column(
        alignment=ft.alignment.center,
        controls=[
            ft.TextField(label="Nome do Usuário", text_align=ft.TextAlign.LEFT),
            ft.Checkbox(label="Permitir uso", value=False),
            ft.TextButton("Cadastrar", on_click=print("Cadastrado"))
        ]
    )
    
    title = ft.Container(
        alignment=ft.alignment.center,
        content=ft.Text("Cadastro de usuários", text_align=ft.alignment.center),
    )
    
    page.add(
        title,
        inputs
    )

ft.app(target=Main)