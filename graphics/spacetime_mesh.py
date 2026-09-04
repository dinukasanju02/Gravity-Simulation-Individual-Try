import math
from panda3d.core import LineSegs


class SpacetimeMesh:
    """
    Dynamic 3D spacetime-curvature mesh.

    The mesh bends downward around massive celestial bodies.
    Larger mass = stronger curvature.
    """

    def __init__(self, app, size=34, step=2.0):
        self.app = app
        self.size = size
        self.step = step

        self.root = app.render.attachNewNode("3D Spacetime Mesh")
        self.visible = True
        self.mesh_node = None

    def set_visible(self, visible):
        self.visible = visible

        if visible:
            self.root.show()
        else:
            self.root.hide()

    def _calculate_z(self, x, y, bodies):
        """
        Calculate the vertical displacement of the spacetime surface.

        This creates the visual 'sinking' effect.
        """

        z = 0.0

        for body in bodies:

            dx = x - body.position.x
            dy = y - body.position.y

            distance = math.sqrt(
                dx * dx +
                dy * dy
            ) + 1.5

            # Stronger bodies create deeper curvature.
            strength = min(
                9.0,
                body.mass ** 0.55 * 0.045
            )

            z -= strength / distance

        return z

    def update(self, bodies):

        if not self.visible:
            return

        # Remove the previous visual mesh.
        if self.mesh_node is not None:
            self.mesh_node.removeNode()
            self.mesh_node = None

        lines = LineSegs()

        lines.setThickness(1.0)
        lines.setColor(
            0.65,
            0.18,
            0.95,
            0.50
        )

        values = [
            -self.size + i * self.step
            for i in range(
                int((2 * self.size) / self.step) + 1
            )
        ]

        # -------------------------------------------------
        # X-direction grid lines
        # -------------------------------------------------

        for y in values:

            first_point = True

            for x in values:

                z = self._calculate_z(
                    x,
                    y,
                    bodies
                )

                if first_point:

                    lines.moveTo(
                        x,
                        y,
                        z
                    )

                    first_point = False

                else:

                    lines.drawTo(
                        x,
                        y,
                        z
                    )

        # -------------------------------------------------
        # Y-direction grid lines
        # -------------------------------------------------

        for x in values:

            first_point = True

            for y in values:

                z = self._calculate_z(
                    x,
                    y,
                    bodies
                )

                if first_point:

                    lines.moveTo(
                        x,
                        y,
                        z
                    )

                    first_point = False

                else:

                    lines.drawTo(
                        x,
                        y,
                        z
                    )

        # Create the new geometry.
        self.mesh_node = self.root.attachNewNode(
            lines.create()
        )