import flet as ft
import firebase_admin
from firebase_admin import credentials, db
import datetime
import os
import logging
import sys

# Configurar logging
logging.basicConfig(filename="control.log", level=logging.DEBUG, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Inicializar o Firebase
def inicializar_firebase():
    try:
        if getattr(sys, 'frozen', False):
            main_path = os.path.dirname(sys.executable)
        else:
            main_path = os.path.abspath(".")
            
        credentials_path = os.path.join(main_path, 'controle-de-pais-firebase.json')

        cred = credentials.Certificate(credentials_path)
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://controle-de-pais-default-rtdb.firebaseio.com/'
        })
        logging.info("Firebase inicializado com sucesso.")
    except Exception as e:
        logging.error(f"Erro ao inicializar o Firebase: {e}")

inicializar_firebase()

# Funções auxiliares
def carregar_usuarios():
    try:
        ref = db.reference('usuarios')
        usuarios = ref.get()
        logging.info("Lista de usuários carregada com sucesso.")
        return list(usuarios.keys()) if usuarios else []
    except Exception as e:
        logging.error(f"Erro ao carregar lista de usuários: {e}")

def carregar_configuracoes_usuario(usuario):
    try:
        ref = db.reference(f'usuarios/{usuario}')
        data = ref.get()
        if data:
            return data.get('uso_permitido', False), data.get('tempo_total', 0)
        logging.info(f"Configurações carregadas para o usuário {usuario}.")
        return False, 0
    except Exception as e:
        logging.error(f"Erro ao carregar configurações do usuário {usuario}: {e}")
        return False, 0

def salvar_configuracoes(usuario, uso_permitido, tempo_total_em_segundos):
    try:
        ref = db.reference(f'usuarios/{usuario}')
        ref.update({
            'uso_permitido': uso_permitido,
            'tempo_total': tempo_total_em_segundos,
            'tempo_restante': tempo_total_em_segundos if uso_permitido else 0,
            'ultimo_login': datetime.datetime.now().isoformat()
        })
        logging.info(f"Configurações salvas para o usuário {usuario}.")
    except Exception as e:
        logging.error(f"Erro ao salvar configurações no Firebase: {e}")

# Definir o componente
class ControleDePais(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.tempos_totais = [("Meia hora", 1800), ("Uma hora", 3600), ("Uma hora e meia", 5400), ("Duas horas", 7200)]
        self.usuarios = carregar_usuarios()

    def build(self):
        self.lista_usuarios = ft.Dropdown(
            options=[ft.dropdown.Option(usuario) for usuario in self.usuarios],
            on_change=self.on_usuario_change
        )

        self.var_uso_permitido = ft.Checkbox(label="Uso Permitido")
        self.var_tempo_total = ft.Dropdown(
            options=[ft.dropdown.Option(texto) for texto, _ in self.tempos_totais]
        )

        self.botao_salvar = ft.ElevatedButton(text="Salvar Configurações", on_click=self.on_salvar_click)

        self.dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Sucesso"),
            content=ft.Text("Configurações salvas com sucesso!"),
            actions=[
                ft.TextButton("Ok", on_click=self.handle_close_success)
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
            uso_permitido, tempo_total_em_segundos = carregar_configuracoes_usuario(usuario)
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
        salvar_configuracoes(usuario, uso_permitido, tempo_total_em_segundos)
        
        self.dlg_modal.title = ft.Text("Sucesso")
        self.dlg_modal.content = ft.Text("Configurações salvas com sucesso!")
        self.page.open(self.dlg_modal)
        self.update()

    def handle_close_success(self, e):
        self.page.close(self.dlg_modal)