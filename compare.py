# compare.py
#
# This script runs the comparison between timeseries data as specified in config.yaml
#
# Usage: python compare.py config.yaml
#
# Caleb Phillips <caleb.phillips@nrel.gov>

import yaml
import sys
import importlib
import json
import dateutil
import re
import base64
import requests
sys.path.append('.')

# Check options and load config
if len(sys.argv) < 2:
  print "Usage: python compare.py <config.yaml>"
  quit()

conf = yaml.load(file(sys.argv[1],'r'))
left = conf["left"]
right = conf["right"]

# FIXME: validate configuration file and give nice errors
#        if something (necessary) is missing

# Load the module t class with the name s
def get_module_class(t,s):
  m = importlib.import_module(".".join([t,s]))
  return getattr(m,s)

# Apply a series of transformative modules
def apply_trans(ts,modlist):
  for m in modlist:
    ts = m.apply(ts)
  return ts

def get_dap_file(path,config):
  api_url = "https://dteuqmpcac.execute-api.us-west-2.amazonaws.com/test/request-data"
  out_dir = config["cache_dir"] + "/dap/" + path  
  credentials = base64.b64encode("%s:%s" % (config["login"], config["pass"]))
  auth = {"Authorization": "Basic %s" % credentials}

  params = {
    "output": "json",
    "filter": {
        "Dataset": path
        #"file_type": ["txt"],
        #"date_time": {
        #    "between": ["20160505000000", "20160507000000"]
        #}
    }
  }

  print params

  req = requests.post(api_url, headers=auth, data=json.dumps(params), verify=False)
  print(req.text)

# Figure out where the file is (local or remote)
# and fetch if necessary
def get_file(path,remote):
  proto = None
  m = re.match(r"([a-z]+)://(.*)",path,re.IGNORECASE)
  if m:
    proto = m.group(1)
    path = m.group(2)
  else:
    proto = "local"

  if proto == "local":
    return path
  elif proto == "dap":
    return get_dap_file(path,remote["dap"])

def time_align(conf,x,y):
  # apply time window
  if "window" in conf.keys():
    if conf["window"]["lower"].__class__.__name__ != 'datetime':
      lower = dateutil.parser.parse(conf["window"]["lower"])
    else:
      lower = conf["window"]["lower"]
    if conf["window"]["upper"].__class__.__name__ != 'datetime':
      upper = dateutil.parser.parse(conf["window"]["upper"])
    else:
      upper = conf["window"]["upper"]

    x = x[x.index <= upper]
    x = x[x.index >= lower]
    y = y[y.index <= upper]
    y = y[y.index >= lower]

  # trim to extent of left or right
  if "trim" in conf.keys():
    if conf["trim"] == "left":
      lower = x.index.min()
      upper = x.index.max()
      y = y[y.index <= upper]
      y = y[y.index >= lower]
    elif conf["trim"] == "right":
      lower = y.index.min()
      upper = y.index.max()
      x = x[x.index <= upper]
      x = x[x.index >= lower]
    
  return (x,y)
    

# Pre-load all the metric modules into an array
metrics = [get_module_class("metrics",m)() for m in conf["metrics"]]

# Pre-load all the qa/qc modules into an array
preproc = []
for q in conf["prepare"]:
  k,c = q.popitem()
  preproc.append(get_module_class("prepare",k)(c))

# Load the data and compute the metrics
results = []
left["path"] = get_file(left["path"],conf["remote"])
left["input"] = get_module_class("inputs",left["format"])(left["path"],left["var"])
left["data"] = apply_trans(left["input"].get_ts(conf["location"]),preproc)
for i in range(0,len(right)):
  right[i]["path"] = get_file(right[i]["path"],conf["remote"])
  right[i]["input"] = get_module_class("inputs",right[i]["format"])(right[i]["path"],right[i]["var"])
  right[i]["data"] = apply_trans(right[i]["input"].get_ts(conf["location"]),preproc)
  results.append({"path": right[i]["path"], "var": right[i]["var"], "location": conf["location"]})
  for m in metrics:
    x,y = time_align(conf["time"],left["data"],right[i]["data"])
    results[i][m.__class__.__name__] = m.compute(x,y)

# FIXME: allow different output formats besides JSON

# Output the results
print json.dumps(results)
