import pygame
from os import path
import keys
from math import sin, cos, asin, degrees, radians


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


class Entity(SpriteObject):
    def __init__(self, *group,
                 images=['entities/error.png'], hp: int = 100, speed: int = 20, acceleration: float = 1.5):
        super().__init__(*group)
        self.angle = 0                      # Угол наклона изображения
        self.tick = 0                       # Текущий тик для изображения
        self.current = 0                    # Текущий номер изображения
        self.max_tick = 15                  # Макс. Значение self.tick, после которого меняется изображения
        self.hp = hp                        # Здоровье
        self.speed = speed                  # Максимальная длина шага
        self.acceleration = acceleration    # Ускорение при беге
        self.images = images                # список путей к спрайтам
        self.image = self.images[0]
        self.rect = self.image.get_rect()

    def change_sprite(self):
        """Класс для изменения картинки на следующую"""
        if len(self.images) - 2 >= self.current:
            self.current = -1
        self.current += 1
        x, y = self.rect.x, self.rect.y
        self.image = self.images[self.tick]
        self.rect.x = x
        self.rect.y = y
        self.rotate(self.angle)

    def nev_tick(self):
        self.tick += 1

    def load_image(self):
        pass # TODO Доделать смену спрайтов


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
        self.rect = self.image.get_rect()
        self.rect.x = 350
        self.rect.y = 250

    def update(self):
        angle = self.angle_to_mouse()
        # TODO поворот игрока. Именно сверху!

        #  Определяю, какие кнопочки нажаты и куда нужно воевать
        key_state = pygame.key.get_pressed()
        x_core, y_core = 0, 0
        if key_state[keys.player_keys['UP']]:
            x_core = 1
        if key_state[keys.player_keys['DOWN']]:
            x_core -= 1
        if key_state[keys.player_keys['LEFT']]:
            y_core += 1
        if key_state[keys.player_keys['RIGHT']]:
            y_core -= 1

        if x_core == 0:
            if y_core == 0:
                return None
            x_core = 1


        x, y = self.center()
        xm, ym = pygame.mouse.get_pos()
        angle_move = angle
        angle_move += 90 * y_core
        angle_move = radians(angle_move)
        x_circle, y_circle = cos(angle_move), sin(angle_move)
        x_move, y_move = -x_circle * self.speed * x_core, y_circle * self.speed * x_core
        self.world_move(x_move, y_move)
        # TODO Проверку на препяствия и ускорение


    def center(self):
        """
        Возвращает центр спрайта игрока
        :return: int: x, int: y
        """
        # Возможно, как-то можно вытащить по отдельности x и y, я не знаю
        def x():
            return self.rect.x + Player.CENTER

        def y():
            return self.rect.y + Player.CENTER
        return x(), y()  # FIXME Эта штука может некорректно работать после поворота игрока

    def world_move(self, x, y):
        """
        Двигает world относительно игрока на x, y
        """
        for sprite in self.world.sprites():
            x, y = int(x), int(y)
            sprite.vector_move(x, y)

    def get_move_vector(self, x, y, radius=1):
        """
        Возвращает координаты, лежащие на определённом расстоянии и на одной линии с x, y и 0, 0
        :param x: координата относительно игрока
        :param y: вторая координата относительно игрока
        :param radius: шаг игрока. Если не указано, берётся 1
        :return: 2 float-овых значения координат
        """
        if x == y == 0:
            return 0, 0
        c = (x ** 2 + y ** 2) ** 0.5    # получаю расстояние между курсором и игроком
        c = radius / c                  # получаю коофициент подобия
        return x * c, y * c

    def angle_to_mouse(self):
        """
        Возвращает относительные координаты курсора
        :return: float градус до курсора
        """
        x_mouse, y_mouse = pygame.mouse.get_pos()
        x_player, y_player = self.center()
        x_relative, y_relative = -(x_player - x_mouse), y_player - y_mouse
        x, y = self.get_move_vector(x_relative, y_relative)
        angle = abs(degrees(asin(y)))
        # if x > 0 and y > 0: angle += 0
        if x > 0 > y:
            angle = 360 - angle
        if x < 0:
            if y > 0:
                angle = 180 - angle
            else:
                angle += 180
        return angle


class Enemy(Entity):
    pass


class BackGround(SpriteObject):
    def __init__(self, *group):
        super().__init__(*group)
        self.group = group

    def setup(self, img):
        self.image = load_image(img)
        self.rect = self.image.get_rect()
