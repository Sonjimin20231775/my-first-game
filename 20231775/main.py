import pygame
import sys

# 플레이어
from sprite_data.Player_Idle import load_player_frames as load_idle
from sprite_data.Player_Left import load_player_frames as load_left
from sprite_data.Player_Right import load_player_frames as load_right

# 총알
from sprite_data.Bullet import load_bullet_frames
from sprite_data.Bullet_02 import load_bullet_frames as load_clone_bullet

# 적
from sprite_data.Enemy import load_enemy_frames
from sprite_data.Enemy_02 import load_enemy_frames as load_enemy2
from sprite_data.Enemy_03 import load_enemy_frames as load_enemy3
from sprite_data.Enemy_Bullet import load_bullet_frames as load_enemy_bullet

# 배경
from sprite_data.Background import load_background_frames

# 씬
from Scenes.Title import start_screen
from Scenes.Over import game_over_screen, draw_scrolling_background
from Scenes.Pause import pause_screen

# 시스템
from Systems.Display import (
    BASE_WIDTH,
    BASE_HEIGHT,
    create_window,
    create_game_surface,
    handle_resize,
    present
)
from Systems.PlayerSystem import (
    create_player,
    update_player_movement,
    update_player_animation,
    get_clones,
    handle_player_shoot,
    handle_clone_attack,
    render_player
)
from Systems.EnemySystem import (
    handle_enemy_spawn,
    update_enemies,
    update_enemy_bullets,
    render_enemies
)
from Systems.BulletSystem import (
    update_player_bullets,
    update_clone_bullets,
    handle_player_bullet_collisions,
    handle_clone_bullet_collisions,
    render_player_bullets,
    render_clone_bullets
)
from Systems.UISystem import draw_ui
from Systems.SoundSystem import load_sounds, play_sound

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = BASE_WIDTH, BASE_HEIGHT
FPS = 60
BLACK = (0, 0, 0)

window = create_window()
pygame.display.set_caption("Space Shooter")
clock = pygame.time.Clock()
font = pygame.font.SysFont("malgungothic", 24)

ENEMY_BULLET_SIZE = 16

load_sounds()


def run_game(window, bg_frames):
    game_surface = create_game_surface()
    player = create_player(WIDTH, HEIGHT)

    idle_frames = load_idle()
    left_frames = load_left()
    right_frames = load_right()

    bullet_frames = load_bullet_frames()
    clone_bullet_frames = load_clone_bullet()
    enemy_bullet_frames = load_enemy_bullet()

    enemy1 = load_enemy_frames()
    enemy2 = load_enemy2()
    enemy3 = load_enemy3()

    bg_index = 0
    bg_timer = 0
    bg_scroll_y = 0
    bg_scroll_speed = 1

    current_frames = idle_frames

    bullets = []
    clone_bullets = []
    enemies = []

    player_level = 1
    MAX_LEVEL = 5

    player_exp = 0
    exp_to_next = 50
    score = 0

    lives = 3
    max_lives = 5
    invincible = 0

    shoot_cd = 0
    spawn_timer = 0
    game_time = 0

    frame_index = 0
    frame_timer = 0
    clone_attack_timer = 0

    while True:
        dt = clock.tick(FPS)
        game_time += dt

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if e.type == pygame.VIDEORESIZE:
                window = handle_resize(e, window)

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    paused_surface = game_surface.copy()
                    window, pause_result = pause_screen(window, paused_surface)

                    if pause_result == "quit":
                        return window, "title", score
                    elif pause_result == "restart":
                        return window, "restart", 0

        keys = pygame.key.get_pressed()

        current_frames = update_player_movement(
            player, keys, WIDTH,
            current_frames, idle_frames, left_frames, right_frames
        )

        frame_timer, frame_index = update_player_animation(
            frame_timer, frame_index, current_frames, dt
        )

        bg_timer += dt
        if bg_timer >= 150:
            bg_index = (bg_index + 1) % len(bg_frames)
            bg_timer = 0

        bg = bg_frames[bg_index]
        bg_h = bg.get_height()
        step_y = max(1, bg_h - 2)
        bg_scroll_y = (bg_scroll_y + bg_scroll_speed) % step_y

        clones = get_clones(player_level)

        shoot_cd = handle_player_shoot(
            player, player_level, keys, bullets, shoot_cd
        )

        clone_attack_timer = handle_clone_attack(
            player, player_level, clones, enemies,
            clone_bullets, clone_attack_timer, dt
        )

        bullets = update_player_bullets(bullets)
        update_clone_bullets(clone_bullets)

        spawn_timer = handle_enemy_spawn(
            enemies, spawn_timer, game_time,
            enemy1, enemy2, enemy3, WIDTH
        )

        update_enemies(enemies, player)
        update_enemy_bullets(enemies)

        player_exp, score = handle_player_bullet_collisions(
            bullets, enemies, player_exp, score
        )

        player_exp, score = handle_clone_bullet_collisions(
            clone_bullets, enemies, player_exp, score
        )

        if invincible > 0:
            invincible -= 1
        else:
            for en in enemies[:]:
                if player.colliderect(en["rect"]):
                    play_sound("player_hit")
                    enemies.remove(en)
                    lives -= 1
                    invincible = 90
                    break

            for en in enemies:
                for b in en["bullets"][:]:
                    rect = pygame.Rect(b["x"], b["y"], 10, 10)
                    if player.colliderect(rect):
                        play_sound("player_hit")
                        en["bullets"].remove(b)
                        lives -= 1
                        invincible = 90
                        break

        if lives <= 0:
            play_sound("gameover")
            return window, "game_over", score

        if player_exp >= exp_to_next:
            play_sound("levelup")
            player_exp -= exp_to_next

            if player_level < MAX_LEVEL:
                player_level += 1
            else:
                if lives < max_lives:
                    lives += 1

            exp_to_next += 20

        draw_scrolling_background(game_surface, bg, bg_scroll_y)

        render_player_bullets(game_surface, bullets, bullet_frames)
        render_clone_bullets(game_surface, clone_bullets, clone_bullet_frames)
        render_enemies(game_surface, enemies, enemy_bullet_frames, ENEMY_BULLET_SIZE)
        render_player(game_surface, player, clones, current_frames, frame_index, invincible)

        draw_ui(
            game_surface,
            font,
            WIDTH,
            lives,
            max_lives,
            score,
            player_level,
            player_exp,
            exp_to_next
        )

        present(window, game_surface, BLACK)


def main():
    global window

    bg_frames = load_background_frames()
    current_scene = "title"

    while True:
        if current_scene == "title":
            window = start_screen(window, bg_frames)
            current_scene = "game"

        elif current_scene == "game":
            window, result, final_score = run_game(window, bg_frames)

            if result == "restart":
                current_scene = "game"
            elif result == "title":
                current_scene = "title"
            else:
                current_scene = "game_over"

        elif current_scene == "game_over":
            window, over_result = game_over_screen(window, bg_frames, final_score)

            if over_result == "restart":
                current_scene = "game"
            elif over_result == "title":
                current_scene = "title"
            else:
                break

    pygame.quit()
    sys.exit()


main()