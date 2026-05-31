# ════ NEON OVERDRIVE — HUD System ════════════════════════════════════════

import pygame
from config import Colour, SCREEN_WIDTH, SCREEN_HEIGHT

class HUD:
    """In-race heads-up display."""

    def __init__(self):
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 20)

    def draw_speed(self, surface: pygame.Surface, speed: float):
        """Display current car speed."""
        speed_kmh = abs(speed * 3.6)  # Convert to km/h
        text = self.font_large.render(f'{int(speed_kmh)} km/h', True, Colour.NEON_CYAN)
        surface.blit(text, (20, 20))

    def draw_lap_info(self, surface: pygame.Surface, lap: int, lap_time: float, best_time: float):
        """Display lap counter and times."""
        lap_text = self.font_medium.render(f'Lap: {lap}', True, Colour.NEON_MAGENTA)
        time_text = self.font_small.render(f'Time: {lap_time:.2f}s | Best: {best_time:.2f}s', True, Colour.NEON_YELLOW)
        surface.blit(lap_text, (20, 80))
        surface.blit(time_text, (20, 120))

    def draw_nitro_bar(self, surface: pygame.Surface, nitro: float):
        """Display nitro boost charge bar."""
        bar_width = 200
        bar_height = 20
        bar_x = SCREEN_WIDTH - bar_width - 20
        bar_y = 20

        # Background
        pygame.draw.rect(surface, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))

        # Fill
        fill_width = int(bar_width * (nitro / 100.0))
        pygame.draw.rect(surface, Colour.NEON_GREEN, (bar_x, bar_y, fill_width, bar_height))

        # Border
        pygame.draw.rect(surface, Colour.NEON_GREEN, (bar_x, bar_y, bar_width, bar_height), 2)

        # Label
        label = self.font_small.render('NITRO', True, Colour.NEON_GREEN)
        surface.blit(label, (bar_x + 70, bar_y - 25))

    def draw_minimap(self, surface: pygame.Surface, cars: list, track):
        """Draw minimap in corner."""
        map_size = 200
        map_x = SCREEN_WIDTH - map_size - 10
        map_y = SCREEN_HEIGHT - map_size - 10

        # Background
        pygame.draw.rect(surface, (20, 20, 40), (map_x, map_y, map_size, map_size))
        pygame.draw.rect(surface, Colour.NEON_CYAN, (map_x, map_y, map_size, map_size), 2)

        # Draw cars
        scale_x = map_size / track.width
        scale_y = map_size / track.height

        for car in cars:
            mini_x = int(map_x + car.pos.x * scale_x)
            mini_y = int(map_y + car.pos.y * scale_y)
            colour = car.colour if car.car_id != 0 else Colour.NEON_YELLOW
            pygame.draw.circle(surface, colour, (mini_x, mini_y), 3)

    def draw_leaderboard(self, surface: pygame.Surface, cars: list):
        """Draw position/lap leaderboard."""
        sorted_cars = sorted(cars, key=lambda c: (c.current_lap, -c.distance_travelled), reverse=True)
        x, y = 20, SCREEN_HEIGHT - 150

        title = self.font_medium.render('POSITIONS', True, Colour.NEON_MAGENTA)
        surface.blit(title, (x, y))
        y += 40

        for i, car in enumerate(sorted_cars[:4], 1):
            text = self.font_small.render(f'{i}. Car {car.car_id}', True, car.colour)
            surface.blit(text, (x, y))
            y += 30
