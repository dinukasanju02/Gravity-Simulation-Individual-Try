from panda3d.core import Vec3


class PhysicsEngine:
    """Newtonian N-body gravitational physics."""

    def __init__(self, G=0.0008):
        self.G = G
        self.bodies = []

    def set_bodies(self, bodies):
        self.bodies = list(bodies)

    def calculate_accelerations(self):
        accelerations = {
            body: Vec3(0, 0, 0) for body in self.bodies
        }

        for body in self.bodies:
            for other in self.bodies:
                if body is other:
                    continue

                offset = other.position - body.position
                distance_sq = max(offset.lengthSquared(), 0.16)

                # Newton's law:
                # F = G * m1 * m2 / r^2
                # a = F / m1 = G * m2 / r^2
                direction = offset.normalized()
                accelerations[body] += (
                    direction * self.G * other.mass / distance_sq
                )

        return accelerations

    def update(self, dt):
        accelerations = self.calculate_accelerations()

        for body, acceleration in accelerations.items():
            body.apply_acceleration(acceleration, dt)

        for body in self.bodies:
            body.move(dt)
