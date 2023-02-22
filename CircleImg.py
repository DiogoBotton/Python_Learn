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
centroX, centroY = width // 2, height // 2
raio_circulo = 64
RED = (255,0,0)

# Desenha um círculo no centro da imagem
for x in range(centroX-raio_circulo, centroX+raio_circulo):
    for y in range(centroY-raio_circulo, centroY+raio_circulo):
        colorRGB = img.getpixel((x,y))
        img.putpixel((x,y), RED)

img.show()