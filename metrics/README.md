# Metrics

This directory contains algorithms to compute timeseries comparison metrics.

To add your own, simply copy an existing file or use this interface (template):

```
# foobarbaz.py
#
# The best metric.
#
# Your Name <your.name@someplace.gov>

class foobarbaz:

  # This function takes two datetime-indexed pandas dataframes as input
  # and returns a single float value
  def compute(self,x,y):
    return None    

```
