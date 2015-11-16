#!/bin/env python3
import pulp
import sys
import math
import numpy as np
from matplotlib import pyplot

def do_pitmine(price):
    zlim,ylim,xlim = price.shape
    prob = pulp.LpProblem("pitmine", pulp.LpMaximize)

    # Create a dict of variables "d_zyx"
    ds = {}
    for z in range(zlim):
        for y in range(ylim):
            for x in range(xlim):
                if (z <= y < ylim - z) and (z <= x < xlim - z):
                    # Give our variables names like d003002001 for 3-deep,
                    # 2-across.  These names aren't actually used anywhere,
                    # but PuLP makes them mandatory and they have to be
                    # unique.
                    name = "d{:03}{:03}{:03}".format(z, y, x)
                    ds[z,y,x] = pulp.LpVariable(name, cat=pulp.LpBinary)
                else:
                    # These cells are guaranteed to be zero, no need to
                    # include them in the model.
                    ds[z,y,x] = 0

                if z == 0:
                    continue

                def addconstraint(dy, dx):
                    nonlocal prob
                    if (0 <= y + dy < ylim and 0 <= x + dx < xlim):
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

    # Maximizing profit
    prob += sum(ds[z,y,x] * price[z,y,x] for z,y,x in ds)

    outcome = prob.solve()
    print(pulp.LpStatus[outcome])

    # Plot an image
    image = np.zeros((zlim,ylim,xlim))
    for z, y, x in ds:
        image[z,y,x] = pulp.value(ds[z,y,x])

    # Print out how deep we went (a birds-eye view of the mine depth)
    print(np.sum(image, 0))

    # Do a 3D plot of the mine
    from mpl_toolkits.mplot3d import Axes3D
    fig = pyplot.figure()
    ax = fig.add_subplot(111, projection='3d')
    x = np.arange(0, xlim)
    y = np.arange(0, ylim)
    x, y = np.meshgrid(y, x)
    ax.plot_surface(x, y, -np.sum(image, 0), cmap='terrain', rstride=1,
            cstride=1, linewidth=0)
    ax.set_zlim(-xlim/1.4, 0) # hack to make it look square
    pyplot.show()
    pyplot.imsave('output.png', np.sum(image, 0), cmap='terrain')

lamb = 1.03

def main():
    try:
        xlim = int(sys.argv[1])
    except IndexError:
        print("usage: {} <dim>".format(sys.argv[0]))
        exit(1)

    ylim = xlim

    # Since the maximum angle is 45°, we only need our grid to be half as deep
    # as it is wide
    zlim = int(math.ceil(xlim / 2))

    import scipy.stats
    price = scipy.stats.expon.rvs(loc=-1, scale=lamb, size=(zlim, ylim, xlim))
    do_pitmine(price)

if __name__ == "__main__":
    main()

