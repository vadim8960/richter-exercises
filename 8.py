import pygame 
from pygame import *
from math import *
import random

def calc_len_wosqrt(p1, p2):
	return sqrt(((p1[0] - p2[0]) * (p1[0] - p2[0]) + (p1[1] - p2[1]) * (p1[1] - p2[1])))

def find_shortest(set_a, set_b):
	min_d = 10000
	min_p = []
	for i in range(len(set_a)):
		for j in range(len(set_b)):
			if (calc_len_wosqrt(set_a[i], set_b[j]) < min_d):
				min_p.append((set_a[i], set_b[j]))
				min_d = calc_len_wosqrt(set_a[i], set_b[j])
	print('Shortest way: {}\nPoint from set a: {}\nPoint from set b: {}'.format(min_d, min_p[len(min_p) - 1][0], min_p[len(min_p) - 1][1]))
	return min_p[len(min_p) - 1]

def draw_map(screen, set_a, colora, set_b, colorb, shortes_way):
	for i in range(len(set_a)):
		draw.circle(screen.get_surface(), colora, set_a[i], 1)

	for i in range(len(set_b)):
		draw.circle(screen.get_surface(), colorb, set_b[i], 1)

	draw.line(screen.get_surface(), 0xFF0000, shortes_way[0], shortes_way[1], 1)

	screen.update()

def main():
	pygame.init()

	size = (400, 400)
	colorA = 0x00FF00
	colorB = 0x0000FF

	set_a = []
	set_a.append((245, 182))
	set_a.append((263, 180))
	set_a.append((287, 176))
	set_a.append((301, 181))
	set_a.append((311, 178))
	set_a.append((320, 179))
	set_a.append((330, 179))
	set_a.append((338, 176))
	set_a.append((348, 180))

	set_b = []
	set_b.append((254, 156))
	set_b.append((296, 164))
	set_b.append((318, 168))
	set_b.append((331, 172))
	set_b.append((342, 174))

	screen = pygame.display

	screen.init()
	screen.set_mode(size, pygame.RESIZABLE)
	
	pixel_arr = pygame.PixelArray(screen.get_surface())

	draw_map(screen, set_a, colorA, set_b, colorB, find_shortest(set_a, set_b))

	while 1:
		pass

if __name__ == '__main__':
	main()