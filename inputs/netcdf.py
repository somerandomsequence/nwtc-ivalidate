# this input parser expects to be given a directory filled with netcdf files - each a grid at one particular time

import os
from netCDF4 import Dataset

class netcdf:

	def __init__(self,path,var):
		self.path = path
		self.var = var

	def get_ts(self,loc):
		i = loc["i"]
		j = loc["j"]
		r = []
		for l in os.listdir(self.path):
			ih = Dataset(l, 'r')
			t = ih.variables["Times"][0]
			v = ih.variables[self.var][0][i][j]
			ih.close()
			r.append((t,v))
		return r


	