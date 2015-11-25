import numpy as np

subtractor = 0.0045

#cu_mean = 0.01 # the real mine had a copper grade mean of 0.0085, and its pretty closely correlated to 
#fixed cost per block is $1.66/t, here we will assume its 1.66 perblock
fixed = 1.66
#process cost is prices at 5.6/t, we will assume its 5.6 perblock
process = 5.6
#copper price as of 31/05/2015 is 6294.78/t, again we will assume its per block
#price = 6294.78/1100
#to get a greater percentage of blocks whose values are 0
#recovery
recovery = 0.88

def makeGradeMatrix (cu_mat, cu_lambda):
	depth=np.shape(cu_mat)[0]
	width=np.shape(cu_mat)[1]

	for row in range(depth):
		for col in range(width):
			cu_mat[row][col]=max(0,np.random.exponential(cu_lambda)-subtractor) 

def makeValueMatrix (va_mat, cu_mat, price):
	depth=np.shape(cu_mat)[0]
	width=np.shape(cu_mat)[1]

	for row in range(depth):
		for col in range(width):
			va_mat[row][col] = max(0, price * recovery * cu_mat[row][col] / 100 - process) - fixed