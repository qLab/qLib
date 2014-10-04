import re
import json


def extract(pre, path):
	'''This function extracts a subfolder after a given folder in a path name.'''
	r = re.search("/%s/[^/]+" % pre, path).group(0)
	r = re.search("[^/]+$", r).group(0)
	return r



# get project name
# (extracting from ".../environment_ql_OBJ/<project name>/...")
#
PROJ = extract("environment_ql_OBJ", HIP)
PROJ = extract(PROJ, HIP)
PROJSH = PROJ



projs = {}
try:
	with open("%s/projs.json" % ENV_SCRIPT_PATH) as f:
		projs = json.loads( f.read() )
except:
	err('failed projs.json')

if PROJ in projs:
	PROJSH = projs[PROJ]['shortname']



# extract asset dir name, if the file is within the "assets" dir
# (extracting from ".../asset/<asset name>/...")
#
if "/assets/" in HIP:
	ASSETNAME = extract("assets", HIP)



# extract shot name, if the file is within the "shots" folder
# (extracting from ".../shots/<shot name>/...")
#
if "/shots/" in HIP:
	SHOT = extract("shots", HIP)

	# try to read the "ranges.json" file,
	# containing the frame range for each shot
	#
	ranges = {}
	try:
		with open("%s/%s/ranges.json" % (ENV_SCRIPT_PATH, PROJ, ) ) as f:
			ranges = json.loads( f.read() )
	except:
		err('failed to read ranges.json')

	# if the shot was listed in the "ranges.json" file,
	# set the shot range variables
	#
	if SHOT in ranges:
		r = ranges[str(SHOT)]
		SHOTSTART, SHOTEND = r[0], r[1]


