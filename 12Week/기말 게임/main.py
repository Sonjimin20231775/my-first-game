import pygame
import sys

from Data.Player.Player import Player
from Data.Player.SONAR_Attack import SonarAttack
from Data.Background.Backgrounds import Backgrounds
from Data.Camera.Camera import Camera
from Data.Item.ItemSpawner import ItemSpawner
from Data.Item.SpecialItemSpawner import SpecialItemSpawner

pygame.init()

GAME_WIDTH, GAME_HEIGHT = 1920, 1080
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720

screen = pygame.display.set_mode(
    (WINDOW_WIDTH, WINDOW_HEIGHT),
    pygame.RESIZABLE
)
pygame.display.set_caption("Echo Exploration Game")

game_surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))

clock = pygame.time.Clock()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

player = Player(
    GAME_WIDTH // 2 - 20,
    GAME_HEIGHT // 2 - 20
)

camera = Camera(
    GAME_WIDTH,
    GAME_HEIGHT
)

sonar = SonarAttack()
backgrounds = Backgrounds(GAME_WIDTH, GAME_HEIGHT)

item_spawner = ItemSpawner(GAME_WIDTH, GAME_HEIGHT)
special_item_spawner = SpecialItemSpawner(GAME_WIDTH, GAME_HEIGHT)

money = 0
special_item_count = 0

upgrade_save_screen = False

font = pygame.font.SysFont(None, 40)
big_font = pygame.font.SysFont(None, 80)


def draw_scaled_screen():
    window_width, window_height = screen.get_size()

    scale = min(
        window_width / GAME_WIDTH,
        window_height / GAME_HEIGHT
    )

    scaled_width = int(GAME_WIDTH * scale)
    scaled_height = int(GAME_HEIGHT * scale)

    scaled_surface = pygame.transform.smoothscale(
        game_surface,
        (scaled_width, scaled_height)
    )

    x = (window_width - scaled_width) // 2
    y = (window_height - scaled_height) // 2

    screen.fill(BLACK)
    screen.blit(scaled_surface, (x, y))


def draw_upgrade_save_screen():
    overlay = pygame.Surface(
        (GAME_WIDTH, GAME_HEIGHT),
        pygame.SRCALPHA
    )

    overlay.fill((0, 0, 0, 180))
    game_surface.blit(overlay, (0, 0))

    title = big_font.render(
        "Upgrade / Save Screen",
        True,
        WHITE
    )

    text1 = font.render(
        "This screen will be used for upgrades and saving.",
        True,
        WHITE
    )

    text2 = font.render(
        "Press ESC to close.",
        True,
        WHITE
    )

    game_surface.blit(
        title,
        (
            GAME_WIDTH // 2 - title.get_width() // 2,
            300
        )
    )

    game_surface.blit(
        text1,
        (
            GAME_WIDTH // 2 - text1.get_width() // 2,
            430
        )
    )

    game_surface.blit(
        text2,
        (
            GAME_WIDTH // 2 - text2.get_width() // 2,
            500
        )
    )


running = True
while running:
    dt = min(clock.tick(60) / 1000, 0.05)

    game_surface.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            player_center_x = player.x + player.size / 2
            player_center_y = player.y + player.size / 2

            if event.key == pygame.K_SPACE:
                sonar.start(
                    player_center_x,
                    player_center_y,
                    max_radius=180,
                    expand_speed=8
                )

            if event.key == pygame.K_k:
                sonar.start(
                    player_center_x,
                    player_center_y,
                    max_radius=2000,
                    expand_speed=35
                )

            if event.key == pygame.K_f:
                if special_item_count > 0 and not upgrade_save_screen:
                    special_item_count -= 1
                    upgrade_save_screen = True

            if event.key == pygame.K_ESCAPE:
                upgrade_save_screen = False

    if not upgrade_save_screen:
        player.update()
        camera.update(player)

        sonar.update()
        backgrounds.update(dt, camera)

        item_spawner.update(dt, camera)
        special_item_spawner.update(dt, camera)

        player_rect = pygame.Rect(
            player.x,
            player.y,
            player.size,
            player.size
        )

        for item in item_spawner.items[:]:
            if sonar.detect_item(item):
                item.reveal()

            if item.can_collect() and player_rect.colliderect(item.get_rect()):
                money += item.value
                item_spawner.items.remove(item)

        for item in special_item_spawner.items[:]:
            if sonar.detect_item(item):
                item.reveal()

            if item.can_collect() and player_rect.colliderect(item.get_rect()):
                special_item_count += item.value
                special_item_spawner.items.remove(item)

    backgrounds.draw(game_surface, camera)
    item_spawner.draw(game_surface, camera)
    special_item_spawner.draw(game_surface, camera)

    player.draw(game_surface, camera)
    sonar.draw(game_surface, camera)

    money_text = font.render(
        f"Money: {money}",
        True,
        WHITE
    )

    special_text = font.render(
        f"Save/Upgrade Item: {special_item_count}",
        True,
        WHITE
    )

    game_surface.blit(money_text, (20, 20))
    game_surface.blit(special_text, (20, 65))

    if upgrade_save_screen:
        draw_upgrade_save_screen()

    draw_scaled_screen()

    pygame.display.flip()

pygame.quit()
sys.exit()