import pygame
import random
import math

pygame.init()

WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fancy Particle Playground")

clock = pygame.time.Clock()

particles = []

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        angle = random.uniform(0, math.pi * 2)
        speed = random.uniform(2, 6)

        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed

        self.life = random.randint(60, 120)
        self.max_life = self.life

        self.size = random.randint(3, 6)

        self.color = [
            random.randint(150,255),
            random.randint(120,255),
            random.randint(180,255)
        ]

    def update(self):

        self.x += self.vx
        self.y += self.vy

        self.vy += 0.05
        self.vx *= 0.99
        self.vy *= 0.99

        self.life -= 1

        # 색상 살짝 변화
        self.color[0] = min(255, self.color[0] + random.randint(-1,1))
        self.color[1] = min(255, self.color[1] + random.randint(-1,1))
        self.color[2] = min(255, self.color[2] + random.randint(-1,1))

    def draw(self, surf):

        if self.life <= 0:
            return

        alpha = int(255 * (self.life / self.max_life))

        glow_surface = pygame.Surface((40,40), pygame.SRCALPHA)

        for i in range(3):
            radius = self.size + i*2
            glow_alpha = int(alpha / (i+1))

            pygame.draw.circle(
                glow_surface,
                (*self.color, glow_alpha),
                (20,20),
                radius
            )

        surf.blit(glow_surface, (self.x-20, self.y-20))

    def alive(self):
        return self.life > 0


def draw_background(surface, t):

    for y in range(HEIGHT):
        c = int(60 + 40 * math.sin(y * 0.01 + t))
        color = (10, c, 80 + c//2)
        pygame.draw.line(surface, color, (0, y), (WIDTH, y))


running = True
time = 0

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    mouse = pygame.mouse.get_pos()
    buttons = pygame.mouse.get_pressed()

    if buttons[0]:
        for _ in range(10):
            particles.append(Particle(mouse[0], mouse[1]))

    time += 0.03

    draw_background(screen, time)

    for p in particles:
        p.update()
        p.draw(screen)

    particles = [p for p in particles if p.alive()]

    pygame.display.flip()
    clock.tick(60)

pygame.quit()