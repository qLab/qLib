import re
import json


def extract(pre, path):
	'''.'''
	r = re.search("/%s/[^/]+" % pre, path).group(0)
	r = re.search("[^/]+$", r).group(0)
	return r


PROJ = extract("environment_ql_OBJ", HIP)
PROJ = extract(PROJ, HIP)
PROJSH = PROJ

projs = {}
try:
	with open("%s/projs.json" % ENV_SCRIPT_PATH) as f:
		projs = json.loads( f.read() )
except:
	pass

if PROJ in projs:
	PROJSH = projs[PROJ]['shortname']

if "/assets/" in HIP:
	ASSETNAME = extract("assets", HIP)

if "/shots/" in HIP:
	SHOT = extract("shots", HIP)
	ranges = {}
	try:
		with open("%s/%s/ranges.json" % (ENV_SCRIPT_PATH, PROJ, ) ) as f:
			ranges = json.loads( f.read() )
	except:
		pass
	if SHOT in ranges:
		r = ranges[str(SHOT)]
		SHOTSTART, SHOTEND = r[0], r[1]


