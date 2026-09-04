from panda3d.core import Vec3


class CameraController:
    """Interactive third-person orbital camera."""

    def __init__(self, app):
        self.app = app

        self.target = Vec3(0, 0, 0)
        self.distance = 92.0
        self.heading = 25.0
        self.pitch = 28.0

        self.dragging = False
        self.last_mouse = None

        for event in ("mouse1", "mouse3"):
            app.accept(event, self.start_drag)
        app.accept("mouse1-up", self.stop_drag)
        app.accept("mouse3-up", self.stop_drag)

        app.accept("wheel_up", self.zoom_in)
        app.accept("wheel_down", self.zoom_out)

        app.taskMgr.add(self.update, "camera_controller")

    def start_drag(self):
        if self.app.mouseWatcherNode.hasMouse():
            m = self.app.mouseWatcherNode.getMouse()
            self.last_mouse = (m.getX(), m.getY())
            self.dragging = True

    def stop_drag(self):
        self.dragging = False
        self.last_mouse = None

    def zoom_in(self):
        self.distance = max(18, self.distance - 5)

    def zoom_out(self):
        self.distance = min(180, self.distance + 5)

    def update(self, task):
        # Keyboard movement changes the point the camera looks at.
        if self.app.mouseWatcherNode.isButtonDown(
            __import__("panda3d.core").core.KeyboardButton.asciiKey("w")
        ):
            self.target.y += 0.45
        if self.app.mouseWatcherNode.isButtonDown(
            __import__("panda3d.core").core.KeyboardButton.asciiKey("s")
        ):
            self.target.y -= 0.45
        if self.app.mouseWatcherNode.isButtonDown(
            __import__("panda3d.core").core.KeyboardButton.asciiKey("a")
        ):
            self.target.x -= 0.45
        if self.app.mouseWatcherNode.isButtonDown(
            __import__("panda3d.core").core.KeyboardButton.asciiKey("d")
        ):
            self.target.x += 0.45
        if self.app.mouseWatcherNode.isButtonDown(
            __import__("panda3d.core").core.KeyboardButton.asciiKey("q")
        ):
            self.target.z -= 0.35
        if self.app.mouseWatcherNode.isButtonDown(
            __import__("panda3d.core").core.KeyboardButton.asciiKey("e")
        ):
            self.target.z += 0.35

        if self.dragging and self.app.mouseWatcherNode.hasMouse():
            m = self.app.mouseWatcherNode.getMouse()
            current = (m.getX(), m.getY())

            if self.last_mouse:
                dx = current[0] - self.last_mouse[0]
                dy = current[1] - self.last_mouse[1]
                self.heading -= dx * 90
                self.pitch = max(8, min(80, self.pitch + dy * 70))

            self.last_mouse = current

        self._position_camera()
        return task.cont

    def _position_camera(self):
        import math

        h = math.radians(self.heading)
        p = math.radians(self.pitch)

        x = self.target.x + self.distance * math.cos(p) * math.sin(h)
        y = self.target.y - self.distance * math.cos(p) * math.cos(h)
        z = self.target.z + self.distance * math.sin(p)

        self.app.camera.setPos(x, y, z)
        self.app.camera.lookAt(self.target)
