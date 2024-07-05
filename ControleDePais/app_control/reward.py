import flet as ft
import services as sv

# Definir o componente
class RecompensasUsuario(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.tempos_totais = [("10 minutos", 600), ("15 minutos", 900), ("20 minutos", 1200), ("30 minutos", 1800)]
        self.usuarios = sv.carregar_usuarios()

    def build(self):
        self.lista_usuarios = ft.Dropdown(
            options=[ft.dropdown.Option(usuario) for usuario in self.usuarios],
            on_change=self.on_usuario_change
        )

        self.recompensas_lista = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Descrição")),
                ft.DataColumn(ft.Text("Tempo (segundos)")),
                ft.DataColumn(ft.Text("Data")),
                ft.DataColumn(ft.Text("Ações"))
            ]
        )

        self.botao_cadastrar = ft.ElevatedButton(text="Cadastrar Recompensa", on_click=self.on_abrir_modal_click)

        self.var_tempo_total = ft.Dropdown(
            options=[ft.dropdown.Option(texto) for texto, _ in self.tempos_totais]
        )
        
        self.var_descricao = ft.TextField(label="Descrição")
        
        self.dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Cadastrar Recompensa"),
            content=ft.Column(
                controls=[
                    ft.Text("Tempo Total de Uso:"),
                    self.var_tempo_total,
                    ft.Text("Descrição:"),
                    self.var_descricao
                ]
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=self.handle_close_modal),
                ft.TextButton("Salvar", on_click=self.on_adicionar_click)
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )

        self.feedback_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Sucesso"),
            content=ft.Text("Operação realizada com sucesso!"),
            actions=[
                ft.TextButton("Ok", on_click=self.handle_close_feedback)
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )

        return ft.Column(
            scroll=True,
            controls=[
                ft.Container(
                    alignment=ft.alignment.center,
                    margin=25,
                    content=ft.Text("Gerenciamento de Recompensas de Usuários", size=20)
                ),
                ft.Column(
                    controls=[
                        ft.Text("Selecione o Usuário:"),
                        self.lista_usuarios
                    ],
                    spacing=20
                ),
                
                ft.Row(height=15),
                
                ft.Container(
                    alignment=ft.alignment.center,
                    content=self.botao_cadastrar
                ),
                
                ft.Row(height=15),
                
                ft.Container(
                    height=300,
                    content=ft.ListView(
                        controls=[self.recompensas_lista],
                        padding=16
                    )
                )
            ]
        )

    def on_usuario_change(self, e):
        usuario = self.lista_usuarios.value
        if usuario:
            recompensas = sv.carregar_recompensas_usuario(usuario)
            if recompensas.__len__() == 0:
                self.recompensas_lista.rows = [
                    ft.DataRow(cells=[ft.DataCell(ft.Text("Nenhuma recompensa cadastrada."))])
                ]
            else:
                self.recompensas_lista.rows = [
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(recompensa['descricao'])),
                        ft.DataCell(ft.Text(str(recompensa['tempo_total']))),
                        ft.DataCell(ft.Text(recompensa['data'])),
                        ft.DataCell(ft.IconButton(icon=ft.icons.DELETE, on_click=lambda e, r_id=recompensa_id: self.on_deletar_click(usuario, r_id)))
                    ]) for recompensa_id, recompensa in recompensas.items()
                ]
            self.update()

    def on_abrir_modal_click(self, e):
        if not self.lista_usuarios.value:
            self.feedback_modal.title = ft.Text("Erro")
            self.feedback_modal.content = ft.Text("Por favor, selecione um usuário.")
            self.page.open(self.feedback_modal)
        else:
            self.page.open(self.dlg_modal)

    def on_adicionar_click(self, e):
        usuario = self.lista_usuarios.value
        tempo_total_str = self.var_tempo_total.value
        descricao = self.var_descricao.value

        if not usuario or not tempo_total_str or not descricao:
            self.feedback_modal.title = ft.Text("Erro")
            self.feedback_modal.content = ft.Text("Por favor, preencha todos os campos.")
            self.page.open(self.feedback_modal)
            return

        tempo_total_em_segundos = next((valor for texto, valor in self.tempos_totais if texto == tempo_total_str), None)
        sv.salvar_recompensa(usuario, descricao, tempo_total_em_segundos)
        
        self.feedback_modal.title = ft.Text("Sucesso")
        self.feedback_modal.content = ft.Text("Recompensa adicionada com sucesso!")
        self.page.open(self.feedback_modal)
        self.handle_close_modal(None)
        self.on_usuario_change(None)

    def on_deletar_click(self, usuario, recompensa_id):
        sv.deletar_recompensa(usuario, recompensa_id)
        self.feedback_modal.title = ft.Text("Sucesso")
        self.feedback_modal.content = ft.Text("Recompensa deletada com sucesso!")
        self.page.open(self.feedback_modal)
        self.on_usuario_change(None)

    def handle_close_modal(self, e):
        self.page.close(self.dlg_modal)

    def handle_close_feedback(self, e):
        self.page.close(self.feedback_modal)