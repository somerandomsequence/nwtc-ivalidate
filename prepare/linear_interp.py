# linear_interp.py
#
# Perform a linear interpolation for the given period or sample size.
#
# Caleb Phillips <caleb.phillips@nrel.gov>

import numpy as np
import pandas as pd
import time
import datetime

class linear_interp:

  def __init__(self,config):
    self.config = config

  def get_sample_ts(self,t):
    tmin = min(t)
    tmax = max(t)
    if "period" in self.config.keys():
      period = self.config["period"]
      n = ((tmax-tmin)/period) + 1
    else:
      n = self.config["n"]
    
    return np.linspace(tmin,tmax,n)

  def apply(self,ts):
    t = map(lambda x: time.mktime(x.timetuple()),ts.index)
    v = ts.as_matrix()[:,0]
    tprime = self.get_sample_ts(t)
    vprime = np.interp(tprime,t,v)
    return pd.DataFrame(index=tprime,data={ts.columns[0]: vprime})
