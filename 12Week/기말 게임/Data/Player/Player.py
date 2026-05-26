import pygame
import math


class Player:
    def __init__(self, x, y):
        self.size = 40
        self.x = x
        self.y = y

        self.vel_x = 0
        self.vel_y = 0

        self.accel = 1
        self.decel = 1
        self.max_speed = 5

        self.color = (255, 0, 0)

    def limit_speed(self):
        speed = math.sqrt(self.vel_x ** 2 + self.vel_y ** 2)

        if speed > self.max_speed:
            scale = self.max_speed / speed
            self.vel_x *= scale
            self.vel_y *= scale

    def decelerate_vector(self):
        speed = math.sqrt(self.vel_x ** 2 + self.vel_y ** 2)

        if speed == 0:
            return

        if speed <= self.decel:
            self.vel_x = 0
            self.vel_y = 0
            return

        new_speed = speed - self.decel
        scale = new_speed / speed

        self.vel_x *= scale
        self.vel_y *= scale

    def handle_input(self):
        keys = pygame.key.get_pressed()
        moving = False

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel_x -= self.accel
            moving = True
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel_x += self.accel
            moving = True
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.vel_y -= self.accel
            moving = True
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.vel_y += self.accel
            moving = True

        self.limit_speed()

        if not moving:
            self.decelerate_vector()

    def update(self):
        self.handle_input()

        self.x += self.vel_x
        self.y += self.vel_y

    def draw(self, screen, camera):
        screen_x, screen_y = camera.apply(self.x, self.y)

        pygame.draw.rect(
            screen,
            self.color,
            (screen_x, screen_y, self.size, self.size)
        )