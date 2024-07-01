# import flet as ft

# def Main(page: ft.Page):
#     page.title = "Cadastro de Usuários"
#     page.bgcolor = "ccc"
#     inputs = ft.Column(
#         alignment=ft.alignment.center,
#         controls=[
#             ft.TextField(label="Nome do Usuário", text_align=ft.TextAlign.LEFT),
#             ft.Checkbox(label="Permitir uso", value=False),
#             ft.TextButton("Cadastrar", on_click=print("Cadastrado"))
#         ]
#     )
    
#     title = ft.Container(
#         alignment=ft.alignment.center,
#         content=ft.Text("Cadastro de usuários", text_align=ft.alignment.center),
#     )
    
#     page.add(
#         title,
#         inputs
#     )

# ft.app(target=Main)

import flet as ft

def main(page: ft.Page):
    page.title = "Interface de Usuário com Flet"

    # Função para lidar com o clique no botão
    def handle_button_click(e):
        selected_user = user_dropdown.value
        permission = permission_checkbox.value
        selected_hours = hours_dropdown.value
        
        result.value = f"Usuário: {selected_user}\nUso permitido: {'Sim' if permission else 'Não'}\nTempo selecionado: {selected_hours}"
        page.update()

    # Campo de seleção de usuários
    user_dropdown = ft.Dropdown(
        label="Selecione o usuário",
        options=[
            ft.dropdown.Option("Usuário 1"),
            ft.dropdown.Option("Usuário 2"),
            ft.dropdown.Option("Usuário 3")
        ]
    )

    # Checkbox "Uso permitido"
    permission_checkbox = ft.Checkbox(label="Uso permitido")

    # Campo de seleção de quantidade de horas
    hours_dropdown = ft.Dropdown(
        label="Selecione a quantidade de horas",
        options=[
            ft.dropdown.Option("Meia hora"),
            ft.dropdown.Option("Uma hora"),
            ft.dropdown.Option("Duas horas"),
            ft.dropdown.Option("Três horas")
        ]
    )

    # Botão para exibir os valores selecionados
    submit_button = ft.ElevatedButton(text="Enviar", on_click=handle_button_click)

    # Rótulo para mostrar o resultado
    result = ft.Text(value="")

    # Adiciona os componentes à página
    page.add(user_dropdown, permission_checkbox, hours_dropdown, submit_button, result)

# Inicia o aplicativo
ft.app(target=main)
