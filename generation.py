# -*- coding: utf-8 -*-

import pygame as py
import time
import numpy as np
import PIL.Image as im
from terrain_utils import Terrain




diam_perl = int(input("Perlin ou Diamant (0 ou 1): "))
n = int(input("Taille du monde (2^n)+1 avec n="))
n = 2**n+1

t = Terrain(n,diam_perl)
t1 = time.time()
t.generate()
print("generation: ",time.time()-t1,"s")
pixels = t.to_pixels_map()

file_path = "rendu.png"
pixels = np.array(pixels, dtype=np.uint8)
image = im.fromarray(pixels, mode='RGB')
image.save(file_path)
print("Image enregistrée dans:", file_path)

if n < 50 or n > 1000:
    print("Terrain trop grand ou trop petit pour un affichage")
    exit(0)

#Pygame
py.init()
win = py.display.set_mode((n,n))
py.display.set_caption("Generation de terrain")

#Display
for y in range(t.size):
    for x in range(t.size):
        py.draw.rect(win, pixels[y][x], (x, y, 1, 1))
print("affichage en: ",time.time()-t1,"s")

run = True
while run:
    py.time.delay(50)
    
    
    for event in py.event.get():
        if event.type == py.QUIT:
            run = False
    
    py.display.update()
    
py.quit()
