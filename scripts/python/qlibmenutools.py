"""
        @file       qlibmenutools.py
        @author     xy
        @since      2019-12-10

        @brief      Menu related convenience functions.
"""

import os
import traceback

import hou
import qlibutils
import re
import subprocess


def get_all_parms(kwargs, unlocked_only=False):
    """Get all (both normal and locked) parms, related to an RMB menu click.
    """
    r = None
    try:
        r = kwargs["parms"]
        if not unlocked_only:
            r += kwargs["locked_parms"]
    except:
        pass
    return r



def parm_is_string(kwargs):
    """Determines if the (first) RMB-clicked parameter is a string.
    """
    r = False
    try:
        r = get_all_parms(kwargs)[0].parmTemplate().type()==hou.parmTemplateType.String
    except:
        print("ERROR: %s" % traceback.format_exc())
    return r



def parm_is_float(kwargs):
    """Determines if the (first) RMB-clicked parameter is a float.
    """
    r = False
    try:
        r = get_all_parms(kwargs)[0].parmTemplate().type()==hou.parmTemplateType.Float
    except:
        print("ERROR: %s" % traceback.format_exc())
    return r



def parm_is_framenum(kwargs):
    """Determines if the (first) RMB-clicked parameter describes a frame number (e.g. startframe).
    """
    r = False
    try:
        p = get_all_parms(kwargs)[0]
        r = p.parmTemplate().type()==hou.parmTemplateType.Int \
            and "frame" in p.name().lower()
    except:
        print("ERROR: %s" % traceback.format_exc())
    return r



def parm_is_framerange(kwargs):
    """Determines if the (first) RMB-clicked parameter describes a frame range.
    """
    r = False
    try:
        t = get_all_parms(kwargs)[0].parmTemplate()
        r = t.type() in (hou.parmTemplateType.Int, hou.parmTemplateType.Float, ) \
            and t.numComponents()>1
    except:
        print("ERROR: %s" % traceback.format_exc())
    return r



def parm_is_ramp(kwargs):
    """Determines if the (first) RMB-clicked parameter is a float.
    """
    r = False
    try:
        r = get_all_parms(kwargs)[0].parmTemplate().type()==hou.parmTemplateType.Ramp
    except:
        print("ERROR: %s" % traceback.format_exc())
    return r



def parm_is_copyable(kwargs):
    """Determines if the (first) RMB-clicked parameter is of a type that can be copied to the system clipboard.
    """
    # TODO: this can probably be improved
    return not parm_is_ramp(kwargs)



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
        print("ERROR: %s" % traceback.format_exc())
    return r



def parm_has_target_node(kwargs):
    """Checks if the (first) RMB-clicked parm points to another node in the hip file.
    """
    r = False
    try:
        p = get_all_parms(kwargs)[0]
        r = len(p.node().glob(p.evalAsString())) > 0
    except:
        print("ERROR: %s" % traceback.format_exc())
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


def reset_parm(parm):
    """.
    """
    reset_parms( { "parms": (parm, ) } )


def select_target_nodes(kwargs):
    """.
    """
    parms = get_all_parms(kwargs)
    for parm in parms:
        nodes = parm.node().glob(parm.evalAsString())
        for node in nodes:
            node.setSelected(True)


def expand_target_wildcards(kwargs):
    """.
    """
    parms = get_all_parms(kwargs)
    for parm in parms:
        pnode = parm.node()
        nodes = pnode.glob(parm.evalAsString())
        paths = " ".join( [ pnode.relativePathTo(n) for n in nodes ] )
        reset_parm(parm)
        parm.set(paths)


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
    parms = get_all_parms(kwargs)
    to_abs = None # None=yet to be decided, True=convert to abs 1=to rel

    for parm in parms:
        pnode = parm.node()
        paths_in = parm.evalAsString().split() # paths as string
        paths_out = []

        for path in paths_in:
            parmname = ""
            if pnode.parm(path):
                # if it's a parm, pop/remember parm name and still deal w/ node paths
                parmname = re.search("/[^/]+$", path).group(0)
                path = re.sub(parmname+"$", "", path)

            target = pnode.node(path)

            if target:
                # works with single nodes but not with patterns
                path_rel = pnode.relativePathTo(target)
                path_abs = target.path()

                # decide if we want to convert all to abs or rel
                if to_abs is None:
                    to_abs = re.sub("[/]+$", "", path)!=path_abs # (strip trailing slashes for comparison)

                paths_out.append( (path_abs if to_abs else path_rel) + parmname )
            else:
                # probably a pattern, don't deal with it
                paths_out.append(path + parmname)

        path = " ".join(paths_out)
        reset_parm(parm)
        parm.set(path)


def switch_spaces_newlines(kwargs):
    """Converts between spaces and newlines in a string parm.
    (Called from PARMmenu.xml)
    """
    parms = get_all_parms(kwargs)
    to_newlines = None

    for parm in parms:
        v = parm.evalAsString()

        if to_newlines is None:
            to_newlines = " " in v

        v = re.sub("[\n ]+", "\n" if to_newlines else " ", v)
        reset_parm(parm)
        parm.set(v)


def add_parm_value_multiplier(kwargs, add_exponent=False):
    """Adds a value/multipler parameter pair to the specified parameter.
    (Called from PARMmenu.xml)
    """
    p = kwargs['parms'][0]
    try:
        n = p.node()

        v = p.eval()
        t = p.parmTemplate()
        g = n.parmTemplateGroup()

        ptn = t.name()
        pn = p.name()
        pl = t.label()

        if t.numComponents()>1:
            pl = "%s %d" % (pl, p.componentIndex()+1, )

        pvn = '%s_value' % pn
        pmn = '%s_mult' % pn
        pxn = '%s_exp' % pn
        t = hou.FloatParmTemplate(name=p.name(), label="...", num_components=1)

        expr = "ch('%s') * ch('%s')" % (pvn, pmn, )

        if not n.parm(pvn) and not n.parm(pmn):
            # value
            t.setName(pvn)
            t.setLabel('%s (v)' % pl)
            t.setDefaultValue( (v, ) )
            g.insertAfter(ptn, t)
            # mult
            t.setName(pmn)
            t.setLabel('%s (%%)' % pl)
            t.setMinValue(0.0)
            t.setMaxValue(2.0)
            t.setDefaultValue( (1.0, ) )
            g.insertAfter(pvn, t)

            if add_exponent and not n.parm(pxn):
                # exp
                t.setName(pxn)
                t.setLabel('%s (exp)' % pl)
                t.setMinValue(0.001)
                t.setMaxValue(4.0)
                t.setDefaultValue( (2.0, ) )
                g.insertAfter(pmn, t)

                expr = "ch('%s') * pow(ch('%s'), ch('%s'))" % (pvn, pmn, pxn, )

            # add parms
            n.setParmTemplateGroup(g)

            p.setExpression(expr)
        else:
            hou.ui.setStatusMessage("Value/multiplier params already exist for %s" % p.path(),
                severity=hou.severityType.Warning)
    except:
        hou.ui.setStatusMessage("couldn't set up value/multiplier parameters on %s" % p.path(),
            severity=hou.severityType.Error)
        print("ERROR: %s" % traceback.format_exc())


def set_ramp_basis(kwargs, ramp_basis):
    """Set all knots on a ramp to the specified type.
    (Called from PARMmenu.xml)
    """
    try:
        p = kwargs['parms'][0]
        v = p.eval()
        num_keys = len(v.basis())
        new_basis = (ramp_basis, ) * num_keys
        new_ramp = hou.Ramp(new_basis, list(v.keys()), list(v.values()))
        p.set(new_ramp)
    except:
        hou.ui.setStatusMessage("couldn't set ramp interpolation type on %s" % p.path(),
            severity=hou.severityType.Error)


def build_upstream_channel_refs_menu(kwargs):
    """Builds a dynamic submenu of upstream parameters
    that can be linked in as a channel reference expression.
    """
    node = get_all_parms(kwargs)[0].node()

    nodes = hou.hscript("opdepend -i %s" % node.path())[0].split()
    nodes = [ hou.node(n) for n in nodes ]

    types = ( hou.parmTemplateType.String, )
    parms = []

    # TODO: filter out menus so it'll be only string fields!
    def iz_good(pt):
        r = False
        try:
            if len(pt)>0: # because of separators...
                p = pt[0]
                s = p.evalAsString()
                r = \
                    (pt.parmTemplate().type() in types) \
                    and s!="" and "/" not in s \
                    and not p.isDisabled() and p.isVisible()
        except:
            print(pt)
            print("ERROR: %s" % traceback.format_exc())
        return r

    for n in nodes:
        n.updateParmStates()
        parms += [ pt[0] for pt in n.parmTuples() if iz_good(pt) ]

    parms = [ p.path() for p in parms ]
    parms = parms[:10] # limit number of menu items

    menu_items = []
    for pn in parms:
        p = hou.parm(pn)
        rel_pn = node.relativePathTo(p.node())+"/"+p.name()
        rel_path = [ rel_pn ]
        if len(p.keyframes())>0 or p.evalAsString()!=p.rawValue():
            rel_path += [ "<anim/expr>" ]
        rel_path = "  ".join(rel_path)

        menu_items.append(rel_pn)
        label = p.evalAsString()
        label = label[:40] + ( label[40:] and "..." )
        menu_items.append('"%s"  ( %s )' % (label, rel_path, ) )

    return menu_items


def set_upstream_channel_ref_value(kwargs):
    """Callback function related to the menu above.
    """
    src = hou.parmTuple(kwargs["selectedtoken"])
    reset_parms(kwargs)
    parms = get_all_parms(kwargs)
    for parm in parms:
        parm.set("`chs(\"%s\""")`" % kwargs["selectedtoken"])


def open_as_fs_path(kwargs):
    """Considers parm value as an FS path and opens it in
    the filesystem browser.
    """
    dirs = [ os.path.dirname(p.evalAsString()) for p in get_all_parms(kwargs) ]
    dirs = list(set(dirs)) # don't open anything twice
    for dir in dirs:
        qlibutils.open_dir(dir)


def open_in_mplay(kwargs):
    """Considers parm value as an FS path and opens it in mplay.
    """
    dirs = [ p.unexpandedString() for p in get_all_parms(kwargs) ]
    dirs = list(set(dirs)) # don't open anything twice
    if len(dirs)>0:
        qlibutils.statmsg("mplay %s" % dirs[0])
        r=subprocess.call(["mplay", dirs[0]])
        if r!=0:
            qlibutils.statmsg("ERROR while calling mplay %s" % dirs[0], warn=True)



def set_as_playback_range(kwargs, startFrame=True):
    """Set up playback range based on the parameter passed on in kwargs.
    """
    parm = get_all_parms(kwargs)[0]
    t = parm.parmTemplate()

    # playback range as integers
    r = list(hou.playbar.playbackRange())
    r = [ int(r[0]), int(r[1]), ]

    if t.numComponents()>1:
        print(parm)
        r = parm.tuple().eval()
        r = [ int(r[0]), int(r[1]), ]
    else:
        # one component: either start or end frame
        r[ 0 if startFrame else 1 ] = parm.evalAsInt()

    hou.playbar.setRestrictRange(False)
    hou.playbar.setPlaybackRange(r[0], r[1])


def copy_all_parm_values_to_clipboard(kwargs):
    """.
    """
    parms = get_all_parms(kwargs)
    R = []
    for parm in parms:
        try:
            R.append(str(parm.eval()))
        except:
            pass
    R = "\n".join(R)
    hou.ui.copyTextToClipboard(R)
