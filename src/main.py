from os import path
import pygame
from pygame import Vector2, image
from time import monotonic
from core.gravity import PhysicsObject,physics_objects
from objects.planet import Planet
from objects.player import Player

SCREEN_SIZE = (1024, 768)
ASSETS_PATH="assets/"
IMG_PATH=path.join(ASSETS_PATH, "img/")

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE, pygame.SCALED, vsync=1)
pygame.display.set_caption('JAAJ')

planet_a = Planet(Vector2(512, 380), 300, image.load(path.join(IMG_PATH, "planet1.png")))

player = Player(Vector2(0, 0), image.load(path.join(IMG_PATH, "player.png")))


planets = [
    planet_a,
]

last_time = monotonic()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    new_time = monotonic()
    delta = new_time - last_time
    last_time = new_time
    
    PhysicsObject.update_all(delta)
    Planet.all.update()
    Player.all.update(delta)
    player.process_collisions([planet_a], delta)

    screen.fill((255, 255, 255))

    Planet.all.draw(screen)
    Player.all.draw(screen)    

    pygame.display.flip()
    #print("FPS ", 1 / delta)

pygame.quit()
