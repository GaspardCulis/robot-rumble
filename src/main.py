from os import path
import pygame
from pygame import Color, Rect, Vector2, image
from time import monotonic

from objects.planet import Planet
from objects.player import Player
from objects.bullet import Bullet

from core.gravity import PhysicsObject
from ui import homescreen

SCREEN_SIZE = (1024, 768)
ASSETS_PATH="assets/"
IMG_PATH=path.join(ASSETS_PATH, "img/")

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE, pygame.SCALED, vsync=1)
pygame.display.set_caption('Game')


homescreen.home_screen(screen)


planet_a = Planet(Vector2(512, 380), 300, image.load(path.join(IMG_PATH, "planet1.png")))
planet_b = Planet(Vector2(1200, 200), 100, image.load(path.join(IMG_PATH, "planet2.png")))

player = Player(Vector2(9, 30), image.load(path.join(IMG_PATH, "player.png")))

player.velocity = Vector2(0, 550)
player.set_rotation(-90)
camera_pos = Vector2()
camera_zoom = 1

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
    Bullet.all.update()

    screen.fill((255, 255, 255))

    screen.blits([(spr.image, spr.rect.move(camera_pos).scale_by(camera_zoom, camera_zoom)) for spr in Bullet.all])
    screen.blits([(spr.image, spr.rect.move(camera_pos).scale_by(camera_zoom, camera_zoom)) for spr in Planet.all])
    screen.blits([(spr.image, spr.rect.move(camera_pos).scale_by(camera_zoom, camera_zoom)) for spr in Player.all])

    mouse_pos = Vector2(pygame.mouse.get_pos()) - camera_pos
    if pygame.mouse.get_pressed()[0]:
        player.handle_click(mouse_pos)

    dest = -(player.position - Vector2(SCREEN_SIZE)/2)
    # add mouse deviation
    dest.x += (pygame.mouse.get_pos()[0] / SCREEN_SIZE[0] - 0.5) * -500
    dest.y += (pygame.mouse.get_pos()[1] / SCREEN_SIZE[1] - 0.5) * -500

    camera_pos.x = pygame.math.lerp(camera_pos.x, dest.x, min(abs(delta * (max(player.velocity.x/100, 1))), 1))  # abs(player.velocity.x)
    camera_pos.y = pygame.math.lerp(camera_pos.y, dest.y, min(abs(delta * (max(player.velocity.y/100, 1))), 1))
    pygame.display.flip()
    # print("FPS ", 1 / delta)

pygame.quit()
