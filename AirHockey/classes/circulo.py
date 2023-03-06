import time

class Circulo:
    def __init__(self, id, raio, x, y, gramas):
        self.raio = raio
        self.id = id
        self.x = x
        self.y = y
        self.velocidade = 0
        self.velx = 0
        self.vely = 0
        self.massa = gramas # EM GRAMAS
        self.tempo = time.time()
    
    def Att_Pos(self, x, y):
        self.x = x
        self.y = y
        self.tempo = time.time()
    
    def Att_Vel(self, velocidade):
        self.velocidade = velocidade
    
    def Att_Vel_XY(self, velx, vely):
        self.velx = velx
        self.vely = vely