import hou


class State(object):
    def __init__(self, scene_viewer, state_name):
        self.state_name = state_name
        self.scene_viewer = scene_viewer
        self._base_xy = None
        self._cam_focal = None
        self._cam_p = None          # camera pivot (look-at point) in world space
        self._cam_t = None          # camera tranaslation in camera-something space
        self._cam_ws = None         # camera position in world space
        self._undo = False

    def onGenerate(self, kwargs):
        self.scene_viewer.setPromptMessage(
            "<--  Drag left/right  -->\n"
            "\nLMB: Dolly/Zoom ('Vertigo')"
            "   MMB: Focal Length Zoom"
            "   RMB: Dolly"
            "\nHold SPACE for regular viewport navigation",
            #"\n\nShift+Left Click to specify new dolly-zoom focal distance"
            hou.promptMessageType.Message
            )

    def onResume(self, kwargs):
        self.onGenerate(kwargs)

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

        lmb = device.isLeftButton()
        mmb = device.isMiddleButton()
        rmb = device.isRightButton()
        if lmb or mmb or rmb:
            # left mouse button is down
            x = device.mouseX()
            y = device.mouseY()

            if device.isShiftKey():
                prim = viewport.queryPrimAtPixel(None, int(x), int(y))
                print("prim:", prim)

            if not self._undo:
                self._undo = True
                self.scene_viewer.beginStateUndo("Zoom")
                #print "begin undo"

            if self._base_xy:
                dx = x - self._base_xy[0]
                dy = y - self._base_xy[1]
                delta = dx

                #print "delta:", delta

                if mmb: # kwargs["mode"]=="zoom":
                    # regular zoom
                    f = self._cam_focal + delta * 0.1
                    cam.setFocalLength(f)
                else:
                    # dolly zoom
                    # (using relative delta and include original distance so
                    # -hopefully- we'll stay scene size independent)
                    width, _ = self.scene_viewer.contentSize()
                    t = self._cam_t - self._dolly_dir * (delta/width)*2.0*self._dist_orig

                    try:
                        cam.setTranslation(t) # NOTE: this might throw an exception
                        if lmb:
                            dist = t-self._cam_p
                            dist = dist.length()
                            f = self._cam_focal * (dist / self._dist_orig)
                            cam.setFocalLength(f)
                    except:
                        pass

            else:
                self._base_xy = (x, y, )
                self._cam_focal = cam.focalLength()
                self._cam_p = hou.Vector3(cam.pivot()) # view pivot
                self._cam_t = hou.Vector3(cam.translation()) # camera translation
                self._cam_ws = hou.Vector3(0,0,0) * viewport.viewTransform() # camera pt in world space
                d = self._cam_ws - self._cam_p
                self._dist_orig = d.length()
                self._dolly_dir = hou.Vector3(0,0,1)
        else:
            # no left mouse button
            self._base_xy = None
            if self._undo:
                self._undo = False
                self.scene_viewer.endStateUndo()
                #print "end undo"




