import pygame
import sys
from Systems.SoundSystem import play_sound

WHITE = (255, 255, 255)
YELLOW = (255, 220, 80)
GRAY = (180, 180, 180)

BASE_WIDTH = 800
BASE_HEIGHT = 600


def pause_screen(window, paused_surface):
    clock = pygame.time.Clock()

    big_font = pygame.font.SysFont("malgungothic", 48, True)
    mid_font = pygame.font.SysFont("malgungothic", 32, True)
    font = pygame.font.SysFont("malgungothic", 24)

    menu_items = ["Resume", "Restart", "Quit"]
    selected_index = 0

    while True:
        clock.tick(60)

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
                        return window, "resume"
                    elif selected_index == 1:
                        return window, "restart"
                    elif selected_index == 2:
                        return window, "quit"

                elif e.key == pygame.K_ESCAPE:
                    return window, "resume"

        game_surface = paused_surface.copy()

        overlay = pygame.Surface((BASE_WIDTH, BASE_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        game_surface.blit(overlay, (0, 0))

        pause_text = big_font.render("PAUSED", True, WHITE)

        resume_color = YELLOW if selected_index == 0 else WHITE
        restart_color = YELLOW if selected_index == 1 else WHITE
        quit_color = YELLOW if selected_index == 2 else WHITE

        resume_prefix = "▶ " if selected_index == 0 else "   "
        restart_prefix = "▶ " if selected_index == 1 else "   "
        quit_prefix = "▶ " if selected_index == 2 else "   "

        resume_text = mid_font.render(f"{resume_prefix}Resume", True, resume_color)
        restart_text = mid_font.render(f"{restart_prefix}Restart", True, restart_color)
        quit_text = mid_font.render(f"{quit_prefix}Quit", True, quit_color)

        guide1 = font.render("UP / DOWN : Select", True, WHITE)
        guide2 = font.render("Z : Confirm", True, WHITE)
        guide3 = font.render("ESC : Resume", True, GRAY)

        game_surface.blit(pause_text, pause_text.get_rect(center=(400, 160)))
        game_surface.blit(resume_text, resume_text.get_rect(center=(400, 270)))
        game_surface.blit(restart_text, restart_text.get_rect(center=(400, 330)))
        game_surface.blit(quit_text, quit_text.get_rect(center=(400, 390)))
        game_surface.blit(guide1, guide1.get_rect(center=(400, 480)))
        game_surface.blit(guide2, guide2.get_rect(center=(400, 515)))
        game_surface.blit(guide3, guide3.get_rect(center=(400, 550)))

        scaled = pygame.transform.smoothscale(game_surface, window.get_size())
        window.blit(scaled, (0, 0))
        pygame.display.flip()