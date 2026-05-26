import pygame


class BaseBackground:
    def __init__(self, image, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.image = pygame.transform.scale(
            image,
            (self.screen_width, self.screen_height)
        )

    def draw(self, screen, camera):
        tile_w = self.image.get_width()
        tile_h = self.image.get_height()

        start_x = int(-camera.x % tile_w) - tile_w
        start_y = int(-camera.y % tile_h) - tile_h

        for x in range(start_x, self.screen_width + tile_w, tile_w):
            for y in range(start_y, self.screen_height + tile_h, tile_h):
                screen.blit(self.image, (x, y))