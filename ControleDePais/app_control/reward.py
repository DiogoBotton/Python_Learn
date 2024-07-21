import datetime
import flet as ft
import services as sv

# Definir o componente
class RecompensasUsuario(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.tempos_totais = [("10 minutos", 600), ("15 minutos", 900), ("20 minutos", 1200), ("30 minutos", 1800)]
        self.usuarios = sv.carregar_usuarios()
        self.recompensas_por_pagina = 5
        self.pagina_atual = 0
        self.filtro_tipo = None

    def build(self):
        self.lista_usuarios = ft.Dropdown(
            options=[ft.dropdown.Option(usuario) for usuario in self.usuarios],
            on_change=self.on_usuario_change
        )

        self.recompensas_lista = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Descrição")),
                ft.DataColumn(ft.Text("Tempo")),
                ft.DataColumn(ft.Text("Data")),
                ft.DataColumn(ft.Text("Ações"))
            ]
        )

        self.botao_cadastrar = ft.ElevatedButton(text="Cadastrar Recompensa", on_click=self.on_abrir_modal_click)

        self.saldo_usuario_component = ft.Text(f"Saldo de tempo: {0} minutos.")

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

        self.filtro_dropdown = ft.Dropdown(
            options=[
                ft.dropdown.Option("Todos"),
                ft.dropdown.Option("Acréscimo"),
                ft.dropdown.Option("Débito")
            ],
            on_change=self.on_filtro_change
        )

        self.paginacao_controls = ft.Row(
            controls=[
                ft.IconButton(icon=ft.icons.CHEVRON_LEFT, on_click=self.on_pagina_anterior),
                ft.IconButton(icon=ft.icons.CHEVRON_RIGHT, on_click=self.on_pagina_proxima)
            ]
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
                    alignment=ft.alignment.center,
                    content=ft.Column(
                        controls=[
                            ft.Text("Filtrar por tipo de recompensa:"),
                            self.filtro_dropdown
                        ]
                    )
                ),
                ft.Container(
                    alignment=ft.alignment.center,
                    content=self.saldo_usuario_component
                ),
                ft.Row(height=15),
                ft.Container(
                    content=ft.ListView(
                        controls=[self.recompensas_lista],
                        padding=16
                    )
                ),
                ft.Row(height=15),
                self.paginacao_controls
            ]
        )

    def on_usuario_change(self, e):
        self.pagina_atual = 0
        self.filtro_tipo = None
        self.atualizar_tabela()

    def on_filtro_change(self, e):
        filtro = self.filtro_dropdown.value
        if filtro == "Acréscimo":
            self.filtro_tipo = True
        elif filtro == "Débito":
            self.filtro_tipo = False
        else:
            self.filtro_tipo = None
        self.pagina_atual = 0
        self.atualizar_tabela()

    def atualizar_tabela(self):
        usuario = self.lista_usuarios.value
        if usuario:
            recompensas = sv.carregar_recompensas_usuario(usuario)
            if self.filtro_tipo is not None:
                recompensas = {k: v for k, v in recompensas.items() if v['isIncrease'] == self.filtro_tipo}
            
            if recompensas.__len__() == 0:
                self.recompensas_lista.rows.clear()
            else:
                recompensas_items = list(recompensas.items())
                inicio = self.pagina_atual * self.recompensas_por_pagina
                fim = inicio + self.recompensas_por_pagina
                recompensas_pagina = recompensas_items[inicio:fim]
                self.recompensas_lista.rows = [
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(recompensa['descricao'])),
                        ft.DataCell(ft.Text(str(recompensa['tempo_total'] // 60))),
                        ft.DataCell(ft.Text(datetime.datetime.fromisoformat(recompensa['data']).strftime("%d/%m/%Y"))),
                        ft.DataCell(ft.IconButton(icon=ft.icons.DELETE, on_click=lambda e, r_id=recompensa_id: self.on_deletar_click(usuario, r_id)))
                    ]) for recompensa_id, recompensa in recompensas_pagina
                ]
            saldo_usuario = sv.calcular_saldo(usuario) // 60
            self.saldo_usuario_component.value = f"Saldo de tempo: {saldo_usuario} minutos."
            self.update()

    def on_pagina_anterior(self, e):
        if self.pagina_atual > 0:
            self.pagina_atual -= 1
            self.atualizar_tabela()

    def on_pagina_proxima(self, e):
        usuario = self.lista_usuarios.value
        recompensas = sv.carregar_recompensas_usuario(usuario)
        if (self.pagina_atual + 1) * self.recompensas_por_pagina < len(recompensas):
            self.pagina_atual += 1
            self.atualizar_tabela()

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
        isIncrease = True # Por padrão é sempre um acréscimo

        if not usuario or not tempo_total_str or not descricao:
            self.feedback_modal.title = ft.Text("Erro")
            self.feedback_modal.content = ft.Text("Por favor, preencha todos os campos.")
            self.page.open(self.feedback_modal)
            return

        tempo_total_em_segundos = next((valor for texto, valor in self.tempos_totais if texto == tempo_total_str), None)
        sv.salvar_recompensa(usuario, descricao, tempo_total_em_segundos, isIncrease)
        
        self.feedback_modal.title = ft.Text("Sucesso")
        self.feedback_modal.content = ft.Text("Recompensa adicionada com sucesso!")
        self.page.open(self.feedback_modal)
        self.handle_close_modal(None)
        self.atualizar_tabela()

    def on_deletar_click(self, usuario, recompensa_id):
        sv.deletar_recompensa(usuario, recompensa_id)
        self.feedback_modal.title = ft.Text("Sucesso")
        self.feedback_modal.content = ft.Text("Recompensa deletada com sucesso!")
        self.page.open(self.feedback_modal)
        self.atualizar_tabela()

    def handle_close_modal(self, e):
        self.page.close(self.dlg_modal)

    def handle_close_feedback(self, e):
        self.page.close(self.feedback_modal)
