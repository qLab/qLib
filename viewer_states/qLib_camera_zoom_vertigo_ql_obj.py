import hou


import qLibCameraZoomVertigo



def createViewerStateTemplate():
    state_name = "qLib::camera_zoom_vertigo_ql_obj"
    state_label = "Camera Zoom/Vertigo (obj) [qL]"
    template = hou.ViewerStateTemplate(
            state_name,
            state_label,
            hou.objNodeTypeCategory(),
            #contexts = [ hou.sopNodeTypeCategory(), hou.dopNodeTypeCategory(), hou.lopNodeTypeCategory(), ],
        )
    template.bindFactory(qLibCameraZoomVertigo.State)

    return template




