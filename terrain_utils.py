
import random
import math


class Terrain:
    
    def __init__(self, size : int, diamant : bool):
        self.size = size
        self.nb_lissage = 0
        self.diamant = diamant
        self.matrice = [[0 for i in range(size)] for j in range(size)]
        
    def generate(self):
        if self.diamant:
            #DIAMANT
            self.matrice = diamantcarre(self.matrice)
            for _ in range(3):
                self.terrain_lissage()    

        else:
            #PERLIN
            self.matrice = perlin(self.matrice)

        self.calibrage(self.diamant)
    
    def calibrage(self, sigmo : bool):
        if sigmo:
            moy = moyenne(self.matrice)
            for x in range(self.size):
                for y in range(self.size):
                    self.matrice[x][y] = sigmoid_cal(self.matrice[x][y],moy)
        self.maximum = maximum(self.matrice)
        self.minimum = minimum(self.matrice)
        for x in range(self.size):
            for y in range(self.size):
                self.matrice[x][y] = linear_cal(self.matrice[x][y],self.minimum,self.maximum)
        self.maximum = maximum(self.matrice)
        self.minimum = minimum(self.matrice)
    
    def terrain_lissage(self):
        self.matrice = lissage(self.matrice, 1)
        self.nb_lissage += 1
    
    def to_pixels_map(self):
        return [[color(self.matrice[x][y],self.minimum,self.maximum)  for x in range(self.size)] for y in range(self.size)]



#HEAT_COLORS = [(0,255,0),(0,255,64),(0,255,128),(0,255,191),(0,255,255),(0,191,255),
#               (0,128,255),(0,64,255),(0,0,255),(64,0,255),(128,0,255),
#               (191,0,255),(255,0,255),(255,0,191),(255,0,128),(255,0,64),(255,0,0)]

COLORS = [  (22, 0, 119),(37, 0, 199),(51, 0, 254),(0, 152, 254),(254, 253, 0),(20, 254, 0),(42, 180, 0),(29, 125, 0),
            (127, 127, 127),(240, 240, 240)]
def color(z,mini,maxi):
    v = ((z-mini)/(maxi-mini))*(len(COLORS)-1)
    return COLORS[round(v)]

def maximum(L):
    return max(max(row) for row in L)

def minimum(L):
    return min(min(row) for row in L)

def somme(L):
    return sum(sum(row) for row in L)

def moyenne(L):
    return somme(L)/(len(L)**2)

def diamantcarre(T):
    h = len(T)
    T[0][0] = random.randrange(-h, h)  # initialisation des coins #
    T[0][h-1] = random.randrange(-h, h)
    T[h-1][h-1] = random.randrange(-h, h)
    T[h-1][0] = random.randrange(-h, h)
    i = h-1
    while i > 1:
        a = i//2
        for x in range(a,h,i):     # début de la phase du diamant #
            for y in range(a,h,i): 
                moyenne = (T[x - a][y - a] + T[x - a][y + a] + T[x + a][y + a] + T[x + a][y - a]) / 4
                T[x][y] = moyenne + random.randrange(-a, a)    
        décalage = 0
        for x in range(0,h,a): # début de la phase du carré #
            if décalage == 0 :
                décalage = a
            else:
                décalage = 0
            for y in range(0,h,i):
                somme = 0
                n = 0
                if x >= a :
                    somme = somme + T[x - a][y]
                    n = n+1
                if x + a < h :
                    somme = somme + T[x + a][y]
                    n = n+1
                if y >= a :
                    somme = somme + T[x][y - a]
                    n = n+1
                if y + a < h :
                    somme = somme + T[x][y + a]
                    n = n+1
                T[x][y] = somme / n + random.randrange(-a, a)
        i = a
    return T


def lerp(a0, a1, w):
    return (1 - w)*a0 + w*a1

def dotGridGradient(ix, iy, x, y, G):
    
    dx = x - ix
    dy = y - iy
    
    return (dx*G[0] + dy*G[1])

def perlin_node(x, y, G, h):
    scale_factor = h #ZOOM (>1)
    
    x = x/scale_factor
    y = y/scale_factor
    x0 = int(x)
    x1 = x0 + 1
    y0 = int(y)
    y1 = y0 + 1
    
    sx = x - x0
    sy = y - y0
    
    n0 = dotGridGradient(x0, y0, x, y, G[x0][y0])
    n1 = dotGridGradient(x1, y0, x, y, G[x1][y0])
    ix0 = lerp(n0, n1, sx)
    n0 = dotGridGradient(x0, y1, x, y, G[x0][y1])
    n1 = dotGridGradient(x1, y1, x, y, G[x1][y1])
    
    ix1 = lerp(n0, n1, sx)
    value = lerp(ix0, ix1, sy)
    return value

def perlin(T):
    n = len(T)
    G = [0]*(n+1)
    for i in range(n):
        Temp = [0]*n
        for i2 in range(n):
            Temp[i2] = [random.randint(-1,1),random.randint(-1,1)]
        G[i] = Temp

    for j in range(1,7):
        for x in range(n):
            for y in range(n):
                T[x][y] += ((j/7))*perlin_node(x,y,G,2**j) #A=1 F=j

    for x in range(n):
        for y in range(n):
            T[x][y] += 3.3*perlin_node(x,y,G,2**8) #A=3.3 F=8
    
    return T

def lissage(T,power):
    size=len(T)
    C=T
    for x in range(0,size):
        for y in range(0,size):
            nb = 0
            s = C[x][y]
            for dx in range(-power,power+1):
                for dy in range(-power,power+1):
                    if x+dx >= 0 and x+dx < size and y+dy >= 0 and y+dy < size:
                        nb += 1
                        s += C[x+dx][y+dy]
            m = s/nb
            T[x][y] = m
    return T

def sigmoid_cal(v,moy):
    return 1/(1+(math.exp(-(v-moy)/3)))

def linear_cal(v,mini,maxi):
    return (v-(maxi+mini)/2)*(10/(maxi-mini))


if __name__ == '__main__':
    print("This file is not meant to be executed")
    exit(1)