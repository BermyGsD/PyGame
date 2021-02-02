import pygame
from os import path
import keys
from math import sin, cos, asin, degrees, radians
from log import logging


@logging
def load_image(name='images/error'):
    if not path.isfile(name):
        print(f"Файл с изображением '{name}' не найден")
        raise ValueError(f'Нет файла по пути {name}')
    image = pygame.image.load(name)
    image.convert_alpha()
    return image


class SpriteObject(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)

    def move_center_to(self, x, y):
        """Передвигает центр объекта в x, y"""
        self.rect.center = x, y

    def move(self, x, y):
        """передвигает объект на x, y"""
        self.rect.x += x
        self.rect.y += y

    def load_image(self, image: pygame.surface, angle: float = 0):
        """
        Загружает surface и меняет маску
        :param image:
        :param angle:
        :return:
        """
        self.image = pygame.transform.rotate(image, angle)
        self.rect = self.image.get_rect()

    def collide(self, group: pygame.sprite.Group):
        return bool(pygame.sprite.spritecollide(self, group, False, pygame.sprite.collide_circle))


class Entity(SpriteObject):
    def __init__(self, *group, obstacles: pygame.sprite.Group, entities: pygame.sprite.Group,
                 images=['images/error.png'], hp: int = 100, speed: int = 10, acceleration: float = 1.5):
        super().__init__(*group)
        self.obstacles = obstacles
        self.entities = entities
        self.angle = 0                          # Угол наклона изображения
        self.tick = 0                           # Текущий тик для изображения
        self.current = 0                        # Текущий номер изображения
        self.max_tick = 10                      # Макс. Значение self.tick, после которого меняется изображения
        self.hp = hp                            # Здоровье
        self.speed = speed                      # Максимальная длина шага
        self.acceleration = acceleration        # Ускорение при беге
        self.images = images                    # список путей к спрайтам
        self.load_image(load_image(self.images[self.current]), self.angle)
        self.rect = self.image.get_rect()
        self.radius = 13                        # Радиус кружочка для столкновений
        self.update_sprite()

    def change_sprite(self):
        """Метод для изменения картинки на следующую. Берёт следующий по счёту спрайт из self.image"""
        if len(self.images) - 1 <= self.current:
            self.current = -1
        if current:
            self.current = current
        else:
            self.current += 1
        self.update_sprite()

    def update_sprite(self, name=None):
        """
        Обновляет изображние на следующее в images или на указанное в name
        :param name:
        :return:
        """
        x, y = self.rect.center
        if name:
            self.load_image(load_image(name), self.angle)
        else:
            self.load_image(load_image(self.images[self.current]), self.angle)
        self.rect = self.image.get_rect()
        self.move_center_to(x, y)

    def new_tick(self, a=1):
        """Добавляет тик и, если он не меньше максимального, вызывает change_sprite и обнуляет self.tick"""
        self.tick += a
        if self.tick >= self.max_tick:
            self.tick = 0
            self.change_sprite()

    def can_move_to(self, delta_x, delta_y) -> bool:
        """
        Определяет, может ли объект сдвинутся на x, y
        :param delta_x: сдвиг по x
        :param delta_y: сдвиг по y
        """
        delta_x = -int(delta_x)
        delta_y = -int(delta_y)
        self.move(delta_x, delta_y)
        ans = True
        pygame.display.flip()
        if self.collide(self.obstacles):
            ans = False
        self.move(-delta_x, -delta_y)
        return ans


class Player(Entity):
    class Gun:
        def __init__(self, speed, scatter, damage):
            self.speed = speed
            self.scatter = scatter
            self.damage = damage

        def do_piu_piu(self, coordinates, angle):
            pass

    NO_GUN_IMAGES = ['images\\player\\player_0.png', 'images\\player\\player_1.png',
                     'images\\player\\player_2.png']
    GUN_1 = Gun(1, 1, 1)
    GUN_2 = Gun(1, 1, 1)

    def __init__(self, *group, obstacles: pygame.sprite.Group, world: pygame.sprite.Group):
        """
        :param group: группы для добавления спрайта игрока
        :param world: группа с спрайтами кроме игрока
        """
        super().__init__(*group, obstacles=obstacles, images=Player.NO_GUN_IMAGES)
        self.world = world
        self.rect = self.image.get_rect()
        self.rect.x = 350
        self.rect.y = 250
        self.gun = Player.GUN_1

    def update(self):
        angle = self.angle_to_mouse()
        self.angle = radians(degrees(angle + 90 + 180))
        self.update_sprite()
        #  Определяю, какие кнопочки нажаты и куда нужно воевать
        key_state = pygame.key.get_pressed()
        x_core, y_core = 0, 0
        speed = self.speed
        a = 1
        if key_state[keys.player_keys['UP']]:
            x_core = 1
        if key_state[keys.player_keys['DOWN']]:
            x_core -= 1
        if key_state[keys.player_keys['LEFT']]:
            y_core += 1
        if key_state[keys.player_keys['RIGHT']]:
            y_core -= 1
        if key_state[keys.player_keys['RUN']]:
            speed *= self.acceleration
            a = 2

        if x_core == 0:
            q = 90
            if y_core == 0:
                self.change_sprite(1)
                return None
            x_core = 1
        elif x_core == -1:
            q = -45
        else:
            q = 45

        angle_move = angle
        angle_move += q * y_core
        angle_move = radians(angle_move)
        x_circle, y_circle = cos(angle_move), sin(angle_move)
        x_move, y_move = -x_circle * speed * x_core, y_circle * speed * x_core
        while not self.can_move_to(x_move, y_move):
            x_move //= 1.1
            y_move //= 1.1
            if x_move < 1 and y_move < 1:
                x_move = y_move = 0
                break
        self.world_move(x_move, y_move)
        self.new_tick(a)
        if pygame.mouse.get_pressed()[0]:
            self.gun.do_piu_piu(self.rect.center, angle)

    def world_move(self, x, y):
        """
        Двигает world относительно игрока на x, y
        """
        for sprite in self.world.sprites():
            x, y = int(x), int(y)
            sprite.move(x, y)

    @staticmethod
    def get_move_vector(x, y, radius=1):
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
        x_player, y_player = self.rect.center
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

    def setup(self, img):
        self.load_image(load_image(img))


class Obstacle(SpriteObject):
    def __init__(self, *groups, x, y, image='images/error.png'):
        super().__init__(*groups)
        self.load_image(load_image(image))
        self.rect = self.image.get_rect()
        self.move(x, y)


class Wall(Obstacle):
    def __init__(self, *groups, x, y, image='images/environment/wall_1.png'):
        super().__init__(*groups, x=x, y=y, image=image)


class GUI:
    def __init__(self, screen, player):
        self.player = player
        self.screen = screen

    def update(self):
        pygame.draw.rect(self.screen, (120, 0, 0), ((0, 0), (self.player.hp, 10)))


class Bullet(SpriteObject):
    def __init__(self, *groups, delta_x, delta_y, x, y):
        super().__init__(groups)
        self.delta_x, self.delta_y = delta_x, delta_y
        self.move_center_to(x, y)

    def update(self):
        self.move(self.delta_x, self.delta_y)
