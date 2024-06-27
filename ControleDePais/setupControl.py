from cx_Freeze import setup, Executable

# Buildar com: python setupControl.py build

# Inclua os arquivos que você quer adicionar
include_files = ['controle-de-pais-firebase.json']

# Crie o executável, win32GUI serve para não abrir o console ao executar o programa
executables = [Executable("control.py", base="Win32GUI")]

# Defina as opções
options = {
    'build_exe': {
        'include_files': include_files,
    }
}

# Configure o setup
setup(
    name="Controle de Pais - Controle",
    version="1.0",
    description="Configurações do Controle de Pais.",
    options=options,
    executables=executables
)