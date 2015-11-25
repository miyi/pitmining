import numpy as np

subtractor = 0.9945
fixed = 1.66
process = 5.6
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