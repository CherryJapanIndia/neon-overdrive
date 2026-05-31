# ════ NEON OVERDRIVE — Configuration ════════════════════════════════════

import pygame
from enum import Enum

# ── Screen Settings ───────────────────────────────────────────────────────
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 960
FPS = 60
FRAME_TIME = 1.0 / FPS

# ── Colours (Cyberpunk Neon Palette) ──────────────────────────────────────
class Colour:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BG_DARK = (10, 10, 20)
    GRID = (30, 50, 80)
    NEON_CYAN = (0, 255, 200)
    NEON_MAGENTA = (255, 0, 200)
    NEON_YELLOW = (255, 255, 0)
    NEON_GREEN = (0, 255, 100)
    NEON_BLUE = (0, 100, 255)
    NEON_PURPLE = (200, 0, 255)
    DANGER_RED = (255, 50, 50)
    WARNING_ORANGE = (255, 165, 0)

# ── Physics Constants ─────────────────────────────────────────────────────
class Physics:
    GRAVITY = 600.0  # pixels/sec²
    CAR_MASS = 1.0
    DRIFT_FRICTION = 0.92
    GRIP_FRICTION = 0.88
    MAX_SPEED = 800.0  # pixels/sec
    ACCELERATION = 1200.0
    BRAKE_DECEL = 1600.0
    TURN_SPEED = 360.0  # degrees/sec
    DRIFT_THRESHOLD = 45.0  # degrees
    NITRO_ACCEL = 2000.0

# ── Track Settings ────────────────────────────────────────────────────────
class Track:
    CHECKPOINT_RADIUS = 80.0
    WAYPOINT_RADIUS = 40.0
    LAP_COUNT = 3
    STARTING_POSITIONS = 4

# ── AI Settings ───────────────────────────────────────────────────────────
class AIConfig:
    PATHFINDING_INTERVAL = 0.5  # seconds
    LOOKAHEAD_DISTANCE = 200.0
    RUBBER_BAND_FACTOR = 1.2
    REACTION_TIME = 0.1  # seconds

# ── Game Difficulty ───────────────────────────────────────────────────────
class Difficulty(Enum):
    CASUAL = 1
    NORMAL = 2
    EXPERT = 3
    HARDCORE = 4
