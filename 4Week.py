import pygame
import sys
import math
from sprites import load_sprite

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Collision Debug System")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)

# 색상
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

# ---------------- 스프라이트 ----------------
player_img = load_sprite("adventurer", (80, 110))
fixed_img = load_sprite("rocket", (80, 160))

player_rect = player_img.get_rect(topleft=(100, 100))
fixed_rect = fixed_img.get_rect(center=(WIDTH // 2, HEIGHT // 2))

speed = 5

# 회전
angle = 0
rotation_speed = 1


# ---------------- OBB 꼭짓점 ----------------
def get_rotated_corners(rect, angle):
    cx, cy = rect.center
    w, h = rect.width / 2, rect.height / 2

    corners = [(-w, -h), (w, -h), (w, h), (-w, h)]
    rotated = []

    rad = math.radians(angle)

    for x, y in corners:
        rx = x * math.cos(rad) - y * math.sin(rad)
        ry = x * math.sin(rad) + y * math.cos(rad)
        rotated.append((cx + rx, cy + ry))

    return rotated


# ---------------- SAT ----------------
def get_axes(points):
    axes = []
    for i in range(len(points)):
        p1 = points[i]
        p2 = points[(i + 1) % len(points)]

        edge = (p2[0] - p1[0], p2[1] - p1[1])
        normal = (-edge[1], edge[0])

        length = math.hypot(normal[0], normal[1])
        axes.append((normal[0] / length, normal[1] / length))

    return axes


def project(points, axis):
    dots = [p[0]*axis[0] + p[1]*axis[1] for p in points]
    return min(dots), max(dots)


def is_colliding_obb(points1, points2):
    axes = get_axes(points1) + get_axes(points2)

    for axis in axes:
        min1, max1 = project(points1, axis)
        min2, max2 = project(points2, axis)

        if max1 < min2 or max2 < min1:
            return False

    return True


# ---------------- 메인 루프 ----------------
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # 이동
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_rect.x -= speed
    if keys[pygame.K_RIGHT]:
        player_rect.x += speed
    if keys[pygame.K_UP]:
        player_rect.y -= speed
    if keys[pygame.K_DOWN]:
        player_rect.y += speed

    # Z 키로 회전 속도 증가
    if keys[pygame.K_z]:
        rotation_speed = 3
    else:
        rotation_speed = 1

    angle += rotation_speed

    # 중심 & 반지름
    player_center = player_rect.center
    fixed_center = fixed_rect.center

    player_radius = player_rect.width // 2
    fixed_radius = fixed_rect.width // 2

    # ---------------- 충돌 판정 ----------------

    # 1. Circle
    dx = player_center[0] - fixed_center[0]
    dy = player_center[1] - fixed_center[1]
    collision_circle = (dx*dx + dy*dy) < (player_radius + fixed_radius) ** 2

    # 2. AABB
    collision_aabb = player_rect.colliderect(fixed_rect)

    # 3. OBB (SAT)
    player_points = get_rotated_corners(player_rect, 0)
    fixed_points = get_rotated_corners(fixed_rect, angle)
    collision_obb = is_colliding_obb(player_points, fixed_points)

    # ---------------- 배경 ----------------
    if collision_obb:
        screen.fill((255, 200, 200))
    else:
        screen.fill(WHITE)

    # ---------------- 스프라이트 ----------------
    screen.blit(player_img, player_rect.topleft)

    rotated_surface = pygame.transform.rotate(fixed_img, angle)
    rect = rotated_surface.get_rect(center=fixed_rect.center)
    screen.blit(rotated_surface, rect.topleft)

    # ---------------- 시각화 ----------------
    # Circle
    pygame.draw.circle(screen, BLUE, player_center, player_radius, 2)
    pygame.draw.circle(screen, BLUE, fixed_center, fixed_radius, 2)

    # AABB
    pygame.draw.rect(screen, RED, player_rect, 2)
    pygame.draw.rect(screen, RED, fixed_rect, 2)

    # OBB
    pygame.draw.polygon(screen, GREEN, player_points, 2)
    pygame.draw.polygon(screen, GREEN, fixed_points, 2)

    # ---------------- 텍스트 표시 ----------------
    def draw_text(text, y, color):
        img = font.render(text, True, color)
        screen.blit(img, (10, y))

    draw_text(f"Circle: {'HIT' if collision_circle else 'MISS'}", 10, BLUE)
    draw_text(f"AABB: {'HIT' if collision_aabb else 'MISS'}", 40, RED)
    draw_text(f"OBB: {'HIT' if collision_obb else 'MISS'}", 70, GREEN)

    pygame.display.flip()
    clock.tick(60)