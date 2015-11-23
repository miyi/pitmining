import numpy as np

cu_mean = 0.0085 # the real mine had a copper grade mean of 0.0085, and its pretty closely correlated to 
#fixed cost per block is $1.66/t, here we will assume its 1.66 perblock
fixed = 1.66
#process cost is prices at 5.6/t, we will assume its 5.6 perblock
process = 5.6
#copper price as of 31/05/2015 is 6294.78/t, again we will assume its per block
price = 6294.78
#recovery
recovery = 0.88
#multiplier, tonnage of material per block, but maybe 15900 s a bit high?

class The_Pit:
	def __init__(self,width, price=price, cu_mean=cu_mean):
		self.width = int(width)
		self.depth = int(width/2)
		#init cu_matrix
		self.cu_matrix = [[0 for x in range(self.width)] for x in range(self.depth)]
		#does this set seed do anything?
		np.random.seed(10)
		makeGradeMatrix(self.cu_matrix)
		#init value matrix
		self.va_matrix = [[0 for x in range(self.width)] for x in range(self.depth)]
		makeValueMatrix(self.va_matrix, self.cu_matrix)
		#init decision vars
		decision = [[0 for x in range(self.width)] for x in range(self.depth)]

def makeGradeMatrix (cu_mat):
	cu_lambda = 1/cu_mean
	depth=np.shape(cu_mat)[0]
	width=np.shape(cu_mat)[1]

	for row in range(depth):
		for col in range(width):
			cu_mat[row][col]=np.random.exponential(cu_lambda) 

def makeValueMatrix (va_mat, cu_mat):
	depth=np.shape(cu_mat)[0]
	width=np.shape(cu_mat)[1]

	for row in range(depth):
		for col in range(width):
			va_mat[row][col] = price * recovery * cu_mat[row][col] / 100 - process - fixed

def main():
	pit_1 = The_Pit(20)
	print(pit_1.va_matrix)

if __name__ == "__main__":
    main()
	