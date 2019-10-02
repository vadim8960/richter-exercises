import pygame 
from pygame import *
from math import *
import numpy as np
from delaunay2D import Delaunay2D

# Create a random set of points
seeds = np.random.random((10, 2))

# Create delaunay Triangulation
dt = Delaunay2D()
for s in seeds:
    dt.addPoint(s)

print(seeds)
# Dump triangles 
print (dt.exportTriangles())