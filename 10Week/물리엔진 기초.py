import pygame
import sys

# =========================
# 기본 설정
# =========================
pygame.init()

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jump Test")

clock = pygame.time.Clock()

# 색상
WHITE = (255, 255, 255)
BLUE = (50, 100, 255)
GREEN = (50, 200, 50)
BLACK = (0, 0, 0)

# =========================
# 물리 값
# =========================
GRAVITY = 0.5
JUMP_SPEED = -12
MAX_FALL = 15
GROUND_Y = 500

# =========================
# 플레이어 클래스
# =========================
class Player:
    def __init__(self):
        self.x = 100
        self.y = GROUND_Y

        self.width = 50
        self.height = 50

        self.vx = 0
        self.vy = 0

        self.speed = 5
        self.on_ground = True

    def jump(self):
        if self.on_ground:
            self.vy = JUMP_SPEED

    def update(self):
        # 중력 적용
        self.vy = min(self.vy + GRAVITY, MAX_FALL)

        # 위치 이동
        self.y += self.vy
        self.x += self.vx

        # 바닥 충돌
        if self.y >= GROUND_Y:
            self.y = GROUND_Y
            self.vy = 0
            self.on_ground = True
        else:
            self.on_ground = False

        # 화면 밖 제한
        if self.x < 0:
            self.x = 0

        if self.x > WIDTH - self.width:
            self.x = WIDTH - self.width

    def draw(self, surface):
        pygame.draw.rect(
            surface,
            BLUE,
            (self.x, self.y, self.width, self.height)
        )

# =========================
# 객체 생성
# =========================
player = Player()

# =========================
# 메인 루프
# =========================
running = True

while running:
    dt = clock.tick(60)

    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # 점프
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()

    # 키 입력
    keys = pygame.key.get_pressed()

    player.vx = 0

    if keys[pygame.K_LEFT]:
        player.vx = -player.speed

    if keys[pygame.K_RIGHT]:
        player.vx = player.speed

    # 업데이트
    player.update()

    # =========================
    # 그리기
    # =========================
    screen.fill(WHITE)

    # 바닥
    pygame.draw.line(
        screen,
        GREEN,
        (0, GROUND_Y + player.height),
        (WIDTH, GROUND_Y + player.height),
        5
    )

    # 플레이어
    player.draw(screen)

    pygame.display.flip()

pygame.quit()
sys.exit()