from pit2d import *
from minemaker import *
import numpy as np
import pulp as pp
import matplotlib.pyplot as plt
import scipy.stats as st

cu_mean = 0.01 # the real mine had a copper grade mean of 0.0085, and its pretty closely correlated to 
#fixed cost per block is $1.66/t, here we will assume its 1.66 perblock
fixed = 1.66
#process cost is prices at 5.6/t, we will assume its 5.6 perblock
process = 5.6
#copper price as of 31/05/2015 is 6294.78/t, again we will assume its per block
price = 6294.78/1000
#to get a greater percentage of blocks whose values are 0
#recovery
recovery = 0.88

#how to measure sigma?

def model_prices(price, step=100, sig = 0.3):
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

def showImage(array):
	fig = plt.figure()
	ax = fig.add_subplot(1,1,1)
	ax.set_aspect('equal')
	plt.imshow(array, interpolation='nearest', cmap=plt.cm.ocean)
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

def main():
	width = 100
	pitfolder = findAll(width, pv=price)
	base = concat_solution(width, pitfolder)
	showImage(base)





if __name__ == "__main__":
    main()
#for the heat map I will define the price_point as having a x% chance of realizing a market value that is above this price point

