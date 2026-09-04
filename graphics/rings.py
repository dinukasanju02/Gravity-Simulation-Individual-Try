import math
from panda3d.core import Geom, GeomNode, GeomVertexData, GeomVertexFormat
from panda3d.core import GeomVertexWriter, GeomTriangles, NodePath


class TorusRings:
    """Small procedural 3D torus mesh used for Saturn's rings."""

    def __init__(self, render, major_radius=2.25, tube_radius=0.08):
        self.node = render.attachNewNode("Saturn 3D Rings")
        self._build(major_radius, tube_radius)

    def _build(self, R, r):
        segments = 96
        sides = 8

        data = GeomVertexData(
            "torus", GeomVertexFormat.getV3(), Geom.UHStatic
        )
        writer = GeomVertexWriter(data, "vertex")

        for i in range(segments):
            u = 2 * math.pi * i / segments
            for j in range(sides):
                v = 2 * math.pi * j / sides
                radius = R + r * math.cos(v)
                x = radius * math.cos(u)
                y = radius * math.sin(u)
                z = r * math.sin(v)
                writer.addData3(x, y, z)

        triangles = GeomTriangles(Geom.UHStatic)

        for i in range(segments):
            ni = (i + 1) % segments
            for j in range(sides):
                nj = (j + 1) % sides
                a = i * sides + j
                b = ni * sides + j
                c = ni * sides + nj
                d = i * sides + nj
                triangles.addVertices(a, b, c)
                triangles.addVertices(a, c, d)

        geom = Geom(data)
        geom.addPrimitive(triangles)

        node = GeomNode("3D Ring Geometry")
        node.addGeom(geom)
        ring = self.node.attachNewNode(node)
        ring.setColor(0.84, 0.69, 0.42, 0.85)
        ring.setTwoSided(True)

        # Saturn's rings are slightly tilted.
        self.node.setP(12)

    def set_pos(self, position):
        self.node.setPos(position)

    def set_scale(self, scale):
        self.node.setScale(scale)
