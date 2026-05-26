import random
from Data.Item.SpecialItem import SpecialItem


class SpecialItemSpawner:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.items = []
        self.max_items = 3

        self.spawn_timer = 0
        self.spawn_interval_min = 20
        self.spawn_interval_max = 30

        self.next_spawn_time = random.uniform(
            self.spawn_interval_min,
            self.spawn_interval_max
        )

    def update(self, dt, camera):
        self.spawn_timer += dt

        if self.spawn_timer >= self.next_spawn_time:
            if len(self.items) < self.max_items:
                self.spawn_item(camera)

            self.spawn_timer = 0
            self.next_spawn_time = random.uniform(
                self.spawn_interval_min,
                self.spawn_interval_max
            )

        for item in self.items[:]:
            item.update(dt)

            if item.should_delete:
                self.items.remove(item)

    def spawn_item(self, camera):
        x = random.randint(
            int(camera.x),
            int(camera.x + self.screen_width - 36)
        )

        y = random.randint(
            int(camera.y),
            int(camera.y + self.screen_height - 36)
        )

        self.items.append(SpecialItem(x, y))

    def draw(self, screen, camera):
        for item in self.items:
            item.draw(screen, camera)