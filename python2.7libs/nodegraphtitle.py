# NOTE: this file has to be checked against and updated for every new Houdini version!

from __future__ import print_function
import hou
import nodegraphprefs as prefs

def networkEditorTitleLeft(editor):
    try:
        title = ''
        pwd = editor.pwd()
        playerparm = pwd.parm('isplayer')
        if playerparm is not None and playerparm.evalAsInt() != 0:
            title += 'Network in Playback Mode\n'
        if prefs.showPerfStats(editor):
            profile = hou.perfMon.activeProfile()
            if profile is not None:
                profiletitle = profile.title()
                if not profiletitle:
                    profiletitle = 'Profile ' + str(profile.id())
                title += profiletitle + ': ' + prefs.perfStatName(editor)

    except:
        title = ''

    return title


def add_extra_title_right_ql(editor, pwd, title):
    """Add extra information based on selection, hidden nodes, etc.
    """

    try:
        # show all/selected if something's selected
        all_items = len(pwd.allItems())
        selected = len(hou.selectedItems())
        if selected>0:
            title += "\n\nselected: %d\n(of %d)" % (selected, all_items, )

        # show all/hidden if there's hidden
        all_nodes = len(pwd.children())
        hidden_nodes = len([ n for n in pwd.children() if n.isHidden() ])
        if hidden_nodes>0:
            title += "\n\nhidden: %d\n(of %d)" % (hidden_nodes, all_nodes, )

        # TODO: show more info on the shift+Z panel thing?

    except:
        pass

    return title



def networkEditorTitleRight(editor):
    try:
        title = ''
        pwd = editor.pwd()
        title += pwd.childTypeCategory().label()

    except:
        title = ''

    title = add_extra_title_right_ql(editor, pwd, title)

    return title
