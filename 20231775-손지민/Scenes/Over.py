import pygame
import sys
from Systems.SoundSystem import play_sound

WHITE = (255, 255, 255)
RED = (220, 50, 50)
YELLOW = (255, 220, 80)

BASE_WIDTH = 800
BASE_HEIGHT = 600


def draw_scrolling_background(surface, bg_image, scroll_y):
    bg_w = bg_image.get_width()
    bg_h = bg_image.get_height()

    overlap = 2
    step_x = bg_w - overlap
    step_y = bg_h - overlap

    start_y = -bg_h + scroll_y

    for x in range(0, BASE_WIDTH + bg_w, step_x):
        y = start_y
        while y < BASE_HEIGHT:
            surface.blit(bg_image, (x, y))
            y += step_y


def game_over_screen(window, bg_frames, final_score):
    clock = pygame.time.Clock()
    game_surface = pygame.Surface((BASE_WIDTH, BASE_HEIGHT))

    big_font = pygame.font.SysFont("malgungothic", 48, True)
    mid_font = pygame.font.SysFont("malgungothic", 32, True)
    font = pygame.font.SysFont("malgungothic", 24)

    bg_index = 0
    bg_timer = 0
    scroll_y = 0
    scroll_speed = 1

    menu_items = ["Restart", "Title", "Quit"]
    selected_index = 0

    while True:
        dt = clock.tick(60)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if e.type == pygame.VIDEORESIZE:
                window = pygame.display.set_mode((e.w, e.h), pygame.RESIZABLE)

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % len(menu_items)
                    play_sound("interact")

                elif e.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % len(menu_items)
                    play_sound("interact")

                elif e.key == pygame.K_z:
                    play_sound("interact")
                    if selected_index == 0:
                        return window, "restart"
                    elif selected_index == 1:
                        return window, "title"
                    elif selected_index == 2:
                        return window, "quit"

                elif e.key == pygame.K_ESCAPE:
                    return window, "quit"

        bg_timer += dt
        if bg_timer >= 150:
            bg_index = (bg_index + 1) % len(bg_frames)
            bg_timer = 0

        bg = bg_frames[bg_index]
        bg_h = bg.get_height()
        step_y = max(1, bg_h - 2)
        scroll_y = (scroll_y + scroll_speed) % step_y

        draw_scrolling_background(game_surface, bg, scroll_y)

        overlay = pygame.Surface((BASE_WIDTH, BASE_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        game_surface.blit(overlay, (0, 0))

        over_text = big_font.render("GAME OVER", True, RED)
        score_text = mid_font.render(f"Score : {final_score}", True, WHITE)

        restart_color = YELLOW if selected_index == 0 else WHITE
        title_color = YELLOW if selected_index == 1 else WHITE
        quit_color = YELLOW if selected_index == 2 else WHITE

        restart_prefix = "▶ " if selected_index == 0 else "   "
        title_prefix = "▶ " if selected_index == 1 else "   "
        quit_prefix = "▶ " if selected_index == 2 else "   "

        restart_text = mid_font.render(f"{restart_prefix}Restart", True, restart_color)
        title_text = mid_font.render(f"{title_prefix}Title", True, title_color)
        quit_text = mid_font.render(f"{quit_prefix}Quit", True, quit_color)

        guide_text = font.render("UP / DOWN : Select   Z : Confirm", True, WHITE)

        game_surface.blit(over_text, over_text.get_rect(center=(400, 170)))
        game_surface.blit(score_text, score_text.get_rect(center=(400, 240)))
        game_surface.blit(restart_text, restart_text.get_rect(center=(400, 330)))
        game_surface.blit(title_text, title_text.get_rect(center=(400, 390)))
        game_surface.blit(quit_text, quit_text.get_rect(center=(400, 450)))
        game_surface.blit(guide_text, guide_text.get_rect(center=(400, 530)))

        scaled = pygame.transform.smoothscale(game_surface, window.get_size())
        window.blit(scaled, (0, 0))
        pygame.display.flip()