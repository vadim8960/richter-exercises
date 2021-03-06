import pygame
from pygame import *
from math import *
import random
import time

def d2r(d):
	return (d / 57.296)

def r2d(r):
	return int(r * 57.296)

def g_f(x, s, m):
	return ( 1/(sqrt(2*pi)*s)*e**(-0.5*(float(x-m)/s)**2) )

def gauss_function(sigma, m, n):
	b = m - n
	e = m + n

	step = (e - b) / n
	arr = []
	for i in range(n):
		arr.append((int(b), 1000 * g_f(b, sigma, m)))
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

def get_rand_elem(list_d):
	return list_d[random.randint(0, len(list_d) - 1)]

def check_coun(screen, pixel_arr, x, y, color):
	if ((((pixel_arr[x + 1, y] == screen.get_surface().map_rgb(color) or pixel_arr[x - 1, y] == screen.get_surface().map_rgb(color)) ^
		  (pixel_arr[x, y + 1] == screen.get_surface().map_rgb(color) or pixel_arr[x, y - 1] == screen.get_surface().map_rgb(color))) or 
	     ((pixel_arr[x, y + 1] == screen.get_surface().map_rgb(color) or pixel_arr[x - 1, y] == screen.get_surface().map_rgb(color))^
	      (pixel_arr[x + 1, y + 1] == screen.get_surface().map_rgb(color) or pixel_arr[x, y - 1] == screen.get_surface().map_rgb(color)))) or 
	    (((pixel_arr[x + 1, y] == screen.get_surface().map_rgb(color) or pixel_arr[x, y + 1] == screen.get_surface().map_rgb(color)) ^
		  (pixel_arr[x + 1, y + 1] == screen.get_surface().map_rgb(color) or pixel_arr[x, y - 1] == screen.get_surface().map_rgb(color))) or 
	     ((pixel_arr[x + 1, y + 1] == screen.get_surface().map_rgb(color) or pixel_arr[x - 1, y] == screen.get_surface().map_rgb(color))^
	      (pixel_arr[x - 1, y + 1] == screen.get_surface().map_rgb(color) or pixel_arr[x, y - 1] == screen.get_surface().map_rgb(color))))): 
		return 1
	return 0

def create_rect(x, y, size):
	return [ [x - size[0] / 2, y - size[1] / 2],
			 [x + size[0] / 2, y - size[1] / 2],
			 [x + size[0] / 2, y + size[1] / 2],
			 [x - size[0] / 2, y + size[1] / 2]]

def get_random_angle():
	return d2r(random.randint(0, 360))

def generate_map(screen, colorA):
	draw.line(screen.get_surface(), colorA, (0, 0), (900, 0), 10)
	draw.line(screen.get_surface(), colorA, (0, 0), (0, 600), 10)
	draw.line(screen.get_surface(), colorA, (0, 600), (900, 600), 10)
	draw.line(screen.get_surface(), colorA, (900, 600), (900, 0), 10)

	draw.line(screen.get_surface(), colorA, (450, 600), (450, 200), 10)
	draw.line(screen.get_surface(), colorA, (450, 200), (750, 200), 10)
	draw.line(screen.get_surface(), colorA, (320, 0), (320, 200), 10)
	draw.line(screen.get_surface(), colorA, (700, 600), (700, 420), 10)
	# draw.line(screen.get_surface(), colorA, (225, 450), (225, 200), 10)

	draw.polygon(screen.get_surface(), colorA, create_rect(225, 190, (200, 125)))
	draw.circle(screen.get_surface(), colorA, (225, 450), 75)
	draw.polygon(screen.get_surface(), colorA, create_rect(675, 420, (250, 30)))
	# draw.circle(screen.get_surface(), colorA, (670, 190), 140)

def draw_minkovsky_sum(screen, pixel_arr, colorA, colorAaug, robot_rad, size):
	for i in range(1, size[0] - 1):
		for j in range(1, size[1] - 1):
			if (check_coun(screen, pixel_arr, i, j, colorA)):
				draw.circle(screen.get_surface(), colorAaug, (i, j), robot_rad)
				generate_map(screen, colorA)
	screen.update()

def calc_len_wosqrt(p1, p2):
	return int(sqrt(((p1[0] - p2[0]) * (p1[0] - p2[0]) + (p1[1] - p2[1]) * (p1[1] - p2[1]))))

def generate_data_points(screen, pixel_arr, count, delta, colorA, colorAaug, size):
	i = 0
	count_loop = 0
	point_arr = []
	color = (255, 255, 255)
	while (i < count):
		count_loop += 1
		x = int(random.randint(0, size[0] - 1))
		y = int(random.randint(0, size[1] - 1))
		if (pixel_arr[x, y] == screen.get_surface().map_rgb((0, 0, 0))):
			flag = 1
			for j in range(0, len(point_arr)):
				if (calc_len_wosqrt([x, y], point_arr[j][0]) < delta):
					flag = 0
					count_loop += 1
					break

			if flag:
				ang = get_random_angle()
				point_arr.append([(x, y), ang, 0,])
				draw.line(screen.get_surface(), 0xFFFFFF, (x, y), (int(x + 6 * cos(ang)), int(y + 6 * sin(ang))), 1)
				draw.circle(screen.get_surface(), 0xFFFFFF, (x, y), 2)
				# pixel_arr[x, y] = color
				i += 1
				count_loop = 0
			elif count_loop >= count:
				i = count
	print('Count data points: {}'.format(len(point_arr)))
	return point_arr

def generate_robot(screen, pixel_arr, size, color):
	res = []
	while 1:
		x = int(random.randint(0, size[0] - 1))
		y = int(random.randint(0, size[1] - 1))
		if (pixel_arr[x, y] == screen.get_surface().map_rgb((0, 0, 0))):
			ang = get_random_angle()
			res.append([(x, y), ang, 0])
			draw.line(screen.get_surface(), color, (x, y), (int(x + 6 * cos(ang)), int(y + 6 * sin(ang))), 1)
			draw.circle(screen.get_surface(), color, (x, y), 2)
			break
	return res

def calc_dist_lidar_beam(screen, pixel_arr, part, color):
	for i in range(len(part)):
		dist = 0
		ang = part[i][1]
		x = part[i][0][0]
		y = part[i][0][1]
		while 1:
			new_x = int(x + dist * cos(ang))
			new_y = int(y + dist * sin(ang))
			if (pixel_arr[new_x, new_y] == screen.get_surface().map_rgb(color)):
				dist -= 1
				break

			pixel_arr[new_x, new_y] = 0xFFFFFF
			dist += 1
		part[i][2] = dist

def draw_particles(screen, pixel_arr, part, color):
	for i in range(len(part)):
		draw.circle(screen.get_surface(), color, (part[i][0][0], part[i][0][1]), 2)
		draw.line(screen.get_surface(), color, (part[i][0][0], part[i][0][1]),
		             (int(part[i][0][0] + 6 * cos(part[i][1])), int(part[i][0][1] + 6 * sin(part[i][1]))), 1)

def calc_probabilities(particles, robot, delta):
	dist = robot[0][2]
	max_prob = 0
	for i in range(len(particles)):
		particles[i][2] = exp( -(float((particles[i][2] - dist))**2)/(2 * delta**2) )

		if (particles[i][2] > max_prob):
			max_prob = particles[i][2]
	return max_prob

def remove_small_prob_part(particles, robot, delta):
	max_prob = calc_probabilities(particles, robot, delta)

	#             TODO:
	# Reduce max count of particles by 10%

	count_loop = int(len(particles) * 0.1)

	print('Before remove: {}'.format(len(particles)))
	for i in range(count_loop):
		index = 0
		min_p = 1000000
		for j in range(len(particles)):
			if (particles[i][2] < min_p):
				inxed = j
				min_p = particles[j][2]
		particles.remove(particles[index])

	count_remove = len(particles)
	print('After remove: {}\n-----------------------'.format(count_remove))

	res = []
	for i in range(len(particles)):
		if (particles[i][2] > 0.5 * max_prob):
			res.append(particles[i])
			count_remove -= 1
	return res, count_remove

def norm_particles(particles):
	s = 0
	for i in range(len(particles)):
		s += particles[i][2]
	for i in range(len(particles)):
		particles[i][2] /= s

def generate_gauss_particles(particles, count_remove, sigma_a, sigma_d):
	res = []
	for i in range(len(particles)):
		res.append(particles[i])
		count_new_p = int(particles[i][2] * count_remove * 0.5)

		gauss_points_x = get_unique(gauss_function(sigma_d, particles[i][0][0], 100))
		gauss_points_y = get_unique(gauss_function(sigma_d, particles[i][0][1], 100))
		gauss_points_ang = get_unique(gauss_function(sigma_a, r2d(particles[i][1]), 100))

		prob_array_x = []
		prob_array_y = []
		prob_array_a = []
		p_ends = []

		for j in range(len(gauss_points_x)):
			for k in range(int(gauss_points_x[j][1])):
				prob_array_x.append(gauss_points_x[j][0])

		for j in range(len(gauss_points_y)):
			for k in range(int(gauss_points_y[j][1])):
				prob_array_y.append(gauss_points_y[j][0])

		for j in range(len(gauss_points_ang)):
			for k in range(int(gauss_points_ang[j][1])):
				prob_array_a.append(gauss_points_ang[j][0])

		for j in range(count_new_p):
			a = d2r(get_rand_elem(prob_array_a))
			x = get_rand_elem(prob_array_x)
			y = get_rand_elem(prob_array_y)
			res.append([(x, y), a, 0])
	return res

def shift_particles(particles, robot, delta):
	res_p = []
	res_r = []
	for i in range(len(particles)):
		x = int(particles[i][0][0] + delta * cos(particles[i][1]))
		y = int(particles[i][0][1] + delta * sin(particles[i][1]))

		res_p.append([(x, y), particles[i][1], 0])

	x = int(robot[0][0][0] + delta * cos(robot[0][1]))
	y = int(robot[0][0][1] + delta * sin(robot[0][1]))
	res_r.append([(x, y), robot[0][1], 0])
	return res_p, res_r
	
def check_particles(screen, pixel_arr, particles, size, delta, color):
	res = []
	for i in range(len(particles)):
		if (particles[i][0][0] < 0 or particles[i][0][0] >= size[0] or
			particles[i][0][1] < 0 or particles[i][0][1] >= size[1] or 
		  ((particles[i][0][0] < delta * 2 or particles[i][0][0] >= size[0] - delta * 2) and
		   (particles[i][0][1] < delta * 2 or particles[i][0][1] >= size[1] - delta * 2))):
			continue
		if (pixel_arr[particles[i][0][0], particles[i][0][1]] == screen.get_surface().map_rgb(color)):
			continue
		res.append(particles[i])
	return res

def rotate_particles(particles, robot, ang):
	robot[0][1] += d2r(ang)
	for i in range(len(particles)):
		particles[i][1] += d2r(ang)

def move_new_position(screen, pixel_arr, robot, color):
	max_a = 0
	max_d = -1
	res = []
	for i in range(360):
		robot[0][1] = d2r(i)
		calc_dist_lidar_beam(screen, pixel_arr, robot, color)
		if (robot[0][2] > max_d):
			max_d = robot[0][2]
			max_a = i

	# robot[0][0][0] = robot[0][0][0] + 0.5 * max_d * cos(d2r(max_a))
	# robot[0][0][1] = robot[0][0][1] + 0.5 * max_d * sin(d2r(max_a))
	# robot[0][1] = d2r(max_a)
	res.append([(int(robot[0][0][0] + 0.5 * max_d * cos(d2r(max_a))), int(robot[0][0][1] + 0.5 * max_d * sin(d2r(max_a)))),
	               d2r(max_a), 0])
	return res

def main():
	size = (900, 600)
	colorA = (0, 128, 255)
	colorAaug = (128, 194, 255)
	colorRobot = 0xFF0000
	delta_rad = 15
	count_particles = 2500
	sigma_d = 15
	sigma_a = 10

	pygame.init()
	screen = pygame.display
	screen.init()
	screen.set_mode(size, pygame.RESIZABLE)
	pixel_arr = pygame.PixelArray(screen.get_surface())

	generate_map(screen, colorA)
	draw_minkovsky_sum(screen, pixel_arr, colorA, colorAaug, delta_rad, size)
	particles = generate_data_points(screen, pixel_arr, count_particles, delta_rad, colorA, colorAaug, size)
	robot = generate_robot(screen, pixel_arr, size, colorRobot)
	draw_minkovsky_sum(screen, pixel_arr, colorA, 0x000000, delta_rad, size)
	screen.update()

	while 1:
		particles = check_particles(screen, pixel_arr, particles, size, delta_rad, colorA)

		calc_dist_lidar_beam(screen, pixel_arr, particles, colorA)
		calc_dist_lidar_beam(screen, pixel_arr, robot, colorA)

		particles, count_remove = remove_small_prob_part(particles, robot, delta_rad) 
		
		norm_particles(particles)
		particles = generate_gauss_particles(particles, count_particles, sigma_a, sigma_d)

		# particles, robot = shift_particles(particles, robot, delta_rad)
		pixel_arr[:][:] = 0x000000
		draw_particles(screen, pixel_arr, particles, 0xFFFFFF)
		draw_particles(screen, pixel_arr, robot, colorRobot)
		generate_map(screen, colorA)
		screen.update()
		sigma_d -= 0.5
		if (not sigma_d):
			sigma_d = 10
		if (not len(particles)):
			sigma_d = 15
			robot = move_new_position(screen, pixel_arr, robot, colorA)
			# particles, robot = shift_particles(particles, robot, delta_rad)
			generate_map(screen, colorA)
			draw_minkovsky_sum(screen, pixel_arr, colorA, colorAaug, delta_rad, size)
			particles = generate_data_points(screen, pixel_arr, count_particles, delta_rad, colorA, colorAaug, size)
			draw_minkovsky_sum(screen, pixel_arr, colorA, 0x000000, delta_rad, size)
			screen.update()

		rotate_particles(particles, robot, 13)

	while 1:
		pass


if __name__ == '__main__':
	main()
