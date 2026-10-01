"""
GameEngine: owns all balloons, spawns new ones, and handles clicks.

Task 2 adds normal, bonus, and penalty balloon types.
No lives system or timer is implemented yet.
"""

import random

from game.balloon import Balloon
from game.click_detection import check_pop
from game.renderer import WIDTH, HEIGHT

SPAWN_INTERVAL_FRAMES = 45


class GameEngine:
    def __init__(self):
        self.balloons = []
        self.frames_until_spawn = 0
        self.score = 0

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
        popped = check_pop(self.balloons, pos)
        if popped is not None:
            self.balloons.remove(popped)
            self.score += popped.points

    def update(self):
        self.frames_until_spawn -= 1
        if self.frames_until_spawn <= 0:
            self._spawn_balloon()
            self.frames_until_spawn = SPAWN_INTERVAL_FRAMES

        for b in self.balloons:
            b.update()

        self.balloons = [b for b in self.balloons if not b.is_past_bottom(HEIGHT)]

    def draw(self, surface, font):
        from game import renderer

        renderer.draw_scene(surface, self.balloons)
        renderer.draw_text(surface, font, f"Score: {self.score}", (10, 10))