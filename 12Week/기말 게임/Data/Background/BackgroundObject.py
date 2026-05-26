import pygame


class BackgroundObject:
    def __init__(
        self,
        image,
        x,
        y,
        move_x=0,
        move_y=0,
        object_type="moving",
        life_time=None,
        fade_in_time=0,
        fade_out_time=0
    ):
        self.original_image = image
        self.image = image.copy()

        self.x = x
        self.y = y

        self.move_x = move_x
        self.move_y = move_y

        self.object_type = object_type
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

        self.life_time = life_time
        self.age = 0

        self.fade_in_time = fade_in_time
        self.fade_out_time = fade_out_time

        self.alpha = 255

        if self.fade_in_time > 0:
            self.alpha = 0

        self.should_delete = False
        self.invisible_time = 0

    def update(self, dt, screen_width, screen_height, camera):
        self.x += self.move_x
        self.y += self.move_y
        self.rect.topleft = (self.x, self.y)

        self.age += dt

        if self.object_type == "moving":
            if self.is_visible_on_screen(screen_width, screen_height, camera):
                self.invisible_time = 0
            else:
                self.invisible_time += dt

                if self.invisible_time >= 10:
                    self.should_delete = True

        elif self.object_type == "static":
            if self.life_time is not None and self.age >= self.life_time:
                self.should_delete = True

        self.update_alpha()

    def update_alpha(self):
        if self.object_type != "static":
            return

        if self.life_time is None:
            self.alpha = 255
            return

        if self.fade_in_time > 0 and self.age < self.fade_in_time:
            self.alpha = int(255 * (self.age / self.fade_in_time))

        elif self.fade_out_time > 0 and self.age > self.life_time - self.fade_out_time:
            remain_time = self.life_time - self.age
            self.alpha = int(255 * (remain_time / self.fade_out_time))

        else:
            self.alpha = 255

        self.alpha = max(0, min(255, self.alpha))

    def draw(self, screen, camera):
        if self.alpha <= 0:
            return

        screen_x, screen_y = camera.apply(self.x, self.y)

        self.image.set_alpha(self.alpha)
        screen.blit(self.image, (screen_x, screen_y))

    def is_visible_on_screen(self, width, height, camera):
        screen_x, screen_y = camera.apply(self.x, self.y)

        screen_rect = pygame.Rect(0, 0, width, height)
        object_rect = pygame.Rect(
            screen_x,
            screen_y,
            self.rect.width,
            self.rect.height
        )

        return object_rect.colliderect(screen_rect)