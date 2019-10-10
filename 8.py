import pygame
from pygame import *
from math import *
import random

def calc_len_wosqrt(p1, p2):
	return sqrt(((p1[0] - p2[0]) * (p1[0] - p2[0]) + (p1[1] - p2[1]) * (p1[1] - p2[1])))

def find_shortest(set_a, set_b, delta):
	min_p = []
	for i in range(len(set_a)):
		for j in range(len(set_b)):
			if (calc_len_wosqrt(set_a[i], set_b[j]) < delta):
				flag = 1
				for k in range(len(min_p)):
					if (set_a[i] in min_p[k] or set_b[j] in min_p[k]):
						if (calc_len_wosqrt(set_a[i], set_b[j]) < min_p[k][2]):
							min_p[k][0] = set_a[i]
							min_p[k][1] = set_b[j]
							min_p[k][2] = calc_len_wosqrt(set_a[i], set_b[j])
						flag = 0

				if flag:		
					min_p.append( [set_a[i], set_b[j], calc_len_wosqrt(set_a[i], set_b[j])] )
	return min_p

def draw_map(screen, set_a, colora, set_b, colorb, shortes_way):
	for i in range(len(set_a)):
		draw.circle(screen.get_surface(), colora, set_a[i], 1)

	for i in range(len(set_b)):
		draw.circle(screen.get_surface(), colorb, set_b[i], 1)

	for i in range(len(shortes_way)):
		draw.line(screen.get_surface(), 0xFF0000, shortes_way[i][0], shortes_way[i][1], 1)

	screen.update()

def main():

	task = int(input())

	pygame.init()

	size = (1000, 1000)
	colorA = 0x00FF00
	colorB = 0x0000FF
	delta = 40

	set_a = []
	set_b = []
	if task == 1:
		set_a.append([245, 182])
		set_a.append([263, 180])
		set_a.append([287, 176])
		set_a.append([301, 181])
		set_a.append([311, 178])
		set_a.append([320, 179])
		set_a.append([330, 179])
		set_a.append([338, 176])
		set_a.append([348, 180])

		set_b.append([254, 156])
		set_b.append([296, 164])
		set_b.append([318, 168])
		set_b.append([331, 172])
		set_b.append([342, 174])

		for i in range(len(set_a)):
			set_a[i][0] *= 2
			set_a[i][1] *= 2

		for i in range(len(set_b)):
			set_b[i][0] *= 2
			set_b[i][1] *= 2
	else:
		set_a.append((699, 131))
		set_a.append((698, 198))
		set_a.append((699, 246))
		set_a.append((700, 343))

		set_b.append((660, 376))
		set_b.append((671, 310))
		set_b.append((682, 248))
		set_b.append((692, 193))

	screen = pygame.display

	screen.init()
	screen.set_mode(size, pygame.RESIZABLE)
	
	pixel_arr = pygame.PixelArray(screen.get_surface())

	draw_map(screen, set_a, colorA, set_b, colorB, find_shortest(set_a, set_b, delta))

	while 1:
		pass

if __name__ == '__main__':
	main()