"""
        @file       qlibutils.py
        @author     xy
        @since      2012-07-23

        @brief      qLib-related utility functions.
"""

import hou

import datetime
import glob
import os
import sys
import re
import subprocess
import traceback

# for paste_clipboard_to_netview()
from hutil import Qt
import nodegraphutils

FLASH_SECONDS = 6.0


# TODO: msg functions with exception handling


def is_platform(name):
    assert type(name) is str
    return sys.platform.lower().startswith(name.lower())

def is_linux():
    return is_platform('linux')

def is_windows():
    return is_platform('win')

def is_mac():
    return is_platform('darwin')


def houVersionAsFloat():
    v = hou.applicationVersion()
    return float( "%d.%d" % (v[0], v[1], ) )


def statmsg(msg, warn=False):
    """.
    """
    assert type(msg) is str
    s = hou.severityType.ImportantMessage if warn else hou.severityType.Message
    if warn:
        msg = "WARNING: %s" % msg
    if hou.isUIAvailable():
        hou.ui.setStatusMessage(msg, severity=s)


def ynreq(text="Are you sure?",
    buttons=("Yes", "No", ) ):
    """Shows an "Are you sure Y/N" style yes/no dialog.
    """
    do_it = 1
    try:
        do_it = hou.ui.displayMessage(text,
            buttons=buttons,
            default_choice=1, close_choice=1)
    except:
        print "ERROR: %s" % traceback.format_exc()
    return do_it==0



def set_namespace_aliases(prefix="qLib::", alias=True, verbose=False):
    """Defines (non-)namespaced aliases for operators with a particular namespace prefix.

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
    """Copies the specified string to the system clipboard.

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
        hou.ui.copyTextToClipboard(contents)
    except:
        pass


def do_crash_recovery(calledFromUI=False):
    """Performs crash recovery from an emergency-saved file.
    """
    tmpdir = str(hou.getenv("HOUDINI_TEMP_DIR") or hou.getenv("TEMP"))
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

        if ynreq(msg, buttons=("DELETE", "Skip", )):
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
    """Opens the specified directory in the system file browser.
    """
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
    """Finds filesystem paths for specified HDAs.
    """
    hdas = []
    for node in nodes:
        d = node.type().definition()
        if d:
            path = d.libraryFilePath()
            if path != 'Embedded':
                hdas.append(path)
    return hdas


def open_hda_dirs():
    """Opens folders for the selected HDAs.
    """
    hdas = get_hda_paths(hou.selectedNodes())
    dirs = set()

    for h in hdas:
        dirs.add(os.path.split(h)[0])

    for d in dirs:
        open_dir(d)


def hdapath_to_clipboard():
    """Copies the full path of the first selected HDA to the clipboard.
    """
    hdas = get_hda_paths(hou.selectedNodes())
    hdas = '\n'.join(hdas)
    to_clipboard(hdas)


def nodes_to_clipboard(fullPaths=False, hdaTypeNames=False):
    """Copies the names or full paths of selected nodes to the clipboard.
    """
    sep = '\n' if fullPaths else ' '
    nodes = hou.selectedNodes()

    func = lambda n: n.name()

    if hdaTypeNames:
        func = lambda n: n.type().name()

    if fullPaths:
            func = lambda n: n.path()
            if hdaTypeNames:
                func = lambda n: "%s (%s)" % (n.path(), n.type().name(), )

    text = sep.join([ func(n) for n in nodes ])
    to_clipboard(text)


def find_camera(oppattern, path=None):
    """Finds a camera OBJ within nested subnets and returns its full path.
    """
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
    """Creates a dated backup of an output file of a ROP.
    Useful as a ROP Pre-Render call.
    """
    pass


def remove_embedded_hdas():
    """Remove all embedded HDAs from the scene.
    """
    do_it = ynreq(
        "Remove all Embdedded HDAs (OTLs) from the current scene?\n"
        "Warning: This cannot be undone!\n\n"
        "NOTE: Embedded definitions that don't have a non-embedded version available\n"
        "will not be removed.",
        buttons=("Ok", "Cancel", ))

    if do_it:
        hou.hda.uninstallFile("Embedded")


def find_same_nodes(nodes):
    """Find the same node types in a network.
    """

    def type_name(n):
        """Build a (not exactly correct) full typename (but without the asset version)."""
        r = n.networkItemType().name().lower()
        if r=="node":
            r = "::".join(n.type().nameComponents()[0:-1])
        return r

    r = []
    if len(nodes)>0:
        types = set()
        for n in nodes:
            types.add(type_name(n))

        all = nodes[0].parent().allItems()
        r = [ n for n in all if type_name(n) in types ]
    return r


def find_same_colored(nodes):
    """Find nodes with the same color(s) as the specified node(s).
    TODO:
        - make sure there's no need for per-component floating point comparison
    """
    r = []
    if len(nodes)>0:
        colors = set()
        for n in nodes:
            colors.add(n.color())

        all = nodes[0].parent().allItems()
        r = [ n for n in all if n.color() in colors ]
    return r


def get_shape_name(node):
    """Return shape name of the node.
    """
    #TODO: assert: node is a node object
    shape = None
    try:
        shape = node.userData("nodeshape") or node.type().defaultShape()
    except:
        pass
    return shape


def find_same_shape(nodes):
    """Find nodes with the same shape(s) as the specified node(s).
    TODO:
        - make sure there's no need for per-component floating point comparison
    """
    r = []
    if len(nodes)>0:
        shapes = set()
        for n in nodes:
            shapes.add(get_shape_name(n))

        all = nodes[0].parent().allItems()
        r = [ n for n in all if get_shape_name(n) in shapes ]
    return r


def get_netview_path(kwargs):
    """Finds the path of the current network view from kwargs.
    """
    if "editor" in kwargs:
        return kwargs["editor"].pwd()
    else:
        # TODO: raise an error
        return None


def is_node_locked(node):
    """Check if node is locked. Implementation level LOL.
    """
    r = False
    if "isHardLocked" in dir(node):
        r = node.isHardLocked()
    elif "isLocked" in dir(node):
        r = node.isLocked()
    return r


def has_embedded_def(node):
    """Check if the node's HDA definition is Embedded.
    """
    d = node.type().definition()
    r = d and d.libraryFilePath() == "Embedded"
    return r


def get_node_author(node, username_only=False):
    """Returns the author of the specified node.
    """
    author = '???'
    try:
        # digging up author info using an archaic command
        author = hou.hscript('opstat -u %s' % node.path())[0].split(' ')[-1].split('\n')[0]
        if username_only:
            author = author.split("@")[0]
    except:
        pass # we can't hack the info out, just return '???'
    return author


def get_node_authors(nodes, username_only=False):
    """Returns a list of authors for the specified list of nodes.
    """
    r = set()
    for n in nodes:
        r.add(get_node_author(n, username_only=username_only))
    return list(r)


def has_author(node, authors, username_only=False):
    """Check if a node has one of the authors in the "authors" list.
    """
    a = get_node_author(node, username_only=username_only)
    return a in authors


def parm_is_keyframed(parm):
    """Checks if parm is keyframed.
    A parm is considered keyframed if there's at least 2 keyframes,
    or has a single one with a curve expression thing on it (ending with "()")

    parm: a hou.Parm
    """
    num_keys = len(parm.keyframes())
    if num_keys>1:
        return True
    if num_keys==1:
        k = parm.keyframes()[0]
        # single keyframe: should be a hscript expression of "bezier()" or similar
        return \
            k.expressionLanguage() == hou.exprLanguage.Hscript and \
            re.match("^[a-z]*\(\)$", k.expression())
    return False


def parm_is_time_dependent(parm):
    """Checks if parm is time-dependent.
    """
    return parm.isTimeDependent()


def has_parm_with_criteria(node, criteria):
    """Returns True if the specified node has any parms
    that match a given criteria.

    criteria: (lambda) function with a hou.Parm as argument
    """
    parms = node.parms() # should it be parmTuples()?
    for parm in parms:
        if criteria(parm):
            return True
    return False


def has_keyframed_parms(node):
    """Check if a node has keyframed parms.
    """
    return has_parm_with_criteria(node, parm_is_keyframed)


def has_time_dependent_parms(node):
    """Check if a node has time-dependent parms.
    """
    return has_parm_with_criteria(node, parm_is_time_dependent)


def add_to_selection(nodes, kwargs, selectMode=None):
    """Extends the current node selection with 'nodes', according to
    the modifier keys in kwargs.

    no modifier:    replace selection
    shift, alt:     add to selection
    ctrl:           remove from selection
    ctrl+shift:     intersect with selection
    """
    assert selectMode is None or type(selectMode) is str

    haz_shift = kwargs["shiftclick"] or kwargs['altclick']
    haz_ctrl = kwargs["ctrlclick"]

    if selectMode is None:
        # determine select mode based on kwargs
        if haz_shift or haz_ctrl:
            # we got some modifier pressed
            if haz_shift:
                    # shift: add (union), shift+ctrl: intersect
                    selectMode = "intersect" if haz_ctrl else "add"
            else:
                # ctrl: remove from selection
                selectMode = "remove"
    else:
        selectMode = selectMode.lower()

    current = set(hou.selectedItems())
    sel = set(nodes)
    sel_length_old = len(sel)

    if selectMode=="intersect":
        sel = sel.intersection(current)
    elif selectMode=="add":
        sel = sel.union(current)
    elif selectMode=="remove":
        sel = current.difference(sel)
    else:
        selectMode = "replace"

    if sel is not None:
        hou.clearAllSelected()
        for n in sel:
            n.setSelected(True)

    # report back

    msg0 = "Select (%s) %d matches: Now %d selected (was %d)" \
        % ( selectMode.lower(), sel_length_old, len(sel), len(current), )

    if "editor" in kwargs:
        kwargs["editor"].flashMessage("BUTTONS_reselect", msg0, FLASH_SECONDS)

    statmsg("%s   (ALT: add to selection"
        ", CTRL:remove from selecton"
        ", CTRL+ALT:intersect with selection)" % msg0)


def select_netview_nodes(kwargs, criteria, allItems=False, selectMode=None):
    """Select nodes.
    """
    path = get_netview_path(kwargs)
    child_func = path.allItems if allItems else path.children
    sel = None
    try:
        sel = [ n for n in child_func() if criteria(n) ]
    except:
        statmsg("Couldn't select / Selection criteria not applicable", warn=True)

    if sel is not None:
        add_to_selection(sel, kwargs, selectMode=selectMode)


def set_netview_selection(kwargs, criteria, allItems=False):
    """Replace selection with nodes matching a criteria function.
    """
    select_netview_nodes(kwargs, criteria, allItems=allItems, selectMode="replace")



def reset_nodes(kwargs, nodes, resetColor=True, resetShape=True):
    """.
    """
    for n in nodes:
        if resetColor:
            d = n.type().defaultColor()
            if d!=n.color():
                n.setColor(d)
        if resetShape:
            if "nodeshape" in n.userDataDict():
                n.destroyUserData("nodeshape")



def embedded_img_prefix(image_name):
    """.
    """
    return "opdef:/qLib::Object/embedded_images?%s" % image_name


def embedded_hda_typename():
    return 'qLib::embedded_images'


def get_embedded_img_hdadef():
    category = hou.objNodeTypeCategory()
    embedded = 'Embedded'
    hda_def = hou.hdaDefinition(category, embedded_hda_typename(), embedded)
    return hda_def


def get_existing_images(kwargs):
    """Return a list of paths (opdef:/...) for existing images in the hip file.
    """
    R = []
    hda_def = get_embedded_img_hdadef()
    if hda_def:
        R = [ n for n in hda_def.sections() if n.endswith(".png") ]
    return R


def hip_has_pasted_images(kwargs):
    """.
    """
    return len(get_existing_images(kwargs))>0


def add_image_to_netview(image_path, pane, pwd):
    """.
    """
    # add image to network view
    image = hou.NetworkImage(image_path)
    image.setBrightness(0.75)
    #image.setRect(hou.BoundingRect(0, 0, 5, 2))
    s = pane.visibleBounds()
    center = s.center()
    s.translate(-center)
    s.scale((0.25, 0.25, ))
    s.translate(center)
    image.setRect(s)

    images = nodegraphutils.loadBackgroundImages(pwd)
    images.append(image)
    pane.setBackgroundImages(images)
    nodegraphutils.saveBackgroundImages(pwd, images)


def paste_clipboard_to_netview(kwargs):
    """Paste clipboard contents (text or image) into the network editor.
    """
    clipboard = Qt.QtGui.QGuiApplication.clipboard()
    image = clipboard.image()
    text = clipboard.text()
    pane = kwargs.get('editor', None)

    if pane:
        pwd = pane.pwd()

        if image.isNull():
            # paste text (if any)
            if text!="":
                note = pwd.createStickyNote()
                note.move(pane.visibleBounds().center())
                s = note.size()
                s = hou.Vector2((s.x()*1.5, s.y()*0.5, ))
                note.setText(text)
                note.setSize(s)
        else:
            # paste image

            # generate automatic name
            image_name = 'image_' + datetime.datetime.now().replace(microsecond=0).isoformat('_').replace(":", "")

            msg = []

            images = sorted(get_existing_images(kwargs))
            if len(images)>0:
                msg.append("Existing images:")
                c=0
                for i in images:
                    msg.append("   - %s" % i)
                    c+=1
                    if c>=20:
                        break
                if c<len(images):
                    msg.append("   - (...)  ")
                msg.append('\n(Images are stored in an embedded "qLib::embedded_images" /obj node).')

            msg = "\n".join(msg)

            ok, image_name = hou.ui.readInput("Enter name of image to be pasted",
                buttons=('Ok', 'Cancel', ), close_choice=1, help=msg,
                initial_contents=image_name)
            if image_name=='':
                ok = 1
            image_name += '.png'

            if ok==0:
                hda_typename = embedded_hda_typename()
                hda_def = get_embedded_img_hdadef()
                
                # create hda definition if doesn't exist
                if not hda_def:
                    temp_node = hou.node('/obj').createNode('subnet')
                    hda_node = temp_node.createDigitalAsset(name=hda_typename, save_as_embedded=True)
                    hda_node.destroy()
        
                hda_def = get_embedded_img_hdadef()
        
                # create an instance in /obj if doesn't exist
                node = None
                nodes = [ n for n in hou.node('/obj').children() if n.type().name()==hda_typename ]
                
                if len(nodes)==0:
                    node = hou.node('/obj').createNode(hda_typename, node_name="embedded_images")
                    node.setComment("embedded BG images for network views\n(do not delete)")
                    hou.hscript("opset -Y on %s" % node.path())
                    pass # set comment "do not delete"
        
                # add clipboard image to hda definition (as section)
                ba = Qt.QtCore.QByteArray();
                buffer = Qt.QtCore.QBuffer(ba)
                buffer.open(Qt.QtCore.QIODevice.WriteOnly)
                image.save(buffer, "png")       
                buffer.close()
                hda_def.addSection(image_name, str(buffer.data()))
                
                # add image to network view
                add_image_to_netview(embedded_img_prefix(image_name), pane, pwd)


def paste_existing_image(kwargs):
    """.
    """
    images = sorted(get_existing_images(kwargs))
    pane = kwargs.get('editor', None)
    sel = hou.ui.selectFromList(images, exclusive=True,
                                title="Paste Existing Image",
                                message="Select Image to Paste")
    if len(sel)>0 and pane:
        image_name = images[sel[0]]
        pwd = pane.pwd()
        add_image_to_netview(embedded_img_prefix(image_name), pane, pwd)




def embed_selected_hdas(kwargs):
    """Embed HDA definitions of selected nodes (interactive only).
    """
    defs = set()

    for s in hou.selectedNodes():
        d = s.type().definition()
        if d and d.libraryFilePath()!="Embedded":
            defs.add(d)

    defs = list(defs)

    if len(defs)==0:
        statmsg("No nodes with embeddable definitions were selected")
        return

    msg = "Embed the following HDA(s) into the current hip file?\n\n"
    msg += "\n".join([ "HDA:  %s\npath:  %s\n" % (d.nodeType().name(), d.libraryFilePath(), ) for d in defs ])

    if ynreq(msg, buttons=("Embed", "Cancel", )):
        for d in defs:
            d.copyToHDAFile("Embedded")
            # TODO: switch definition? this seems to switch it
#


def show_houdinipath(kwargs):
    """Displays entries .
    """
    hou.ui.displayMessage(
        "Houdini Path ($HOUDINI_PATH) entries (in order)",
        details = "\n".join(hou.houdiniPath()),
        details_expanded=True)


def show_shellcmd_results(kwargs, cmd, label):
    """Runs a shell command and displays its results.
    """

    try:
        result = os.popen(cmd).read()
        hou.ui.displayMessage(
            "%s\n(shell command: '%s')" % (label, cmd, ),
            details = result,
            details_expanded=True
        )

    except:
        print "ERROR: %s" % traceback.format_exc()


def displayHelpPath(path):
    """Wrapper for displaying a help page.
    """
    assert type(path) is str
    hou.ui.curDesktop().displayHelpPath(path)


def clipboard_has_node_paths(kwargs):
    """Return True if the clipboard contains valid node path(s).
    """
    R = False
    n = hou.ui.getTextFromClipboard().split()
    n = n[0] if len(n)>0 else ""
    R = hou.node(n)!=None
    return R


def paste_clipboard_as_object_merge(kwargs):
    """Paste copied clipboard node path(s) as Object Merge SOP(s).
    """
    try:
        nodes = [ hou.node(n) for n in hou.ui.getTextFromClipboard().split() ]

        haz_shift = kwargs["shiftclick"] or kwargs['altclick']

        objm = None
        root = kwargs['editor'].pwd()
        offset = (0, 0, )

        for node in nodes:
            if objm==None or haz_shift:
                objm = root.createNode("object_merge",
                    node_name="objm_%s" % node.name())
                objm.setPosition( kwargs['editor'].visibleBounds().center() )
                objm.move(offset)
                offset = ( offset[0]+1.0, offset[1]-1.0, )
                objm.parm("numobj").set(0)

            if objm:
                n = objm.parm("numobj")
                i = n.eval()+1
                n.set(i)
                objm.parm("objpath%d" %i).set(objm.relativePathTo(node))
    except:
        print "ERROR: %s" % traceback.format_exc()



def update_gallery_items(kwargs=None):
    """Reload all gallery items.
    """
    galleries = hou.galleries.galleries()
    gal_files = set() # a set of all currently loaded gallery files

    # collect all loaded galleries and remove them
    for g in galleries:
        try:
            f = re.search('"([^\"]+)"', repr(g)).group(1)
            gal_files.add(f)
            #print "found:", f
            hou.galleries.removeGallery(f)
        except:
            pass

    # look for new gallery files in the paths, and collect them
    paths = hou.houdiniPath("HOUDINI_GALLERY_PATH")
    for path in paths:
        files = glob.glob(path+"/*.gal")
        gal_files.update(files)

    # install all found gallery files
    for file in gal_files:
        #print "installing:", file
        hou.galleries.installGallery(file)
