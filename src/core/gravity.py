from pygame import Vector2
import math

G = 800
 
class PhysicsObject():
    all_objects: list['PhysicsObject'] = []
    def __init__(self, mass: float, position: Vector2, passive: bool = False, static = False, **kw):
        super().__init__(**kw)
        # La masse de l'objet
        self.mass = mass
        # Si l'objet a une influence gravitationnelle sur les autres.
        self.passive = passive
        # Si l'objet ne bouge pas
        self.static = static
            
        self.position = position
        self.velocity = Vector2(0, 0)

        PhysicsObject.all_objects.append(self)

    def kill(self):
        PhysicsObject.all_objects.remove(self)

    def update_forces(self, delta: float):
        force = Vector2(0, 0)
        for o in filter(lambda x : not (x.passive or x == self), PhysicsObject.all_objects):
            distance = self.position.distance_squared_to(o.position)
            f = G * (self.mass * o.mass) / distance
            force += f * (o.position - self.position).normalize()

        self.velocity += (force / self.mass) * delta
        self.position += self.velocity * delta

    def check_bounds(self):
        if self.position.x > 3000 or self.position.x < -3000 or self.position.y > 3000 or self.position.y < -3000:
            self.kill()

    @staticmethod
    def update_all(delta: float):
        for o in PhysicsObject.all_objects:
            if not o.static:
                o.update_forces(delta)
            o.check_bounds()
