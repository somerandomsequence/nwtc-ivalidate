# trim.py
#
# This is a simple QC function which discards points above or below given thresholds
#
# Caleb Phillips <caleb.phillips@nrel.gov>

class trim:

  def __init__(self,config):
    self.upper = config["upper"]
    self.lower = config["lower"]

  def apply(self,ts):
    k = ts.columns[0]
    ts = ts[ts[k] >= self.lower]
    ts = ts[ts[k] <= self.upper]
    return ts
