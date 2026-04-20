import pygame
from Systems.SoundSystem import play_sound

BULLET_W, BULLET_H = 12, 20
CLONE_BULLET_SIZE = 14


def update_player_bullets(bullets):
    for b in bullets:
        b.y -= 10
    return [b for b in bullets if b.bottom > 0]


def update_clone_bullets(clone_bullets):
    for b in clone_bullets:
        b["x"] += b["vx"]
        b["y"] += b["vy"]


def handle_player_bullet_collisions(bullets, enemies, player_exp, score):
    for b in bullets[:]:
        for en in enemies[:]:
            if b.colliderect(en["rect"]):
                play_sound("enemy_hit")
                bullets.remove(b)
                en["hp"] -= 1

                if en["hp"] <= 0:
                    enemies.remove(en)
                    player_exp += 10

                    if en["type"] == "enemy1":
                        score += 10
                    elif en["type"] == "enemy2":
                        score += 20
                    elif en["type"] == "enemy3":
                        score += 30
                break

    return player_exp, score


def handle_clone_bullet_collisions(clone_bullets, enemies, player_exp, score):
    for b in clone_bullets[:]:
        rect = pygame.Rect(b["x"], b["y"], 10, 10)
        for en in enemies[:]:
            if rect.colliderect(en["rect"]):
                play_sound("enemy_hit")
                clone_bullets.remove(b)
                en["hp"] -= 1

                if en["hp"] <= 0:
                    enemies.remove(en)
                    player_exp += 10

                    if en["type"] == "enemy1":
                        score += 10
                    elif en["type"] == "enemy2":
                        score += 20
                    elif en["type"] == "enemy3":
                        score += 30
                break

    return player_exp, score


def render_player_bullets(surface, bullets, bullet_frames):
    for b in bullets:
        surface.blit(
            pygame.transform.scale(bullet_frames[0], (BULLET_W, BULLET_H)),
            b.topleft
        )


def render_clone_bullets(surface, clone_bullets, clone_bullet_frames):
    for b in clone_bullets:
        surface.blit(
            pygame.transform.scale(clone_bullet_frames[0], (CLONE_BULLET_SIZE, CLONE_BULLET_SIZE)),
            (b["x"], b["y"])
        )