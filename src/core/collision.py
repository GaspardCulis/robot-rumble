import pygame
from pygame import Rect, Vector2
from abc import ABC, abstractmethod

COLLISION_SHAPE_COLOR = pygame.Color(0, 255, 255, 150)

class CollisionShape(ABC):
    def __init__(self, origin: Vector2) -> None:
        self.origin = origin
     
    @abstractmethod
    def collides_with(self, o: 'CollisionShape') -> bool:
        pass

    @abstractmethod
    def debug_draw(self, screen: pygame.Surface):
        pass 

class CircleShape(CollisionShape):
    def __init__(self, origin, radius):
        super().__init__(origin)
        self.radius = radius
    
    def collides_with(self, o: 'CollisionShape') -> bool:
        if isinstance(o, CircleShape):
            return self.origin.distance_squared_to(o.origin) <= (self.radius + o.radius)**2
        elif isinstance(o, RectShape):
            # Calculer le point le plus proche sur le rectangle par rapport au centre du cercle
            closest_x = max(o.origin.x, min(self.origin.x, o.origin.x + o.size.x))
            closest_y = max(o.origin.y + o.size.y, min(self.origin.y, o.origin.y))
            
            # Calculer la distance entre le centre du cercle et le point le plus proche            
            distance_squared = (self.origin.x - closest_x) ** 2 + (self.origin.y - closest_y) ** 2
            
             # Vérifier si la distance est inférieure ou égale au carré du rayon du cercle
            return distance_squared <= self.radius ** 2            
        else:
            raise Exception("Unsupported collision detection")

    def debug_draw(self, screen: pygame.Surface):
        pygame.draw.circle(screen, COLLISION_SHAPE_COLOR, self.origin, self.radius)


class RectShape(CollisionShape):
    def __init__(self, origin: Vector2, size: Vector2) -> None:
        super().__init__(origin)
        self.size = size

    def collides_with(self, o: 'CollisionShape') -> bool:
        if isinstance(o, RectShape):
            return self.get_rect().colliderect(o.get_rect())
        elif isinstance(o, CircleShape):
            return o.collides_with(self)
        else:
            raise Exception("Unsupported collision detection")

    def get_rect(self) -> Rect:
        return Rect(self.origin, self.size)

    def debug_draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, COLLISION_SHAPE_COLOR, self.get_rect())
        
        

class CollisionObject():
    def __init__(self, collision_shape: CollisionShape, **kw) -> None:
        super().__init__(**kw)
        self.shape = collision_shape

    def collides_with(self, o: 'CollisionObject') -> bool:
        return self.shape.collides_with(o.shape)
