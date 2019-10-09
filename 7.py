import pygame 
from pygame import *
from math import *
import random

def d2r(d):
	return (d / 57.296)

def g_f(x, s, m):
	return ( 1/(sqrt(2*pi)*s)*e**(-0.5*(float(x-m)/s)**2) )

def gauss_function(sigma, m, n):
	b = m - n / 3
	e = m + n / 3
	step = (e - b) / n
	arr = []
	for i in range(n):
		arr.append((int(b), 10000000 * g_f(b, sigma, m)))
		b += step
	return arr

def get_rand_elem(list_d):
	return list_d[random.randint(0, len(list_d) - 1)]

def get_unique(arr):
	res = []
	res.append(arr[0])
	iter = 0
	for i in range(1, len(arr)):
		if (arr[i][0] == res[iter][0]):
			continue
		res.append(arr[i])
		iter += 1
	return res

def rand_color():
	return ( random.randint(0, 0xFFFFFF) )

def calc_end_points(p_b, ang, sigma_a, dist, sigma_d, n):
	gauss_points_dist = get_unique(gauss_function(sigma_d, dist, n))
	gauss_points_ang = get_unique(gauss_function(sigma_a, ang, n))
	print('{} \n {}'.format(gauss_points_ang, gauss_points_dist))

	prob_array_d = []
	prob_array_a = []
	p_ends = []

	for i in range(len(gauss_points_dist)):
		for j in range(int(gauss_points_dist[i][1])):
			prob_array_d.append(gauss_points_dist[i][0])


	for i in range(len(gauss_points_ang)):
		for j in range(int(gauss_points_ang[i][1])):
			prob_array_a.append(gauss_points_ang[i][0])

	for i in range(n):
		a = d2r(get_rand_elem(prob_array_a))
		d = get_rand_elem(prob_array_d)
		p_ends.append(( int(p_b[0] + d * cos(a)), int(p_b[1] + d * sin(a)) ))

	return p_ends

def main():
	pygame.init()

	size = (400, 400)
	colorA = (0, 128, 255)
	colorAaug = (128, 194, 255)
	point_st = (100, 100)
	angle = 45
	dist = 100
	sigma_d = 5
	sigma_a = 5
	count_p = 50000

	screen = pygame.display

	screen.init()
	screen.set_mode(size, pygame.RESIZABLE)
	
	pixel_arr = pygame.PixelArray(screen.get_surface())

	draw.circle(screen.get_surface(), colorA, point_st, 5)

	points_end = calc_end_points(point_st, angle, sigma_a, dist, sigma_d, count_p)

	for i in range(len(points_end)):
		pixel_arr[points_end[i]] = rand_color()
		# pixel_arr[points_end[i]] = 0xFFFFFF

	screen.update()

	while 1:
		pass


if __name__ == '__main__':
	main()