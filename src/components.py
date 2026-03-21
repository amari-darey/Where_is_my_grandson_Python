import pygame
from abc import ABC
from dataclasses import dataclass
from collections import deque
from enum import Enum


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
class ComponentState(Component):
    current_state: Enum
    previous_state: Enum
    all_states: Enum

@dataclass
class ComponentPatrol(Component):
    points: deque
    