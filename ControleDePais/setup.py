from cx_Freeze import setup, Executable

# Inclua os arquivos que você quer adicionar
include_files = ['controle-de-pais-firebase.json']

# Crie o executável
executables = [Executable("main.py")]

# Defina as opções
options = {
    'build_exe': {
        'include_files': include_files,
    }
}

# Configure o setup
setup(
    name="Controle de Pais",
    version="1.0",
    description="Posso usar o PC?",
    options=options,
    executables=executables
)