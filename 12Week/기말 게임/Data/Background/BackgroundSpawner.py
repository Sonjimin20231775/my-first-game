import random
from Data.Background.BackgroundObject import BackgroundObject


class BackgroundSpawner:
    def __init__(self, screen_width, screen_height, object_data, object_type):
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.object_data = object_data
        self.object_type = object_type

        self.max_objects = 8 if object_type == "moving" else 14
        self.min_spawn_distance = 120

        self.base_move_x = -0.4 if object_type == "moving" else 0
        self.base_move_y = 0.25 if object_type == "moving" else 0

        for data in self.object_data:
            data["spawn_timer"] = 0

    def update(self, objects, dt, camera=None):
        for data in self.object_data:
            data["spawn_timer"] += dt

            if data["spawn_timer"] >= data["spawn_interval"]:
                self.spawn_group(objects, data, camera)
                data["spawn_timer"] = 0

    def spawn_group(self, objects, data, camera):
        spawn_count = random.randint(
            data["spawn_count_min"],
            data["spawn_count_max"]
        )

        for _ in range(spawn_count):
            self.spawn_one(objects, data, camera)

    def spawn_one(self, objects, data, camera):
        if self.count_same_type(objects) >= self.max_objects:
            return

        image = data["image"]

        move_x = self.base_move_x * data["speed_scale"]
        move_y = self.base_move_y * data["speed_scale"]

        spawn_range = data["spawn_range"]

        if self.object_type == "static" and camera is not None:
            x = random.randint(
                int(camera.x + spawn_range["x_min"]),
                int(camera.x + spawn_range["x_max"])
            )

            y = random.randint(
                int(camera.y + spawn_range["y_min"]),
                int(camera.y + spawn_range["y_max"])
            )
        else:
            x = random.randint(
                spawn_range["x_min"],
                spawn_range["x_max"]
            )

            y = random.randint(
                spawn_range["y_min"],
                spawn_range["y_max"]
            )

        new_rect = image.get_rect(topleft=(x, y))

        for obj in objects:
            expanded_rect = obj.rect.inflate(
                self.min_spawn_distance,
                self.min_spawn_distance
            )

            if new_rect.colliderect(expanded_rect):
                return

        life_time = None
        fade_in_time = 0
        fade_out_time = 0

        if self.object_type == "static":
            life_time = random.uniform(
                data["life_time_min"],
                data["life_time_max"]
            )

            fade_in_time = data["fade_in_time"]
            fade_out_time = data["fade_out_time"]

        objects.append(
            BackgroundObject(
                image=image,
                x=x,
                y=y,
                move_x=move_x,
                move_y=move_y,
                object_type=self.object_type,
                life_time=life_time,
                fade_in_time=fade_in_time,
                fade_out_time=fade_out_time
            )
        )

    def count_same_type(self, objects):
        count = 0

        for obj in objects:
            if obj.object_type == self.object_type:
                count += 1

        return count