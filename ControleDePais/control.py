import tkinter as tk
from tkinter import messagebox
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
def carregar_configuracoes_usuario(*args):
    try:
        usuario = lista_usuarios.get()
        ref = db.reference(f'usuarios/{usuario}')
        data = ref.get()
        if data:
            var_uso_permitido.set(data.get('uso_permitido', False))
            tempo_total_em_segundos = data.get('tempo_total', 0)
            for texto, valor in tempos_totais:
                if tempo_total_em_segundos == valor:
                    var_tempo_total.set(texto)
                    break
        logging.info(f"Configurações carregadas para o usuário {usuario}.")
    except Exception as e:
        logging.error(f"Erro ao carregar configurações do usuário {usuario}: {e}")
        
# Função para salvar configurações no Firebase
def salvar_configuracoes():
    try:
        usuario = lista_usuarios.get()
        uso_permitido = var_uso_permitido.get()
        tempo_total_str = var_tempo_total.get()

        if not usuario or not tempo_total_str:
            messagebox.showerror("Erro", "Por favor, selecione um usuário válido e um tempo total.")
            return

        tempo_total_em_segundos = next((valor for texto, valor in tempos_totais if texto == tempo_total_str), None)

        ref = db.reference(f'usuarios/{usuario}')
        ref.update({
            'uso_permitido': uso_permitido,
            'tempo_total': tempo_total_em_segundos,
            'tempo_restante': tempo_total_em_segundos if uso_permitido else 0,
            'ultimo_login': datetime.datetime.now().isoformat()
        })
        messagebox.showinfo("Sucesso", "Configurações salvas com sucesso!")
        logging.info(f"Configurações salvas para o usuário {usuario}.")
    except Exception as e:
        logging.error(f"Erro ao salvar configurações no Firebase: {e}")

# Configurar a interface gráfica
root = tk.Tk()
root.title("Configuração de Horários de Uso")

# Label e OptionMenu para a lista de usuários
tk.Label(root, text="Usuário:").grid(row=0, column=0, padx=10, pady=10)
usuarios = carregar_usuarios()
lista_usuarios = tk.StringVar(root)
lista_usuarios.set(usuarios[0] if usuarios else "Nenhum usuário disponível")
option_menu_usuarios = tk.OptionMenu(root, lista_usuarios, *usuarios) # TODO: Aqui ainda ocorre erro em caso da lista de usuários ser vazia
option_menu_usuarios.grid(row=0, column=1, padx=10, pady=10)
lista_usuarios.trace('w', carregar_configuracoes_usuario)

# Checkbox para uso permitido
var_uso_permitido = tk.BooleanVar()
checkbox_uso_permitido = tk.Checkbutton(root, text="Uso Permitido", variable=var_uso_permitido)
checkbox_uso_permitido.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

# Label e OptionMenu para o tempo total permitido
tk.Label(root, text="Tempo Total:").grid(row=2, column=0, padx=10, pady=10)
var_tempo_total = tk.StringVar(root)
var_tempo_total.set(tempos_totais[0][0])
option_menu_tempo_total = tk.OptionMenu(root, var_tempo_total, *[texto for texto, valor in tempos_totais])
option_menu_tempo_total.grid(row=2, column=1, padx=10, pady=10)

# Botão para salvar as configurações
button_salvar = tk.Button(root, text="Salvar Configurações", command=salvar_configuracoes)
button_salvar.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Iniciar a interface gráfica
root.mainloop()