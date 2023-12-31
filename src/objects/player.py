import math
import random
from typing import Tuple

import pygame as pg
from pygame import Vector2, constants, transform
from pygame.key import ScancodeWrapper
from pygame.math import lerp
from pygame.sprite import Group, Sprite

import network
from core.gravity import PhysicsObject
from core.sound import Sound
from core.spritesheets import SpriteSheet
from objects.blackhole import BlackHole
from objects.gunbullet import GunBullet
from objects.holegun import BlackHoleGun
from objects.minigun import Minigun
from objects.planet import Planet
from objects.shotgun import Shotgun
from objects.weapon import Weapon

PLAYER_MASS = 800
PLAYER_HEIGHT = 80
PLAYER_VELOCITY = 500
ON_GROUND_THRESHOLD = 1

PLAYER_SPRITES_PATH = "assets/img/player"

class PlayerSpritesheet():
    def __init__(self, idle: SpriteSheet, run: SpriteSheet) -> None:
        self.idle = idle
        self.run = run

PLAYER_SPRITESHEETS = [
    PlayerSpritesheet(
        SpriteSheet("assets/img/player/player_idle.png", 3, 3, 0.1, frame_count=7, sprite_size=Vector2(PLAYER_HEIGHT)),
        SpriteSheet("assets/img/player/player_run.png", 3, 3, 0.1, frame_count=7, sprite_size=Vector2(PLAYER_HEIGHT))
    ),
    PlayerSpritesheet(
        SpriteSheet("assets/img/player/shiba_idle.png", 1, 4, 0.1, sprite_size=Vector2(PLAYER_HEIGHT)),
        SpriteSheet("assets/img/player/shiba_run.png", 1, 4, 0.1, sprite_size=Vector2(PLAYER_HEIGHT))
    ),
    PlayerSpritesheet(
        SpriteSheet("assets/img/player/shrek_idle.png", 1, 4, 0.1, sprite_size=Vector2(PLAYER_HEIGHT)),
        SpriteSheet("assets/img/player/shrek_run.png", 1, 3, 0.1, sprite_size=Vector2(PLAYER_HEIGHT))
    ),
    PlayerSpritesheet(
        SpriteSheet("assets/img/player/timoreo_idle.png", 1, 12, 0.1, sprite_size=Vector2(PLAYER_HEIGHT)),
        SpriteSheet("assets/img/player/timoreo_run.png", 1, 8, 0.1, sprite_size=Vector2(PLAYER_HEIGHT))
    )
]
        

class Player(PhysicsObject, Sprite):
    all: Group = Group()
    max_id: list[int] = [0]

    def __init__(self, position: Vector2, avatar_index: int = 0):
        super().__init__(mass=PLAYER_MASS, position=position, passive=True, static=False)
        self.new_position = position
        self.remote = False
        # Degrees
        self.rotation = 0.0
        # Ranges from 0.0 to 100.0
        self.percentage = 0.0
        self.lives = 3
        self.isDead = False
        self.is_running = False

        self.avatar_index = avatar_index
        self.avatar = PLAYER_SPRITESHEETS[avatar_index]

        self.frames = self.avatar.idle

        self.image = transform.rotozoom(self.frames.get_frame(), self.rotation, 1.0)
        self.rect = self.image.get_rect(center=self.image.get_rect(center=self.position).center)
        self.radius = PLAYER_HEIGHT / 2
        self.onground = False
        self.gotshot = False

        self.input_velocity = Vector2(0)

        self.weapons: list[Weapon] = [
            Minigun(self),
            Shotgun(self),
            BlackHoleGun(self),
        ]
        self.name = ""
        self.selected_weapon_index = 0
        self.unique_id = self.max_id[0]
        self.max_id[0] += 1
        self.all.add(self)

        self.spectated_player_index = 0

    def set_avatar(self, index: int):
        self.avatar_index = index
        self.avatar = PLAYER_SPRITESHEETS[self.avatar_index]

    def kill(self):
        self.lives -= 1
        if self.lives == 0:
            super().kill()
            self.all.remove(self)
            self.isDead = True
            print("Game over")
        else:
            print("dead")
            self.respawn_on_random_planet()
            self.percentage = 0
        Sound.get().play('ejection')

    def respawn_on_random_planet(self):

        spawn_positions: list[Tuple[float, Vector2, float, Planet]] = []
        for i in range(20):
            random_index = random.randint(0, len(Planet.all) - 1)
            random_planet = list(Planet.all)[random_index]
            self.set_rotation(random.randint(0, 360))
            self.position = random_planet.position + Vector2(1, 0).rotate(self.rotation)
            self.process_collision(random_planet, 0)

            if len(BlackHole.all) == 0:
                pos = Vector2(0)
            else:
                nearest_blackhole = \
                sorted(BlackHole.all, key=lambda b: b.position.distance_to(self.position) - b.radius)[0]
                pos = nearest_blackhole.position
            spawn_positions.append((self.position.distance_to(pos), self.position, self.rotation, random_planet))

        sorted_positions = sorted(spawn_positions, key=lambda p: p[0])
        final_position = sorted_positions[-1]
        self.position = final_position[1]
        self.rotation = final_position[2]
        planet = final_position[3]

        self.velocity = Vector2(0)

        # Set rotation
        target_angle = - math.degrees(
            math.atan2(planet.position.y - self.position.y, planet.position.x - self.position.x)) + 90

        self.set_rotation(target_angle)

    def update(self, delta: float):
        # Rotate towards nearest planet
        nearest_planet = sorted(Planet.all, key=lambda p: p.position.distance_to(self.position) - p.radius)[0]
        target_angle = - math.degrees(
            math.atan2(nearest_planet.position.y - self.position.y, nearest_planet.position.x - self.position.x)) + 90

        short_angle = (target_angle - self.rotation) % 360
        short_angle = 2 * short_angle % 360 - short_angle

        # Handles rect position set, frame update and rotation
        self.set_rotation(self.rotation + short_angle * delta * 6)
        if self.remote:
            self.position = Vector2(
                pg.math.lerp(self.position.x, self.new_position.x, min(delta * network.converter.TICK_RATE, 1)),
                pg.math.lerp(self.position.y, self.new_position.y, min(delta * network.converter.TICK_RATE, 1)))

        self.onground = self.position.distance_to(
            nearest_planet.position) < self.radius + nearest_planet.radius + ON_GROUND_THRESHOLD
        if self.onground:
            self.process_collision(nearest_planet, delta)

        self.process_bullets()

    def process_keys(self, keys: ScancodeWrapper, delta: float):
        """
        Met à jour le joueur en fonction d'un appui de  touche
        """

        if keys[constants.K_d]:
            self.input_velocity.x = lerp(self.input_velocity.x, PLAYER_VELOCITY, min(delta * 2, 1))
        if keys[constants.K_q]:
            self.input_velocity.x = lerp(self.input_velocity.x, -PLAYER_VELOCITY, min(delta * 2, 1))
        if not (keys[constants.K_d] or keys[constants.K_q]):
            self.input_velocity.x = lerp(self.input_velocity.x, 0, min(delta * 6, 1))
            self.is_running = False
        elif self.onground:
            self.is_running = True
        if (keys[constants.K_z] or keys[constants.K_SPACE]) and self.onground:
            speed = Vector2(0, -1).rotate(-self.rotation) * 600
            self.velocity += speed
            self.position += speed * delta  # Move, to avoid clipping instantly
            self.jumped = True
            Sound.get().play('jump')
        if keys[constants.K_s]:
            self.input_velocity.y = lerp(self.input_velocity.y, PLAYER_VELOCITY * 0.75, min(delta * 4, 1))
        else:
            self.input_velocity.y = lerp(self.input_velocity.y, 0, min(delta * 10, 1))

        # Update position
        self.position += self.input_velocity.rotate(-self.rotation) * delta

    def process_collision(self, collider: Planet, delta: float):
        """
        Met à jour le joueur en fonction de potentiels objets en collision
        """
        if not hasattr(self, "first_frame"):
            self.first_frame = False
            return
        # Check if lands on his feets
        collision_normal: Vector2 = (self.position - collider.position).normalize()
        # La différence entre notre rotation et l'angle de la normale au sol
        rotation_normal_diff = abs((collision_normal.angle_to(Vector2(1, 0)) + 360) % 360 - (self.rotation + 450) % 360)
        if rotation_normal_diff > 30 or self.gotshot:
            # Not on feets, bounce
            velocity_along_normal = self.velocity.dot(collision_normal)
            reflexion_vector = self.velocity - 2 * velocity_along_normal * collision_normal
            self.velocity = (1.2 if self.gotshot else 0.5) * reflexion_vector
            self.gotshot = False
        else:
            # Clip to the floor
            self.velocity = Vector2(0)
            self.jumped = False
        # In both cases, we want to set the position to the floor
        clip_position = collider.position + collision_normal * (self.radius + collider.radius)
        self.position = clip_position

    def handle_click(self, buttons: Tuple[bool, bool, bool], last_buttons: Tuple[bool, bool, bool], position: Vector2):
        if self.isDead:
            return
        # Shooting
        if buttons[2] and not last_buttons[2]:
            self.selected_weapon_index = (self.selected_weapon_index + 1) % len(self.weapons)

        if buttons[0]:
            self.velocity -= self.weapons[self.selected_weapon_index].shoot(position)

    def process_bullets(self):
        for bullet in pg.sprite.spritecollide(self, GunBullet.all, False):
            if bullet.owner_id != self.unique_id:
                self.percentage += bullet.damage
                self.velocity += Vector2(1, 0).rotate(-bullet.angle) * bullet.kb * (self.percentage / 100 + 1)
                bullet.kill()
                self.gotshot = True

    def set_rotation(self, rotation: float):
        self.rotation = rotation
        if self.is_running:
            self.frames = self.avatar.run
        else:
            self.frames = self.avatar.idle
        self.image = pg.transform.rotate(self.frames.get_frame(), self.rotation)
        self.rect = self.image.get_rect(center=self.image.get_rect(center=self.position).center)
