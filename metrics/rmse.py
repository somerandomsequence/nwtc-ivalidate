# rmse.py
#
# This is a naive root mean squared error (RMSE) calculation
#
# If the input vectors differ, it takes the first N elements of each
# so that the size is the same. Error is computed pairwise without regard
# to the timestamps.
#
# Caleb Phillips <caleb.phillips@nrel.gov>


import numpy as np

class rmse:

  def compute(self,x,y):
    # just values (second member of tuple)
    # note: this isn't time aligning at all, just compares the 
    #       values as they arrive
    x = x.as_matrix()[:,0]
    y = y.as_matrix()[:,0]
    # naively truncate longer array if one is shorter
    if len(x) > len(y):
      x = x[0:len(y)]
    if len(y) > len(x):
      y = y[0:len(x)]
    return float(np.mean((np.array(x) - np.array(y))**2))
