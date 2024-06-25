import time
import datetime
import firebase_admin
from firebase_admin import credentials, db
import pyautogui
import getpass
import socket
import os
import ctypes

# Instalar antes: pip install firebase-admin pyautogui

main_path = os.path.dirname(__file__)
credentials_path = os.path.join(main_path, 'controle-de-pais-firebase.json')

# Configurar o Firebase Realtime Database
cred = credentials.Certificate(credentials_path)
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://controle-de-pais-default-rtdb.firebaseio.com/'
})

# Função para bloquear a tela
def bloquear_tela():
    ##pyautogui.alert(text='Uso do computador não permitido ou tempo de uso esgotado!', title='Aviso', button='OK')
    ctypes.windll.user32.LockWorkStation()
# Verificar conexão com a Internet
def verificar_conexao():
    try:
        socket.create_connection(("8.8.8.8", 53))
        return True
    except OSError:
        return False

# Verificar tempo de uso permitido
def verificar_tempo(usuario):
    ref = db.reference(f'usuarios/{usuario}')
    data = ref.get()
    
    if data:
        uso_permitido = data.get('uso_permitido', False)
        tempo_restante = data.get('tempo_restante', 0)
        
        if uso_permitido and tempo_restante > 0:
            return True, tempo_restante
        else:
            return False, 0
    return False, 0

# Atualizar tempo restante no Firebase
def atualizar_tempo_restante(usuario, tempo_restante):
    ref = db.reference(f'usuarios/{usuario}')
    ref.update({
        'tempo_restante': tempo_restante,
        'ultimo_login': datetime.datetime.now().isoformat()
    })

# Registrar usuário no banco de dados se não existir
def registrar_usuario(usuario, tempo_total):
    ref = db.reference(f'usuarios/{usuario}')
    if not ref.get():
        ref.set({
            'uso_permitido': False,
            'tempo_total': tempo_total,
            'tempo_restante': 0,
            'ultimo_login': datetime.datetime.now().isoformat()
        })

# Função principal para verificar e bloquear se necessário
def verificar_e_bloquear():
    usuario = getpass.getuser()
    registrar_usuario(usuario, 3600)  # Define 1 hora de uso total para novos usuários
    
    if not verificar_conexao():
        bloquear_tela()
        return
    
    permitido, tempo_restante = verificar_tempo(usuario)
    
    if permitido:
        print(f"Tempo de uso permitido por {tempo_restante // 60} minutos.")
        while tempo_restante > 0:
            time.sleep(300)  # Dorme por 5 minutos
            tempo_restante -= 300
            atualizar_tempo_restante(usuario, tempo_restante)
            if not verificar_conexao():
                bloquear_tela()
                return
        bloquear_tela()
        atualizar_tempo_restante(usuario, 0)
    else:
        print("Uso não permitido. Bloqueando o PC.")
        bloquear_tela()

if __name__ == "__main__":
    verificar_e_bloquear()