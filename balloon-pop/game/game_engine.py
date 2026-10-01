"""
GameEngine: owns all balloons, spawns new ones, handles clicks,
score, lives, timing, and restarting rounds.
"""

import math
import random
import pygame

from game.balloon import Balloon
from game.click_detection import check_pop
from game.renderer import WIDTH, HEIGHT

SPAWN_INTERVAL_FRAMES = 45
ROUND_DURATION = 30


class GameEngine:
    def __init__(self):
        self.balloons = []
        self.frames_until_spawn = 0
        self.score = 0
        self.lives = 3
        self.game_over = False
        self.time_remaining = ROUND_DURATION
        self.round_start_time = pygame.time.get_ticks()

    def _spawn_balloon(self):
        radius = random.randint(16, 44)
        x = random.randint(radius + 10, WIDTH - radius - 10)
        speed = random.uniform(1.5, 3.0)

        balloon_type = random.choices(
            ["normal", "bonus", "penalty"],
            weights=[6, 2, 2],
        )[0]

        self.balloons.append(
            Balloon(
                x=x,
                y=-radius,
                radius=radius,
                speed=speed,
                balloon_type=balloon_type,
            )
        )

    def handle_click(self, pos):
        if self.game_over:
            return

        popped = check_pop(self.balloons, pos)

        if popped is not None:
            self.balloons.remove(popped)
            self.score += popped.points

    def update(self):
        if self.game_over:
            return

        # Update the countdown timer.
        elapsed_seconds = (
            pygame.time.get_ticks() - self.round_start_time
        ) / 1000

        self.time_remaining = max(
            0,
            ROUND_DURATION - elapsed_seconds,
        )

        # End the round when the timer reaches zero.
        if self.time_remaining <= 0:
            self.time_remaining = 0
            self.game_over = True
            return

        # Spawn balloons while the round is active.
        self.frames_until_spawn -= 1

        if self.frames_until_spawn <= 0:
            self._spawn_balloon()
            self.frames_until_spawn = SPAWN_INTERVAL_FRAMES

        # Move balloons.
        for b in self.balloons:
            b.update()

        # Detect missed balloons.
        remaining_balloons = []
        missed_balloons = 0

        for b in self.balloons:
            if b.is_past_bottom(HEIGHT):
                missed_balloons += 1
            else:
                remaining_balloons.append(b)

        self.balloons = remaining_balloons

        # Deduct lives for missed balloons.
        if missed_balloons > 0:
            self.lives -= missed_balloons

            if self.lives <= 0:
                self.lives = 0
                self.game_over = True

    def restart(self):
        """Start a completely new round."""
        self.balloons = []
        self.frames_until_spawn = 0
        self.score = 0
        self.lives = 3
        self.game_over = False
        self.time_remaining = ROUND_DURATION
        self.round_start_time = pygame.time.get_ticks()

    def draw(self, surface, font):
        from game import renderer

        renderer.draw_scene(surface, self.balloons)

        renderer.draw_text(
            surface,
            font,
            f"Score: {self.score}",
            (10, 10),
        )

        renderer.draw_text(
            surface,
            font,
            f"Lives: {self.lives}",
            (10, 40),
        )

        renderer.draw_text(
            surface,
            font,
            f"Time: {math.ceil(self.time_remaining)}",
            (10, 70),
        )

        if self.game_over:
            renderer.draw_banner(
                surface,
                font,
                f"GAME OVER  -  Final Score: {self.score}",
            )

            renderer.draw_text(
                surface,
                font,
                "Press R to restart",
                (surface.get_width() // 2 - 90, surface.get_height() // 2 + 30),
            )