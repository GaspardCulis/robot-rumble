import pygame
from pygame import Vector2, Rect
from time import monotonic
from core.gravity import PhysicsObject
from core.player import PlayerObject
SCREEN_SIZE = (1024, 768)

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE, pygame.SCALED, vsync=1)
pygame.display.set_caption('JAAJ')

planet_a = PhysicsObject(69, Vector2(500, 600))
planet_b = PhysicsObject(69, Vector2(500, 500))
planet_c = PhysicsObject(69, Vector2(500, 550), passive=True)

player1 = PlayerObject(Vector2(screen.get_width()/2, screen.get_height()/2), [], 80,80)


planet_a.velocity = Vector2(0.5, 0)
planet_b.velocity = Vector2(-0.5, 0)

planets = [
    planet_a,
    planet_b,
]

last_time = monotonic()
rect = Rect(player1.position.x, player1.position.y, player1.width, player1.height)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    new_time = monotonic()
    delta = new_time - last_time
    last_time = new_time
    screen.fill((255, 255, 255))

    for p in planets:
        pygame.draw.circle(screen, (0, 0, 255), p.position, 10)

    rect.x = player1.position.x
    rect.y = player1.position.y
    pygame.draw.rect(screen, "red",rect)
    for b in player1.bullets:
        pygame.draw.rect(screen, "green", Rect(b.position.x, b.position.y, 20, 20))
    player1.parseInput(pygame.key.get_pressed(), delta)

    PhysicsObject.update_all(delta*100)

    pygame.display.flip()
    print("FPS ", 1 / delta)

pygame.quit()
