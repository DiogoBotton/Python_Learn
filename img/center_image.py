import os  # Importa o módulo para trabalhar com operações de sistema de arquivos
from PIL import Image  # Importa classes da biblioteca Pillow para manipulação de imagens

def centralize_image(input_path, output_path, desired_size=(224, 224), background_color=(0, 0, 0)):
    # Abre a imagem original no caminho especificado
    img = Image.open(input_path)
    
    # Reduz a imagem para caber dentro do tamanho desejado, mantendo a proporção
    img.thumbnail(desired_size, Image.ANTIALIAS)
    
    # Cria uma nova imagem do tamanho desejado com a cor de fundo especificada
    new_img = Image.new("RGB", desired_size, background_color)
    
    # Calcula a posição para centralizar a imagem dentro da nova imagem
    position = (
        (desired_size[0] - img.width) // 2,
        (desired_size[1] - img.height) // 2
    )
    
    # Cola a imagem redimensionada no centro da nova imagem
    new_img.paste(img, position)
    
    # Salva a nova imagem no caminho de saída especificado
    new_img.save(output_path)

def process_images_in_directory(root_directory, output_root_directory, desired_size=(224, 224), background_color=(0, 0, 0)):
    # Percorre todas as pastas e subpastas dentro do diretório raiz fornecido
    for subdir, dirs, files in os.walk(root_directory):
        for file in files:
            # Cria o caminho completo para a imagem de entrada
            input_path = os.path.join(subdir, file)

            # Calcula o caminho relativo da subpasta para manter a estrutura
            relative_path = os.path.relpath(subdir, root_directory)

            # Cria o caminho completo da subpasta no diretório de saída
            output_subdir = os.path.join(output_root_directory, relative_path)

            # Cria as pastas necessárias no diretório de saída (caso não existam)
            os.makedirs(output_subdir, exist_ok=True)

            # Define o caminho completo para salvar a imagem processada
            output_path = os.path.join(output_subdir, file)

            # Chama a função para centralizar e salvar a imagem
            centralize_image(input_path, output_path, desired_size, background_color)

# Caminhos de exemplo - defina o caminho da pasta de entrada e saída
input_directory = "Utensilios Escolhidos"
output_directory = "Imagens_centralizadas"

# Processa todas as imagens na pasta de entrada e suas subpastas
process_images_in_directory(input_directory, output_directory)
