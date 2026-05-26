import pygame
import math


class SonarAttack:
    def __init__(self):
        self.active = False

        self.x = 0
        self.y = 0

        self.radius = 0
        self.max_radius = 180
        self.expand_speed = 8

        self.color = (0, 150, 255)

        self.alpha = 255
        self.fade_speed = 6
        self.fading = False

    def start(self, x, y, max_radius=180, expand_speed=8):
        if not self.active:
            self.active = True

            self.x = x
            self.y = y

            self.radius = 0
            self.max_radius = max_radius
            self.expand_speed = expand_speed

            self.alpha = 255
            self.fading = False

    def update(self):
        if not self.active:
            return

        if not self.fading:
            self.radius += self.expand_speed

            if self.radius >= self.max_radius:
                self.fading = True
        else:
            self.alpha -= self.fade_speed

            if self.alpha <= 0:
                self.alpha = 0
                self.active = False

    def draw(self, screen, camera):
        if not self.active:
            return

        screen_x, screen_y = camera.apply(self.x, self.y)

        size = self.max_radius * 2 + 20
        surface = pygame.Surface((size, size), pygame.SRCALPHA)

        draw_color = (
            self.color[0],
            self.color[1],
            self.color[2],
            int(self.alpha)
        )

        pygame.draw.circle(
            surface,
            draw_color,
            (size // 2, size // 2),
            int(self.radius),
            2
        )

        screen.blit(
            surface,
            (
                screen_x - size // 2,
                screen_y - size // 2
            )
        )

    def detect_item(self, item):
        if not self.active:
            return False

        item_center_x = item.x + item.size / 2
        item_center_y = item.y + item.size / 2

        dx = item_center_x - self.x
        dy = item_center_y - self.y
        distance = math.sqrt(dx * dx + dy * dy)

        return distance <= self.radius