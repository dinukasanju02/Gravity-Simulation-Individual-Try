from direct.gui.DirectGui import DirectFrame, DirectLabel, DirectButton
from panda3d.core import TextNode


class IntroScreen:
    """Purple project title screen shown when the application starts."""

    def __init__(self, app):
        self.app = app
        self.frame = DirectFrame(
            frameColor=(0.035, 0.008, 0.08, 0.97),
            frameSize=(-1, 1, -1, 1)
        )

        DirectLabel(
            parent=self.frame,
            text="GRAVITY SIMULATION",
            text_scale=0.105,
            text_fg=(0.78, 0.30, 1.0, 1),
            text_align=TextNode.ACenter,
            pos=(0, 0, 0.28),
            frameColor=(0, 0, 0, 0)
        )

        DirectLabel(
            parent=self.frame,
            text="FULL 3D SOLAR SYSTEM",
            text_scale=0.052,
            text_fg=(0.92, 0.88, 1.0, 1),
            text_align=TextNode.ACenter,
            pos=(0, 0, 0.10),
            frameColor=(0, 0, 0, 0)
        )

        DirectLabel(
            parent=self.frame,
            text="Project by Dhinuka S Madurawala",
            text_scale=0.038,
            text_fg=(0.70, 0.60, 0.88, 1),
            text_align=TextNode.ACenter,
            pos=(0, 0, -0.05),
            frameColor=(0, 0, 0, 0)
        )

        DirectButton(
            parent=self.frame,
            text="START SIMULATION",
            scale=0.075,
            pos=(0, 0, -0.30),
            frameColor=(0.38, 0.08, 0.58, 1),
            text_fg=(1, 1, 1, 1),
            command=self.start
        )

    def start(self):
        self.frame.destroy()
