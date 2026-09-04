from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import AmbientLight, DirectionalLight

from core.physics_engine import PhysicsEngine
from core.celestial_body import Star, Planet, Moon
from graphics.starfield import StarField
from graphics.spacetime_mesh import SpacetimeMesh
from graphics.camera import CameraController
from graphics.orbit_trail import OrbitTrail
from ui.intro_screen import IntroScreen
from ui.hud import HUD


class GravitySimulation(ShowBase):
    """Main application class coordinating the OOP simulation."""

    def __init__(self):
        super().__init__()
        self.disableMouse()
        self.setBackgroundColor(0.004, 0.002, 0.015)

        self.paused = False
        self.mesh_visible = True
        self.trails_visible = True
        self.simulation_time = 0.0

        self._setup_lights()

        self.bodies = []
        self.initial_states = []
        self.trails = []

        self._create_solar_system()

        self.starfield = StarField(self, 750)
        self.spacetime = SpacetimeMesh(self, size=34, step=2.0)
        self.camera_controller = CameraController(self)
        self.hud = HUD(self)
        self.intro = IntroScreen(self)

        self.accept("space", self.toggle_pause)
        self.accept("m", self.toggle_mesh)
        self.accept("t", self.toggle_trails)
        self.accept("r", self.reset_simulation)
        self.accept("escape", self.userExit)

        self.taskMgr.add(self.update, "gravity_update")

    def _setup_lights(self):
        ambient = AmbientLight("ambient")
        ambient.setColor((0.12, 0.12, 0.16, 1))
        self.render.setLight(self.render.attachNewNode(ambient))

        sunlight = DirectionalLight("sunlight")
        sunlight.setColor((1.0, 0.86, 0.68, 1))
        light_node = self.render.attachNewNode(sunlight)
        light_node.setHpr(-25, -55, 0)
        self.render.setLight(light_node)

    def _create_solar_system(self):
        # Distances are deliberately compressed so the whole system is visible.
        sun = Star(
            "Sun", 333000.0, 4.2,
            (0, 0, 0), (0, 0, 0),
            (1.0, 0.70, 0.10, 1)
        )
        self.bodies.append(sun)

        planets = [
            ("Mercury", 0.055, 0.48, 8.0, 0.10, (0.55, 0.55, 0.58, 1)),
            ("Venus",   0.815, 0.75, 12.0, -0.06, (0.92, 0.67, 0.32, 1)),
            ("Earth",   1.000, 0.82, 16.0, 0.04, (0.18, 0.45, 1.0, 1)),
            ("Mars",    0.107, 0.62, 20.0, 0.11, (0.88, 0.27, 0.12, 1)),
            ("Jupiter", 317.8, 1.80, 28.0, -0.08, (0.78, 0.58, 0.37, 1)),
            ("Saturn",  95.2,  1.55, 37.0, 0.06, (0.82, 0.70, 0.48, 1)),
            ("Uranus",  14.5, 1.15, 47.0, -0.10, (0.42, 0.82, 0.90, 1)),
            ("Neptune", 17.1, 1.12, 58.0, 0.08, (0.20, 0.38, 0.95, 1)),
        ]

        G = self.physics_G()
        for name, mass, radius, distance, inclination, color in planets:
            speed = (G * sun.mass / distance) ** 0.5

            # Give every planet a slightly different 3D starting orientation.
            angle = len(self.bodies) * 0.55
            x = distance * __import__("math").cos(angle)
            y = distance * __import__("math").sin(angle)
            z = distance * 0.035 * __import__("math").sin(inclination * 10)

            position = (x, y, z)
            velocity = (
                -speed * __import__("math").sin(angle),
                speed * __import__("math").cos(angle),
                speed * inclination * 0.025
            )

            planet = Planet(name, mass, radius, position, velocity, color)
            self.bodies.append(planet)

            if name == "Saturn":
                planet.create_rings(self.render)

        earth = next(b for b in self.bodies if b.name == "Earth")
        moon = Moon(
            "Moon", 0.0123, 0.24,
            (earth.position.x + 1.7, earth.position.y, earth.position.z + 0.25),
            (earth.velocity.x, earth.velocity.y + 1.05, earth.velocity.z + 0.15),
            (0.72, 0.72, 0.76, 1),
            parent=earth
        )
        self.bodies.append(moon)

        for body in self.bodies:
            body.create_model(self.render)

        self.physics = PhysicsEngine(G=G)
        self.physics.set_bodies(self.bodies)

        for body in self.bodies:
            self.initial_states.append(body.save_state())

        for body in self.bodies:
            if isinstance(body, Planet):
                self.trails.append(OrbitTrail(self, body, maximum_points=180))

    @staticmethod
    def physics_G():
        return 0.0008

    def toggle_pause(self):
        self.paused = not self.paused

    def toggle_mesh(self):
        self.mesh_visible = not self.mesh_visible
        self.spacetime.set_visible(self.mesh_visible)

    def toggle_trails(self):
        self.trails_visible = not self.trails_visible
        for trail in self.trails:
            trail.set_visible(self.trails_visible)

    def reset_simulation(self):
        for body, state in zip(self.bodies, self.initial_states):
            body.restore_state(state)

        for trail in self.trails:
            trail.clear()

        self.simulation_time = 0.0
        self.paused = False

    def update(self, task):
        if not self.paused:
            dt = 0.018
            self.physics.update(dt)
            self.simulation_time += dt

            for body in self.bodies:
                body.update_model()

            for trail in self.trails:
                trail.update()

            self.spacetime.update(self.bodies)

        self.hud.update(
            self.paused,
            self.mesh_visible,
            self.trails_visible,
            self.simulation_time
        )
        return Task.cont


if __name__ == "__main__":
    GravitySimulation().run()
