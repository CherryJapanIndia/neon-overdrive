# ════ NEON OVERDRIVE — Track System ═══════════════════════════════════════

import pygame
from physics import Vector2
from config import Colour, Track

class Checkpoint:
    """Track checkpoint for lap validation."""

    def __init__(self, pos_x: float, pos_y: float, checkpoint_id: int):
        self.pos = Vector2(pos_x, pos_y)
        self.id = checkpoint_id
        self.radius = Track.CHECKPOINT_RADIUS
        self.passed_by = set()  # Car IDs that passed

    def check_pass(self, car_pos: Vector2, car_id: int) -> bool:
        """Check if car passed through checkpoint."""
        dx = car_pos.x - self.pos.x
        dy = car_pos.y - self.pos.y
        dist_sq = dx*dx + dy*dy
        if dist_sq < self.radius * self.radius:
            if car_id not in self.passed_by:
                self.passed_by.add(car_id)
                return True
        return False

class Waypoint:
    """AI pathfinding waypoint."""

    def __init__(self, pos_x: float, pos_y: float, waypoint_id: int):
        self.pos = Vector2(pos_x, pos_y)
        self.id = waypoint_id
        self.radius = Track.WAYPOINT_RADIUS

class Track:
    """Track definition with checkpoints and waypoints."""

    def __init__(self, name: str, width: int, height: int):
        self.name = name
        self.width = width
        self.height = height
        self.checkpoints = []
        self.waypoints = []
        self.starting_line = None
        self.bg_colour = Colour.BG_DARK
        self.track_colour = Colour.GRID

    def add_checkpoint(self, pos_x: float, pos_y: float) -> Checkpoint:
        """Add checkpoint to track."""
        cp = Checkpoint(pos_x, pos_y, len(self.checkpoints))
        self.checkpoints.append(cp)
        return cp

    def add_waypoint(self, pos_x: float, pos_y: float) -> Waypoint:
        """Add waypoint for AI pathfinding."""
        wp = Waypoint(pos_x, pos_y, len(self.waypoints))
        self.waypoints.append(wp)
        return wp

    def render(self, surface: pygame.Surface):
        """Draw track background and visual guides."""
        surface.fill(self.bg_colour)

        # Draw grid pattern
        grid_size = 100
        for x in range(0, self.width, grid_size):
            pygame.draw.line(surface, self.track_colour, (x, 0), (x, self.height), 1)
        for y in range(0, self.height, grid_size):
            pygame.draw.line(surface, self.track_colour, (0, y), (self.width, y), 1)

        # Draw checkpoints
        for cp in self.checkpoints:
            pygame.draw.circle(surface, Colour.NEON_CYAN, (int(cp.pos.x), int(cp.pos.y)), int(cp.radius), 2)

        # Draw waypoints (faint)
        for wp in self.waypoints:
            pygame.draw.circle(surface, (50, 100, 150), (int(wp.pos.x), int(wp.pos.y)), int(wp.radius), 1)

class TrackBuilder:
    """Factory for building different tracks."""

    @staticmethod
    def build_neon_circuit(width: int = 1280, height: int = 960) -> Track:
        """Build the main futuristic neon circuit."""
        track = Track('Neon Circuit', width, height)
        track.bg_colour = Colour.BG_DARK

        # Define checkpoints (forming a circuit)
        checkpoints_pos = [
            (640, 100),   # Start/finish
            (1100, 400),  # Turn 1
            (900, 800),   # Turn 2
            (200, 800),   # Turn 3
            (100, 400),   # Turn 4
        ]

        for i, (x, y) in enumerate(checkpoints_pos):
            track.add_checkpoint(x, y)

        # Define waypoints for AI
        waypoints_pos = [
            (640, 150), (900, 250), (1100, 400), (1000, 600),
            (900, 800), (500, 850), (200, 800), (100, 600),
            (100, 400), (200, 200), (500, 100), (640, 100),
        ]

        for i, (x, y) in enumerate(waypoints_pos):
            track.add_waypoint(x, y)

        track.starting_line = (640, 100)
        return track
