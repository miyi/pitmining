#!/bin/env python3
import pulp
import sys
import math

try:
    width = int(sys.argv[1])
    num_holes = int(sys.argv[2])
except IndexError:
    print("usage: {} <dim> <m3>".format(sys.argv[0]))
    exit(1)

# Since the maximum angle is 45°, we only need our grid to be half as deep as
# it is wide
depth = int(math.ceil(width / 2))

# Create a 2d array of variables "d_zy"
ds = []
for z in range(depth):
    arr = []
    for y in range(width):
        name = "d{:3}{:3}".format(z, y)
        arr.append(pulp.LpVariable(name, cat=pulp.LpBinary))
    ds.append(arr)

prob = pulp.LpProblem("pitmine", pulp.LpMaximize)

# Slope angle constraints
for y in range(width):
    for z in range(1,depth):
        # Add three constraints, one per block above this one
        prob += ds[z][y] <= ds[z-1][y]
        if y > 0:
            prob += ds[z][y] <= ds[z-1][y-1]
        else: # y == 0
            prob += ds[z][y] <= 0

        if y < width - 1:
            prob += ds[z][y] <= ds[z-1][y+1]
        else:
            prob += ds[z][y] <= 0

# Dig-time constraint
prob += sum(sum(d1) for d1 in ds) <= num_holes

# Maximizing profit from randomly valued dirt.
from random import random
prob += sum(sum(d*random() for d in d1) for d1 in ds), "objective"

prob.solve()

# Plot an image
from matplotlib import pyplot
import numpy
image = numpy.array([[int(pulp.value(d)) for d in d1] for d1 in ds])
pyplot.imsave('output.png', image, cmap='copper')

