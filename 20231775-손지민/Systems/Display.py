import pygame

BASE_WIDTH = 800
BASE_HEIGHT = 600


def create_window():
    return pygame.display.set_mode((BASE_WIDTH, BASE_HEIGHT), pygame.RESIZABLE)


def create_game_surface():
    return pygame.Surface((BASE_WIDTH, BASE_HEIGHT)).convert()


def handle_resize(event, current_window):
    width = max(400, event.w)
    height = max(300, event.h)
    return pygame.display.set_mode((width, height), pygame.RESIZABLE)


def get_scaled_rect(window):
    win_w, win_h = window.get_size()

    scale = min(win_w / BASE_WIDTH, win_h / BASE_HEIGHT)

    scaled_w = int(BASE_WIDTH * scale)
    scaled_h = int(BASE_HEIGHT * scale)

    x = (win_w - scaled_w) // 2
    y = (win_h - scaled_h) // 2

    return pygame.Rect(x, y, scaled_w, scaled_h)


def present(window, game_surface, clear_color=(0, 0, 0)):
    window.fill(clear_color)

    target_rect = get_scaled_rect(window)

    scaled_surface = pygame.transform.smoothscale(
        game_surface,
        (target_rect.width, target_rect.height)
    )

    window.blit(scaled_surface, target_rect.topleft)
    pygame.display.flip()