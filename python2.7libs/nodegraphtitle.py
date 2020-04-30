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

def networkEditorTitleRight(editor):
    try:
        title = ''
        pwd = editor.pwd()
        title += pwd.childTypeCategory().label()

    except:
        title = ''

    return title

