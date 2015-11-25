import numpy as np
import pulp 
import matplotlib.pylab as plt
from matplotlib import pyplot
from minemaker import *

class The_Pit:
	def __init__(self, width, price, cu_mean=0.01, sd = 10):
		self.price = price
		self.width = int(width)
		self.depth = int(width/2)
		#init cu_matrix which is the the pitmine grade
		self.cu_matrix = [[0 for x in range(self.width)] for x in range(self.depth)]
		self.va_matrix = [[0 for x in range(self.width)] for x in range(self.depth)]
		self.ds = []
		self.solution = [[0 for x in range(self.width)] for x in range(self.depth)]
		
		#does this set seed do anything?
		np.random.seed(sd)
		#initialize mine
		makeGradeMatrix(self.cu_matrix, cu_lambda = 1/cu_mean)
		makeValueMatrix(self.va_matrix, self.cu_matrix, price)
		#initialize computations
		self.compute()

	
	def compute(self):
		self.appendLP()
		self.prob = pulp.LpProblem("pitmine", pulp.LpMaximize) 
		self.setConstraint()
		self.setObjective()
		self.prob.solve()
		self.solution = np.array([[int(pulp.value(d)) for d in d1] for d1 in self.ds])

	def appendLP(self):
   		for row in range(self.depth):
   			new = []
   			for col in range(self.width):
   				name = "d{:3}{:3}".format(row, col)
   				new.append(pulp.LpVariable(name, cat=pulp.LpBinary))
   			self.ds.append(new)

	def setConstraint(self):
		for col in range(self.width):
			for row in range(1, self.depth):
			# Add three constraints, one per block above this one
				self.prob += self.ds[row][col] <= self.ds[row-1][col]
				if col > 0:
					self.prob += self.ds[row][col] <= self.ds[row-1][col-1]
				else:
					self.prob += self.ds[row][col] <= 0
				if col < self.width - 1:
					self.prob += self.ds[row][col] <= self.ds[row-1][col+1]
				else:
					self.prob += self.ds[row][col] <= 0

	def setObjective(self):
		self.prob += sum(sum(d*v for d, v in zip(d1,v1)) for d1,v1 in zip(self.ds, self.va_matrix)), "objective"
	 

	def showImage(self):
		fig = plt.figure()
		ax = fig.add_subplot(1,1,1)
		ax.set_aspect('equal')
		plt.imshow(self.solution, interpolation='nearest', cmap=plt.cm.ocean)

		plt.colorbar()
		plt.show()


	