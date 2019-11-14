import hou


class ScrubState(object):
    def __init__(self, scene_viewer, state_name):
        self.state_name = state_name
        self.scene_viewer = scene_viewer
        self._base_xy = None
        self._cam_focal = None
        self._cam_p = None
        self._cam_t = None
        self._undo = False

    def onGenerate(self, kwargs):
        pass
        self.scene_viewer.setPromptMessage(
            "Drag left/right to adjust. Use RMB menu to select mode.\n\n"
            "Shift+Left Click to specify new dolly-zoom focal distance"
            )

    def onExit(self, kwargs):
        self.scene_viewer.clearPromptMessage()
        # in case someone exits mid-drag...
        if self._undo:
            self._undo = False
            self.scene_viewer.endStateUndo()
            #print "end undo #2"


    def onMouseEvent(self, kwargs):
        device = kwargs["ui_event"].device()
        viewport = self.scene_viewer.curViewport()
        cam = viewport.defaultCamera()

        # TODO: shift-LMB should specify new vertigo distance!

        if device.isLeftButton():
            # left mouse button is down
            x = device.mouseX()
            y = device.mouseY()

            if not self._undo:
                self._undo = True
                self.scene_viewer.beginStateUndo("Zoom")
                #print "begin undo"
            
            if self._base_xy:
                dx = x - self._base_xy[0]
                dy = y - self._base_xy[1]
                delta = dx
                
                #print "delta:", delta
                
                if kwargs["mode"]=="zoom":
                    # regular zoom
                    f = self._cam_focal + delta * 0.1
                    cam.setFocalLength(f)
                else:
                    # dolly zoom
                    # (using relative delta and include original distance so
                    # -hopefully- we'll stay scene size independent)
                    width, _ = self.scene_viewer.contentSize()
                    t = self._cam_t - self._dolly_dir * (delta/width)*2.0*self._dist_orig

                    cam.setTranslation(t) # NOTE: this might throw an exception
                    dist = t-self._cam_p
                    dist = dist.length()
                    f = self._cam_focal * (dist / self._dist_orig)
                    #cam.setFocalLength(f)
                
            else:
                self._base_xy = (x, y, )
                self._cam_focal = cam.focalLength()
                self._cam_p = hou.Vector3(cam.pivot()) # view pivot
                self._cam_t = hou.Vector3(cam.translation()) # camera translation
                d = self._cam_t - self._cam_p
                self._dist_orig = d.length()
                # TODO: FIX THIS-- dolly dir should always point towards camera direction!
                d = hou.Vector3(0,0,1)# * cam.rotation().inverted()
                # WTF?! just {0,0,1} works?!?!
                d = d.normalized()
                self._dolly_dir = d
                print "_cam_t", self._cam_t
                #print "_cam_p", self._cam_p
        else:
            # no left mouse button
            self._base_xy = None
            if self._undo:
                self._undo = False
                self.scene_viewer.endStateUndo()
                #print "end undo"



def createViewerStateTemplate():
    state_name = "qLib::camera_zoom_vertigo_ql"
    state_label = "Camera Zoom/Vertigo [qL]"
    template = hou.ViewerStateTemplate(
            state_name,
            state_label,
            hou.objNodeTypeCategory(),
            #contexts = [ hou.sopNodeTypeCategory(), hou.dopNodeTypeCategory(), hou.lopNodeTypeCategory(), ],
        )
    template.bindFactory(ScrubState)

    menu = hou.ViewerStateMenu(state_name, state_label)
    menu.addRadioStrip("mode", "Mode", "vertigo")
    menu.addRadioStripItem("mode", "vertigo", "Dolly-Zoom ('Vertigo')")
    menu.addRadioStripItem("mode", "zoom", "Regular Zoom (focal length)")
    template.bindMenu(menu)
    
    return template




