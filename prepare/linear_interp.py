# linear_interp.py
#
# Perform a linear interpolation for the given period or sample size.
#
# Caleb Phillips <caleb.phillips@nrel.gov>

import numpy as np
import time
import datetime

class linear_interp:

  def __init__(self,config):
    self.config = config

  def get_sample_ts(self,t):
    tmin = min(t)
    tmax = max(t)
    if "n" in self.config.keys():
      n = self.config["n"]
      tprime = np.linspace(tmin,tmax,n)
    else:
      period = self.config["period"]
      tprime = np.arrange(tmin,tmax,period)
      tprime.append(tmax)      
    return tprime

  def apply(self,ts):
    t = map(lambda x: time.mktime(x[0].timetuple()),ts)
    v = map(lambda x: x[1],ts)
    tprime = self.get_sample_ts(t)
    vprime = np.interp(tprime,t,v)
    return [(tprime[i],vprime[i]) for i in range(0,len(tprime))]

