import pygame
from time import monotonic

SCREEN_SIZE = (1280, 720)

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE, pygame.SCALED, vsync=1)
pygame.display.set_caption('JAAJ')

last_time = monotonic()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    new_time = monotonic()
    delta = new_time - last_time
    last_time = new_time
    screen.fill((255, 255, 255))

    pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)

    pygame.display.flip()
    print("FPS ", 1 / delta)

pygame.quit()
