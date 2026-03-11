from uuid import uuid1, UUID
from src.components import Component


class World:
    def __init__(self):
        self.__entities = {}

    def create_entity(self) -> UUID:
        """Создание новой сущность

        Returns:
            UUID: id новой сущности
        """
        entity = uuid1()
        self.__entities[entity] = {}
        return entity
    
    def add_component(self, entity: UUID, *components: Component) -> None:
        """Добавление компонентов к сущности

        Args:
            entity (UUID): id сущности
            components (Component): экземпляры компонентов
        """
        for component in components:
            self.__entities[entity][type(component)] = component

    def get_component(self, entity: UUID, component: Component) -> Component:
        """Получить компонент конкретной сущности

        Args:
            entity (UUID): id сущности
            component (Component): класс искомого компонента

        Returns:
            Component: Искомый компонент
        """

        return self.__entities[entity][component]

    def get_entities_with_all(self, *components: Component) -> tuple[UUID]:
        """Получить сущности имеющие все переданные компоненты

        Args:
            components (Component): классы компонентов

        Returns:
            tuple[UUID]: кортеж с id сущностей
        """

        components = set(components)
        entities = set()
        for entity, entity_components in self.__entities.items():
            if components.issubset(set(entity_components.keys())):
                entities.add(entity)
        
        return tuple(entities)
