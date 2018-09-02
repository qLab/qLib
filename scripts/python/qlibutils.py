"""
        @file       qlibutils.py
        @author     xy
        @since      2012-07-23

        @brief      qLib-related utility functions.
"""

import hou

import glob
import os
import platform
import re
import subprocess
import traceback


# TODO: msg functions with exception handling


def is_platform(name='none'):
    return name.lower() in platform.system().lower()

def is_linux():
    return is_platform('linux')

def is_windows():
    return is_platform('win')

def is_mac():
    return is_platform('mac')



def statmsg(msg, warn=False):
    '''.'''
    s = hou.severityType.Warning if warn else hou.severityType.Message
    if hou.isUIAvailable():
        hou.ui.setStatusMessage(msg, severity=s)


def set_namespace_aliases(prefix="qLib::", alias=True, verbose=False):
    """
    Defines (non-)namespaced aliases for operators with a particular namespace prefix.

    This is used for always creating the namespaced versions of assets, even if an
    older .hip file contains non-namespaced asset names.

    Mapping looks like:  <opname>  -->  <prefix>::<opname>::<version>


    @note
            IMPORTANT: Although the manual says it's fine to omit the version of a
            namespaced asset (and that would refer to the latest version),
            omitting it results in files getting messed up when loaded,
            so version numbers _are_ included in the opaliases.

    @note
            This function should be called (preferably) on Houdini startup, e.g.

            import qlibutils
            qlibutils.set_namespace_aliases( ["qLib::", "myStuff::"] )

    @todo
            For each asset, the highest version number should be found and used.
            Right now it uses the first version it founds (which is fine for now).

    """

    if type(prefix) is list:
        for p in prefix:
            set_namespace_aliases(p)
        return

    assert "::" in prefix, "Include trailing '::' characters in prefix"

    cmds = []
    for file in hou.hda.loadedFiles():

        names = [(d.nodeType().name(), d.nodeTypeCategory().name())
                 for d in list(hou.hda.definitionsInFile(file))
                 if prefix in d.nodeType().name()]

        for n in names:

            try:
                # strip namespace prefix and version suffix
                old = re.sub("^[^:]+::", "", n[0])
                old = re.search("^[^:]+", old).group(0)

                # opalias <network> <namespaced-op.> <plain-old-op.>
                cmd = "opalias %s %s %s" % (n[1], n[0], old)

                if cmd not in cmds:
                    if verbose:
                        print cmd
                    if alias:
                        hou.hscript(cmd)
                    cmds.append(cmd)
                else:
                    print "# ALREADY ALIASED: %s (%s)" % (cmd, file)

            except:
                print "ERROR: %s" % traceback.format_exc()


def to_clipboard(contents="", env=None):
    """
    Copy the specified string to the system clipboard.

    @note
            - Linux only at the moment
            - requires xclip to be installed

    @todo
            Make it work under other OSs than linux?
    """
    try:
        contents = str(contents)
        if env:
            contents = str(hou.getenv(env))

        statmsg("(linux) to clipboard: '%s'" % contents)
        cmd = 'xclip'
        if is_windows():
            cmd = 'clip'
        if is_mac():
            cmd = 'pbcopy'
        hou.hscript('unix \'echo -n "%s" | %s\'' % (contents, cmd, ))
        # hackety hack
    except:
        pass


def do_crash_recovery(calledFromUI=False):
    tmpdir = str(hou.getenv("TEMP") or hou.getenv("HOUDINI_TEMP_DIR"))
    files = glob.glob(os.path.join(tmpdir, '*.hip'))

    uicall = calledFromUI

    if hou.isUIAvailable() and len(files) > 0:

        td = os.path.join(tmpdir, '')  # dir with '/'
        files = [(f, os.path.getmtime(f), ) for f in files]
        files = sorted(files, key=lambda f: f[1], reverse=True)
        files = [str(re.sub('^%s' % td, '', f[0])) for f in files]

        sel = hou.ui.selectFromList(files, exclusive=True,
                                    title="Crash Recovery",
                                    message="Select .hip File to Recover")

        recovered = False
        if len(sel) > 0:
            f = files[sel[0]]
            fn = os.path.join(tmpdir, f)

            # extract HIPNAME
            f = re.sub('^crash.', '', f)
            f = re.sub('\..+_[0-9]+\.hip', '.hip', f)

            # do recovery
            try:
                hou.hipFile.clear(True)
                hou.hipFile.load(fn, True)
                hou.setUpdateMode(hou.updateMode.Manual)
                recovered = True
            except:
                hou.ui.setStatusMessage(
                    "error while recovering file %s" % fn, hou.severityType.Error)
                print "ERROR: %s" % traceback.format_exc()

            hou.hipFile.setName(f)

        # delete crash file(s)

        msg = 'Cleanup: Delete all crash recovery hip files?'
        if recovered:
            msg = \
                'File recovered. Make sure to save it to a safe location.\n' \
                'NOTE: Update mode is set to "Manual" to avoid potential re-crashes.\n' \
                '\n%s' % msg

        d = hou.ui.displayMessage(msg, buttons=("DELETE", "Skip", ))
        if d == 0:
            files = \
                glob.glob(os.path.join(tmpdir, 'crash.*')) + \
                glob.glob(os.path.join(tmpdir, '*.hip'))
            for f in files:
                try:
                    os.remove(f)
                except:
                    pass

            hou.ui.setStatusMessage(
                "crash recovery cleanup: deleted %d files" % len(files))
        else:
            pass  # user cancelled

    else:
        # no crash files found
        #
        if uicall:
            hou.ui.setStatusMessage(
                '  Crash Recovery:  No emergency-saved .hip file(s) found -- nothing to recover. (%s)' % tmpdir, hou.severityType.ImportantMessage)
            pass


def open_dir(dir="", env=None):
    '''.'''
    dir = str(dir)

    if env:
        dir = str(hou.getenv(env))

    if not os.path.exists(dir):
        statmsg("Directory doesn't exist (%s)" % dir, warn=True)
        return

    if is_linux():
        statmsg("(linux) xdg-open %s" % dir)
        subprocess.call(["xdg-open", dir])

    if is_windows():
        dir = dir.replace('/', '\\')
        statmsg("(windows) start %s" % dir)
        subprocess.call(["start", dir])

    if is_mac():
        statmsg("(mac) open %s" % dir)
        subprocess.call(["open", dir])


def get_hda_paths(nodes):
    '''Find filesystem paths for specified HDAs.'''

    hdas = []
    for node in nodes:
        d = node.type().definition()
        if d:
            path = d.libraryFilePath()
            if path != 'Embedded':
                hdas.append(path)
    return hdas


def open_hda_dirs():
    '''Open folders.'''
    hdas = get_hda_paths(hou.selectedNodes())
    dirs = set()

    for h in hdas:
        dirs.add(os.path.split(h)[0])

    for d in dirs:
        open_dir(d)


def hdapath_to_clipboard():
    '''Copy the full path of the first selected HDA to the clipboard.'''
    hdas = get_hda_paths(hou.selectedNodes())
    hdas = ' '.join(hdas)
    to_clipboard(hdas)


def find_camera(oppattern, path=None):
    '''Finds a camera OBJ within nested subnets and returns its full path.'''
    r = ''
    try:
        root = hou.pwd()
        if path:
            root = hou.node(path)
        root = root.glob(oppattern)

        if len(root) > 0:
            cam = [n.path() for n in root[0].allSubChildren()
                   if n.type().name() == 'cam']
            if len(cam) > 0:
                r = cam[0]
            else:
                pass  # no camera found
        else:
            pass  # no root node found

    except:
        pass  # TODO: error handling

    return r


def backup_rop_output_file():
    '''Creates a dated backup of an output file of a ROP. Useful as a ROP Pre-Render call.'''
    pass
