import pygame 
from pygame import *
from math import *
import random
import numpy as np
from delaunay2D import Delaunay2D
from dijkstra import *
import numpy
from catmullromsplines import *

def generate_map(screen, colorA, points, points_spl):
	for i in range(1, len(points)):
		draw.line(screen.get_surface(), 0xFF0000, points[i - 1], points[i], 5)
	for i in range(1, len(points_spl)):
		draw.line(screen.get_surface(), 0x00FF00, points_spl[i - 1], points_spl[i], 2)

def main():
	pygame.init()

	size = (300, 400)
	colorA = (0, 128, 255)
	colorAaug = (128, 194, 255)
	delta_rad = 15
	robot_rad = 15
	points = []

	points.append((200, 50))
	points.append((180, 120))
	points.append((60, 170))
	points.append((60, 240))
	points.append((180, 360))
	points.append((180, 250))
	points.append((220, 200))
	points.append((280, 200))
	points.append((230, 170))
	points.append((240, 100))
	points.append(points[0])
	points.append(points[1])
	points.append(points[2])

	screen = pygame.display

	screen.init()
	screen.set_mode(size)
	
	pixel_arr = pygame.PixelArray(screen.get_surface())

	new_p = catmullrom_splines(points)

	generate_map(screen, colorA, points, new_p)

	screen.update()

	while 1:
		continue

if __name__ == '__main__':
	main()