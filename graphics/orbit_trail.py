from panda3d.core import LineSegs


class OrbitTrail:
    """
    Displays the recent 3D path of a celestial body.

    Each planet gets its own independent trail.
    """

    def __init__(self, app, body, maximum_points=180):

        self.app = app
        self.body = body
        self.maximum_points = maximum_points

        self.points = []

        # Parent node for this planet's trail.
        self.root = app.render.attachNewNode(
            f"{body.name} 3D Orbit Trail"
        )

        # Keep a reference to the actual geometry NodePath.
        self.trail_node = None

    def set_visible(self, visible):

        if visible:
            self.root.show()
        else:
            self.root.hide()

    def clear(self):

        self.points.clear()

        if self.trail_node is not None:
            self.trail_node.removeNode()
            self.trail_node = None

    def update(self):

        # Store current 3D position.
        self.points.append(
            tuple(self.body.position)
        )

        # Limit trail length.
        if len(self.points) > self.maximum_points:
            self.points.pop(0)

        if len(self.points) < 2:
            return

        # Delete the previous geometry correctly.
        if self.trail_node is not None:
            self.trail_node.removeNode()
            self.trail_node = None

        # Create new 3D line geometry.
        lines = LineSegs()

        lines.setThickness(1.2)

        lines.setColor(
            self.body.color[0],
            self.body.color[1],
            self.body.color[2],
            0.8
        )

        # Start at first recorded position.
        lines.moveTo(
            *self.points[0]
        )

        # Connect all positions.
        for point in self.points[1:]:

            lines.drawTo(
                *point
            )

        # Attach geometry to the trail parent.
        self.trail_node = self.root.attachNewNode(
            lines.create()
        )