import pygame
import pygame.gfxdraw
from pygame import *
from math import *
import time

def matrixmult(m1,m2):
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

def draw_polygon(screen, color, rot_points):
	draw.polygon(screen.get_surface(), color, ((rot_points[0][0], rot_points[0][1]), (rot_points[1][0], rot_points[1][1]), 
											   (rot_points[2][0], rot_points[2][1]), (rot_points[3][0], rot_points[3][1])))

# pixel_arr[x + 1, y + 1] == color and
# 		pixel_arr[x + 1, y - 1] == color and
# 		pixel_arr[x - 1, y + 1] == color and
# 		pixel_arr[x - 1, y - 1] == color

def check_coun(screen, pixel_arr, x, y, color):
	if (pixel_arr[x + 1, y] == screen.get_surface().map_rgb(color) and
		pixel_arr[x - 1, y] == screen.get_surface().map_rgb(color) and
		pixel_arr[x, y + 1] == screen.get_surface().map_rgb(color) and
		pixel_arr[x, y - 1] == screen.get_surface().map_rgb(color)): 
		return 0
	return 1

pygame.init()

size = (400, 400)
center_circle = (100, 100)
rad_circle = 41
colorA = (0, 128, 255)
colorB = (255, 0, 0)
colorAaug = (128, 194, 255)

screen = pygame.display

points = [[35, 35], [-35, 35], [-35, -35], [35, -35]]
rot_mat = [[cos(30), -sin(30)], [sin(30), cos(30)]]

rot_points = matrixmult(points, rot_mat)
		
for i in range(0, len(rot_points)):
	for j in range(0, len(rot_points[i])):
		rot_points[i][j] = int(250 + rot_points[i][j])

screen.init()
screen.set_mode(size)

draw_polygon(screen, colorA, rot_points)
draw.circle(screen.get_surface(), colorB, center_circle, rad_circle)
my_draw = pygame.gfxdraw
pixel_arr = pygame.PixelArray(screen.get_surface())

screen.update()

for i in range(1, size[0] - 1):
	for j in range(1, size[1] - 1):
		if (check_coun(screen, pixel_arr, i, j, colorA)):
			draw.circle(screen.get_surface(), colorAaug, (i, j), rad_circle)
			draw_polygon(screen, colorA, rot_points)
			screen.update()
			# time.sleep(0.1)

while 1:
	continue