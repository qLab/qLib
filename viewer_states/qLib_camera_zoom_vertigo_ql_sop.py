import hou


import qLibCameraZoomVertigo



def createViewerStateTemplate():
    state_name = "qLib::camera_zoom_vertigo_ql_sop"
    state_label = "Camera Zoom/Vertigo (sop) [qL]"
    template = hou.ViewerStateTemplate(
            state_name,
            state_label,
            hou.sopNodeTypeCategory(),
            #contexts = [ hou.sopNodeTypeCategory(), hou.dopNodeTypeCategory(), hou.lopNodeTypeCategory(), ],
        )
    template.bindFactory(qLibCameraZoomVertigo.State)

    return template




