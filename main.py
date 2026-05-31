# ════ NEON OVERDRIVE — Main Game Loop ═════════════════════════════════════

import pygame
import sys
import random
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, Colour
from car import Car
from track import TrackBuilder
from hud import HUD
from physics import Vector2

class GameState:
    MENU = 0
    RACING = 1
    PAUSED = 2
    RESULTS = 3

class Game:
    """Main game engine."""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('🏎️  NEON OVERDRIVE — Futuristic Racing')
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = GameState.RACING

        # Game objects
        self.track = TrackBuilder.build_neon_circuit(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.cars = []
        self.hud = HUD()

        # Spawn player car and 3 AI
        self._spawn_cars()

    def _spawn_cars(self):
        """Create player and AI cars."""
        start_x, start_y = self.track.starting_line
        for i in range(4):
            offset_x = (i % 2) * 60
            offset_y = (i // 2) * 60
            car = Car(start_x + offset_x, start_y + offset_y, car_id=i)
            self.cars.append(car)

    def handle_input(self):
        """Process keyboard input."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = GameState.PAUSED if self.state == GameState.RACING else GameState.RACING

        # Continuous input
        keys = pygame.key.get_pressed()
        player_car = self.cars[0]

        throttle = 0.0
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            throttle = 1.0
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            throttle = -1.0

        steering = 0.0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            steering = -1.0
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            steering = 1.0

        brake = keys[pygame.K_SPACE]
        nitro = keys[pygame.K_LSHIFT]

        player_car.set_input(throttle, steering, brake, nitro)

        # AI input (simple pathfinding)
        for car in self.cars[1:]:
            self._ai_input(car)

    def _ai_input(self, car: Car):
        """Compute AI steering and acceleration."""
        if not self.track.waypoints:
            return

        # Find nearest waypoint
        nearest = min(self.track.waypoints, key=lambda w: (car.pos.x - w.pos.x)**2 + (car.pos.y - w.pos.y)**2)
        target_x = nearest.pos.x - car.pos.x
        target_y = nearest.pos.y - car.pos.y

        # Steering toward target
        import math
        target_angle = math.degrees(math.atan2(target_y, target_x))
        angle_diff = (target_angle - car.rotation) % 360
        if angle_diff > 180:
            angle_diff -= 360

        steering = max(-1, min(1, angle_diff / 90))
        car.set_input(0.8, steering, False, random.random() < 0.1)

    def update(self):
        """Update game state."""
        if self.state != GameState.RACING:
            return

        dt = self.clock.tick(FPS) / 1000.0

        # Update cars
        for car in self.cars:
            car.update(dt, self.track)

        # Check checkpoint passes
        for car in self.cars:
            for cp in self.track.checkpoints:
                if cp.check_pass(car.pos, car.car_id):
                    car.current_lap += 1
                    car.best_lap_time = min(car.best_lap_time, car.lap_time)
                    car.lap_time = 0.0

    def render(self):
        """Draw game world."""
        self.track.render(self.screen)

        # Draw cars
        for car in self.cars:
            car.render(self.screen)

        # Draw HUD
        player = self.cars[0]
        self.hud.draw_speed(self.screen, player.physics.velocity.magnitude())
        self.hud.draw_lap_info(self.screen, player.current_lap, player.lap_time, player.best_lap_time)
        self.hud.draw_nitro_bar(self.screen, player.nitro_charge)
        self.hud.draw_minimap(self.screen, self.cars, self.track)
        self.hud.draw_leaderboard(self.screen, self.cars)

        pygame.display.flip()

    def run(self):
        """Main game loop."""
        while self.running:
            self.handle_input()
            self.update()
            self.render()

        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()
