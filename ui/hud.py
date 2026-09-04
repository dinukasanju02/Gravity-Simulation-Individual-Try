from direct.gui.DirectGui import DirectLabel
from panda3d.core import TextNode


class HUD:
    """Simulation information and controls."""

    def __init__(self, app):
        self.label = DirectLabel(
            text="",
            text_scale=0.030,
            text_align=TextNode.ALeft,
            pos=(-1.30, 0, 0.88),
            frameColor=(0.02, 0.01, 0.04, 0.62),
            text_fg=(0.90, 0.82, 1.0, 1)
        )

    def update(self, paused, mesh, trails, simulation_time):
        self.label["text"] = (
            "3D GRAVITY SIMULATION\n"
            f"Status: {'PAUSED' if paused else 'RUNNING'}\n"
            f"Simulation Time: {simulation_time:.1f}\n"
            f"Spacetime Mesh: {'ON' if mesh else 'OFF'}\n"
            f"Orbit Trails: {'ON' if trails else 'OFF'}\n\n"
            "LEFT MOUSE  Rotate\n"
            "WASD         Move focus\n"
            "Q / E        Move up/down\n"
            "WHEEL        Zoom\n"
            "SPACE        Pause\n"
            "M            Mesh\n"
            "T            Trails\n"
            "R            Reset\n"
            "ESC          Exit"
        )
