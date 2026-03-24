import pygame
import sys
import math
import random

pygame.init()
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Two Objects Control")

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)

# 🔵 원
circle_x = 200
circle_y = 300
circle_radius = 50
circle_color = BLUE
circle_speed = 10

# 🔺 삼각형
tri_x = 600
tri_y = 300
tri_size = 60
tri_color = RED
tri_speed = 10

# 🟩 사각형 (자동 이동)
rect_x = 400
rect_y = 300
rect_size = 100
rect_dx = 3
rect_dy = 3
rect_color = GREEN

# 충돌 상태
was_colliding = False
was_rect_colliding = False

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # =========================
    # 🔥 이동 예측
    next_circle_x = circle_x
    next_circle_y = circle_y
    next_tri_x = tri_x
    next_tri_y = tri_y

    # 🔵 원 이동
    if keys[pygame.K_a]:
        next_circle_x -= circle_speed
    if keys[pygame.K_d]:
        next_circle_x += circle_speed
    if keys[pygame.K_w]:
        next_circle_y -= circle_speed
    if keys[pygame.K_s]:
        next_circle_y += circle_speed

    # 🔺 삼각형 이동
    if keys[pygame.K_LEFT]:
        next_tri_x -= tri_speed
    if keys[pygame.K_RIGHT]:
        next_tri_x += tri_speed
    if keys[pygame.K_UP]:
        next_tri_y -= tri_speed
    if keys[pygame.K_DOWN]:
        next_tri_y += tri_speed

    # =========================
    # 🔥 원 vs 삼각형 충돌
    dx = next_circle_x - next_tri_x
    dy = next_circle_y - next_tri_y
    distance = math.sqrt(dx**2 + dy**2)

    is_colliding = distance < circle_radius + tri_size

    if is_colliding and not was_colliding:
        circle_color = tuple(random.randint(0, 255) for _ in range(3))
        tri_color = tuple(random.randint(0, 255) for _ in range(3))

    if not is_colliding:
        circle_x = next_circle_x
        circle_y = next_circle_y
        tri_x = next_tri_x
        tri_y = next_tri_y

    was_colliding = is_colliding

    # =========================
    # 🟩 사각형 자동 이동
    rect_x += rect_dx
    rect_y += rect_dy

    # 🔥 벽 튕김
    if rect_x <= 0 or rect_x + rect_size >= 800:
        rect_dx *= -1
    if rect_y <= 0 or rect_y + rect_size >= 800:
        rect_dy *= -1

    # =========================
    # 🔥 사각형 vs 원 충돌
    dx = (rect_x + rect_size / 2) - circle_x
    dy = (rect_y + rect_size / 2) - circle_y
    dist_circle = math.sqrt(dx**2 + dy**2)

    collide_circle = dist_circle < circle_radius + rect_size / 2

    # 🔥 사각형 vs 삼각형 충돌
    dx = (rect_x + rect_size / 2) - tri_x
    dy = (rect_y + rect_size / 2) - tri_y
    dist_tri = math.sqrt(dx**2 + dy**2)

    collide_tri = dist_tri < tri_size + rect_size / 2

    rect_colliding = collide_circle or collide_tri

    # 🔥 충돌 시작 시 (사각형)
    if rect_colliding and not was_rect_colliding:
        rect_color = tuple(random.randint(0, 255) for _ in range(3))

        # 튕김
        rect_dx *= -1
        rect_dy *= -1

    was_rect_colliding = rect_colliding

    # =========================
    # 🔥 화면 제한
    circle_x = max(circle_radius, min(800 - circle_radius, circle_x))
    circle_y = max(circle_radius, min(800 - circle_radius, circle_y))

    tri_x = max(tri_size, min(800 - tri_size, tri_x))
    tri_y = max(tri_size, min(800 - tri_size, tri_y))

    # =========================
    # FPS
    fps = clock.get_fps()
    fps_text = font.render(f"FPS: {int(fps)}", True, BLACK)

    screen.fill(WHITE)

    # 🔵 원
    pygame.draw.circle(screen, circle_color, (circle_x, circle_y), circle_radius)

    # 🔺 삼각형
    pygame.draw.polygon(screen, tri_color, [
        (tri_x, tri_y - tri_size),
        (tri_x - tri_size, tri_y + tri_size),
        (tri_x + tri_size, tri_y + tri_size)
    ])

    # 🟩 사각형
    pygame.draw.rect(screen, rect_color, (rect_x, rect_y, rect_size, rect_size))

    screen.blit(fps_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()