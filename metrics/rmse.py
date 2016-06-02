class rmse:
	def compute(x,y):
		s = 0
		n = 0
		for i in range(1,len(x)):
			s += ((x - y) ** 2)
			n += 1
		return s/n