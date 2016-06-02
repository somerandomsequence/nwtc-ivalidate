import yaml
import sys
import importlib

sys.path.append('.')

conf = yaml.load(file(sys.argv[1],'r'))

left = conf["left"]
right = conf["right"]

def get_input_class(s):
	m = importlib.import_module("inputs."+s)
	return getattr(m,s)

def get_metric_class(s):
	m = importlib.import_module("metrics."+s)
	return getattr(m,s)

left["input"] = get_input_class(left["format"])(left["path"],left["var"])
left["data"] = left["input"].get_ts(conf["location"])
for i in range(0,len(right)):
	right[i]["input"] = get_input_class(right[i]["format"])(right[i]["path"],right[i]["var"])
	right[i]["data"] = right[i]["input"].get_ts(conf["location"])
	right[i]["results"] = {}
	#for m in conf["metrics"]:
	#	right[i]["metric"] = importlib.import_module("metrics."+m)(right[i]["path"])
	#	right[i]["results"][m] = right[i]["metric"].compute(right[i]["input"].get_ts())

print right