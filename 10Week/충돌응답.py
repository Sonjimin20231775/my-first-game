import pygame
import sys

pygame.init()

# =========================
# 화면 설정
# =========================
WIDTH = 900
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Collision Test")

clock = pygame.time.Clock()

# =========================
# 색상
# =========================
WHITE = (255, 255, 255)
BLUE = (50, 100, 255)
BLACK = (30, 30, 30)
GREEN = (50, 200, 50)

# =========================
# 물리 값
# =========================
GRAVITY = 0.5
JUMP_SPEED = -12
MAX_FALL = 15

RESTITUTION = 0.0
FRICTION = 0.85

# =========================
# 벽 클래스
# =========================
class Wall:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)

    def draw(self, surface):
        pygame.draw.rect(surface, BLACK, self.rect)

# =========================
# 플레이어 클래스
# =========================
class Player:
    def __init__(self):
        self.x = 100
        self.y = 100

        self.width = 50
        self.height = 50

        self.rect = pygame.Rect(
            self.x,
            self.y,
            self.width,
            self.height
        )

        self.vx = 0
        self.vy = 0

        self.speed = 0.8
        self.on_ground = False

    def jump(self):
        if self.on_ground:
            self.vy = JUMP_SPEED

    def update(self, walls):

        # 중력
        self.vy = min(self.vy + GRAVITY, MAX_FALL)

        self.on_ground = False

        # =========================
        # X 이동
        # =========================
        self.x += self.vx
        self.rect.x = int(self.x)

        for w in walls:
            if self.rect.colliderect(w.rect):
                resolve_x(self, w)

        # =========================
        # Y 이동
        # =========================
        self.y += self.vy
        self.rect.y = int(self.y)

        for w in walls:
            if self.rect.colliderect(w.rect):
                resolve_y(self, w)

        # =========================
        # 마찰
        # =========================
        if self.on_ground:
            self.vx *= FRICTION

            # 너무 작으면 멈춤
            if abs(self.vx) < 0.1:
                self.vx = 0

    def draw(self, surface):
        pygame.draw.rect(surface, BLUE, self.rect)

# =========================
# 충돌 처리 함수
# =========================
def resolve_x(player, wall):

    # 오른쪽 이동 중
    if player.vx > 0:
        player.rect.right = wall.rect.left

    # 왼쪽 이동 중
    elif player.vx < 0:
        player.rect.left = wall.rect.right

    player.x = player.rect.x

    # 튕김 제거
    player.vx *= -RESTITUTION


def resolve_y(player, wall):

    # 아래로 떨어지는 중
    if player.vy > 0:
        player.rect.bottom = wall.rect.top
        player.on_ground = True

    # 위로 점프 중
    elif player.vy < 0:
        player.rect.top = wall.rect.bottom

    player.y = player.rect.y

    # 튕김 제거
    player.vy *= -RESTITUTION

# =========================
# 객체 생성
# =========================
player = Player()

walls = [
    Wall(0, 550, 900, 50),      # 바닥
    Wall(300, 450, 200, 30),    # 발판
    Wall(600, 350, 200, 30),    # 발판
]

# =========================
# 메인 루프
# =========================
running = True

while running:

    clock.tick(60)

    # 이벤트
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:
                player.jump()

    # 키 입력
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player.vx -= player.speed

    if keys[pygame.K_RIGHT]:
        player.vx += player.speed

    # 업데이트
    player.update(walls)

    # =========================
    # 그리기
    # =========================
    screen.fill(WHITE)

    for wall in walls:
        wall.draw(screen)

    player.draw(screen)

    pygame.display.flip()

pygame.quit()
sys.exit()