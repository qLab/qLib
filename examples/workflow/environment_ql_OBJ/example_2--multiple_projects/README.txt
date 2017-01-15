Environment qL (OBJ) -- Multiple projects example
=================================================


This is an example "projects root" folder, containing
two projects (titled AvDemeisen and JernauGurgeh).


There's a single configuration file (site_env.py) that takes care of
all housekeeping when opening a hip file within these projects.

Based on the path of the hip file, the site environment config
decides the role of the file (asset or shot) and sets up variables
accordingly.


Configuration files:

	site_env.py:
		(global)
		The main (and only) env config file

	site_env_short.py:
		(global)
		Same as the above file but with comments removed

	projs.json:
		(global)
		A JSON file, containing the list of all projects
		and related global data (currently, the short name of each project).

	ranges.json:
		(per-project)
		A JSON file, containing a list of shot IDs and
		related data (currently, the frame range for each shot).



The following Houdini variables are set up by site_env.py on a hip file open
(based on the file path):

	PROJ:
		Project name (name of the project root folder).

	PROJSH:
		Short name of the project (looked up from projs.json).

	ASSETNAME:
		If the file is in the assets/ subfolder, this will
		have the name of the containing folder (within assets/).

	SHOT:
		If the file is within the shots/ folder, this will
		contain the name of the folder for the actual shot.

	SHOTSTART,
	SHOTEND:
		If the file is a shot file (valid SHOT variable),
		these will be initialized from the "ranges.json"
		file.




