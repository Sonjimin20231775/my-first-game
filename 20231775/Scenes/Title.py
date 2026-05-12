import pygame
import sys
from Systems.SoundSystem import play_sound

WHITE = (255, 255, 255)
YELLOW = (255, 220, 80)
GRAY = (180, 180, 180)

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


def start_screen(window, bg_frames):
    clock = pygame.time.Clock()
    game_surface = pygame.Surface((BASE_WIDTH, BASE_HEIGHT))

    big_font = pygame.font.SysFont("malgungothic", 48, True)
    mid_font = pygame.font.SysFont("malgungothic", 32, True)
    font = pygame.font.SysFont("malgungothic", 24)

    bg_index = 0
    bg_timer = 0
    scroll_y = 0
    scroll_speed = 1

    menu_items = ["Game Start", "Quit"]
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
                        return window
                    elif selected_index == 1:
                        pygame.quit()
                        sys.exit()

                elif e.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

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
        overlay.fill((0, 0, 0, 120))
        game_surface.blit(overlay, (0, 0))

        title_text = big_font.render("Space Shooter", True, WHITE)
        game_surface.blit(title_text, title_text.get_rect(center=(400, 170)))

        start_color = YELLOW if selected_index == 0 else WHITE
        quit_color = YELLOW if selected_index == 1 else WHITE

        start_prefix = "▶ " if selected_index == 0 else "   "
        quit_prefix = "▶ " if selected_index == 1 else "   "

        start_text = mid_font.render(f"{start_prefix}Game Start", True, start_color)
        quit_text = mid_font.render(f"{quit_prefix}Quit", True, quit_color)

        game_surface.blit(start_text, start_text.get_rect(center=(400, 280)))
        game_surface.blit(quit_text, quit_text.get_rect(center=(400, 340)))

        control_title = font.render("[ Controls ]", True, YELLOW)
        control1 = font.render("LEFT / RIGHT : Move", True, WHITE)
        control2 = font.render("SPACE : Shoot", True, WHITE)
        control3 = font.render("UP / DOWN : Select Menu", True, WHITE)
        control4 = font.render("Z : Confirm", True, WHITE)
        control5 = font.render("ESC : Pause / Quit", True, GRAY)

        game_surface.blit(control_title, control_title.get_rect(center=(400, 430)))
        game_surface.blit(control1, control1.get_rect(center=(400, 470)))
        game_surface.blit(control2, control2.get_rect(center=(400, 500)))
        game_surface.blit(control3, control3.get_rect(center=(400, 530)))
        game_surface.blit(control4, control4.get_rect(center=(400, 560)))

        scaled = pygame.transform.smoothscale(game_surface, window.get_size())
        window.blit(scaled, (0, 0))
        pygame.display.flip()