# ════ NEON OVERDRIVE — Physics Engine ═════════════════════════════════════

import math
import random
from dataclasses import dataclass
from config import Physics, Colour

@dataclass
class Vector2:
    """2D vector for physics calculations."""
    x: float = 0.0
    y: float = 0.0

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __mul__(self, scalar: float):
        return Vector2(self.x * scalar, self.y * scalar)

    def magnitude(self) -> float:
        return math.sqrt(self.x**2 + self.y**2)

    def normalize(self):
        mag = self.magnitude()
        if mag > 0:
            self.x /= mag
            self.y /= mag
        return self

    def dot(self, other) -> float:
        return self.x * other.x + self.y * other.y

    def rotate(self, angle_deg: float):
        """Rotate vector by angle in degrees."""
        rad = math.radians(angle_deg)
        cos_a = math.cos(rad)
        sin_a = math.sin(rad)
        new_x = self.x * cos_a - self.y * sin_a
        new_y = self.x * sin_a + self.y * cos_a
        self.x, self.y = new_x, new_y
        return self

class CarPhysics:
    """Core car physics: acceleration, drifting, grip, collision."""

    def __init__(self, mass: float = Physics.CAR_MASS):
        self.mass = mass
        self.velocity = Vector2(0, 0)
        self.acceleration = Vector2(0, 0)
        self.rotation = 0.0  # degrees
        self.angular_velocity = 0.0
        self.is_drifting = False
        self.drift_angle = 0.0
        self.traction = 1.0

    def apply_force(self, force: Vector2):
        """Apply force to car, update acceleration."""
        self.acceleration = force * (1.0 / self.mass)

    def update(self, dt: float, friction_coeff: float):
        """Update velocity and position based on forces and friction."""
        # Apply friction
        self.velocity.x *= friction_coeff
        self.velocity.y *= friction_coeff

        # Apply acceleration
        self.velocity.x += self.acceleration.x * dt
        self.velocity.y += self.acceleration.y * dt

        # Clamp speed
        speed = self.velocity.magnitude()
        if speed > Physics.MAX_SPEED:
            self.velocity = self.velocity.normalize() * Physics.MAX_SPEED

        return self.velocity

    def apply_drift_physics(self, steering_input: float, dt: float):
        """Calculate drift angle and reduce grip during drift."""
        if self.is_drifting:
            self.drift_angle = steering_input * 15.0
            self.traction = 0.7  # Reduced grip while drifting
        else:
            self.drift_angle = steering_input * 5.0
            self.traction = 1.0

class CollisionResolver:
    """Handle car-to-car and car-to-wall collisions."""

    @staticmethod
    def circle_collision(pos1, rad1, pos2, rad2) -> bool:
        """Check if two circles collide."""
        dx = pos2[0] - pos1[0]
        dy = pos2[1] - pos1[1]
        dist = math.sqrt(dx*dx + dy*dy)
        return dist < (rad1 + rad2)

    @staticmethod
    def resolve_collision(car1, car2, restitution: float = 0.6):
        """Bounce two cars apart elastically."""
        dx = car2.pos.x - car1.pos.x
        dy = car2.pos.y - car1.pos.y
        dist = math.sqrt(dx*dx + dy*dy)
        if dist == 0: return

        # Normalize collision vector
        nx = dx / dist
        ny = dy / dist

        # Relative velocity
        dvx = car2.velocity.x - car1.velocity.x
        dvy = car2.velocity.y - car1.velocity.y
        dvn = dvx * nx + dvy * ny

        if dvn >= 0: return  # Already separating

        # Impulse
        impulse = -(1 + restitution) * dvn / 2
        car1.velocity.x -= impulse * nx
        car1.velocity.y -= impulse * ny
        car2.velocity.x += impulse * nx
        car2.velocity.y += impulse * ny
