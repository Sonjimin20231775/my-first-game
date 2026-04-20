import pygame
import random
import sys

from sprite_data.Player_Idle import load_player_frames as load_idle
from sprite_data.Player_Left import load_player_frames as load_left
from sprite_data.Player_Right import load_player_frames as load_right
from sprite_data.Bullet import load_bullet_frames
from sprite_data.Enemy import load_enemy_frames   # 🔥 추가

pygame.init()


def get_korean_font(size):
    candidates = ["malgungothic", "applegothic", "nanumgothic", "notosanscjk"]
    for name in candidates:
        font = pygame.font.SysFont(name, size)
        if font.get_ascent() > 0:
            return font
    return pygame.font.SysFont(None, size)


WIDTH, HEIGHT = 800, 600
FPS = 60

WHITE   = (255, 255, 255)
GRAY    = (20,  20,  40)
RED     = (220, 50,  50)
YELLOW  = (240, 220, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")
clock = pygame.time.Clock()
font = get_korean_font(36)
font_big = get_korean_font(72)

LEVELS = [
    {"enemy_speed": 2, "spawn": 60, "label": "Lv.1"},
    {"enemy_speed": 3, "spawn": 40, "label": "Lv.2"},
    {"enemy_speed": 5, "spawn": 25, "label": "Lv.3"},
]

PLAYER_W, PLAYER_H = 40, 40
ENEMY_W,  ENEMY_H  = 40, 40
BULLET_W, BULLET_H = 12, 20


def spawn_enemy(level_cfg):
    x = random.randint(0, WIDTH - ENEMY_W)
    return pygame.Rect(x, -ENEMY_H, ENEMY_W, ENEMY_H)


def draw_hud(score, lives, level_cfg):
    screen.blit(font.render(f"Score: {score}", True, WHITE), (10, 10))
    screen.blit(font.render(f"Lives: {'♥ ' * lives}", True, RED), (WIDTH - 180, 10))
    screen.blit(font.render(level_cfg["label"], True, YELLOW), (WIDTH // 2 - 25, 10))


def game_over_screen(score):
    screen.fill((10, 10, 30))
    screen.blit(font_big.render("GAME OVER", True, RED), (220, 220))
    screen.blit(font.render(f"Score: {score}", True, WHITE), (350, 310))
    screen.blit(font.render("R: Restart   Q: Quit", True, WHITE), (270, 360))
    pygame.display.flip()
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_r: return True
                if e.key == pygame.K_q: pygame.quit(); sys.exit()


def main():
    player = pygame.Rect(WIDTH // 2 - 20, HEIGHT - 70, PLAYER_W, PLAYER_H)

    # 🔥 애니메이션 로드
    idle_frames  = load_idle()
    left_frames  = load_left()
    right_frames = load_right()
    bullet_frames = load_bullet_frames()
    enemy_frames  = load_enemy_frames()   # 🔥 추가

    current_frames = idle_frames

    # 플레이어 애니메이션
    frame_index = 0
    frame_timer = 0
    FRAME_DELAY = 120

    # 총알 애니메이션
    bullet_index = 0
    bullet_timer = 0
    BULLET_DELAY = 80

    # 적 애니메이션
    enemy_index = 0
    enemy_timer = 0
    ENEMY_DELAY = 150

    bullets  = []
    enemies  = []
    score    = 0
    lives    = 3
    shoot_cd = 0
    spawn_timer = 0
    level_idx = 0
    level_cfg = LEVELS[level_idx]
    invincible = 0

    while True:
        dt = clock.tick(FPS)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()

        keys = pygame.key.get_pressed()

        moving_left = False
        moving_right = False

        # 이동
        if keys[pygame.K_LEFT] and player.left > 0:
            player.x -= 6
            moving_left = True

        if keys[pygame.K_RIGHT] and player.right < WIDTH:
            player.x += 6
            moving_right = True

        if keys[pygame.K_UP] and player.top > 0:
            player.y -= 6

        if keys[pygame.K_DOWN] and player.bottom < HEIGHT:
            player.y += 6

        # 플레이어 애니메이션 상태
        if moving_left:
            if current_frames != left_frames:
                current_frames = left_frames
                frame_index = 0

        elif moving_right:
            if current_frames != right_frames:
                current_frames = right_frames
                frame_index = 0

        else:
            if current_frames != idle_frames:
                current_frames = idle_frames
                frame_index = 0

        # 플레이어 애니메이션 업데이트
        frame_timer += dt
        if frame_timer >= FRAME_DELAY:
            frame_index = (frame_index + 1) % len(current_frames)
            frame_timer = 0

        # 🔫 총알 생성
        shoot_cd -= 1
        if keys[pygame.K_SPACE] and shoot_cd <= 0:
            b = pygame.Rect(player.centerx - BULLET_W // 2, player.top, BULLET_W, BULLET_H)
            bullets.append(b)
            shoot_cd = 15

        # 총알 이동
        bullets = [b for b in bullets if b.bottom > 0]
        for b in bullets:
            b.y -= 10

        # 🔥 총알 애니메이션
        bullet_timer += dt
        if bullet_timer >= BULLET_DELAY:
            bullet_index = (bullet_index + 1) % len(bullet_frames)
            bullet_timer = 0

        # 적 생성
        spawn_timer += 1
        if spawn_timer >= level_cfg["spawn"]:
            spawn_timer = 0
            enemies.append(spawn_enemy(level_cfg))

        for en in enemies:
            en.y += level_cfg["enemy_speed"]

        enemies = [en for en in enemies if en.top < HEIGHT]

        # 🔥 적 애니메이션
        enemy_timer += dt
        if enemy_timer >= ENEMY_DELAY:
            enemy_index = (enemy_index + 1) % len(enemy_frames)
            enemy_timer = 0

        # 충돌
        for b in bullets[:]:
            for en in enemies[:]:
                if b.colliderect(en):
                    bullets.remove(b)
                    enemies.remove(en)
                    score += 10
                    break

        # 플레이어 충돌
        if invincible > 0:
            invincible -= 1
        else:
            for en in enemies:
                if player.colliderect(en):
                    lives -= 1
                    invincible = 90
                    enemies.clear()
                    if lives <= 0:
                        if game_over_screen(score):
                            main()
                        return
                    break

        # 🎨 렌더링
        screen.fill(GRAY)

        # 총알 렌더링
        for b in bullets:
            frame = bullet_frames[bullet_index]
            scaled = pygame.transform.scale(frame, (BULLET_W, BULLET_H))
            screen.blit(scaled, b.topleft)

        # 🔥 적 렌더링 (변경됨)
        for en in enemies:
            frame = enemy_frames[enemy_index]
            scaled = pygame.transform.scale(frame, (ENEMY_W, ENEMY_H))
            screen.blit(scaled, en.topleft)

        # 플레이어 렌더링
        blink = (invincible // 10) % 2 == 0
        if blink:
            frame = current_frames[frame_index]
            scaled = pygame.transform.scale(frame, (PLAYER_W, PLAYER_H))
            screen.blit(scaled, player.topleft)

        draw_hud(score, lives, level_cfg)
        pygame.display.flip()


main()