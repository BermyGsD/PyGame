import pygame
import keys
from sprites import *
from log import logging
from constant import *


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


class Game:
    @logging
    def __init__(self, screen):
        self.all_sprites = ALL_SPRITES          # группа для всех спрайтов
        self.entities = ENTITIES                # группа для сущностей
        self.obstacles = OBSTACLES              # группа для фоновых
        self.all_without_player = WORLD         # группа для всего, кроме игрока

        # Должен быть способ сделать это без кучи почти не отличающихся групп. Но я не знаю, как (Pasha)
        self.running = True
        self.screen = screen
        self.background = BackGround()
        self.load_level()
        self.player = Player()
        self.all_sprites.draw(self.screen)
        self.gui = GUI(self.player)
        pygame.display.flip()

    @logging
    def load_level(self):
        from levels import test
        self.background.setup(test.GAME['BACKGROUND'])
        wall_image = test.GAME['WALL_IMAGE']
        tile_image = test.GAME['TILE_IMAGE']
        lvlmap = open(test.GAME['WALLS'])
        lvlmap = lvlmap.readlines()
        for i in range(len(lvlmap)):
            for j in range(len(lvlmap[i])):
                x, y = j * 64, i * 64
                a = lvlmap[i][j]
                if a == '#':
                    Wall(x=x, y=y, image=wall_image)
                elif a == '.':
                    pass
                elif a == '@':
                    pass
                elif a == '!':
                    print(x, y)
                    a = Enemy(x, y)
                    a.load_image(load_image(), angle=1)

    def update(self):
        ALL_SPRITES.update()
        self.gui.update()
