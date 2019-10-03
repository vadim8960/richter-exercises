import pygame 
from pygame import *
from math import *
import random
import numpy as np
from delaunay2D import Delaunay2D
import dijkstra 

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

def generate_data_points(screen, pixel_arr, count, delta, colorA, colorAaug, p_b, p_m, p_e):
	i = 0
	count_loop = 0
	point_arr = []
	point_arr.append(p_b)
	point_arr.append(p_m)
	point_arr.append(p_e)
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
	draw.circle(screen.get_surface(), 0xFF0000, p_b, 3)
	draw.circle(screen.get_surface(), 0xFF0000, p_m, 3)
	draw.circle(screen.get_surface(), 0xFF0000, p_e, 3)
	return point_arr

def check_repeat_lines(screen, pixel_arr, p_begin, p_end, end_r):
	x_c = abs(p_begin[0] + p_end[0]) // 2
	y_c = abs(p_begin[1] + p_end[1]) // 2
	if end_r:
		if (pixel_arr[x_c, y_c] == screen.get_surface().map_rgb((0, 0, 0))):
			return 1
		else:
			return 0
	if (pixel_arr[x_c, y_c] == screen.get_surface().map_rgb((0, 0, 0))):
		return (check_repeat_lines(screen, pixel_arr, [x_c, y_c], p_end, 1) and 
			    check_repeat_lines(screen, pixel_arr, p_begin, [x_c, y_c], 1))
	else:
		return 0

def draw_triangulation_lines(screen, pixel_arr, points, delta):
	dt = Delaunay2D()
	seeds = np.array(points)
	for i in seeds:
		dt.addPoint(i)
	tr = dt.exportTriangles()
	print(len(tr))
	for i in range(0, len(tr)):
		if (calc_len_wosqrt(points[tr[i][0]], points[tr[i][1]]) <= delta * delta * delta and 
			check_repeat_lines(screen, pixel_arr, points[tr[i][0]], points[tr[i][1]], 0)):
			draw.line(screen.get_surface(), (255, 255, 255), points[tr[i][0]], points[tr[i][1]], 1)
		if (calc_len_wosqrt(points[tr[i][1]], points[tr[i][2]]) <= delta * delta * delta and 
			check_repeat_lines(screen, pixel_arr, points[tr[i][1]], points[tr[i][2]], 0)):
			draw.line(screen.get_surface(), (255, 255, 255), points[tr[i][1]], points[tr[i][2]], 1)
		if (calc_len_wosqrt(points[tr[i][0]], points[tr[i][2]]) <= delta * delta * delta and
			check_repeat_lines(screen, pixel_arr, points[tr[i][0]], points[tr[i][2]], 0)):
			draw.line(screen.get_surface(), (255, 255, 255), points[tr[i][0]], points[tr[i][2]], 1)

def main():
	pygame.init()

	size = (800, 400)
	colorA = (0, 128, 255)
	colorAaug = (128, 194, 255)
	delta_rad = 13
	start_point = (200, 300)
	end_point = (600, 100)
	middle_point = (400, 200)

	screen = pygame.display

	screen.init()
	screen.set_mode(size)
	
	pixel_arr = pygame.PixelArray(screen.get_surface())

	generate_map(screen, colorA)
	for i in range(1, size[0] - 1):
		for j in range(1, size[1] - 1):
			if (check_coun(screen, pixel_arr, i, j, colorA)):
				draw.circle(screen.get_surface(), colorAaug, (i, j), 25)
				generate_map(screen, colorA)

	p = generate_data_points(screen, pixel_arr, 600, delta_rad, colorA, colorAaug, start_point, middle_point, end_point)
	draw_triangulation_lines(screen, pixel_arr, p, delta_rad)
	screen.update()

	while 1:
		continue

if __name__ == '__main__':
	main()