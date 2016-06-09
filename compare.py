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

# Load the module t class with the name s
def get_module_class(t,s):
  m = importlib.import_module(".".join([t,s]))
  return getattr(m,s)

# Apply a series of transformative modules
def apply_trans(ts,modlist):
  for m in modlist:
    ts = m.apply(ts)
  return ts

# pre-load all the matric modules into an array
metrics = [get_module_class("metrics",m)() for m in conf["metrics"]]

# pre-load all the qa/qc modules into an array
preproc = []
for q in conf["prepare"]:
  k,c = q.popitem()
  preproc.append(get_module_class("prepare",k)(c))

results = []
left["input"] = get_module_class("inputs",left["format"])(left["path"],left["var"])
left["data"] = apply_trans(left["input"].get_ts(conf["location"]),preproc)
for i in range(0,len(right)):
  right[i]["input"] = get_module_class("inputs",right[i]["format"])(right[i]["path"],right[i]["var"])
  right[i]["data"] = apply_trans(right[i]["input"].get_ts(conf["location"]),preproc)
  results.append({"path": right[i]["path"], "var": right[i]["var"]})
  for m in metrics:
    results[i][m.__class__.__name__] = m.compute(left["data"],right[i]["data"])

print json.dumps(results)
