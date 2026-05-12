import pygame
import math
from Systems.SoundSystem import play_sound

PLAYER_W, PLAYER_H = 40, 40
BULLET_W, BULLET_H = 12, 20


def create_player(width, height):
    return pygame.Rect(width // 2, height - 70, PLAYER_W, PLAYER_H)


def update_player_movement(player, keys, width, current_frames, idle_frames, left_frames, right_frames):
    if keys[pygame.K_LEFT] and player.left > 0:
        player.x -= 6
        current_frames = left_frames
    elif keys[pygame.K_RIGHT] and player.right < width:
        player.x += 6
        current_frames = right_frames
    else:
        current_frames = idle_frames

    return current_frames


def update_player_animation(frame_timer, frame_index, current_frames, dt):
    frame_timer += dt
    if frame_timer >= 120:
        frame_index = (frame_index + 1) % len(current_frames)
        frame_timer = 0
    return frame_timer, frame_index


def get_clones(player_level):
    clones = []
    if player_level >= 3:
        clones.append(-50)
    if player_level >= 4:
        clones.append(50)
    return clones


def handle_player_shoot(player, player_level, keys, bullets, shoot_cd):
    shoot_cd -= 1

    if keys[pygame.K_SPACE] and shoot_cd <= 0:
        play_sound("laser")

        if player_level == 1:
            bullets.append(
                pygame.Rect(player.centerx - BULLET_W // 2, player.top, BULLET_W, BULLET_H)
            )
        else:
            bullets.append(
                pygame.Rect(player.centerx - 10 - BULLET_W // 2, player.top, BULLET_W, BULLET_H)
            )
            bullets.append(
                pygame.Rect(player.centerx + 10 - BULLET_W // 2, player.top, BULLET_W, BULLET_H)
            )

        shoot_cd = 15

    return shoot_cd


def handle_clone_attack(player, player_level, clones, enemies, clone_bullets, clone_attack_timer, dt):
    CLONE_ATTACK_DELAY = 2000

    clone_attack_timer += dt
    if clone_attack_timer >= CLONE_ATTACK_DELAY:
        clone_attack_timer = 0

        for offset in clones:
            cx = player.centerx + offset
            cy = player.top

            valid_enemies = [en for en in enemies if en["rect"].centery < player.centery]

            if valid_enemies:
                play_sound("laser")

                target = min(
                    valid_enemies,
                    key=lambda e: (e["rect"].centerx - cx) ** 2 + (e["rect"].centery - cy) ** 2
                )

                dx = target["rect"].centerx - cx
                dy = target["rect"].centery - cy
                dist = math.hypot(dx, dy) or 1

                speed = 10 / 1.5
                shot_count = 2 if player_level >= 5 else 1

                for i in range(shot_count):
                    angle_offset = (i - (shot_count - 1) / 2) * 0.2
                    vx = (dx / dist) * math.cos(angle_offset) - (dy / dist) * math.sin(angle_offset)
                    vy = (dx / dist) * math.sin(angle_offset) + (dy / dist) * math.cos(angle_offset)

                    clone_bullets.append({
                        "x": cx,
                        "y": cy,
                        "vx": vx * speed,
                        "vy": vy * speed
                    })

    return clone_attack_timer


def render_player(surface, player, clones, current_frames, frame_index, invincible):
    frame = current_frames[frame_index]

    if (invincible // 10) % 2 == 0:
        surface.blit(
            pygame.transform.scale(frame, (PLAYER_W, PLAYER_H)),
            player.topleft
        )

    for offset in clones:
        clone_rect = player.copy()
        clone_rect.x += offset
        surface.blit(
            pygame.transform.scale(frame, (PLAYER_W, PLAYER_H)),
            clone_rect.topleft
        )