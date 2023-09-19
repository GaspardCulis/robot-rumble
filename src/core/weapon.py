import abc
from abc import ABC

from pygame import Vector2


class Weapon(ABC):

    def __init__(self):
        pass


    @property
    @abc.abstractmethod
    def COOLDOWN(self):
        pass

    @abc.abstractmethod
    def shoot(self, position: Vector2, velocity: Vector2):
        pass

    @property
    @abc.abstractmethod
    def NAME(self):
        pass

    @property
    @abc.abstractmethod
    def IMAGE_PATH(self):
        pass
