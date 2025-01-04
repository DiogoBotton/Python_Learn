class Retangulo:
    def __init__(self, width, height, x, y, position):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.position = position #'top' or 'bottom'
        self.velx = 0

    def Att_Pos(self, x):
        self.x = x
    
    def Att_Vel_X(self, velx):
        self.velx = velx