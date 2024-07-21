import flet as ft
import services as sv

class ControleDePais(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.tempos_totais = [("3 minutos", 180), ("Meia hora", 1800), ("Uma hora", 3600), ("Uma hora e meia", 5400), ("Duas horas", 7200)]
        self.usuarios = sv.carregar_usuarios()

    def build(self):
        self.lista_usuarios = ft.Dropdown(
            options=[ft.dropdown.Option(usuario) for usuario in self.usuarios],
            on_change=self.on_usuario_change
        )

        self.var_uso_permitido = ft.Switch(label="Uso Permitido")
        self.var_tempo_total = ft.Dropdown(
            options=[ft.dropdown.Option(texto) for texto, _ in self.tempos_totais]
        )

        self.botao_salvar = ft.ElevatedButton(text="Salvar Configurações", on_click=self.on_salvar_click)

        self.dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Sucesso"),
            content=ft.Text("Configurações salvas com sucesso!"),
            actions=[
                ft.TextButton("Ok", on_click=self.handle_close)
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )

        return ft.Column(
            controls=[
                ft.Container(
                    alignment=ft.alignment.center,
                    margin=25,
                    content=ft.Text("Configuração de Controle de Pais", size=20)
                ),
                ft.Column(
                    controls=[
                        ft.Text("Selecione o Usuário:"),
                        self.lista_usuarios
                    ],
                    spacing=20
                ),
                
                ft.Row(height=15),
                
                ft.Column(
                    controls=[self.var_uso_permitido]
                ),
                
                ft.Row(height=15),
                
                ft.Column(
                    controls=[
                        ft.Text("Tempo Total de Uso:"),
                        self.var_tempo_total
                    ],
                    spacing=20
                ),
                ft.Container(
                    alignment=ft.alignment.center,
                    margin=50,
                    content=self.botao_salvar
                )
            ]
        )

    def on_usuario_change(self, e):
        usuario = self.lista_usuarios.value
        if usuario:
            uso_permitido, tempo_total_em_segundos = sv.carregar_configuracoes_usuario(usuario)
            self.var_uso_permitido.value = uso_permitido
            self.var_tempo_total.value = next((texto for texto, valor in self.tempos_totais if valor == tempo_total_em_segundos), "")
            self.update()

    def on_salvar_click(self, e):
        usuario = self.lista_usuarios.value
        uso_permitido = self.var_uso_permitido.value
        tempo_total_str = self.var_tempo_total.value

        if not usuario or not tempo_total_str:
            self.dlg_modal.title = ft.Text("Erro")
            self.dlg_modal.content = ft.Text("Por favor, selecione um usuário válido e um tempo total.")
            self.page.open(self.dlg_modal)
            self.update()
            return

        tempo_total_em_segundos = next((valor for texto, valor in self.tempos_totais if texto == tempo_total_str), None)

        saldo = sv.calcular_saldo(usuario)
        if saldo < tempo_total_em_segundos:
            self.dlg_modal.title = ft.Text("Erro")
            self.dlg_modal.content = ft.Text("Saldo do usuário selecionado insuficiente para liberar o PC.")
            self.page.open(self.dlg_modal)
            self.update()
            return

        sv.salvar_configuracoes(usuario, uso_permitido, tempo_total_em_segundos)
        
        self.dlg_modal.title = ft.Text("Sucesso")
        self.dlg_modal.content = ft.Text("Configurações salvas com sucesso!")
        self.page.open(self.dlg_modal)
        self.update()

    def handle_close(self, e):
        self.page.close(self.dlg_modal)