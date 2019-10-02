import numpy as np
from delaunay2D import Delaunay2D
from random import *

if __name__ == '__main__':

    numSeeds = 1000
    radius = 1000
    seed = []
    for i in range(0, numSeeds):
        p = [randint(0, 800), randint(0, 400)]
        flag = 1
        for j in range(0, len(seed)):
            if p == seed[j]:
                flag = 0
                break
        if flag:
            seed.append(p)
        else:
            i -= 1
    seeds = np.array(seed)
    # seeds = radius * np.random.random((numSeeds, 2))
    print("seeds:\n", seeds)
    print("BBox Min:", np.amin(seeds, axis=0),
          "Bbox Max: ", np.amax(seeds, axis=0))

    center = np.mean(seeds, axis=0)
    # dt = Delaunay2D(center, 50 * radius)
    dt = Delaunay2D()
    
    # Insert all seeds one by one
    for s in seeds:
        dt.addPoint(s)

    # Dump number of DT triangles
    print (len(dt.exportTriangles()))
       
    """
    Demostration of how to plot the data.
    """
    import matplotlib.pyplot as plt
    import matplotlib.tri
    import matplotlib.collections

    # Create a plot with matplotlib.pyplot
    fig, ax = plt.subplots()
    ax.margins(0.1)
    ax.set_aspect('equal')
    plt.axis([-1, radius+1, -1, radius+1])

    cx, cy = zip(*seeds)
    dt_tris = dt.exportTriangles()
    ax.triplot(matplotlib.tri.Triangulation(cx, cy, dt_tris), 'bo--')

    plt.show()
