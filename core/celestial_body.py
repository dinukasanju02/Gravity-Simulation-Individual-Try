from abc import ABC, abstractmethod

from panda3d.core import Vec3
from direct.showbase import ShowBaseGlobal


class CelestialBody(ABC):
    """
    Abstract base class for all celestial bodies.

    Demonstrates:
    - Abstraction
    - Encapsulation
    - Common behaviour for planets, stars and moons
    """

    def __init__(
        self,
        name,
        mass,
        radius,
        position,
        velocity,
        color
    ):
        self._name = name
        self._mass = float(mass)
        self._radius = float(radius)

        self._position = Vec3(*position)
        self._velocity = Vec3(*velocity)

        self._color = color

        self.model = None

    # =====================================================
    # GETTERS
    # =====================================================

    @property
    def name(self):
        return self._name

    @property
    def mass(self):
        return self._mass

    @property
    def radius(self):
        return self._radius

    @property
    def position(self):
        return self._position

    @property
    def velocity(self):
        return self._velocity

    @property
    def color(self):
        return self._color

    # =====================================================
    # PHYSICS
    # =====================================================

    def apply_acceleration(self, acceleration, dt):
        """
        Changes velocity using acceleration.
        """

        self._velocity += acceleration * dt

    def move(self, dt):
        """
        Moves the celestial body according to its velocity.
        """

        self._position += self._velocity * dt

    # =====================================================
    # 3D MODEL
    # =====================================================

    def create_model(self, render):
        """
        Creates the 3D sphere representing the celestial body.
        """

        # Panda3D's loader is available through the active ShowBase.
        loader = ShowBaseGlobal.base.loader

        # Load Panda3D's built-in sphere model.
        self.model = loader.loadModel(
            "models/misc/sphere"
        )

        # Add it to the 3D scene.
        self.model.reparentTo(render)

        # Set the size.
        self.model.setScale(
            self._radius
        )

        # Set the body colour.
        self.model.setColor(
            *self._color
        )

        # Make sure the sphere can be viewed from all sides.
        self.model.setTwoSided(True)

        # Put it at its initial position.
        self.update_model()

    def update_model(self):
        """
        Updates the 3D model position.
        """

        if self.model is not None:
            self.model.setPos(
                self._position
            )

    # =====================================================
    # SAVE / RESTORE
    # =====================================================

    def save_state(self):
        """
        Saves the current position and velocity.

        Used by the Reset function.
        """

        return (
            Vec3(self._position),
            Vec3(self._velocity)
        )

    def restore_state(self, state):
        """
        Restores a previously saved position and velocity.
        """

        self._position = Vec3(
            state[0]
        )

        self._velocity = Vec3(
            state[1]
        )

        self.update_model()

    # =====================================================
    # ABSTRACTION
    # =====================================================

    @abstractmethod
    def body_type(self):
        """
        Abstract method.

        Each child class must implement this.
        """

        raise NotImplementedError


# =========================================================
# STAR CLASS
# =========================================================

class Star(CelestialBody):
    """
    Represents a star.

    In our solar system the main Star object is the Sun.
    """

    def body_type(self):
        return "Star"

    def create_model(self, render):
        """
        Creates the star's 3D sphere and a simple glow effect.
        """

        # Create the main 3D body.
        super().create_model(render)

        loader = ShowBaseGlobal.base.loader

        # Create another slightly larger sphere
        # to simulate a soft glow.
        glow = loader.loadModel(
            "models/misc/sphere"
        )

        glow.reparentTo(
            self.model
        )

        glow.setScale(
            1.18
        )

        glow.setColor(
            1.0,
            0.55,
            0.08,
            0.16
        )

        glow.setTransparency(
            True
        )

        # Glow should not be affected by normal lighting.
        glow.setLightOff(True)


# =========================================================
# PLANET CLASS
# =========================================================

class Planet(CelestialBody):
    """
    Represents a planet.

    Demonstrates inheritance from CelestialBody.
    """

    def __init__(
        self,
        *args,
        **kwargs
    ):
        super().__init__(
            *args,
            **kwargs
        )

        self.rings = None

    def body_type(self):
        return "Planet"

    # =====================================================
    # SATURN RINGS
    # =====================================================

    def create_rings(self, render):
        """
        Creates Saturn's 3D ring system.
        """

        from graphics.rings import TorusRings

        self.rings = TorusRings(
            render,
            2.25,
            0.08
        )

    def update_model(self):
        """
        Updates both the planet and its rings.
        """

        super().update_model()

        if self.rings is not None:

            self.rings.set_pos(
                self._position
            )


# =========================================================
# MOON CLASS
# =========================================================

class Moon(CelestialBody):
    """
    Represents a moon.

    A Moon is also a CelestialBody, demonstrating inheritance
    and polymorphism.
    """

    def __init__(
        self,
        *args,
        parent=None,
        **kwargs
    ):
        super().__init__(
            *args,
            **kwargs
        )

        self.parent = parent

    def body_type(self):
        return "Moon"