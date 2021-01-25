import pygame
from os import path
import keys


def load_image(name):
    if not path.isfile(name):
        print(f"Файл с изображением '{name}' не найден")
        raise ValueError(f'Нет файла по пути {name}')
    image = pygame.image.load(name)
    image.convert_alpha()
    return image


class SpriteObject(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)

    def vector_move(self, x, y):
        self.rect.x += x
        self.rect.y += y
        print(self.rect.x, self.rect.y)



class Entity(SpriteObject):
    def __init__(self, *group, image='entities/error.png', hp: int = 100, speed: int = 30, acceleration: float = 1.5):
        super().__init__(*group)
        self.hp = hp
        self.speed = speed                  # Максимальная длина шага
        self.acceleration = acceleration    # Ускорение при беге
        self.image = load_image(image)
        self.rect = self.image.get_rect()


class Player(Entity):
    CENTER = 32                             # Центр игрока
    MOVE = ['UP', 'DOWN', 'LEFT', 'RIGHT']  # Множество вариантов движения

    def __init__(self, *group, world: pygame.sprite.Group):
        """
        :param group: группы для добавления спрайта игрока
        :param world: группа с спрайтами кроме игрока
        """
        super().__init__(*group)
        self.world = world
        self.image = load_image('entities/player.png')
        self.rect = self.image.get_rect()
        self.rect.x = 350
        self.rect.y = 250
        self.stack = set()

    def add_to_stack(self, action):
        if action in keys.player_keys_list:
            self.stack.add(keys.player_keys[action])
            if len(self.stack & {'UP', 'DOWN'}) == 2:
                self.stack.remove('UP')
                self.stack.remove('DOWN')
            if len(self.stack & {'LEFT', 'RIGHT'}) == 2:
                self.stack.remove('RIGHT')
                self.stack.remove('LEFT')

    def update(self):
        key_state = pygame.key.get_pressed()
        x, y = self.center()
        xm, ym = pygame.mouse.get_pos()
        delta_x, delta_y = x - xm, y - ym                      # координаты мыши относительно игрока
        if delta_y == delta_x == 0:
            delta_y = delta_x = 1
        c = (delta_x ** 2 + delta_y ** 2) ** 0.5               # получаю расстояние между курсором и игроком
        c = self.speed / c                                     # получаю коофициент подобия
        x_move, y_move = int(delta_x * c), int(delta_y * c)
        if delta_y == delta_x == 0:
            x_move = y_move = 0
        if key_state[pygame.K_w]:
            for sprite in self.world.sprites():
                sprite.vector_move(x_move, y_move)
        elif key_state[pygame.K_s]:
            pass
        if key_state[pygame.K_a]:
            pass
        elif key_state[pygame.K_d]:
            pass
        # TODO Допилить остальные варианты
        # TODO Выпилить stack из Player и всё прочее ненужное (Возможно, весь стек)
        # TODO Почитать документацию

        self.stack.clear()

    def center(self):
        # Возвращает координаты центра игрока
        # Возможно, как-то можно вытащить по отдельности x и y, я не знаю
        def x():
            return self.rect.x + Player.CENTER

        def y():
            return self.rect.y + Player.CENTER
        return x(), y()


class Enemy(Entity):
    pass


class BackGround(SpriteObject):
    def __init__(self, *group):
        super().__init__(*group)
        self.group = group

    def setup(self, img):
        self.image = load_image(img)
        self.rect = self.image.get_rect()
