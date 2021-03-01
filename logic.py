"""Поведение ботов и стрельба (наверное)"""
from constant import *
import pygame
import time

pygame.init()


def check_obstacle(point, point2, size=64):
    """
    Возвращает наличие стен на пути
    :param point: первая точка
    :param point2: вторая точка
    :param size: толщина линии
    :return: bool наличие OBSTACLES на пути
    """
    line = pygame.draw.line(SCREEN, (0, 0, 0), point, point2, size)
    objects = OBSTACLES.sprites()
    a = bool(line.collidelistall(objects))
    return not a


class AI:
    def __init__(self, enemy, hero):
        self.enemy = enemy
        self.hero = hero
        self.ex, self.ey, self.hx, self.hy = *self.enemy.rect.center, *self.hero.rect.center

    def attack(self):
        """проверяется доступность героя и либо бот идет в комнату к герою и прячется в укрытие,
         либо шагает из-за него и стреляет"""
        self.ex, self.ey, self.hx, self.hy = *self.enemy.rect.center, *self.hero.rect.center
        can_see = check_obstacle((self.ex, self.ey), (self.hx, self.hy))
        res = True
        if not can_see and len(self.enemy.waypoints) == 0:
            res = self.go_to_hero()
            self.enemy.on_the_way = True
        if res and can_see:
            angle = self.enemy.angle_to_coordinate(self.hx, self.hy, self.ex, self.ey)
            self.enemy.fire(angle + 180)

    def go_to_hero(self):
        """поиск пути к герою и движение к нему"""
        ex, ey, hx, hy = *self.enemy.rect.center, *self.hero.rect.center
        vert, hor = check_obstacle((ex, hy), (hx, hy)), check_obstacle((hx, ey), (hx, hy))
        if not vert and not hor:
            return False
        searching = True
        delta = 0
        resxy = [(ex, ey), (ex, hy)]
        while searching:
            d = 64 * delta
            if vert and check_obstacle((ex, ey), (ex + d, hy)):
                resxy = [(ex, ey), (ex + d, hy)]
                break
            elif hor and check_obstacle((ex, ey), (hx, ey + d)):
                resxy = [(ex, ey), (hx, ey + d)]
                break
            elif vert and check_obstacle((ex, ey), (hx, ey - d)):
                resxy = [(ex, ey), (hx, ey - d)]
                break
            elif hor and check_obstacle((ex, ey), (ex - d, hy)):
                resxy = [(ex, ey), (ex - d, hy)]
                break
            delta += 1
            if delta > 3:
                return False
        self.enemy.waypoints.append((resxy[0][0], resxy[0][1]))
        self.enemy.waypoints.append((resxy[1][0], resxy[1][1]))
        return True
