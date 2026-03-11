import pygame

from src.world import World
from src.components import *


class Systems:
    @staticmethod
    def draw_entities(world: World, window: pygame.Surface):
        entities = world.get_entities_with_all(ComponentImage, ComponentTransform)
        for entity in entities:
            transform = world.get_component(entity, ComponentTransform)
            image = world.get_component(entity, ComponentImage)
            window.blit(image.image, (transform.x, transform.y))