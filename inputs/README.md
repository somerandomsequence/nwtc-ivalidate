# Input parsers

This directory contains input data parser modules -- one file (module) per input data format.

To add your own, simply copy an existing file or use this interface (template):

```
# foobarbaz.py
#
# Parser for my favorite format.
#
# Your Name <your.name@someplace.gov>

import os
from datetime import datetime
import numpy as np
import pandas as pd

# the name of your class should match
# the file name used, e.g., foobarbaz.py
class foobarbaz:

  # initialize the parser object with the
  # path and variable (column) name
  def __init__(self,path,var):
    self.path = path
    self.var = var

  # put code here to extract the timeseries
  # and return it as a datetime-indexed pandas Dataframe
  def get_ts(self,loc):
    return pd.DataFrame()
```
