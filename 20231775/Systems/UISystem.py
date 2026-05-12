import pygame

WHITE = (255, 255, 255)
RED = (220, 50, 50)
GREEN = (50, 220, 80)


def draw_ui(surface, font, width, lives, max_lives, score, player_level, player_exp, exp_to_next):
    for i in range(max_lives):
        heart = "♥" if i < lives else "♡"
        surface.blit(font.render(heart, True, RED), (650 + i * 30, 10))

    score_text = font.render(f"Score: {score}", True, WHITE)
    score_rect = score_text.get_rect(center=(width // 2, 20))
    surface.blit(score_text, score_rect)

    surface.blit(font.render(f"Lv: {player_level}", True, GREEN), (10, 10))
    surface.blit(font.render(f"EXP: {player_exp}/{exp_to_next}", True, WHITE), (10, 40))