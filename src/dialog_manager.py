import pygame
from typing import Callable
from uuid import uuid1,  UUID
from dataclasses import dataclass

from src.world import World
from src.utils import Utils
from src.states import GameState
from src.components import *
from config.game import SCREEN_SIZE
from config.dialog import DIALOG_FON, TIME_TO_NEXT_CHAR
from config.ui import *


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
        self.__fon = Utils.load_image_with_scale(DIALOG_FON, (SCREEN_SIZE[0], SCREEN_SIZE[1]//2))
        self.__fon_pos = 0, SCREEN_SIZE[1]//2
        self.__dialog_image = None
        self.__dialogs = {}
        self.__timer = 0
        self.__dialog_rect = pygame.Rect(0, SCREEN_SIZE[1]//2, SCREEN_SIZE[0], SCREEN_SIZE[1]//2)
        self.__mouse_rect = pygame.Rect(0, 0, 10, 10)
        self.__mouse_released = False

        self.__change_state = change_state_method

        self.__active_dialog = None
        self.__text_index = 0
        self.__char_index = 0
        self.__text_finish = False

        self.__time_to_next_char = TIME_TO_NEXT_CHAR
        self.__time_last_char = 0

    def add_dialog(self, world: World, target: UUID, text: tuple[str]) -> UUID:
        """Добавить диалог

        Args:
            world (World): Экземпляр класса World
            target (UUID): id сущности которая будет говорить
            text (tuple[str]): Кортеж строк которые будут выводится

        Returns:
            UUID: id диалога
        """
        dialog_id = uuid1()
        dialog_component = world.get_component(target, ComponentDialog)

        self.__dialogs[dialog_id] = Dialog(
            title=dialog_component.name,
            text=text,
            image=dialog_component.image
        )

        return dialog_id
    
    def run_dialog(self, dialog_id: UUID) -> None:
        """Запустить диалог  
        Смена состаяния игры на DIALOG

        Args:
            dialog_id (UUID): id диалога
        """
        self.__change_state(GameState.DIALOG)

        self.__active_dialog = self.__dialogs[dialog_id]
        self.__text_index = 0
        self.__char_index = 0
        self.__time_last_char = 100

    def finish_dialog(self) -> None:
        """Окончание диалога  
        Смена состаяния игры на RUN
        """
        self.__change_state(GameState.RUN)

        self.__active_dialog = None
        self.__text_index = 0
        self.__char_index = 0
        self.__time_last_char = 0

    def draw(self, window: pygame.Surface):
        """Отрисовка диалога на экране

        Args:
            window (pygame.Surface): Surface на котором нужно отрисовать диалог
        """
        if not self.__active_dialog: return
        
        window.blit(self.__active_dialog.image, (SCREEN_SIZE[0]-600, SCREEN_SIZE[1]-790))
        window.blit(self.__dialog_image, self.__fon_pos)

    def __draw_dialog_surface(self):
        """Подготовка surface диалога
        """
        self.__dialog_image = pygame.Surface((SCREEN_SIZE[0], SCREEN_SIZE[1]//2), pygame.SRCALPHA)
        self.__dialog_image.blit(self.__fon, (0, 0))
        self.__dialog_image.blit(self.__title_font.render(self.__active_dialog.title, True, FONT_TITLE_COLOR), (110, 40))
        self.__dialog_image.blit(self.__context_font.render(self.__active_dialog.text[self.__text_index][0:self.__char_index], True, FONT_CONTEXT_COLOR), (140, 90))

    def __update_current_text(self):
        """Обновление текущего отображаемого текста  
        Смена строк
        """
        text = self.__active_dialog.text[self.__text_index]
        click_in_dialog = self.__mouse_rect.colliderect(self.__dialog_rect)

        if self.__char_index < len(text):
            if self.__mouse_released and click_in_dialog:
                self.__char_index = len(text) - 1
                self.__mouse_released = False
            else:
                self.__char_index += 1

        else:
            if self.__text_index >= len(self.__active_dialog.text) - 1:
                self.__text_finish = True
            if self.__char_index >= len(text) and self.__mouse_released and click_in_dialog:
                self.__mouse_released = False
                if self.__text_index < len(self.__active_dialog.text) - 1:
                    self.__text_index += 1
                    self.__char_index = 0

    def __mouse_handler(self, mouse_pos: tuple[int, int], mouse_relesed: bool):
        """Обработка событий мыши

        Args:
            mouse_pos (tuple[int, int]): Текущая позиция курсора мыши на экране
            mouse_relesed (bool): Была ли отпущена клавиша мыши
        """
        self.__mouse_rect.x, self.__mouse_rect.y = mouse_pos
        if mouse_relesed:
            self.__mouse_released = True
        if self.__text_finish and mouse_relesed:
            self.finish_dialog()

    def update(self, dt: int, mouse_pos: tuple[int, int], mouse_relesed: bool) -> bool:
        """Обновление состояния диалога

        Args:
            dt (int): Дельта времени в миллисекундах
            mouse_pos (tuple[int, int]): Текущая позиция курсора мыши
            mouse_relesed (bool): Отпущена ли клавиша мыши

        Returns:
            bool: Закончен ли диалог
        """
        self.__time_last_char += dt
        self.__mouse_handler(mouse_pos, mouse_relesed)
        if self.__time_last_char >= self.__time_to_next_char:
            self.__draw_dialog_surface()
            self.__update_current_text()
            self.__time_last_char = 0
        
        return self.__text_finish

