import pygame


class Item:
    def __init__(self, x, y, item_type):
        self.x = x
        self.y = y
        self.size = 30
        self.item_type = item_type

        if item_type == "blue":
            self.color = (0, 100, 255)
            self.value = 10
        elif item_type == "green":
            self.color = (0, 200, 0)
            self.value = 30
        elif item_type == "yellow":
            self.color = (255, 220, 0)
            self.value = 50
        else:
            self.color = (255, 255, 255)
            self.value = 0

        # 생성 직후에는 보이지 않음
        self.alpha = 0
        self.max_alpha = 255

        self.detected = False
        self.visible_timer = 0
        self.visible_duration = 120
        self.fade_speed = 6

        self.age = 0
        self.life_time = 30
        self.should_delete = False

        self.surface = pygame.Surface(
            (self.size, self.size),
            pygame.SRCALPHA
        )

        pygame.draw.rect(
            self.surface,
            self.color,
            (0, 0, self.size, self.size)
        )

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
        # 보이는 상태일 때만 획득 가능
        return self.alpha > 0

    def get_rect(self):
        return pygame.Rect(
            self.x,
            self.y,
            self.size,
            self.size
        )

    def draw(self, screen, camera):
        # 탐지되기 전에는 그리지 않음
        if self.alpha <= 0:
            return

        screen_x, screen_y = camera.apply(self.x, self.y)

        self.surface.set_alpha(self.alpha)
        screen.blit(
            self.surface,
            (screen_x, screen_y)
        )