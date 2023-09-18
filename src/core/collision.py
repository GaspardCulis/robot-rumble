import pygame
from pygame import Rect, Vector2
from abc import ABC, abstractmethod

class CollisionShape(ABC):    
    @abstractmethod
    def collides_with(self, o: 'CollisionShape') -> bool:
        pass   

class CircleShape(CollisionShape):
    def __init__(self, origin, radius):
        self.origin = origin
        self.radius = radius
    
    def collides_with(self, o: 'CollisionShape') -> bool:
        if isinstance(o, CircleShape):
            return self.origin.distance_squared_to(o.origin) <= (self.radius + o.radius)**2
        elif isinstance(o, RectShape):
            # Calculer le point le plus proche sur le rectangle par rapport au centre du cercle
            closest_x = max(o.rect.left, min(self.origin.x, o.rect.right))
            closest_y = max(o.rect.top, min(self.origin.y, o.rect.bottom))
            
            # Calculer la distance entre le centre du cercle et le point le plus proche            
            distance_squared = (self.origin.x - closest_x) ** 2 + (self.origin.y - closest_y) ** 2
            
             # Vérifier si la distance est inférieure ou égale au carré du rayon du cercle
            return distance_squared <= self.radius ** 2            
        else:
            raise Exception("Unsupported collision detection")

class RectShape(CollisionShape):
    def __init__(self, rect: Rect) -> None:
        self.rect = rect

    def collides_with(self, o: 'CollisionShape') -> bool:
        if isinstance(o, RectShape):
            return self.rect.colliderect(o.rect)
        elif isinstance(o, CircleShape):
            return o.collides_with(self)
        else:
            raise Exception("Unsupported collision detection")
            
        

class CollisionObject():
    def __init__(self, collision_shape: CollisionShape) -> None:
        self.shape = collision_shape

    def collides_with(self, o: 'CollisionObject') -> bool:
        return self.shape.collides_with(o.shape)
