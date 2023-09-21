import os
import random as rd

from pygame import Vector2

from objects.planet import Planet, PLANET_ASSETS_PATH

CENTRAL_STAR_RADIUS = 600

MIN_PLANETS = 8
MAX_PLANETS = 10

MIN_PLANET_RADIUS = 80
MAX_PLANET_RADIUS=400

MAX_PLANET_SURFACE_DISTANCE = 6000
MIN_PLANET_SURFACE_DISTANCE = 100

def procedural_generation() -> list[Planet]:
    # Initialisation
    files = os.listdir(PLANET_ASSETS_PATH)
    planet_spritesheets = list(filter(lambda s: s.startswith("planet"), files))
    star_spritesheets = list(filter(lambda s: s.startswith("star"), files))
    
    out: list[Planet] = []
    center = Vector2(0)

    out.append(Planet(center, CENTRAL_STAR_RADIUS, rd.choice(star_spritesheets)))

    for i in range(rd.randint(MIN_PLANETS, MAX_PLANETS)):
        while True:
            random_direction = Vector2(1, 0).rotate(rd.randint(1, 360))
            distance = rd.randint(CENTRAL_STAR_RADIUS, CENTRAL_STAR_RADIUS * 10)
            position: Vector2 = center + (random_direction * distance)
            r = rd.randint(MIN_PLANET_RADIUS, MAX_PLANET_RADIUS)

            sorted_planets = sorted(
                out,
                key=lambda p: position.distance_to(p.position) - r - p.radius
            )

            closest = sorted_planets[0]
            furthest = sorted_planets[-1]
            if position.distance_to(closest.position) - r - closest.radius > MIN_PLANET_SURFACE_DISTANCE \
            and position.distance_to(furthest.position) - r - furthest.radius < MAX_PLANET_SURFACE_DISTANCE:
                out.append(
                    Planet(position, r, rd.choice(planet_spritesheets))
                )
                print(out)
                break

    return out