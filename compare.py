# compare.py
#
# This script runs the comparison between timeseries data as specified in config.yaml
#
# Usage: python compare.py config.yaml
#
#
# Caleb Phillips <caleb.phillips@nrel.gov>

import yaml
import sys
import importlib
import json
sys.path.append('.')

conf = yaml.load(file(sys.argv[1],'r'))

left = conf["left"]
right = conf["right"]

# Load the input format class with the name s
def get_input_class(s):
  m = importlib.import_module("inputs."+s)
  return getattr(m,s)

# Load the input metric class with the name s
def get_metric_class(s):
  m = importlib.import_module("metrics."+s)
  return getattr(m,s)

results = []
left["input"] = get_input_class(left["format"])(left["path"],left["var"])
left["data"] = left["input"].get_ts(conf["location"])
for i in range(0,len(right)):
  right[i]["input"] = get_input_class(right[i]["format"])(right[i]["path"],right[i]["var"])
  right[i]["data"] = right[i]["input"].get_ts(conf["location"])
  results.append({"path": right[i]["path"], "var": right[i]["var"]})
  for m in conf["metrics"]:
    right[i]["metric"] = get_metric_class(m)()
    results[i][m] = right[i]["metric"].compute(left["data"],right[i]["data"])

print json.dumps(results)