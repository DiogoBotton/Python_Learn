import time
import datetime
import firebase_admin
from firebase_admin import credentials, db
import getpass
import socket
import os
import ctypes
import logging
import sys

TEMPO_TOTAL_USUARIO = 1800  # Meia hora

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

# Função para bloquear a tela
def bloquear_pc():
    #pyautogui.alert(text='Uso do computador não permitido ou tempo de uso esgotado!', title='Aviso', button='OK')
    ctypes.windll.user32.ExitWindowsEx(0, 1)
    
# Verificar conexão com a Internet
def verificar_conexao():
    try:
        socket.create_connection(("8.8.8.8", 53))
        logging.info("Há conexão com a internet.")
        return True
    except OSError:
        logging.error(f"Não há conexão com a internet: {e}")
        return False

# Verificar tempo de uso permitido
def verificar_tempo(usuario):
    try:
        ref = db.reference(f'usuarios/{usuario}')
        data = ref.get()

        if data:
            uso_permitido = data.get('uso_permitido', False)
            tempo_restante = data.get('tempo_restante', 0)
            tempo_total = data.get('tempo_total', TEMPO_TOTAL_USUARIO)

            if uso_permitido and tempo_restante > 0:
                return True, tempo_restante, tempo_total
            else:
                return False, 0, TEMPO_TOTAL_USUARIO
        return False, 0
    except Exception as e:
        logging.error(f"Erro ao acessar o Firebase e verificar o tempo de uso, acesso bloqueado: {e}")
        return False, 0

# Atualizar tempo restante no Firebase
def atualizar_tempo_restante(usuario, tempo_restante, uso_permitido = False):
    try:
        ref = db.reference(f'usuarios/{usuario}')
        ref.update({
            'uso_permitido': uso_permitido,
            'tempo_restante': tempo_restante,
            'ultimo_login': datetime.datetime.now().isoformat()
        })
    except Exception as e:
        logging.error(f"Erro ao atualizar o tempo restante no Firebase: {e}")

# Registrar usuário no banco de dados se não existir
def registrar_usuario(usuario, tempo_total):
    try:
        ref = db.reference(f'usuarios/{usuario}')
        if not ref.get():
            ref.set({
                'uso_permitido': False,
                'tempo_total': tempo_total,
                'tempo_restante': 0,
                'ultimo_login': datetime.datetime.now().isoformat()
            })
    except Exception as e:
        logging.error(f"Erro ao registrar o usuário no Firebase: {e}")

# Função principal para verificar e bloquear se necessário
def verificar_e_bloquear():
    TEMPO_DORMIR = 300  # 5 minutos
    usuario = getpass.getuser()
    registrar_usuario(usuario, TEMPO_TOTAL_USUARIO)  # Define 1 hora de uso total para novos usuários
    
    if not verificar_conexao():
        bloquear_pc()
        return
    
    permitido, tempo_restante, tempo_total = verificar_tempo(usuario)
    
    if permitido and tempo_restante <= 0:
        atualizar_tempo_restante(usuario, tempo_total, True)
    
    if permitido:
        print(f"Tempo de uso permitido por {tempo_restante // 60} minutos.")
        while tempo_restante > 0:
            if tempo_restante > TEMPO_DORMIR:
                DORMIR_SEGUNDOS = TEMPO_DORMIR
            else:
                DORMIR_SEGUNDOS = tempo_restante
                
            time.sleep(DORMIR_SEGUNDOS)  # Dorme por 5 minutos ou o tempo restante
            
            tempo_restante -= DORMIR_SEGUNDOS
            
            if tempo_restante > 0:
                atualizar_tempo_restante(usuario, tempo_restante, True)
            else:
                atualizar_tempo_restante(usuario, 0)
                
            if not verificar_conexao():
                bloquear_pc()
                return
        bloquear_pc()
    else:
        print("Uso não permitido. Bloqueando o PC.")
        bloquear_pc()

if __name__ == "__main__":
    verificar_e_bloquear()