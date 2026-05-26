import pygame


class SpecialItem:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 36

        self.color = (180, 80, 255)
        self.value = 1

        self.alpha = 0
        self.max_alpha = 255

        self.detected = False
        self.visible_timer = 0
        self.visible_duration = 120
        self.fade_speed = 6

        self.age = 0
        self.life_time = 40
        self.should_delete = False

    def reveal(self):
        self.detected = True
        self.visible_timer = self.visible_duration

    def update(self, dt):
        self.age += dt

        if self.age >= self.life_time:
            self.should_delete = True

        if self.detected:
            self.alpha += self.fade_speed
            if self.alpha > self.max_alpha:
                self.alpha = self.max_alpha

            self.visible_timer -= 1
            if self.visible_timer <= 0:
                self.detected = False
        else:
            self.alpha -= self.fade_speed
            if self.alpha < 0:
                self.alpha = 0

    def can_collect(self):
        return self.alpha > 0

    def get_rect(self):
        return pygame.Rect(
            self.x,
            self.y,
            self.size,
            self.size
        )

    def draw(self, screen, camera):
        if self.alpha <= 0:
            return

        screen_x, screen_y = camera.apply(self.x, self.y)

        surface = pygame.Surface(
            (self.size, self.size),
            pygame.SRCALPHA
        )

        triangle_points = [
            (self.size // 2, 0),
            (0, self.size),
            (self.size, self.size)
        ]

        pygame.draw.polygon(
            surface,
            (
                self.color[0],
                self.color[1],
                self.color[2],
                int(self.alpha)
            ),
            triangle_points
        )

        screen.blit(surface, (screen_x, screen_y))