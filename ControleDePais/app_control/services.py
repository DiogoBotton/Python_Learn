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

def carregar_usuarios():
    try:
        ref = db.reference('usuarios')
        usuarios = ref.get()
        logging.info("Lista de usuários carregada com sucesso.")
        return list(usuarios.keys()) if usuarios else []
    except Exception as e:
        logging.error(f"Erro ao carregar lista de usuários: {e}")

# -------------------------------------------------------------------------------------------
# Reward
# -------------------------------------------------------------------------------------------

def carregar_recompensas_usuario(usuario):
    try:
        ref = db.reference(f'usuarios/{usuario}/recompensas')
        recompensas = ref.get()
        logging.info(f"Recompensas carregadas para o usuário {usuario}.")
        return recompensas if recompensas else []
    except Exception as e:
        logging.error(f"Erro ao carregar recompensas do usuário {usuario}: {e}")
        return []

def salvar_recompensa(usuario, descricao, tempo_total_em_segundos, isIncrease):
    try:
        ref = db.reference(f'usuarios/{usuario}/recompensas')
        nova_recompensa = {
            'descricao': descricao,
            'tempo_total': tempo_total_em_segundos,
            'isIncrease': isIncrease,
            'data': datetime.datetime.now().isoformat()
        }
        ref.push(nova_recompensa)
        logging.info(f"Recompensa salva para o usuário {usuario}.")
    except Exception as e:
        logging.error(f"Erro ao salvar recompensa no Firebase: {e}")

def deletar_recompensa(usuario, recompensa_id):
    try:
        ref = db.reference(f'usuarios/{usuario}/recompensas/{recompensa_id}')
        ref.delete()
        logging.info(f"Recompensa {recompensa_id} deletada para o usuário {usuario}.")
    except Exception as e:
        logging.error(f"Erro ao deletar recompensa no Firebase: {e}")

def calcular_saldo(usuario):
    try:
        recompensas = carregar_recompensas_usuario(usuario)
        saldo = 0
        for recompensa in recompensas.values():
            if recompensa['isIncrease']:
                saldo += recompensa['tempo_total']
            else:
                saldo -= recompensa['tempo_total']
        logging.info(f"Saldo de horas calculado para o usuário {usuario}.")
        return saldo
    except Exception as e:
        logging.error(f"Erro ao calcular saldo do usuário {usuario}: {e}")
        return 0


# -------------------------------------------------------------------------------------------
# Control
# -------------------------------------------------------------------------------------------

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
            'isFirstAccess': True if uso_permitido else False,
            'ultimo_login': datetime.datetime.now().isoformat()
        })
        logging.info(f"Configurações salvas para o usuário {usuario}.")
    except Exception as e:
        logging.error(f"Erro ao salvar configurações no Firebase: {e}")