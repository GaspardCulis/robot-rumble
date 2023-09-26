import asyncio
import os
import random
from asyncio import DatagramTransport
from os import path
from time import monotonic

import pygame
from pygame import Vector2

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN, pygame.SCALED, vsync=1)

from core.camera import Camera
from core.generation import procedural_generation
from core.gravity import PhysicsObject
from core.imageloader import ImageLoader
from core.sound import Sound
from network import server, client
from network.client_callback import ClientCallback
from network.server import ServerProtocol
from network.server_callback import ServerCallback
from objects.blackhole import BlackHole
from objects.bullet import Bullet
from objects.planet import Planet
from objects.player import Player
from objects.weapon import Weapon
from ui import homescreen
from ui.hud import Hud

ASSETS_PATH = "assets/"
IMG_PATH = path.join(ASSETS_PATH, "img/")
BG_PATH = path.join(IMG_PATH, "backgrounds/")

pygame.display.set_caption('Game')
SCREEN_SIZE = pygame.display.get_window_size()

# procedural_generation()

backgrounds_list = os.listdir(BG_PATH)
bg_name = random.choice(backgrounds_list)
bg = ImageLoader.get_instance().load(BG_PATH + "/" + bg_name, scale=screen.get_size(), alpha_channel=False)

state = homescreen.home_screen(screen, bg)
if state == "quit":
    pygame.quit()
    exit(0)


async def run_game(state: tuple[str, int, str, int]):
    ip = state[0]
    port = state[1]
    name = state[2]
    avatar_index = state[3]
    connection: DatagramTransport
    player = Player(Vector2(9, 30), avatar_index)
    player.name = name
    if ip == "0.0.0.0":
        connection, protocol = await server.open_server(ServerCallback(), port)
        Bullet.is_server = True
        # NOTE !!! map MUST be created on both sides !
        planets, seed = procedural_generation()
        print("Map generated with seed", seed)
        protocol.server_seed = seed
    else:
        connection, protocol = await client.connect_to_server(ClientCallback(player), ip, port)
        await protocol.on_connected.wait()  # Block until connected successfully
        # map will be created in the client callback

    hud = Hud(player)
    camera = Camera(player, Vector2(SCREEN_SIZE))

    # Spawn player
    player.respawn_on_random_planet()
    # Move camera immediatly
    camera.update(60)
    # Rotate player
    player.update(60)

    last_time = monotonic()
    last_mouse_buttons = (False, False, False)
    running = True

    Sound.get().loop_music('in_game')
    police = pygame.font.Font("./assets/font/geom.TTF", 24)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        new_time = monotonic()
        delta = new_time - last_time
        last_time = new_time

        mouse_pos = Vector2(pygame.mouse.get_pos()) - camera.get_pos()
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
        screen.blits([(spr.image, spr.rect.move(camera.get_pos()).scale_by(*camera.get_scale())) for spr in Planet.all])
        screen.blits([(spr.image, spr.rect.move(camera.get_pos()).scale_by(*camera.get_scale())) for spr in Player.all])
        screen.blits([(spr.image, spr.rect.move(camera.get_pos()).scale_by(*camera.get_scale())) for spr in
                      filter(lambda w: w.is_selected(), Weapon.all)])
        screen.blits([(spr.image, spr.rect.move(camera.get_pos()).scale_by(*camera.get_scale())) for spr in Bullet.all])
        screen.blits(
            [(spr.image, spr.rect.move(camera.get_pos()).scale_by(*camera.get_scale())) for spr in BlackHole.all])

        # Display usernames
        for p in Player.all:
            p: Player
            name_render = police.render(p.name, True, (255, 255, 255))
            name_render = pygame.transform.rotate(name_render, p.rotation)
            r = Vector2(0, -40).rotate(-p.rotation)
            screen.blit(name_render, name_render.get_rect(center=p.position + r).move(camera.get_pos()).scale_by(*camera.get_scale()))

        hud.weapon_hud(screen)
        hud.hp_hud(screen)
        hud.fps_hud(screen, delta)
        camera.update(delta)

        async def flip():
            pygame.display.flip()

        await asyncio.ensure_future(flip())  # Needs to be async, will block network otherwise
        # print("FPS ", 1 / delta)
    connection.close()
    pygame.quit()


asyncio.run(run_game(state))
