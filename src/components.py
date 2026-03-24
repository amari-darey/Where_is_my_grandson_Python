import pygame
from abc import ABC
from dataclasses import dataclass
from collections import deque
from enum import Enum
from uuid import UUID


class Component(ABC): pass


class ComponentPlayer(Component): pass
class ComponentEnemy(Component): pass
class ComponentZombie(Component): pass


@dataclass
class ComponentTransform(Component): 
    x: int
    y: int
    width: int
    height: int

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    @property
    def vector(self):
        return pygame.Vector2(self.x, self.y)

    @property
    def center_vector(self):
        return pygame.Vector2(self.x + self.width//2, self.y+ self.height//2)
    
@dataclass
class ComponentDirection(Component):
    direction: Enum

@dataclass
class ComponentMapPosition(Component):
    position: tuple[int, int]

@dataclass
class ComponentControl(Component):
    up: int
    left: int
    down: int
    right: int
    attack: int

@dataclass
class ComponentImage(Component):
    image: pygame.Surface


@dataclass
class ComponentDialog(Component):
    name: str
    image: pygame.Surface


@dataclass
class ComponentAnimation(Component):
    frame_rate: int
    time_from_last_frame: int


@dataclass
class ComponentSpeed(Component):
    speed: int

@dataclass
class ComponentVelocity(Component):
    dx: float
    dy: float

@dataclass
class ComponentCollision(Component): 
    min_distance: int

@dataclass
class ComponentState(Component):
    current_state: Enum
    previous_state: Enum
    all_states: Enum

@dataclass
class ComponentPatrol(Component):
    points: deque[tuple[int, int]]
    point_reaching_delay: int
    point_current_delay: int = 0
    point_reached: bool = False

@dataclass
class ComponentChase(Component):
    target: UUID|None
    distanse: int
