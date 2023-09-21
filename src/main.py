import asyncio
import os
import random
from asyncio import DatagramTransport
from os import path
import pygame
from pygame import Color, Rect, Vector2, image
from time import monotonic

from network import server, client
from network.client_callback import ClientCallback
from network.server_callback import ServerCallback
from objects.blackhole import BlackHole

from objects.planet import Planet
from objects.player import Player
from objects.bullet import Bullet

from core.gravity import PhysicsObject
from objects.weapon import Weapon
from ui.hud import Hud
from ui import homescreen

from core.sound import Sound

SCREEN_SIZE = (1024, 768)
ASSETS_PATH="assets/"
IMG_PATH=path.join(ASSETS_PATH, "img/")
BG_PATH = path.join(IMG_PATH, "backgrounds/")

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE, pygame.SCALED, vsync=1)
pygame.display.set_caption('Game')


state = homescreen.home_screen(screen)
if state == "quit":
    pygame.quit()
    exit(0)

Sound.get().loop_music('in_game')

async def run_game(state: tuple[str, int]):
    ip = state[0]
    port = state[1]
    connection: DatagramTransport
    player = Player(Vector2(9, 30), image.load(path.join(IMG_PATH, "player.png")))
    if ip == "0.0.0.0":
        connection = await server.open_server(ServerCallback(), port)
    else:
        connection = await client.connect_to_server(ClientCallback(player), ip, port)
    # NOTE !!! map MUST be created on both sides !
    planet_a = Planet(Vector2(512, 380), 300, "planet1.png")
    planet_b = Planet(Vector2(1200, 200), 100, "planet2.png")

    player.velocity = Vector2(0, 550)
    player.set_rotation(-90)
    camera_pos = Vector2()
    camera_zoom = 1

    hud = Hud(player)


    last_time = monotonic()
    last_mouse_buttons = (False, False, False)
    running = True

    backgrounds_list = os.listdir(BG_PATH)

    bg_name = random.choice(backgrounds_list)
    bg = pygame.image.load(BG_PATH+"/"+bg_name).convert()
    bg = pygame.transform.scale(bg, screen.get_size())
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        new_time = monotonic()
        delta = new_time - last_time
        last_time = new_time

        mouse_pos = Vector2(pygame.mouse.get_pos()) - camera_pos
        mouse_buttons = pygame.mouse.get_pressed()
        player.process_keys(pygame.key.get_pressed(), delta)
        player.handle_click(mouse_buttons, last_mouse_buttons, mouse_pos)
        last_mouse_buttons = mouse_buttons

        PhysicsObject.update_all(delta)
        Planet.all.update()
        Player.all.update(delta)
        Bullet.all.update(delta)
        Weapon.all.update(mouse_pos)

        screen.blit(bg, (0, 0))


        screen.blits([(spr.image, spr.rect.move(camera_pos).scale_by(camera_zoom, camera_zoom)) for spr in Planet.all])
        screen.blits([(spr.image, spr.rect.move(camera_pos).scale_by(camera_zoom, camera_zoom)) for spr in Player.all])
        screen.blits([(spr.image, spr.rect.move(camera_pos).scale_by(camera_zoom, camera_zoom)) for spr in filter(lambda w : w.is_selected(), Weapon.all)])
        screen.blits([(spr.image, spr.rect.move(camera_pos).scale_by(camera_zoom, camera_zoom)) for spr in Bullet.all])
        screen.blits([(spr.image, spr.rect.move(camera_pos).scale_by(camera_zoom, camera_zoom)) for spr in BlackHole.all])

        hud.weapon_hud(screen)

        dest = -(player.position - Vector2(SCREEN_SIZE)/2)
        # add mouse deviation
        dest.x += (pygame.mouse.get_pos()[0] / SCREEN_SIZE[0] - 0.5) * -500
        dest.y += (pygame.mouse.get_pos()[1] / SCREEN_SIZE[1] - 0.5) * -500

        camera_pos.x = pygame.math.lerp(camera_pos.x, dest.x, min(abs(delta * (max(player.velocity.x/100, 1))), 1))  # abs(player.velocity.x)
        camera_pos.y = pygame.math.lerp(camera_pos.y, dest.y, min(abs(delta * (max(player.velocity.y/100, 1))), 1))

        async def flip():
            pygame.display.flip()
        await asyncio.ensure_future(flip())  # Needs to be async, will block network otherwise
        print("FPS ", 1 / delta)
    connection.close()
    pygame.quit()

asyncio.run(run_game(state), debug=True)
