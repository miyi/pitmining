from pit2d import *
from minemaker import *
import numpy as np
import pulp 
import matplotlib.pyplot as plt
import scipy.stats as st
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt
import numpy as np

cu_mean = 0.01 # the real mine had a copper grade mean of 0.0085, and its pretty closely correlated to 
#fixed cost per block is $1.66/t, here we will assume its 1.66 perblock
fixed = 1.66
#process cost is prices at 5.6/t, we will assume its 5.6 perblock
process = 5.6
#copper price as of 31/05/2015 is 6294.78/t, again we will assume its per block
price = 5217.25/1000
#to get a greater percentage of blocks whose values are 0
#recovery
recovery = 0.88

#how to measure sigma?

def model_prices(price, step=100, sig = 0.25):
	price_range = []
	price_range.append(0)
	for percentile in range(1,step):
		inv_log = st.lognorm.ppf(percentile/100, sig, loc=0, scale=1)
		price_range.append(price * inv_log)  
	return price_range

def concat_solution(width, folder):
	base =np.array(makeBaseMatrix(width))
	for percentile in range(1,len(folder)):
		base += np.array(folder[percentile].solution)
	return base


def makeBaseMatrix(width):
	depth = int(width/2)
	return [[0 for x in range(width)] for x in range(depth)]

def showPit(pit):
	fig = plt.figure()
	ax = fig.add_subplot(1,1,1)
	ax.set_aspect('equal')
	plt.imshow(pit.solution, interpolation='nearest', cmap=plt.cm.ocean)
	plt.colorbar()
	plt.show()

def showHeat(array):
	fig = plt.figure()
	ax = fig.add_subplot(1,1,1)
	ax.set_aspect('equal')
	plt.imshow(array, interpolation='nearest', cmap=plt.cm.jet)
	plt.colorbar()
	plt.show()

def findAll(width, pv, cu_mean=0.01, step=100, sd=10):
	allpits = []
	allpits.append(0)
	price_range = model_prices(pv, step=step)
	for percentile in range(1,step):
		pc_price = price_range[percentile]
		snapshot = The_Pit(width=width, price=pc_price, cu_mean=cu_mean, sd=sd)
		allpits.append(snapshot)
		print(percentile)

	return allpits, price_range

def show3d(matrix):
	fig = plt.figure()
	ax = fig.gca(projection='3d')
	depth = np.shape(matrix)[0]
	width = np.shape(matrix)[1]
	X = np.arange(0, width)
	Y = np.arange(0, depth)
	X, Y = np.meshgrid(X, Y)
	Z = matrix
	surf = ax.plot_surface(Y, X, Z, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0, antialiased=False)
	ax.set_zlim(0, 100)

	ax.zaxis.set_major_locator(LinearLocator(10))
	ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

	fig.colorbar(surf, shrink=0.5, aspect=5)

	plt.show()

def main():
	width = 100
	mypit = The_Pit(width, price = price, sd = 1700850)
	pitfolder, pc_price = findAll(width, pv=price, sd = 1700850)
	base = concat_solution(width, pitfolder)
	showHeat(base)
	show3d(base)

if __name__ == "__main__":
    main()
#for the heat map I will define the price_point as having a x% chance of realizing a market value that is above this price point

