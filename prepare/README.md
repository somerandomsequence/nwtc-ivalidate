# Preprocessing

This directory contains quality assurance and quality control (QA/QC algorithms), including
outlier detection and cleaning as well as interpolation and other pre-processing routines.

To add your own, simply copy an existing file or use this interface (template):

```
# foobarbaz.py
#
# Translate the data somehow.
#
# Your Name <your.name@someplace.gov>

class foobarbaz:

  # Do something with the given configuration
  def __init__(self,config):
    self.config = config

  # Input & output is a datetime-indexed pandas dataframe
  def apply(ts):
    return ts
```
