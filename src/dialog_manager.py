import pygame
from typing import Callable
from uuid import uuid1,  UUID
from dataclasses import dataclass

from src.world import World
from src.utils import Utils
from src.states import GameState
from src.components import *
from src.constants import *


@dataclass
class Dialog:
    title: str
    text: tuple[str]
    image: pygame.Surface


class DialogManager:
    def __init__(self, font_path: str|None, change_state_method: Callable):
        pygame.font.init()
        self.__title_font = pygame.font.SysFont(font_path, FONT_TITLE_SIZE, bold=True)
        self.__context_font = pygame.font.SysFont(font_path, FONT_CONTEXT_SIZE)
        self.__fon = Utils.load_image_with_scale("tests/dialog_fon2.png", (SCREEN_SIZE[0], SCREEN_SIZE[1]//2))
        self.__fon_pos = 0, SCREEN_SIZE[1]//2
        self.__dialog_image = None
        self.__dialogs = {}
        self.__timer = 0
        self.__dialog_rect = pygame.Rect(0, SCREEN_SIZE[1]//2, SCREEN_SIZE[0], SCREEN_SIZE[1]//2)
        self.__mouse_rect = pygame.Rect(0, 0, 10, 10)
        self.__mouse_released = False

        self.__change_state = change_state_method

        self.active_dialog = None
        self.text_index = 0
        self.char_index = 0
        self.text_finish = False

        self.time_to_next_char = 100
        self.time_last_char = 0

    def add_dialog(self, world: World, target: UUID, text: tuple[str]) -> UUID:
        dialog_id = uuid1()
        dialog_component = world.get_component(target, ComponentDialog)

        self.__dialogs[dialog_id] = Dialog(
            title=dialog_component.name,
            text=text,
            image=dialog_component.image
        )

        return dialog_id
    
    def run_dialog(self, dialog_id: UUID) -> None:
        self.__change_state(GameState.DIALOG)

        self.active_dialog = self.__dialogs[dialog_id]
        self.text_index = 0
        self.char_index = 0
        self.time_last_char = 100

    def finish_dialog(self) -> None:
        self.__change_state(GameState.RUN)

        self.active_dialog = None
        self.text_index = 0
        self.char_index = 0
        self.time_last_char = 0

    def draw(self, window: pygame.Surface):
        if not self.active_dialog: return
        
        window.blit(self.active_dialog.image, (SCREEN_SIZE[0]-600, SCREEN_SIZE[1]-790))
        window.blit(self.__dialog_image, self.__fon_pos)

    def __draw_dialog_surface(self):
        self.__dialog_image = pygame.Surface((SCREEN_SIZE[0], SCREEN_SIZE[1]//2), pygame.SRCALPHA)
        self.__dialog_image.blit(self.__fon, (0, 0))
        self.__dialog_image.blit(self.__title_font.render(self.active_dialog.title, True, FONT_TITLE_COLOR), (110, 40))
        self.__dialog_image.blit(self.__context_font.render(self.active_dialog.text[self.text_index][0:self.char_index], True, FONT_CONTEXT_COLOR), (140, 90))

    def __update_current_text(self):
        text = self.active_dialog.text[self.text_index]
        click_in_dialog = self.__mouse_rect.colliderect(self.__dialog_rect)

        if self.char_index < len(text):
            if self.__mouse_released and click_in_dialog:
                self.char_index = len(text) - 1
                self.__mouse_released = False
            else:
                self.char_index += 1

        else:
            if self.text_index >= len(self.active_dialog.text) - 1:
                self.text_finish = True
            if self.char_index >= len(text) and self.__mouse_released and click_in_dialog:
                self.__mouse_released = False
                if self.text_index < len(self.active_dialog.text) - 1:
                    self.text_index += 1
                    self.char_index = 0

    def __mouse_handler(self, mouse_pos: tuple[int, int], mouse_relesed: bool):
        self.__mouse_rect.x, self.__mouse_rect.y = mouse_pos
        if mouse_relesed:
            self.__mouse_released = True
        if self.text_finish and mouse_relesed:
            self.finish_dialog()

    def update(self, dt: int, mouse_pos: tuple[int, int], mouse_relesed: bool) -> bool:
        self.time_last_char += dt
        self.__mouse_handler(mouse_pos, mouse_relesed)
        if self.time_last_char >= self.time_to_next_char:
            self.__draw_dialog_surface()
            self.__update_current_text()
            self.time_last_char = 0
        
        return self.text_finish

