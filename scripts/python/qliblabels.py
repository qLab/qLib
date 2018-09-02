"""
        @file       qliblabels.py
        @author     xy
        @since      2014-08-09

        @brief      qLib, node tagging/labeling functions (semantics).
"""

import hou
import re
import traceback
import datetime
import sys



labels = {

    # a completed partial-result
    'waypoint': {
        'cats': ('sop', 'dop', ),
        'color': (1.0, 0.6, 0.6),
        'prefix': 'WP_',
        'prefix.sop': 'GEO_',
        'prefix.dop': 'DOP_',
    },

    # fetch-like op (ObjectMerge, etc.)
    'fetch': {
        'cats': ('sop', ),
        'color': (0.8, 1.0, 0.8),
        'prefix': 'IN_',
    },

    # export-like op (an output point for another fetch)
    'export': {
        'cats': ('sop', ),
        'color': (0.0, 0.3, 0.0),
        'prefix': 'OUT_',
    },

    # RENDER op
    'render': {
        'cats': ('sop', ),
        'color': (0.4, 0.2, 0.6),
        'name': 'RENDER',
    },

    # DISPLAY op
    'display': {
        'cats': ('sop', ),
        'color': (0.0, 0.4, 1.0),
        'name': 'DISPLAY',
    },

    'out': {
        'cats': ('sop', ),
        'color': (0.9, 0.9, 0.9),
        'name': 'OUT',
    },


    # ----
    # default op settings (do not delete this)
    'default': {
        'color': (0.8, 0.8, 0.8),
    },
}


def msg(m):
    msg = "[%s qliblabels.py] %s" % (
        datetime.datetime.now().strftime("%y%m%d %H:%M.%S"), str(m), )
    sys.stderr.write(msg+"\n")
    #print msg


def warn(m):
    msg('WARNING: %s' % m)


def err(m):
    msg('ERROR: %s' % m)


def dbg(m):
    msg('[debug] %s' % m)


dbg('LOADED')


# module-wide constants
#

# name/label for tags parameter
n_tags = '__tags'
l_tags = 'tags (semantics)'

# tag list separator
tags_s = ' '


def has_tags_parm(node):
    '''.'''
    #assert type(node) is hou.Node
    r = node.parm(n_tags) is not None
    return r


def add_tags_parm(node):
    '''.'''
    #assert type(node) is hou.Node

    if not has_tags_parm(node):
        pass  # add tags parm

        #hou_parm_template_group = hou.ParmTemplateGroup()
        hou_parm_template_group = node.parmTemplateGroup()

        # Code for parameter template
        hou_parm_template = hou.StringParmTemplate(n_tags, l_tags,
                                                   1, default_value=([""]), naming_scheme=hou.parmNamingScheme.Base1,
                                                   string_type=hou.stringParmType.Regular,
                                                   menu_items=([]),
                                                   menu_labels=([]),
                                                   icon_names=([]),
                                                   item_generator_script="",
                                                   item_generator_script_language=hou.scriptLanguage.Python,
                                                   menu_type=hou.menuType.Normal)

        hou_parm_template_group.append(hou_parm_template)

        node.setParmTemplateGroup(hou_parm_template_group)
    else:
        dbg('%s already has tags parm' % node.path())

    return node.parm(n_tags)


def rem_tags_parm(node):
    '''.'''
    # assert

    if has_tags_parm(node):
        g = node.parmTemplateGroup()
        t = g.find(n_tags)
        if t:
            g.remove(t)
            node.setParmTemplateGroup(g)
        else:
            dbg('%s -- no tags parm found' % node.path())

    else:
        dbg('%s has no tags parm' % node.path())


def tags_parm(node):
    '''.'''
    return add_tags_parm(node)


def get_tag_list(node):
    '''.'''
    r = []
    if has_tags_parm(node):
        p = tags_parm(node)
        r = p.evalAsString().lower()
        # strip of spaces (in case separator is not a space)
        r = [n.strip() for n in r.split(tags_s)]
    return r


def set_tag_list(node, taglist):
    '''.'''
    assert type(taglist) is list, 'expecting a list of strings'
    l = [n.strip() for n in taglist if n.strip() != '']
    dbg(' -- tags: %s' % str(l))
    l = tags_s.join(l)
    dbg(' -- writing tags: "%s"' % l)
    if len(l) > 0:
        p = tags_parm(node)
        p.set(l)
    else:
        dbg('(removing parm)')
        rem_tags_parm(node)


def get_label_table():
    '''.'''
    return labels


def find_all_prefixes(labels):
    '''.'''
    r = set()

    for L in labels:
        E = labels[L]

        cats = E['cats'] if 'cats' in E else []
        if 'prefix' in E:
            r.add(E['prefix'])
        for c in cats:
            p = 'prefix.%s' % c
            if p in E:
                r.add(E[p])

    r = list(r)
    return r


def get_label_data(label):
    L = get_label_table()
    r = L[label] if label in L else {}
    return r


def apply_color(node):
    '''.'''
    pass
    # TODO: finish this


def apply_naming(node):
    '''.'''
    """
	TODO: make sure to
	- remove _all_ known prefixes as well, when necessary
	- rename to a default name if previous tagging had an explicit naming scheme
	"""
    pass
    c = node.type().category().name().lower()  # 'sop', etc.


def process_op(node, tags, tags_prev=[]):
    '''.'''
    # TODO: set color, prefix/name, etc.
    had_prev_tags = len(tags_prev) > 0

    if len(tags):
        pass  # TODO: apply new color, replace prefix, etc.
    else:
        pass  # TODO: reset op to its defaults


def uimsg(msg, sev=hou.severityType.Message):
    '''.'''
    hou.ui.setStatusMessage('[qLib | semantics]  %s' % str(msg), severity=sev)


def uiwarn(msg):
    uimsg(msg, sev=hou.severityType.Warning)


def shelfToolClicked(kwargs):
    '''.'''
    dbg('shelfToolClicked(): %s' % str(kwargs))
    assert type(kwargs) is dict, 'expecting a dict for kwargs'

    try:
        label = kwargs['toolname'].lower()
        label = re.search('[a-z]*$', label).group(0)

        nodes = hou.selectedNodes()
        add_mode = kwargs['shiftclick'] is True
        clear_mode = kwargs['altclick'] is True

        if label:
            uimsg("%s node(s) to '%s'" %
                  ('added label to' if add_mode else 'labeled', label, ))

            for n in nodes:
                dbg(" -- %s" % n.path())
                tags_prev = get_tag_list(n)
                tags = tags_prev if add_mode else []

                if label not in tags:
                    tags.append(label)

                if clear_mode:
                    tags = []

                set_tag_list(n, tags)
                process_op(n, tags, tags_prev)

        else:
            uiwarn("couldn't determine label from shelf tool '%s'" %
                   kwargs['toolname'])

    except:
        err('shelfToolClicked() failed')
        traceback.print_exc()
        #dbg('%s' % str( traceback.format_exc() ) )

    pass
