import pygame
from uuid import UUID

from src.map_manager import Map
from src.world import World
from src.camera import Camera
from src.utils import Utils
from src.assests_manager import AnimationAssets
from src.components import *
from src.states import *
from config.tiles import TILE_SIZE


class Systems:
    @staticmethod
    def system_draw_entities(world: World, window: pygame.Surface, camera: Camera) -> None:
        """Система отрисовки сущностей  
        Отрисовывает все сущности содержащие компоненты ComponentImage, ComponentTransform

        Args:
            world (World): экземпляр класса World
            window (pygame.Surface): Surface экрана
        """
        entities = world.get_entities_with_all(ComponentImage, ComponentTransform)
        for entity in entities:
            transform = world.get_component(entity, ComponentTransform)
            image = world.get_component(entity, ComponentImage)
            pos_x, pos_y = camera.cordinate_world_to_screen((transform.x, transform.y))
            window.blit(image.image, (pos_x, pos_y))

    @staticmethod
    def system_animation_update(world: World, animation_assets: AnimationAssets, dt: int) -> None:
        """Обновление анимации  
        Если время с последней анимации больше чем frame_rate то в ComponentImage записывается новое изображение

        Args:
            world (World): экземпляр класса World
            dt (int): количество миллисекунд с последнего кадра
        """
        entities = world.get_entities_with_all(ComponentAnimation, ComponentImage, ComponentDirection)
        for entity in entities:
            animation = world.get_component(entity, ComponentAnimation)
            animation.time_from_last_frame += dt
            if animation.time_from_last_frame >= animation.frame_rate:
                image_component = world.get_component(entity, ComponentImage)
                state = world.get_component(entity, ComponentState)
                direction = world.get_component(entity, ComponentDirection)
                asset = animation_assets.get_asset(entity, state.current_state, direction.direction)
                asset.rotate(1)
                animation.time_from_last_frame = 0
                image_component.image = asset[0]

    @staticmethod
    def system_map_draw(map: pygame.Surface, window: pygame.Surface, camera: Camera) -> None:
        """Отрисовка карты с учётом офсета камеры

        Args:
            map (pygame.Surface): Карта
            window (pygame.Surface): Surface на котором нужно отрисовать карту
            camera (Camera): экземпляр класса Camera
        """
        window.blit(map, (0 - camera.ofset_x, 0 - camera.ofset_y))


    @staticmethod
    def system_player_movement(world: World, key: dict, dt: int) -> None:
        """Передвижение персонажа

        Args:
            world (World): экземпляр класса World
            key (dict): Словарь нажатых клавишь (pygame.key.get_pressed())
            dt (int): количество миллисекунд с последнего кадра
        """
        dt = dt / 1000
        entity = world.get_single_entity_with_all(
            ComponentTransform, 
            ComponentPlayer, 
            ComponentControl, 
            ComponentState, 
            ComponentVelocity
            )
        control_component = world.get_component(entity, ComponentControl)
        transform_component = world.get_component(entity, ComponentTransform)
        speed_component = world.get_component(entity, ComponentSpeed)
        state_component = world.get_component(entity, ComponentState)
        direction_component = world.get_component(entity, ComponentDirection)
        velocity_component = world.get_component(entity, ComponentVelocity)
        dx = dy = 0
        if key[control_component.left]:
            dx -= speed_component.speed * dt
        if key[control_component.right]:
            dx += speed_component.speed * dt
        if key[control_component.up]:
            dy -= speed_component.speed * dt
        if key[control_component.down]:
            dy += speed_component.speed * dt

        velocity_component.dx = dx
        velocity_component.dy = dy
        
        if dx > 0:
            direction_component.direction = StateDirection.RIGHT
        if dx < 0:
            direction_component.direction = StateDirection.LEFT
        if not dx and not dy:
            state_component.previous_state = state_component.current_state
            state_component.current_state = state_component.all_states.IDLE
        else:
            state_component.previous_state = state_component.current_state
            state_component.current_state = state_component.all_states.WALK

    @staticmethod
    def system_draw_circle_around_target(
        world: World, 
        camera: Camera, 
        mouse_pos: tuple[int, int]|pygame.Vector2, 
        window: pygame.Surface,
        max_distanse: int = 50
        ) -> None:
        """Система отрисовки круга над текущим таргетов 

        Args:
            world (World): Эклемпляр класса World
            camera (Camera): Эклемпляр класса Camera
            mouse_pos (tuple[int, int] | pygame.Vector2): Позиция мыши на экране
            window (pygame.Surface): Surface окна игры
            max_distanse (int, optional): _description_. Defaults to 50.
        """

        closest_entity = Utils.get_closest_enemy_to_mouse(world, camera, mouse_pos, max_distanse)
        if closest_entity:
            transform = world.get_component(closest_entity, ComponentTransform)
            transform_rect = transform.rect
            pos_x, pos_y = camera.cordinate_world_to_screen(transform_rect.center)
            pygame.draw.circle(window, (255, 0 , 0), (pos_x, pos_y), 35, 6)

    @staticmethod
    def system_patrol_update(world: World, map_manager: Map, dt: int) -> None:
        """Обновление системы патруля.  
        Обновляет:  
            Задержку между достичением точки и движением к следующей  
            Смена текущей точки, если задаржка закончилась  
            Получение пути к новой точке маршрута  

        Args:
            world (World): Экземпляр класса World
            map_manager (Map): Экземпляр класса Map
            dt (int): Время с последнего кадра
        """
        entities = world.get_entities_with_all(ComponentPatrol, ComponentPath, ComponentTransform)
        for entity in entities:
            patrol = world.get_component(entity, ComponentPatrol)
            path = world.get_component(entity, ComponentPath)
            if patrol.point_reached:
                patrol.point_current_delay += dt
                if patrol.point_current_delay >= patrol.point_reaching_delay:
                    patrol.points.rotate(1)
                    patrol.point_current_delay = 0
                    patrol.point_reached = False
                    transform = world.get_component(entity, ComponentTransform)
                    path_to_point = map_manager.get_path_to_point((transform.x, transform.y), patrol.points[0])
                    if path_to_point:    
                        path.path = path_to_point

    @staticmethod
    def system_patrol_update_point_reached(world: World) -> None:
        """Система обновления достижения точки маршрута системы патруля

        Args:
            world (World): Экземпляр класса Map
        """
        entities = world.get_entities_with_all(
            ComponentPatrol, 
            ComponentTransform,
            ComponentState
            )
        for entity in entities:
            state = world.get_component(entity, ComponentState)
            if state.current_state in (StateZombie.PATROL, ):
                patrol = world.get_component(entity, ComponentPatrol)
                if not patrol.point_reached:
                    transform = world.get_component(entity, ComponentTransform)
                    point_map_position = Map.world_to_tile(patrol.points[0])
                    entity_map_position = Map.world_to_tile((transform.x, transform.y))
                    if entity_map_position == point_map_position:
                        patrol.point_reached = True

    @staticmethod
    def system_change_zombie_state(world: World, player: UUID):
        """Система смены состояния зомби

        Args:
            world (World): Экземпляр класса World
            player (UUID): id сущности игрока
        """
        player_pos = world.get_component(player, ComponentTransform).vector
        entities = world.get_entities_with_all(ComponentZombie, ComponentState)
        for entity in entities:
            zombie_pos = world.get_component(entity, ComponentTransform).vector
            zombie_state = world.get_component(entity, ComponentState)
            zombie_chase = world.get_component(entity, ComponentChase)
            if zombie_pos.distance_to(player_pos) < zombie_chase.distanse:
                zombie_chase.target = player
                zombie_state.previous_state = zombie_state.current_state
                zombie_state.current_state = StateZombie.CHASE
            else:
                zombie_chase.target = None
                zombie_state.previous_state = zombie_state.current_state
                zombie_state.current_state = StateZombie.PATROL

    @staticmethod
    def system_move(world: World):
        """Система движения всех сущностей с компонентами ComponentVelocity и ComponentTransform

        Args:
            world (World): Экземпляр класса World
        """
        entities = world.get_entities_with_all(ComponentTransform, ComponentVelocity)
        for entity in entities:
            entity_velocity = world.get_component(entity, ComponentVelocity)
            entity_transform = world.get_component(entity, ComponentTransform)

            entity_transform.x += entity_velocity.dx
            entity_transform.y += entity_velocity.dy

            entity_velocity.dx = 0
            entity_velocity.dy = 0

    @staticmethod
    def system_enemy_move(world: World, dt: int):
        """Система определения направления движения для сущностей с компонентами  
        ComponentTransform, ComponentVelocity и ComponentPath  

        Args:
            world (World): Экземпляр класса World
            dt (int): Время с последнего кадра
        """
        dt = dt / 1000
        entities = world.get_entities_with_all(ComponentTransform, ComponentVelocity, ComponentPath)
        for entity in entities:
            path = world.get_component(entity, ComponentPath)
            
            if not path.path: continue
            transform = world.get_component(entity, ComponentTransform)
            velocity = world.get_component(entity, ComponentVelocity)
            speed = world.get_component(entity, ComponentSpeed).speed
            direction = world.get_component(entity, ComponentDirection)
            step = speed * dt
            rect_center = transform.center_vector
            path_point = path.path[0]
            tile_size = TILE_SIZE//2
            target_center = pygame.Vector2(path_point[0] + tile_size, path_point[1] + tile_size)
            direction_vector = target_center - rect_center
            if direction_vector.length() < step:
                path.path.pop(0)
                velocity.dx = 0
                velocity.dy = 0
                continue

            direction_vector = direction_vector.normalize()

            velocity.dx = direction_vector.x * step
            velocity.dy = direction_vector.y * step

            if direction_vector.x > 0:
                direction.direction = StateDirection.RIGHT
            if direction_vector.x < 0:
                direction.direction = StateDirection.LEFT

    @staticmethod
    def system_collision_separator(world: World):
        """Система отталкивания
        Если слущности сойдутся ближе суммы их ComponentCollision.min_distance 
        они оттолкнутся друг от друга пропорционально их пересечению

        Args:
            world (World): Экземпляр класса World
        """
        entities = world.get_entities_with_all(
            ComponentTransform, 
            ComponentVelocity, 
            ComponentCollision
            )
        for index, entity in enumerate(entities):
            transform = world.get_component(entity, ComponentTransform)
            velocity = world.get_component(entity, ComponentVelocity)
            collision = world.get_component(entity, ComponentCollision)
            for other_entity in range(index + 1, len(entities)):
                other_transform = world.get_component(entities[other_entity], ComponentTransform)
                other_velocity = world.get_component(entities[other_entity], ComponentVelocity)
                other_collision = world.get_component(entities[other_entity], ComponentCollision)

                vel = transform.center_vector - other_transform.center_vector
                distance_square = vel.x * vel.x + vel.y * vel.y

                if distance_square == 0: continue

                min_distance = collision.min_distance + other_collision.min_distance
                min_distance_square = min_distance * min_distance

                if distance_square < min_distance_square:
                    distance = distance_square ** 0.5
                    new_x = vel.x / distance
                    new_y = vel.y / distance

                    dot1 = velocity.dx * new_x + velocity.dy * new_y
                    if dot1 > 0:
                        velocity.dx -= new_x * dot1
                        velocity.dy -= new_y * dot1

                    dot2 = other_velocity.dx * (-new_x) + other_velocity.dy * (-new_y)
                    if dot2 > 0:
                        other_velocity.dx -= new_x * dot2
                        other_velocity.dy -= new_y * dot2

                    overlap = min_distance - distance

                    push_x = new_x * overlap * 0.5
                    push_y = new_y * overlap * 0.5

                    velocity.dx += push_x
                    velocity.dy += push_y
                    other_velocity.dx -= push_x
                    other_velocity.dy -= push_y
