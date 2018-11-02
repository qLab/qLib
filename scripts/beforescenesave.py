"""
        @file       beforescenesave.py
        @author     xy
        @since      2018-11-03

        @brief      Python script that runs before saving a hip file.

        It stores a list of last scene name versions in the file.

        Also, it adds a placeholder entry in the undo queue to indicate
        that the file was saved.
"""

if False: # not kwargs["autosave"]:

    # TODO: store current scene info in hip file
    #
    pass


    # add current scene file name to the undo queue to indicate save
    #
    with hou.undos.group("(-- [qL] Saved as: %s --)" % hou.hipFile.basename()):
        try:
            hou.node("/").setComment("")
        except:
            pass


