import os
import random as rd

from pygame import Vector2

from objects.planet import Planet, PLANET_ASSETS_PATH

CENTRAL_STAR_RADIUS = 400

MIN_PLANETS = 8
MAX_PLANETS = 10

MIN_PLANET_RADIUS = 80
MAX_PLANET_RADIUS=400

MAX_PLANET_SURFACE_DISTANCE = 4000
MIN_PLANET_SURFACE_DISTANCE = 300

def procedural_generation() -> list[Planet]:
    # Initialisation
    files = os.listdir(PLANET_ASSETS_PATH)
    planet_spritesheets = list(filter(lambda s: s.startswith("planet"), files))
    star_spritesheets = list(filter(lambda s: s.startswith("star"), files))
    
    out: list[Planet] = []
    center = Vector2(0)

    out.append(Planet(center, CENTRAL_STAR_RADIUS, rd.choice(star_spritesheets)))

    num_planets = rd.randint(MIN_PLANETS, MAX_PLANETS)
    for i in range(num_planets):
        print(f"\rGenerating planets [{i + 1}/{num_planets}]", end='')
        while True:
            random_planet = rd.choice(out)
            random_direction = Vector2(1, 0).rotate(rd.randint(1, 360))
            radius = rd.randint(MIN_PLANET_RADIUS, MAX_PLANET_RADIUS)
            total_r = int(random_planet.radius + radius)
            distance = rd.randint(MIN_PLANET_SURFACE_DISTANCE - total_r, MAX_PLANET_SURFACE_DISTANCE - total_r)
            position: Vector2 = center + (random_direction * distance)

            sorted_planets = sorted(
                out,
                key=lambda p: position.distance_to(p.position) - total_r
            )

            closest = sorted_planets[0]
            furthest = sorted_planets[-1]
            if position.distance_to(closest.position) - total_r > MIN_PLANET_SURFACE_DISTANCE \
            and position.distance_to(furthest.position) - total_r < MAX_PLANET_SURFACE_DISTANCE:
                out.append(
                    Planet(position, radius, rd.choice(planet_spritesheets))
                )
                break
    
    return out