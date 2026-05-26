import random
from Data.Item.Item import Item


class ItemSpawner:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.items = []

        # 동시에 존재 가능한 아이템 최대 개수
        self.max_items = 20

        self.spawn_timer = 0

        # 초 단위
        self.spawn_interval_min = 5
        self.spawn_interval_max = 10

        self.next_spawn_time = random.uniform(
            self.spawn_interval_min,
            self.spawn_interval_max
        )

        self.item_types = ["blue", "green", "yellow"]

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
        item_type = random.choice(self.item_types)

        x = random.randint(
            int(camera.x),
            int(camera.x + self.screen_width - 30)
        )

        y = random.randint(
            int(camera.y),
            int(camera.y + self.screen_height - 30)
        )

        self.items.append(
            Item(x, y, item_type)
        )

    def draw(self, screen, camera):
        for item in self.items:
            item.draw(screen, camera)