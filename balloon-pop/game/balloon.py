"""
Balloon: falls from the top of the screen. The player must pop it
before it reaches the bottom. Balloons vary in size and type.
"""

import pygame


class Balloon:
    TYPES = {
        "normal": {
            "color": (220, 90, 120),
            "points": 10,
        },
        "bonus": {
            "color": (70, 180, 90),
            "points": 25,
        },
        "penalty": {
            "color": (80, 120, 220),
            "points": -10,
        },
    }

    def __init__(self, x, y, radius, speed, balloon_type="normal"):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed
        self.balloon_type = balloon_type

        properties = self.TYPES[balloon_type]
        self.color = properties["color"]
        self.points = properties["points"]

    def update(self):
        self.y += self.speed

    def is_past_bottom(self, height):
        return self.y - self.radius > height

    def get_rect(self):
        return pygame.Rect(
            int(self.x - self.radius), int(self.y - self.radius),
            self.radius * 2, self.radius * 2,
        )