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

# Instalar antes: pip install firebase-admin pyautogui

try:
    # Obtém o caminho absoluto para o arquivo, considerando o diretório do executável.
    if getattr(sys, 'frozen', False):
        # Rodando como executável
        main_path = os.path.dirname(sys.executable)
    else:
        # Rodando no modo debug
        main_path = os.path.abspath(".")
        
    credentials_path = os.path.join(main_path, 'controle-de-pais-firebase.json')

    # Configurar o Firebase Realtime Database
    cred = credentials.Certificate(credentials_path)
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://controle-de-pais-default-rtdb.firebaseio.com/'
    })
    logging.info("Firebase inicializado com sucesso.")
except Exception as e:
    logging.error(f"Erro ao inicializar o Firebase: {e}")

# Lista de tuplas com opções de tempo e seus valores em segundos
tempos_totais = [("Meia hora", 1800), ("Uma hora", 3600), ("Uma hora e meia", 5400), ("Duas horas", 7200)]

# Função para carregar a lista de usuários do Firebase
def carregar_usuarios():
    try:
        ref = db.reference('usuarios')
        usuarios = ref.get()
        logging.info("Lista de usuários carregada com sucesso.")
        return list(usuarios.keys()) if usuarios else []
    except Exception as e:
        logging.error(f"Erro ao carregar lista de usuários: {e}")

# Função para carregar as configurações do usuário selecionado
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
        
# Função para salvar configurações no Firebase
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

# Configurar a interface gráfica com Flet
def main(page: ft.Page):
    page.title = "Configuração de Controle de Pais"
    page.window_width = 400
    page.window_height = 300
    
    usuarios = carregar_usuarios()

    def on_usuario_change(e):
        usuario = lista_usuarios.value
        if usuario:
            uso_permitido, tempo_total_em_segundos = carregar_configuracoes_usuario(usuario)
            var_uso_permitido.value = uso_permitido
            var_tempo_total.value = next((texto for texto, valor in tempos_totais if valor == tempo_total_em_segundos), "")
            page.update()

    def on_salvar_click(e):
        usuario = lista_usuarios.value
        uso_permitido = var_uso_permitido.value
        tempo_total_str = var_tempo_total.value

        if not usuario or not tempo_total_str:
            page.open(dlg_modal_error)
            page.update()
            return

        tempo_total_em_segundos = next((valor for texto, valor in tempos_totais if texto == tempo_total_str), None)
        salvar_configuracoes(usuario, uso_permitido, tempo_total_em_segundos)
        
        page.open(dlg_modal_success)
        page.update()
    
    def handle_close_error(e):
            page.close(dlg_modal_error)
    
    def handle_close_success(e):
            page.close(dlg_modal_success)
    
    dlg_modal_error = ft.AlertDialog(
        modal=True,
        title=ft.Text("Erro"),
        content=ft.Text("Por favor, selecione um usuário válido e um tempo total."),
        actions=[
            ft.TextButton("Ok", on_click=handle_close_error)
        ],
        actions_alignment=ft.MainAxisAlignment.END
    )
    
    dlg_modal_success = ft.AlertDialog(
        modal=True,
        title=ft.Text("Sucesso"),
        content=ft.Text("Configurações salvas com sucesso!"),
        actions=[
            ft.TextButton("Ok", on_click=handle_close_success)
        ],
        actions_alignment=ft.MainAxisAlignment.END
    )

    lista_usuarios = ft.Dropdown(
        options=[ft.dropdown.Option(usuario) for usuario in usuarios],
        on_change=on_usuario_change
    )

    var_uso_permitido = ft.Checkbox(label="Uso Permitido")
    var_tempo_total = ft.Dropdown(
        options=[ft.dropdown.Option(texto) for texto, _ in tempos_totais]
    )

    botao_salvar = ft.ElevatedButton(text="Salvar Configurações", on_click=on_salvar_click)

    page.add(
        ft.Column(
            controls=[
                ft.Text("Selecione o Usuário:"),
                lista_usuarios,
                var_uso_permitido,
                ft.Text("Tempo Total de Uso:"),
                var_tempo_total,
                botao_salvar
            ]
        )
    )

ft.app(target=main)