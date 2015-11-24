import numpy as np
import pulp as pp
import matplotlib.pylab as plt

cu_mean = 0.01 # the real mine had a copper grade mean of 0.0085, and its pretty closely correlated to 
#fixed cost per block is $1.66/t, here we will assume its 1.66 perblock
fixed = 1.66
#process cost is prices at 5.6/t, we will assume its 5.6 perblock
process = 5.6
#copper price as of 31/05/2015 is 6294.78/t, again we will assume its per block
price = 6294.78/5000
#to get a greater percentage of blocks whose values are 0
subtractor = 0.0045

#recovery
recovery = 0.88
#multiplier, tonnage of material per block, but maybe 15900 s a bit high?

class The_Pit:
	def __init__(self,width, price=price, cu_mean=cu_mean, sd = 10):
		self.width = int(width)
		self.depth = int(width/2)
		#init cu_matrix which is the the pitmine grade
		self.cu_matrix = [[0 for x in range(self.width)] for x in range(self.depth)]
		#does this set seed do anything?
		np.random.seed(sd)
		makeGradeMatrix(self.cu_matrix)
		#init value matrix
		self.va_matrix = [[0 for x in range(self.width)] for x in range(self.depth)]
		makeValueMatrix(self.va_matrix, self.cu_matrix)
		#init decision vars
		self.de_matrix = [[0 for x in range(self.width)] for x in range(self.depth)]
		self.appendLP()
		self.prob = pp.LpProblem("pitmine", pp.LpMaximize)
		self.setConstraint()
		self.setObjective
		#solve?
		self.status = self.prob.solve()

		self.result = [[0 for x in range(self.width)] for x in range(self.depth)]
		self.copyResult

	def copyResult(self):
		for row in range(self.depth):
			for col in range(self.width):
				self.result[row][col] = pp.value(self.de_matrix[row][col])


	def appendLP(self):
		for row in range(self.depth):
			for col in range(self.width):
				name = "d{:3}{:3}".format(row, col)
				self.de_matrix[row][col] = pp.LpVariable(name, 0, 1, cat=pp.LpInteger)


	def setConstraint(self):
		for col in range(self.width):
		    for row in range(1,self.depth):
		        # Add three constraints, one per block above this one
		        self.prob += self.de_matrix[row][col] <= self.de_matrix[row-1][col]
		        if col > 0:
		            self.prob += self.de_matrix[row][col] <= self.de_matrix[row-1][col-1]
		        else: # y == 0
		            self.prob += self.de_matrix[row][col] <= 0

		        if col < self.width - 1:
		            self.prob += self.de_matrix[row][col] <= self.de_matrix[row-1][col+1]
		        else:
		            self.prob += self.de_matrix[row][col] <= 0
	
	def setObjective(self):
		for row in range(self.depth):
			for col in range(self.width):
				self.prob += self.va_matrix[row][col] * self.de_matrix[row][col]            

def initMatrix(depth,width):
	matrix = [[0 for x in range(width)] for x in range(depth)]
	return matrix

def makeGradeMatrix (cu_mat):
	cu_lambda = 1/cu_mean
	depth=np.shape(cu_mat)[0]
	width=np.shape(cu_mat)[1]

	for row in range(depth):
		for col in range(width):
			cu_mat[row][col]=max(0,np.random.exponential(cu_lambda)-subtractor) 

def makeValueMatrix (va_mat, cu_mat):
	depth=np.shape(cu_mat)[0]
	width=np.shape(cu_mat)[1]

	for row in range(depth):
		for col in range(width):
			va_mat[row][col] = max(0, price * recovery * cu_mat[row][col] / 100 - process) - fixed


def main():
	pit_1 = The_Pit(500)

	my_result = [[0 for x in range(pit_1.width)] for x in range(pit_1.depth)]
	for row in range(pit_1.depth):
		for col in range(pit_1.width):
			my_result[row][col] = pp.value(pit_1.de_matrix[row][col])

	matrix1 = np.matrix(my_result)
	matrix2 = np.matrix(pit_1.va_matrix)
	matrix3 = np.matrix(pit_1.cu_matrix)

	fig = plt.figure()
	ax = fig.add_subplot(1,1,1)
	ax.set_aspect('equal')
	plt.imshow(matrix1, interpolation='nearest', cmap=plt.cm.ocean)

	plt.colorbar()
	plt.show()

if __name__ == "__main__":
    main()
	