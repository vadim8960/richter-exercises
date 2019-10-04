import pygame 
from pygame import *
from math import *
import random
import numpy as np
from delaunay2D import Delaunay2D
from dijkstra import *
import numpy

def CatmullRomSpline(P0, P1, P2, P3, nPoints=100):
  P0, P1, P2, P3 = map(numpy.array, [P0, P1, P2, P3])

  alpha = 0.5
  def tj(ti, Pi, Pj):
    xi, yi = Pi
    xj, yj = Pj
    return ( ( (xj - xi)**2 + (yj - yi)**2 )**0.5 )**alpha + ti

  t0 = 0.5
  t1 = tj(t0, P0, P1)
  t2 = tj(t1, P1, P2)
  t3 = tj(t2, P2, P3)

  t = numpy.linspace(t1,t2,nPoints)

  t = t.reshape(len(t),1)
  
  A1 = (t1 - t) / (t1 - t0) * P0 + (t - t0) / (t1 - t0) * P1
  A2 = (t2 - t) / (t2 - t1) * P1 + (t - t1) / (t2 - t1) * P2
  A3 = (t3 - t) / (t3 - t2) * P2 + (t - t2) / (t3 - t2) * P3

  B1 = (t2 - t) / (t2 - t0) * A1 + (t - t0) / (t2 - t0) * A2
  B2 = (t3 - t) / (t3 - t1) * A2 + (t - t1) / (t3 - t1) * A3

  C  = (t2 - t) / (t2 - t1) * B1 + (t - t1) / (t2 - t1) * B2
  return C

def CatmullRomChain(P):
  sz = len(P)
  C = []
  for i in range(sz - 3):
    c = CatmullRomSpline(P[i], P[i + 1], P[i + 2], P[i + 3], 100)
    C.extend(c)
  return C

def generate_map(screen, colorA, points, points_spl):
	for i in range(1, len(points)):
		draw.line(screen.get_surface(), 0xFF0000, points[i - 1], points[i], 5)
	for i in range(1, len(points_spl)):
		draw.line(screen.get_surface(), 0x00FF00, points_spl[i - 1], points_spl[i], 5)


def main():
	pygame.init()

	size = (1000, 500)
	colorA = (0, 128, 255)
	colorAaug = (128, 194, 255)
	delta_rad = 15
	robot_rad = 15
	points = []

	points.append((3.14 / 2 * 100 + 20, sin(3.14 / 2) * 100 + 150))

	it = 0
	while (it <= 3 * 3.14):
		points.append((it * 100 + 20, sin(it) * 100 + 150))
		it += 3.14 / 2

	points.append(((3 * 3.14 - 3.14 / 2) * 100 + 20, sin(3 * 3.14 - 3.14 / 2) * 100 + 150))

	screen = pygame.display

	screen.init()
	screen.set_mode(size)
	
	pixel_arr = pygame.PixelArray(screen.get_surface())

	new_p = CatmullRomChain(points)

	generate_map(screen, colorA, points, new_p)

	screen.update()

	while 1:
		continue

if __name__ == '__main__':
	main()