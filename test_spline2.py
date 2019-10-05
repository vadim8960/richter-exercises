import pygame 
from pygame import *
from math import *
import random
import numpy as np
from delaunay2D import Delaunay2D
from dijkstra import *
import numpy

def make_derivative(p1, p2):
	return (p1[0], (p1[1] - p2[1]) / (p1[0] - p2[0]))

def make_single_spline(p1, p2, p3, p4, count):
	p_x = np.matrix([[p1[0]],[p2[0]],[p3[0]],[p4[0]]])
	p_y = np.matrix([[p1[1]],[p2[1]],[p3[1]],[p4[1]]])
	res = []
	t = 0
	m_mat = np.matrix('0 2 0 0; -1 0 1 0; 2 -5 4 -1; -1 3 -3 1')
	while (t <= 1):
		t_mat = np.matrix([1/2, t/2, (t**2)/2, (t**3)/2])
		r = t_mat * m_mat
		x = r * p_x
		y = r * p_y
		t += (1/count)
		res.append((x.item(), y.item()))
	return res

def catmullrom_splines(points):
	res = []
	p_begin = make_derivative(points[0], points[1])
	p_end = make_derivative(points[len(points) - 1], points[len(points) - 2])
	points.insert(0, p_begin)
	points.append(p_end)
	for i in range(len(points) - 3):
		c = make_single_spline(points[i], points[i + 1], points[i + 2], points[i + 3], 100)
		res.extend(c)
	points.remove(p_begin)
	points.remove(p_end)
	return res

def generate_map(screen, colorA, points, points_spl):
	for i in range(1, len(points)):
		draw.line(screen.get_surface(), 0xFF0000, points[i - 1], points[i], 5)
	for i in range(1, len(points_spl)):
		draw.line(screen.get_surface(), 0x00FF00, points_spl[i - 1], points_spl[i], 5)


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