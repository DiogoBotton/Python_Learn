from PIL import Image
import os

IMAGE_FOLDER = "img"

# Busca imagem na pasta img (constante IMAGE_FOLDER armazena nome de pasta)
def path_image(filename):
    return os.path.join(IMAGE_FOLDER, filename)

# Obtem a imagem
img = Image.open(path_image("PinkFloydWallPaper.jpg"))

# Adquire comprimento e altura da imagem
width, height = img.size
BLACK = (0,0,0)
RED = (255,0,0)
# Cria uma nova imagem baseado em width e height
newImage = Image.new("RGB", (width, height), BLACK)

# Percorre a imagem pixel por pixel e quando x < y modifica a cor do pixel da imagem
for x in range(0, width):
    for y in range(0, height):
        # Adquire valor em RGB da cor do pixel da imagem
        colorRGB = img.getpixel((x,y))
        if x < y:
            newImage.putpixel((x,y), RED)
        else:
            newImage.putpixel((x,y), colorRGB)

newImage.show()