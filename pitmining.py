#!/bin/env python3
import pulp
import sys
import math
import numpy as np
from matplotlib import pyplot

def main():
    try:
        width = int(sys.argv[1])
    except IndexError:
        print("usage: {} <dim>".format(sys.argv[0]))
        exit(1)

    # Since the maximum angle is 45°, we only need our grid to be half as deep as
    # it is wide
    depth = int(math.ceil(width / 2))

    prob = pulp.LpProblem("pitmine", pulp.LpMaximize)

    # Create a dict of variables "d_zyx"
    ds = {}
    for z in range(depth):
        for y in range(width):
            for x in range(width):
                if (z <= y < width - z) and (z <= x < width - z):
                    # Give our variables names like d003002001 for 3-deep,
                    # 2-across.  These names aren't actually used anywhere,
                    # but PuLP makes them mandatory and they have to be
                    # unique.
                    name = "d{:03}{:03}{:03}".format(z, y, x)
                    ds.update({(z,y,x):
                            pulp.LpVariable(name, cat=pulp.LpBinary)})
                else:
                    # These cells are guaranteed to be zero, no need to
                    # include them in the model.
                    ds.update({(z,y,x): 0})

                if z == 0:
                    continue

                def addconstraint(dy, dx):
                    nonlocal prob
                    if (0 <= y + dy < width and 0 <= x + dx < width):
                        prob += ds[z,y,x] <= ds[z-1,y+dy,x+dx]

                # Add nine constraints, one per block above this one
                addconstraint(-1, -1)
                addconstraint(-1, 0)
                addconstraint(-1, 1)
                addconstraint(0, -1)
                addconstraint(0, 0)
                addconstraint(0, 1)
                addconstraint(1, -1)
                addconstraint(1, 0)
                addconstraint(1, 1)

    # Maximizing profit from randomly valued dirt.
    from random import seed, normalvariate
    seed(8) # Tried seeds until I got a "nice" mine.
    prob += sum(d * normalvariate(0.02, 0.25) for d in ds.values())

    outcome = prob.solve()
    print(pulp.LpStatus[outcome])

    # Plot an image
    image = np.zeros((depth,width,width))
    for z, y, x in ds:
        image[z,y,x] = pulp.value(ds[z,y,x])

    # Print out how deep we went (a birds-eye view of the mine depth)
    print(np.sum(image, 0))

    # Do a 3D plot of the mine
    from mpl_toolkits.mplot3d import Axes3D
    fig = pyplot.figure()
    ax = fig.add_subplot(111, projection='3d')
    x = np.arange(0, width)
    x, y = np.meshgrid(x, x)
    ax.plot_surface(x, y, -np.sum(image, 0), cmap='terrain', rstride=1,
            cstride=1, linewidth=0)
    ax.set_zlim(-width/1.4, 0)
    pyplot.show()
    pyplot.imsave('output.png', np.sum(image, 0), cmap='terrain')

if __name__ == "__main__":
    main()

