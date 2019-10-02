import pygame 
from pygame import *
from math import *
import random
import numpy as np
from delaunay2D import Delaunay2D

def matrixmult(m1, m2):
    s = 0
    t = []
    m3 = []
    if len(m2) != len(m1[0]):
        print("you can't")
    else:
        r1 = len(m1)
        c1 = len(m1[0])
        r2 = c1
        c2 = len(m2[0])
        for z in range(0, r1):
            for j in range(0, c2):
                for i in range(0, c1):
                   s = s + m1[z][i] * m2[i][j]
                t.append(s)
                s = 0
            m3.append(t)
            t = []           
    return m3

def check_coun(screen, pixel_arr, x, y, color):
	if ((pixel_arr[x + 1, y] == screen.get_surface().map_rgb(color) or
		pixel_arr[x - 1, y] == screen.get_surface().map_rgb(color)) ^
		(pixel_arr[x, y + 1] == screen.get_surface().map_rgb(color) or
		pixel_arr[x, y - 1] == screen.get_surface().map_rgb(color))): 
		return 1
	return 0

def create_rect(x, y, size):
	return [ [x - size[0]/2, y - size[1]/2],
			 [x + size[0]/2, y - size[1]/2],
			 [x + size[0]/2, y + size[1]/2],
			 [x - size[0]/2, y + size[1]/2]]

def move_rect(x, y, arr):
	outarr = [[0, 0], [0, 0], [0, 0], [0, 0]]
	for i in range(0, len(arr)):
		outarr[i][0] = int(x + arr[i][0])
		outarr[i][1] = int(y + arr[i][1])
	return outarr

def generate_map(screen, colorA):
	draw.line(screen.get_surface(), colorA, (0, 0), (800, 0), 20)
	draw.line(screen.get_surface(), colorA, (0, 0), (0, 400), 20)
	draw.line(screen.get_surface(), colorA, (0, 400), (800, 400), 20)
	draw.line(screen.get_surface(), colorA, (800, 400), (800, 0), 20)
	draw.line(screen.get_surface(), colorA, (400, 400), (400, 275), 20)
	draw.line(screen.get_surface(), colorA, (400, 0), (400, 125), 20)
	draw.polygon(screen.get_surface(), colorA, create_rect(180, 170, (150, 150)))
	draw.polygon(screen.get_surface(), colorA, create_rect(620, 230, (150, 150)))

def calc_len_wosqrt(p1, p2):
	return ((p1[0] - p2[0]) * (p1[0] - p2[0]) + (p1[1] - p2[1]) * (p1[1] - p2[1]))

def generate_data_points(screen, pixel_arr, count, delta, colorA, colorAaug):
	i = 0
	count_loop = 0
	point_arr = []
	color = (255, 255, 255)
	while (i < count):
		count_loop += 1
		x = int(random.randint(0, 799))
		y = int(random.randint(0, 399))
		if (pixel_arr[x, y] == screen.get_surface().map_rgb((0, 0, 0))):
			flag = 1
			for j in range(0, len(point_arr)):
				if (calc_len_wosqrt([x, y], point_arr[j]) < delta * delta):
					flag = 0
					count_loop += 1
					break

			if flag:
				point_arr.append((x, y))
				pixel_arr[x, y] = color
				i += 1
				count_loop = 0
			elif count_loop > count:
				i = count
	print(len(point_arr))
	return point_arr

def draw_triangulation_lines(screen, pixel_arr, points, delta):
	dt = Delaunay2D()
	seeds = np.array(points)
	for i in seeds:
		dt.addPoint(i)
	tr = dt.exportTriangles()
	print(len(tr))
	for i in range(0, len(tr)):
		if (calc_len_wosqrt(points[tr[i][0]], points[tr[i][1]]) <= delta * delta * delta - 3 * delta):
			draw.line(screen.get_surface(), (255, 255, 255), points[tr[i][0]], points[tr[i][1]], 1)
		if (calc_len_wosqrt(points[tr[i][1]], points[tr[i][2]]) <= delta * delta * delta - 3 * delta):
			draw.line(screen.get_surface(), (255, 255, 255), points[tr[i][1]], points[tr[i][2]], 1)
		if (calc_len_wosqrt(points[tr[i][0]], points[tr[i][2]]) <= delta * delta * delta - 3 * delta):
			draw.line(screen.get_surface(), (255, 255, 255), points[tr[i][0]], points[tr[i][2]], 1)


def main():
	pygame.init()

	size = (800, 400)
	colorA = (0, 128, 255)
	colorAaug = (128, 194, 255)
	delta_angle = 0.05
	delta_rad = 10

	ang = 3.14 / 4
	rot_mat = [[cos(ang), -sin(ang)], [sin(ang), cos(ang)]]
	rotation_rect = matrixmult(create_rect(0, 0, (23, 71)), rot_mat)

	screen = pygame.display

	screen.init()
	screen.set_mode(size)
	
	pixel_arr = pygame.PixelArray(screen.get_surface())

	generate_map(screen, colorA)
	while 1:
		for i in range(1, size[0] - 1):
			for j in range(1, size[1] - 1):
				if (check_coun(screen, pixel_arr, i, j, colorA)):
					points = move_rect(i, j, rotation_rect)
					draw.polygon(screen.get_surface(), colorAaug, points)
					# draw.circle(screen.get_surface(), colorAaug, (i, j), 40)
					generate_map(screen, colorA)
		p = generate_data_points(screen, pixel_arr, 1000, delta_rad, colorA, colorAaug)
		draw_triangulation_lines(screen, pixel_arr, p, delta_rad)
		screen.update()
		pixel_arr[0:799, 0:400] = 0x000000
		generate_map(screen, colorA)
		ang += delta_angle
		rot_mat = [[cos(ang), -sin(ang)], [sin(ang), cos(ang)]]
		rotation_rect = matrixmult(create_rect(0, 0, (23, 71)), rot_mat)
	while 1:
		continue

if __name__ == '__main__':
	main()