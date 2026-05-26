import pygame
import os

from Data.Background.BaseBackground import BaseBackground
from Data.Background.BackgroundSpawner import BackgroundSpawner


class Backgrounds:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.objects = []

        self.background_path = "Assets/Graphic/Sprite/Backgrounds"
        self.parts_path = "Assets/Graphic/Sprite/Backgrounds/Parts"

        base_image = self.load_image(
            os.path.join(
                self.background_path,
                "Backgrounds_01.png"
            )
        )

        self.base_background = BaseBackground(
            base_image,
            self.screen_width,
            self.screen_height
        )

        moving_object_data = [
            {
                "image": self.load_image(
                    os.path.join(self.parts_path, "Background_Parts_01.png"),
                    scale=0.8
                ),
                "speed_scale": 0.4,
                "spawn_interval": 1.5,
                "spawn_count_min": 2,
                "spawn_count_max": 4,
                "spawn_range": {
                    "x_min": 0,
                    "x_max": self.screen_width + 700,
                    "y_min": -700,
                    "y_max": self.screen_height // 3
                }
            },
            {
                "image": self.load_image(
                    os.path.join(self.parts_path, "Background_Parts_02.png"),
                    scale=1.0
                ),
                "speed_scale": 0.7,
                "spawn_interval": 2.2,
                "spawn_count_min": 1,
                "spawn_count_max": 3,
                "spawn_range": {
                    "x_min": 0,
                    "x_max": self.screen_width + 800,
                    "y_min": -800,
                    "y_max": self.screen_height // 2
                }
            },
            {
                "image": self.load_image(
                    os.path.join(self.parts_path, "Background_Parts_03.png"),
                    scale=1.2
                ),
                "speed_scale": 1.1,
                "spawn_interval": 3.0,
                "spawn_count_min": 1,
                "spawn_count_max": 2,
                "spawn_range": {
                    "x_min": self.screen_width // 2,
                    "x_max": self.screen_width + 900,
                    "y_min": -700,
                    "y_max": self.screen_height
                }
            },
            {
                "image": self.load_image(
                    os.path.join(self.parts_path, "Background_Parts_04.png"),
                    scale=1.5
                ),
                "speed_scale": 1.7,
                "spawn_interval": 4.5,
                "spawn_count_min": 1,
                "spawn_count_max": 1,
                "spawn_range": {
                    "x_min": self.screen_width,
                    "x_max": self.screen_width + 1000,
                    "y_min": -900,
                    "y_max": self.screen_height // 2
                }
            }
        ]

        static_object_data = [
            {
                "image": self.load_image(
                    os.path.join(self.parts_path, "Background_Parts_05.png"),
                    scale=3.0
                ),
                "speed_scale": 0,
                "spawn_interval": 2.0,
                "spawn_count_min": 1,
                "spawn_count_max": 3,
                "life_time_min": 4.0,
                "life_time_max": 8.0,
                "fade_in_time": 1.0,
                "fade_out_time": 1.0,
                "spawn_range": {
                    "x_min": 0,
                    "x_max": self.screen_width,
                    "y_min": 0,
                    "y_max": self.screen_height
                }
            },
            {
                "image": self.load_image(
                    os.path.join(self.parts_path, "Background_Parts_06.png"),
                    scale=3.0
                ),
                "speed_scale": 0,
                "spawn_interval": 2.5,
                "spawn_count_min": 1,
                "spawn_count_max": 2,
                "life_time_min": 5.0,
                "life_time_max": 10.0,
                "fade_in_time": 1.2,
                "fade_out_time": 1.2,
                "spawn_range": {
                    "x_min": 0,
                    "x_max": self.screen_width,
                    "y_min": 0,
                    "y_max": self.screen_height
                }
            },
            {
                "image": self.load_image(
                    os.path.join(self.parts_path, "Background_Parts_07.png"),
                    scale=3.0
                ),
                "speed_scale": 0,
                "spawn_interval": 2.0,
                "spawn_count_min": 1,
                "spawn_count_max": 2,
                "life_time_min": 5.0,
                "life_time_max": 10.0,
                "fade_in_time": 1.2,
                "fade_out_time": 1.2,
                "spawn_range": {
                    "x_min": 0,
                    "x_max": self.screen_width,
                    "y_min": 0,
                    "y_max": self.screen_height
                }
            },
            {
                "image": self.load_image(
                    os.path.join(self.parts_path, "Background_Parts_08.png"),
                    scale=3.0
                ),
                "speed_scale": 0,
                "spawn_interval": 2.5,
                "spawn_count_min": 1,
                "spawn_count_max": 2,
                "life_time_min": 5.0,
                "life_time_max": 10.0,
                "fade_in_time": 1.2,
                "fade_out_time": 1.2,
                "spawn_range": {
                    "x_min": 0,
                    "x_max": self.screen_width,
                    "y_min": 0,
                    "y_max": self.screen_height
                }
            },
            {
                "image": self.load_image(
                    os.path.join(self.parts_path, "Background_Parts_09.png"),
                    scale=3.0
                ),
                "speed_scale": 0,
                "spawn_interval": 2.0,
                "spawn_count_min": 1,
                "spawn_count_max": 2,
                "life_time_min": 5.0,
                "life_time_max": 10.0,
                "fade_in_time": 1.2,
                "fade_out_time": 1.2,
                "spawn_range": {
                    "x_min": 0,
                    "x_max": self.screen_width,
                    "y_min": 0,
                    "y_max": self.screen_height
                }
            },
            {
                "image": self.load_image(
                    os.path.join(self.parts_path, "Background_Parts_10.png"),
                    scale=3.0
                ),
                "speed_scale": 0,
                "spawn_interval": 2.5,
                "spawn_count_min": 1,
                "spawn_count_max": 2,
                "life_time_min": 5.0,
                "life_time_max": 10.0,
                "fade_in_time": 1.2,
                "fade_out_time": 1.2,
                "spawn_range": {
                    "x_min": 0,
                    "x_max": self.screen_width,
                    "y_min": 0,
                    "y_max": self.screen_height
                }
            }
        ]

        self.moving_spawner = BackgroundSpawner(
            self.screen_width,
            self.screen_height,
            moving_object_data,
            "moving"
        )

        self.static_spawner = BackgroundSpawner(
            self.screen_width,
            self.screen_height,
            static_object_data,
            "static"
        )

    def load_image(self, path, scale=1.0):
        image = pygame.image.load(path).convert_alpha()

        if scale != 1.0:
            width = image.get_width()
            height = image.get_height()

            new_width = int(width * scale)
            new_height = int(height * scale)

            image = pygame.transform.scale(
                image,
                (new_width, new_height)
            )

        return image

    def update(self, dt, camera):
        self.moving_spawner.update(self.objects, dt)
        self.static_spawner.update(self.objects, dt, camera)

        for obj in self.objects[:]:
            obj.update(
                dt,
                self.screen_width,
                self.screen_height,
                camera
            )

            if obj.should_delete:
                self.objects.remove(obj)

    def draw(self, screen, camera):
        self.base_background.draw(screen, camera)

        for obj in self.objects:
            obj.draw(screen, camera)