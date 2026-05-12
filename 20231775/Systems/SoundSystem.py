import pygame

sounds = {}


def load_sounds():
    global sounds

    sounds = {
        "interact": pygame.mixer.Sound("Assets/Sounds/Interact.wav"),
        "laser": pygame.mixer.Sound("Assets/Sounds/Laser_Gun.wav"),
        "player_hit": pygame.mixer.Sound("Assets/Sounds/Player_Hit.wav"),
        "enemy_hit": pygame.mixer.Sound("Assets/Sounds/Enemy_Hit.wav"),
        "levelup": pygame.mixer.Sound("Assets/Sounds/Level_Up.wav"),
        "gameover": pygame.mixer.Sound("Assets/Sounds/Game_Over.wav"),
    }

    sounds["interact"].set_volume(0.4)
    sounds["laser"].set_volume(0.35)
    sounds["player_hit"].set_volume(0.2)
    sounds["enemy_hit"].set_volume(0.1)
    sounds["levelup"].set_volume(0.25)
    sounds["gameover"].set_volume(0.1)


def play_sound(name):
    if name in sounds:
        sounds[name].play()


def set_sound_volume(name, volume):
    if name in sounds:
        sounds[name].set_volume(volume)


def get_sound(name):
    return sounds.get(name)