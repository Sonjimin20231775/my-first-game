import pygame
import random
import math

ENEMY_W, ENEMY_H = 40, 40


def spawn_enemy(enemy_type, frames, width):
    x = random.randint(0, width - ENEMY_W)
    return {
        "type": enemy_type,
        "rect": pygame.Rect(x, -ENEMY_H, ENEMY_W, ENEMY_H),
        "base_x": x,
        "frames": frames,
        "hp": 2 if enemy_type == "enemy3" else 1,
        "bullets": [],
        "shoot_timer": 0,
        "move_timer": 0
    }


def spawn_enemy2_safe(enemies, frames, width):
    for _ in range(20):
        x = random.randint(0, width - ENEMY_W)

        too_close = False
        for en in enemies:
            if en["type"] == "enemy2":
                if abs(en["rect"].centerx - x) < 80:
                    too_close = True
                    break

        if not too_close:
            return {
                "type": "enemy2",
                "rect": pygame.Rect(x, -ENEMY_H, ENEMY_W, ENEMY_H),
                "base_x": x,
                "frames": frames,
                "hp": 1,
                "bullets": [],
                "shoot_timer": 0,
                "move_timer": 0
            }

    return spawn_enemy("enemy2", frames, width)


def handle_enemy_spawn(enemies, spawn_timer, game_time, enemy1, enemy2, enemy3, width):
    spawn_timer += 1

    if spawn_timer > 60:
        spawn_timer = 0

        if game_time < 20000:
            enemies.append(spawn_enemy("enemy1", enemy1, width))

        elif game_time < 40000:
            if random.random() < 0.5:
                enemies.append(spawn_enemy("enemy1", enemy1, width))
            else:
                enemies.append(spawn_enemy2_safe(enemies, enemy2, width))

        else:
            r = random.random()
            if r < 0.4:
                enemies.append(spawn_enemy("enemy1", enemy1, width))
            elif r < 0.7:
                enemies.append(spawn_enemy2_safe(enemies, enemy2, width))
            else:
                enemies.append(spawn_enemy("enemy3", enemy3, width))

    return spawn_timer


def update_enemies(enemies, player):
    for en in enemies:
        if en["type"] == "enemy1":
            en["rect"].y += 3

        elif en["type"] == "enemy2":
            if en["rect"].y < 100:
                en["rect"].y += 2

            en["shoot_timer"] += 1
            if en["shoot_timer"] > 90:
                en["shoot_timer"] = 0

                dx = player.centerx - en["rect"].centerx
                dy = player.centery - en["rect"].centery
                dist = math.hypot(dx, dy) or 1

                en["bullets"].append({
                    "x": en["rect"].centerx,
                    "y": en["rect"].centery,
                    "vx": dx / dist * 5,
                    "vy": dy / dist * 5
                })

        elif en["type"] == "enemy3":
            en["rect"].y += 3
            en["move_timer"] += 1
            en["rect"].x = en["base_x"] + int(50 * math.sin(en["move_timer"] * 0.1))


def update_enemy_bullets(enemies):
    for en in enemies:
        for b in en["bullets"]:
            b["x"] += b["vx"]
            b["y"] += b["vy"]


def render_enemies(surface, enemies, enemy_bullet_frames, enemy_bullet_size):
    for en in enemies:
        surface.blit(
            pygame.transform.scale(en["frames"][0], (ENEMY_W, ENEMY_H)),
            en["rect"].topleft
        )

        for b in en["bullets"]:
            surface.blit(
                pygame.transform.scale(enemy_bullet_frames[0], (enemy_bullet_size, enemy_bullet_size)),
                (b["x"], b["y"])
            )