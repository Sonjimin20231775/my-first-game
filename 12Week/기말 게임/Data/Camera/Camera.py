class Camera:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.x = 0
        self.y = 0

        # 플레이어가 이 범위 안에 있으면 카메라가 따라가지 않음
        self.dead_zone_width = 300
        self.dead_zone_height = 200

    def update(self, target):
        target_center_x = target.x + target.size / 2
        target_center_y = target.y + target.size / 2

        screen_center_x = self.x + self.screen_width / 2
        screen_center_y = self.y + self.screen_height / 2

        left_limit = screen_center_x - self.dead_zone_width / 2
        right_limit = screen_center_x + self.dead_zone_width / 2
        top_limit = screen_center_y - self.dead_zone_height / 2
        bottom_limit = screen_center_y + self.dead_zone_height / 2

        if target_center_x < left_limit:
            self.x -= left_limit - target_center_x

        elif target_center_x > right_limit:
            self.x += target_center_x - right_limit

        if target_center_y < top_limit:
            self.y -= top_limit - target_center_y

        elif target_center_y > bottom_limit:
            self.y += target_center_y - bottom_limit

    def apply(self, x, y):
        return x - self.x, y - self.y