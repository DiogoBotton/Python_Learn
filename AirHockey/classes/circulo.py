import time

class Circulo:
    def __init__(self, raio, x, y, gramas):
        self.raio = raio
        self.x = x
        self.y = y
        self.velocidade = 0
        self.massa = gramas # EM GRAMAS
        self.tempo = time.time()
    
    def Att_Pos(self, x, y):
        self.x = x
        self.y = y
        self.tempo = time.time()
    
    def Att_Vel(self, velocidade):
        self.velocidade = velocidade