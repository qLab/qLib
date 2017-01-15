# ENV_LEVEL_VAR = "yeah"

print "*** SITE ENVIRONMENT ***"

print "hip:", HIP
print "job:", JOB

ENV_VAR_ORDER = [
        "JOB",
        "SCENE",
        "SCENE_NAME",
        "LIB",
        "XRES",
        "YRES",
        "PIXEL_ASPECT",
        ]

# Scan scene OTLs under the $JOB/Asset directory
OTL_PATTERN = JOB + "/Asset/*/Houdini/*.otl"

# If a directory called "Scene" is present in the path
# the scene name will be the directory right to the last
# occurance of "Scene", othervise it the scene name is
# the file name without the ".hip" extension, and $SCENE
# is equal to $HIP
if "/Scene/" in HIP:
    print "'/Scene/' in HIP..."
    p = HIP.split('/')
    i = (len(p) - 1) - p[::-1].index("Scene")
    if i < len(p) - 1:
        SCENE_NAME = p[i+1]
        SCENE = '/'.join(p[:i+2])
else:
    print "no '/Scene/' in HIP..."
    SCENE_NAME = HIPNAME
    if SCENE_NAME.endswith(".hip"):
        SCENE_NAME = SCENE_NAME[:-4]
    SCENE = HIP

# Camera defaults
XRES = 1280
YRES = 720
PIXEL_ASPECT = 1
HAPERTURE = 24.9

# Scene defaults
FPS = 25
