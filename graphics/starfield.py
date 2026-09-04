import random
from direct.showbase import ShowBaseGlobal

class StarField:
    """3D background star field."""

    def __init__(self, app, count=700):
        self.root = app.render.attachNewNode("3D Star Field")

        for _ in range(count):
            star = ShowBaseGlobal.base.loader.loadModel("models/misc/sphere")
            star.reparentTo(self.root)

            star.setPos(
                random.uniform(-190, 190),
                random.uniform(-190, 190),
                random.uniform(-110, 110)
            )

            size = random.uniform(0.018, 0.065)
            star.setScale(size)

            brightness = random.uniform(0.65, 1.0)
            star.setColor(brightness, brightness, brightness, 1)
            star.setLightOff(True)
