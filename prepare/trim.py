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
    return [x for x in ts if x[1] >= self.lower or x[1] <= self.upper]
