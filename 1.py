import pygame
from pygame import *
from math import *

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
	if (pixel_arr[x + 1, y] == screen.get_surface().map_rgb(color) or
		pixel_arr[x - 1, y] == screen.get_surface().map_rgb(color) or
		pixel_arr[x, y + 1] == screen.get_surface().map_rgb(color) or
		pixel_arr[x, y - 1] == screen.get_surface().map_rgb(color)): 
		return 1
	return 0

def main():
	pygame.init()

	size = (400, 400)
	center_circle = (100, 100)
	rad_circle = 20
	colorA = (0, 128, 255)
	colorB = (255, 0, 0)
	colorAaug = (128, 194, 255)

	screen = pygame.display

	points = [[35, 35], [-35, 35], [-35, -35], [35, -35]]
	rot_mat = [[cos(-3.14 / 6), -sin(-3.14 / 6)], [sin(-3.14 / 6), cos(-3.14 / 6)]]

	rot_points = matrixmult(points, rot_mat)
			
	for i in range(0, len(rot_points)):
		for j in range(0, len(rot_points[i])):
			rot_points[i][j] = int(250 + rot_points[i][j])

	screen.init()
	screen.set_mode(size)
	draw.polygon(screen.get_surface(), colorA, rot_points)
	draw.circle(screen.get_surface(), colorB, center_circle, rad_circle)
	pixel_arr = pygame.PixelArray(screen.get_surface())

	for i in range(1, size[0] - 1):
		for j in range(1, size[1] - 1):
			if (check_coun(screen, pixel_arr, i, j, colorA)):
				draw.circle(screen.get_surface(), colorAaug, (i, j), rad_circle)
				draw.polygon(screen.get_surface(), colorA, rot_points)

		screen.update()

	while 1:
		continue


if __name__ == '__main__':
	main()