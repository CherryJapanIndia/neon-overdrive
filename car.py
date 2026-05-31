# ════ NEON OVERDRIVE — Car Entity ════════════════════════════════════════

import math
import pygame
from physics import CarPhysics, Vector2
from config import Physics, Colour

class Car:
    """Player and AI car entity with physics."""

    def __init__(self, pos_x: float, pos_y: float, car_id: int = 0):
        self.pos = Vector2(pos_x, pos_y)
        self.car_id = car_id
        self.physics = CarPhysics()
        self.rotation = 0.0  # degrees, 0° = right
        self.width = 24
        self.height = 40
        self.colour = self._get_colour_by_id(car_id)

        # State tracking
        self.current_lap = 0
        self.lap_time = 0.0
        self.best_lap_time = float('inf')
        self.distance_travelled = 0.0
        self.is_drifting = False
        self.nitro_charge = 100.0
        self.health = 100.0
        self.crashed = False

        # Input state
        self.input_throttle = 0.0  # -1 to 1
        self.input_steering = 0.0  # -1 to 1 (left to right)
        self.input_brake = False
        self.input_nitro = False

    def _get_colour_by_id(self, car_id: int) -> tuple:
        """Get neon colour based on car ID."""
        colours = [
            Colour.NEON_CYAN,
            Colour.NEON_MAGENTA,
            Colour.NEON_YELLOW,
            Colour.NEON_GREEN,
        ]
        return colours[car_id % len(colours)]

    def update(self, dt: float, track=None):
        """Update car physics and state."""
        if self.crashed:
            return

        # Calculate force direction
        rad = math.radians(self.rotation)
        forward_x = math.cos(rad)
        forward_y = math.sin(rad)

        # Apply throttle/brake
        if self.input_throttle > 0:
            accel = Physics.ACCELERATION * self.input_throttle
            if self.input_nitro and self.nitro_charge > 0:
                accel += Physics.NITRO_ACCEL * 0.5
                self.nitro_charge -= 30 * dt
        elif self.input_brake:
            accel = -Physics.BRAKE_DECEL
        else:
            accel = 0

        force = Vector2(forward_x * accel, forward_y * accel)
        self.physics.apply_force(force)

        # Apply steering
        turn_input = self.input_steering * Physics.TURN_SPEED * dt
        self.rotation += turn_input
        self.rotation %= 360

        # Update physics
        friction = Physics.DRIFT_FRICTION if self.is_drifting else Physics.GRIP_FRICTION
        self.physics.update(dt, friction)

        # Update position
        self.pos.x += self.physics.velocity.x * dt
        self.pos.y += self.physics.velocity.y * dt

        # Track boundaries
        if track:
            self._clamp_to_track(track)

        self.lap_time += dt

    def _clamp_to_track(self, track):
        """Keep car within track boundaries."""
        margin = 50
        if self.pos.x < margin or self.pos.x > track.width - margin:
            self.pos.x = max(margin, min(track.width - margin, self.pos.x))
            self.physics.velocity.x *= -0.5

        if self.pos.y < margin or self.pos.y > track.height - margin:
            self.pos.y = max(margin, min(track.height - margin, self.pos.y))
            self.physics.velocity.y *= -0.5

    def render(self, surface: pygame.Surface):
        """Draw car as a rotated rectangle with glow."""
        # Draw glow effect
        glow_radius = int(self.width * 1.5)
        pygame.draw.circle(surface, (*self.colour, 100), (int(self.pos.x), int(self.pos.y)), glow_radius)

        # Draw car body
        rect = pygame.Rect(int(self.pos.x) - self.width//2, int(self.pos.y) - self.height//2, self.width, self.height)
        rotated_rect = pygame.transform.rotate(
            pygame.Surface((self.width, self.height)), -self.rotation
        )
        surface.blit(rotated_rect, rect.topleft)

    def set_input(self, throttle: float, steering: float, brake: bool, nitro: bool):
        """Update input state from player or AI."""
        self.input_throttle = max(-1, min(1, throttle))
        self.input_steering = max(-1, min(1, steering))
        self.input_brake = brake
        self.input_nitro = nitro
