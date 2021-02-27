"""Поведение ботов и стрельба (наверное)"""
from constant import *
import pygame

pygame.init()


def check_obstacle(point, point2, size=2):
    """
    Возвращает наличие стен на пути
    :param point: первая точка
    :param point2: вторая точка
    :param size: толщина линии
    :return: bool наличие OBSTACLES на пути
    """
    line = pygame.draw.line(SCREEN, (100, 100, 200), point, point2, size)
    objects = OBSTACLES.sprites()
    return bool(line.collidelistall(objects))


class AI:
    def __init__(self, enemy, hero):
        self.enemy = enemy
        self.hero = hero
        self.ex, self.ey, self.hx, self.hy = *self.enemy.rect.center, *self.hero.rect.center

    def attack(self):
        """проверяется доступность героя и либо бот идет в комнату к герою и прячется в укрытие,
         либо шагает из-за него и стреляет"""
        can_see = check_obstacle((self.ex, self.ey), (self.hx, self.hy))
        res = True
        if not can_see and not self.enemy.on_the_way:
            res = self.go_to_hero()
            self.enemy.on_the_way = True
            print('sd')
        if res and not self.enemy.on_the_way:
            angle = self.enemy.angle_to_coordinate(self.ex, self.ey, self.hx, self.hy)
            self.enemy.fire(angle)

    def go_to_hero(self):
        """поиск пути к герою и движение к нему"""
        ex, ey, hx, hy = self.ex, self.ey, self.hx, self.hy
        vert, hor = check_obstacle((ex, hy), (hx, hy)), check_obstacle((hx, ey), (hx, hy))
        print(vert, hor)
        if not vert \
                and not hor:
            return False
        searching = True
        delta = 0
        resxy = [(ex, ey), (ex, hy)]
        while searching:
            d = 64 * delta
            if vert and check_obstacle((ex - d, ey), (ex - d), hy):
                resxy = [(ex - d, ey), (ex - d, hy)]
            elif hor and check_obstacle((ex, ey - d), (hx, ey - d)):
                resxy = [(ex, ey - d), (hx, ey - d)]
            elif vert and check_obstacle((ex + d, ey), (ex + d, hy)):
                resxy = [(ex, ey + d), (hx, ey + d)]
            elif hor and check_obstacle((ex, ey + d), (hx, ey + d)):
                resxy = [(ex + d, ey), (ex + d, hy)]
            delta += 1
            if delta > 20:
                return False
        f = 0
        print(resxy)
        if resxy[0] % 64 > 32:
            f = 1
        d = 0
        if resxy[1] % 64 > 32:
            d = 1
        self.enemy.waypoints.append(resxy[1] // 64 * 64 + f)
        self.enemy.waypoints.append(resxy[0] // 64 * 64 + d)
        return True
