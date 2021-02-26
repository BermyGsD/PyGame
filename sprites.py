import pygame
from os import path
import keys
from math import sin, cos, asin, degrees, radians
from log import logging
from random import random
from constant import *


def load_image(name='images/error.png', angle=0.0):
    if not path.isfile(name):
        print(f"Файл с изображением '{name}' не найден")
        raise ValueError(f'Нет файла по пути {name}')
    image = pygame.image.load(name)
    image = pygame.transform.rotate(image, angle)
    image.convert_alpha()
    return image


class SpriteObject(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(WORLD, ALL_SPRITES)
        self.penable = False  # Пробиваем ли объект

    def move_center_to(self, x, y):
        x, y = int(x), int(y)
        """Передвигает центр объекта в x, y"""
        self.rect.center = x, y

    def move(self, x, y):
        """передвигает объект на x, y"""
        x, y = int(x), int(y)
        self.rect.x += x
        self.rect.y += y

    def load_image(self, image: pygame.surface, angle: float = 0):
        """
        Загружает surface и меняет rect
        :param image:
        :param angle:
        :return: None
        """
        self.image = pygame.transform.rotate(image, angle)
        try:                                            # памятник моей тупости: rect картинки изначально имеет 0, 0
            center = self.rect.center                   # координаты, из-за чего враги смещались в нулевые координаты
        except AttributeError:                          # после загрузки изображения (Urmipie)
            self.rect = self.image.get_rect()
        else:
            self.rect = self.image.get_rect()
            self.rect.center = center

    def collide(self, group: pygame.sprite.Group):
        return bool(pygame.sprite.spritecollide(self, group, False, pygame.sprite.collide_circle))

    def hit(self, damage):
        """Возвращает пробиваемость (Может ли пуля продолжить двигаться и нанесённый урон)"""
        return self.penable, 0


class Entity(SpriteObject):
    class Gun:
        def __init__(self, owner, speed=25, scatter=0, damage=10, fire_range=10000, bullet_count=1,
                     fire_speed=50, reload_time=75, magazine=15):
            """
            :param owner: сущность-отправитель
            :param speed: скорость пуль
            :param scatter: разброс пуль
            :param damage: урон от пули
            :param fire_range: дальность
            :param bullet_count: количество пуль за один выстрел
            :param fire_speed: задержка в тиках между выстрелами
            :param reload_time: задержка в тиках при перезарядке
            :param magazine: количество патронов в магазине
            """
            self.bullet_count = bullet_count
            self.shoot_sound = SOUND_MACHINE_GUN
            self.owner = owner
            self.speed = int(speed + (random() - 0.5) * speed * 0.5)
            self.scatter = scatter * 2      # Умножаю, потому что в рассчётах фактически делю на 2
            self.damage = damage
            self.entities = ENTITIES
            self.tick = 0
            self.reload_time = 1
            self.fire_speed = fire_speed
            self.reload_speed = reload_time
            self.magazine = 0
            self.magazine_max = magazine

        def fire(self, coordinates, angle):  # TODO Доделать перезарядку и время между выстрелами
            """
            Стреляет
            :param coordinates: координаты создания пуль
            :param angle: угол направления пуль
            :return: None
            """
            if self.tick >= self.fire_speed and self.reload_time == 0 and self.magazine > 0:
                self.tick = 0
                self.magazine -= 1
                self.shoot_sound.play()
                for _ in range(self.bullet_count):
                    scatter = (random() - 0.5) * self.scatter
                    angle = radians(angle) + scatter
                    x_move, y_move = int(cos(angle) * self.speed), -int(sin(angle) * self.speed)
                    x, y = coordinates
                    Bullet(owner=self.owner, delta_x=x_move, delta_y=y_move,
                           x=x, y=y, damage=self.damage, angle=angle)
            elif self.magazine <= 0:
                self.reload()

        def reload(self):
            self.reload_time += 1

        def new_tick(self):
            if self.reload_time > 0:
                self.reload_time += 1
                if self.reload_time >= self.reload_speed:
                    self.reload_time = 0
                    self.magazine = self.magazine_max
                if self.reload_time >= self.reload_speed:
                    self.reload_speed = 0
                    self.tick = 0
            else:
                self.tick += 1

    def __init__(self, images=['images/error.png'], hp: int = 100, speed: int = 10, acceleration: float = 1.5):
        super().__init__()
        ENTITIES.add(self)
        self.obstacles = OBSTACLES
        self.entities = ENTITIES
        self.score = 0
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
        self.gun = Entity.Gun(owner=self, speed=50, scatter=0.05, damage=5)
        # TODO Норм стандартное оружие
        self.update_sprite()

    def change_sprite(self, current=None):
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
        # self.rect = self.image.get_rect()
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
        if self.collide(OBSTACLES):
        # if pygame.sprite.spritecollideany(self, OBSTACLES.sprites(), pygame.sprite.collide_circle):
            ans = False
        self.move(-delta_x, -delta_y)
        return ans

    def get_move_coordinates(self, delta_x, delta_y):
        """
        Возвращает координаты для движения
        """
        for case in (self.__check_step(delta_x, delta_y), self.__check_step(delta_x, 0), self.__check_step(0, delta_y)):
            if case:
                return case
        return 0, 0

    def __check_step(self, delta_x, delta_y):
        """
        Проверяет возможность прохода в нужную сторону и возвращает координаты, если может двигаться иначе False
        """
        while abs(delta_x) > 1 or abs(delta_y) > 1:
            if self.can_move_to(int(delta_x), int(delta_y)):
                return int(delta_x), int(delta_y)
            delta_x /= 2
            delta_y /= 2
        return False

    def fire(self, angle):
        self.gun.fire(self.rect.center, angle)

    def hit(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            x, y = self.rect.center
            deadbody = SpriteObject()
            deadbody.load_image(load_image('images\\enemy\\enemy_dead.png'))
            deadbody.move_center_to(x, y)
            deadbody.penable = True
            ENTITIES.add(deadbody)
            self.kill()
        return False, damage

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

    def angle_to_coordinate(self, x_from, y_from, x_to, y_to):
        """
        Возвращает угол между двумя точками
        :param x_from: откуда
        :param y_from: откуда
        :param x_to: куда
        :param y_to: куда
        :return: угол в градусах
        """
        x_relative, y_relative = -(x_from - x_to), y_from - y_to
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
        if x == 0 and y == -1:
            angle = 270  # Это не костыль
        return angle


class Player(Entity):
    NO_GUN_IMAGES = ['images\\player\\player_0.png', 'images\\player\\player_1.png',
                     'images\\player\\player_2.png']

    def __init__(self):
        """
        """
        self.GUN_1 = Entity.Gun(self)
        super().__init__(images=Player.NO_GUN_IMAGES)
        WORLD.remove(self)
        self.world = WORLD
        PLAYER.add(self)
        self.radius = 13
        self.rect = self.image.get_rect()
        self.rect.center = PLAYER_COORDINATES
        self.gun = self.GUN_1

    def update(self):
        self.gun.new_tick()
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

        move = True
        if x_core == 0:
            q = 90
            if y_core == 0:
                self.change_sprite(1)
                move = False
            x_core = 1
        elif x_core == -1:
            q = -45
        else:
            q = 45

        if move:
            angle_move = angle
            angle_move += q * y_core
            angle_move = radians(angle_move)
            x_circle, y_circle = cos(angle_move), sin(angle_move)
            x_move, y_move = -x_circle * speed * x_core, y_circle * speed * x_core
            """while not self.can_move_to(x_move, y_move):
                x_move //= 1.1
                y_move //= 1.1
                if x_move < 1 and y_move < 1:
                    x_move = y_move = 0
                    break
            self.world_move(x_move, y_move)"""
            self.world_move(*self.get_move_coordinates(x_move, y_move))
            self.new_tick(a)
        if pygame.mouse.get_pressed()[0]:
            self.fire(angle)

    def world_move(self, x, y):
        """
        Двигает world относительно игрока на x, y
        """
        for sprite in self.world.sprites():
            x, y = int(x), int(y)
            sprite.move(x, y)

    def angle_to_mouse(self):
        """
        Возвращает относительные координаты курсора
        :return: float градус до курсора
        """
        x_mouse, y_mouse = pygame.mouse.get_pos()
        return self.angle_to_coordinate(*self.rect.center, x_mouse, y_mouse)


class Enemy(Entity):
    IMAGES_1 = ['images/enemy/enemy_0.png', 'images/enemy/enemy_1.png', 'images/enemy/enemy_2.png']

    def __init__(self, x, y):
        super().__init__(images=Enemy.IMAGES_1)
        self.move_center_to(x, y)
        self.radius = 16
        self.speed = 5

    def update(self):
        self.gun.new_tick()
        x1, y1, x2, y2 = *self.rect.center, *PLAYER_COORDINATES
        x = 1 if x1 - x2 > 0 else -1
        y = 1 if y1 - y2 > 0 else -1
        self.angle = self.angle_to_coordinate(x1, y1, x2, y2) - 90
        if x >= 0 and y >= 0:
            x, y = -1, 1
            # print(1)
        elif x <= 0 and y >= 0:
            x, y = -1, 1
            # print(2)
        elif x >= 0 and y >= 0:
            # print(3)
            x, y = -1, 1
        else:
            x, y = -1, 1
            # print(4)        # TODO адекватный АИ
        x, y = x * cos(radians(self.angle - 90)) * self.speed, y * sin(radians(self.angle - 90)) * self.speed
        self.gun.fire(self.rect.center, self.angle + 90)
        # print(self.rect.collidelistall(OBSTACLES))
        self.move(*self.get_move_coordinates(x, y))
        self.new_tick()


class BackGround(SpriteObject):
    def __init__(self):
        super().__init__()

    def setup(self, img):
        self.load_image(load_image(img))


class Obstacle(SpriteObject):
    def __init__(self, x, y, image='images/error.png'):
        super().__init__()
        OBSTACLES.add(self)
        self.load_image(load_image(image))
        self.rect = self.image.get_rect()
        # self.radius = 32
        self.move(x, y)


class Wall(Obstacle):
    def __init__(self, x, y, image='images/environment/wall_1.png'):
        super().__init__(x=x, y=y, image=image)


class Bullet(SpriteObject):
    def __init__(self, damage, owner, delta_x, delta_y, x, y, angle):
        """
        :param owner: сущность, создавшая пули
        :param delta_x: каждое обновление прибавляет к x
        :param x: начальная координата
        :param delta_y: каждое обновление прибавляет к y
        :param y: начальная координата y
        """
        self.damage = damage
        super().__init__()
        ENTITIES.remove(self)
        self.load_image(image=load_image('images\\bullet.png', angle=angle))
        self.owner = owner
        self.delta_x, self.delta_y = delta_x, delta_y
        self.move_center_to(x, y)
        self.update()

    def update(self):
        old = self.rect.center
        if not (0 < old[0] < SIZE[0] and 0 < old[1] < SIZE[1]):
            self.kill()
            return None
        self.move(self.delta_x, self.delta_y)
        new = self.rect.center
        line = pygame.draw.line(SCREEN, (100, 100, 200), old, new, 3)
        objects = list(set(ENTITIES.sprites() + OBSTACLES.sprites()))
        try:
            objects.remove(self.owner)
        except ValueError:
            pass
        a = line.collidelistall(objects)
        objects = list(objects[i] for i in a)
        # can_move = None
        if objects:
            old_x, old_y = old
            obj = objects.pop(0)
            kill = obj
            obj = obj.rect.center
            x_kill, y_kill = obj[0] - old_x, obj[1] - old_y
            s_kill = x_kill ** 2 + y_kill ** 2
            for obj in objects:
                x, y = obj.rect.center
                x -= old_x
                y -= old_y
                s = x ** 2 + y ** 2
                if s_kill > s:
                    x_kill, y_kill, s_kill = x, y, s
                    kill = obj
            can_move, damage = kill.hit(self.damage)
            self.owner.score += damage
            if not can_move:
                self.kill()