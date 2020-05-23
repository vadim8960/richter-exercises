import pygame 
from pygame import *
import random
from delaunay2D import *
from dijkstra import *
from catmullromsplines import *
import time

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

def generate_map(screen,  colorA):
	draw.line(screen.get_surface(), colorA, (0, 0), (800, 0), 20)
	draw.line(screen.get_surface(), colorA, (0, 0), (0, 400), 20)
	draw.line(screen.get_surface(), colorA, (0, 400), (800, 400), 20)
	draw.line(screen.get_surface(), colorA, (800, 400), (800, 0), 20)
	draw.line(screen.get_surface(), colorA, (400, 400), (400, 275), 20)
	draw.line(screen.get_surface(), colorA, (400, 0), (400, 125), 20)
	draw.polygon(screen.get_surface(), colorA, create_rect(180, 170, (150, 150)))
	draw.polygon(screen.get_surface(), colorA, create_rect(620, 230, (150, 150)))

# def calc_len(p1, p2):
# 	return sqrt(((p1[0] - p2[0]) * (p1[0] - p2[0]) + (p1[1] - p2[1]) * (p1[1] - p2[1])))

def generate_data_points(screen, pixel_arr, count, delta, colorA, colorAaug, p_b, p_m, p_e, size):
	i = 0
	color = (255, 255, 255)
	count_loop = 0
	point_arr = []
	point_arr.append(p_b)
	point_arr.append(p_m)
	point_arr.append(p_e)
	draw.circle(screen.get_surface(), (255, 0, 0), p_b, 1)
	draw.circle(screen.get_surface(), (0, 255, 0), p_m, 1)
	draw.circle(screen.get_surface(), (255, 0, 0), p_e, 1)
	while (i < count):
		count_loop += 1
		x = int(random.randint(0, size[0] - 1))
		y = int(random.randint(0, size[1] - 1))
		if (pixel_arr[x, y] == screen.get_surface().map_rgb((0, 0, 0))):
			flag = 1
			for j in range(0, len(point_arr)):
				if (calc_len([x, y], point_arr[j]) < delta):
					flag = 0
					count_loop += 1
					break

			if flag:
				point_arr.append((x, y))
				pixel_arr[x, y] = color
				screen.update()
				time.sleep(0.01)
				i += 1
				count_loop = 0
			elif count_loop > count:
				i = count
	print('Count data points: {}'.format(len(point_arr)))
	return point_arr

def check_collision(screen, pixel_arr, p_begin, p_end, delta):
	if (pixel_arr[(p_begin[0] + p_end[0]) // 2, (p_begin[1] + p_end[1]) // 2] != screen.get_surface().map_rgb((0, 0, 0))):
		return 0
	flag_vertic = 0
	if (p_begin[0] == p_end[0]):
		flag_vertic = 1
	else:
		A = p_begin[1] - p_end[1]
		B = p_end[0] - p_begin[0]
		C = p_begin[0] * p_end[1] - p_end[0] * p_begin[1]
		k = -float(A) / float(B)
		v = -float(C) / float(B)

	if (flag_vertic == 0):
		s_p = min(p_begin[0], p_end[0]) + 3
		s_e = max(p_begin[0], p_end[0]) - 3
		for i in range(s_p, s_e):
			if (pixel_arr[i, int(k * i + v)] != screen.get_surface().map_rgb((0, 0, 0))):
				return 0
	else:
		s_p = min(p_begin[1], p_end[1]) + 3
		s_e = max(p_begin[1], p_end[1]) - 3
		for i in range(s_p, s_e):
			if (pixel_arr[p_begin[0], i] != screen.get_surface().map_rgb((0, 0, 0))):
				return 0
		
	return 1

def draw_triangulation_lines(screen, pixel_arr, points, delta, graph):
	flag = 0
	dt = Delaunay2D()
	seeds = np.array(points)
	for i in seeds:
		dt.addPoint(i)
	tr = dt.exportTriangles()
	print('Count triangles: {}'.format(len(tr)))
	for i in range(0, len(tr)):
		if (check_collision(screen, pixel_arr, points[tr[i][0]], points[tr[i][1]], delta)):
			draw.line(screen.get_surface(), (255, 255, 255), points[tr[i][0]], points[tr[i][1]], 1)
			graph.add_edge(tr[i][0], tr[i][1], calc_len(points[tr[i][0]], points[tr[i][1]]))
			flag = 1

		if (check_collision(screen, pixel_arr, points[tr[i][1]], points[tr[i][2]], delta)):
			draw.line(screen.get_surface(), (255, 255, 255), points[tr[i][1]], points[tr[i][2]], 1)
			graph.add_edge(tr[i][1], tr[i][2], calc_len(points[tr[i][1]], points[tr[i][2]]))
			flag = 1

		if (check_collision(screen, pixel_arr, points[tr[i][0]], points[tr[i][2]], delta)):
			draw.line(screen.get_surface(), (255, 255, 255), points[tr[i][0]], points[tr[i][2]], 1)
			graph.add_edge(tr[i][0], tr[i][2], calc_len(points[tr[i][0]], points[tr[i][2]]))
			flag = 1
		
		if (flag):
			screen.update()
			time.sleep(0.01)
			flag = 0

def draw_way(screen, graph, points, color_way):
	way_to_cent, l1 = dijkstra(graph, 0, 1)	
	print('Way from point A to center {}'.format(way_to_cent))
	way_to_end, l2 = dijkstra(graph, 1, 2)	
	print('Way from point center to B {}'.format(way_to_end))

	way = []
	spline_points = []
	way.extend(way_to_cent)
	way.extend(way_to_end[1:])
	for i in range(len(way)):
		spline_points.append(points[way[i]])

	spline_points = catmullrom_splines(spline_points)

	print('Total length with center point: {}'.format(l1 + l2))

	for i in range(1, len(way)):
		draw.line(screen.get_surface(), color_way, points[way[i]], points[way[i - 1]], 2)
		screen.update()
		time.sleep(0.1)
	for i in range(1, len(spline_points)):
		draw.line(screen.get_surface(), 0x00FF00, spline_points[i - 1], spline_points[i], 4)
		screen.update()
		time.sleep(0.005)

def main():
	pygame.init()

	size = (800, 400)
	colorA = (0, 128, 255)
	colorAaug = (128, 194, 255)
	delta_rad = 27
	robot_rad = 15
	start_point = (50, 70)
	middle_point = (400, 200)
	end_point = (750, 200)

	screen = pygame.display

	screen.init()
	screen.set_mode(size, pygame.RESIZABLE)
	time.sleep(3)
	
	pixel_arr = pygame.PixelArray(screen.get_surface())

	generate_map(screen, colorA)
	for i in range(1, size[0] - 1):
		for j in range(1, size[1] - 1):
			if (check_coun(screen, pixel_arr, i, j, colorA)):
				draw.circle(screen.get_surface(), colorAaug, (i, j), robot_rad)
				generate_map(screen, colorA)
		screen.update()

	points = generate_data_points(screen, pixel_arr, 1000, delta_rad, colorA, colorAaug, start_point, middle_point, end_point, size)
	graph = GraphUndirectedWeighted(len(points))
	draw_triangulation_lines(screen, pixel_arr, points, delta_rad, graph)
	draw.circle(screen.get_surface(), (255, 0, 0), start_point, 5)
	draw.circle(screen.get_surface(), (0, 255, 0), middle_point, 5)
	draw.circle(screen.get_surface(), (255, 0, 0), end_point, 5)
	draw_way(screen, graph, points, 0xFF0000)
	screen.update()

	while 1:
		continue

if __name__ == '__main__':
	main()