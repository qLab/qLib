"""
        @file       qlibmenutools.py
        @author     xy
        @since      2019-12-10

        @brief      Menu related convenience functions.
"""

import hou
import traceback


def get_all_parms(kwargs, unlocked_only=False):
    """Get all (both normal and locked) parms, related to an RMB menu click.
    """
    r = kwargs["parms"]
    if not unlocked_only:
        r += kwargs["locked_parms"]
    return r



def parm_is_string(kwargs):
    """Determines if the (first) RMB-clicked parameter is a string.
    """
    r = False
    try:
        r = get_all_parms(kwargs)[0].parmTemplate().type()==hou.parmTemplateType.String
    except:
        print "ERROR: %s" % traceback.format_exc()
    return r



def parm_is_float(kwargs):
    """Determines if the (first) RMB-clicked parameter is a float.
    """
    r = False
    try:
        r = get_all_parms(kwargs)[0].parmTemplate().type()==hou.parmTemplateType.Float
    except:
        print "ERROR: %s" % traceback.format_exc()
    return r



def parm_is_ramp(kwargs):
    """Determines if the (first) RMB-clicked parameter is a float.
    """
    r = False
    try:
        r = get_all_parms(kwargs)[0].parmTemplate().type()==hou.parmTemplateType.Ramp
    except:
        print "ERROR: %s" % traceback.format_exc()
    return r



def parm_is_fspath(kwargs):
    """Checks if the (first) RMB-clicked parm is a filesystem path.
    (Currently it just checks against empty strings)
    """
    r = False
    try:
        p = get_all_parms(kwargs)[0]
        v = p.evalAsString().strip()
        r = p.parmTemplate().type()==hou.parmTemplateType.String and v!=""
    except:
        print "ERROR: %s" % traceback.format_exc()
    return r



def parm_has_target_node(kwargs):
    """Checks if the (first) RMB-clicked parm points to another node in the hip file.
    """
    r = False
    try:
        r = get_all_parms(kwargs)[0].evalAsNode() is not None
    except:
        print "ERROR: %s" % traceback.format_exc()
    return r


def reset_parms(kwargs, unlocked_only=False):
    """Reset all parameters to their default state.
    Especially important is to remove all expression links, as they can
    throw off setting values (the values will be set on parms pointed to
    by the expression). 

    Hopefully this covers all (or, most) scenarios.
    """
    try:
        parms = get_all_parms(kwargs, unlocked_only=unlocked_only)
        for parm in parms:
            parm.lock(False)
            parm.deleteAllKeyframes()
            parm.revertToDefaults()
    except:
        pass


def set_string_parm(kwargs, value):
    """Sets a string parm to a specified value.
    It resets the parm first in order to get rid of any expressions
    (to avoid expressions "bouncing" the parm setting to another parm).
    """
    try:
        reset_parms(kwargs)
	parms = get_all_parms(kwargs)
	for parm in parms:
		parm.set(str(value))
    except:
        pass



def set_parent_opinput(kwargs, index):
    """.
    """
    set_string_parm(kwargs, "%s`opinputpath('..', %d)`" % \
        ('op:' if kwargs['ctrlclick'] else '', index, )
    )


def toggle_abs_rel_path(kwargs):
    """Converts between absolute and relative OP paths.
    (Called from PARMmenu.xml)
    """
    if 'parms' in kwargs:
        for parm in kwargs['parms']:
            try:
                node = parm.node()
                path = parm.evalAsString()

                target = node.node(path)

                path_rel = node.relativePathTo(target)
                path_abs = target.path()

                r = path_rel if path==path_abs else path_abs

                parm.set(r)
            except:
                pass


