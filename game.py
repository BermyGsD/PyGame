from sprites import *
from log import logging
from constant import *
from gui import GUI
from levels_load import LEVEL_LOADER


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
        self.running = True
        self.screen = screen
        self.background = BackGround()
        self.player = Player()
        self.load_level()
        ALL_SPRITES.draw(self.screen)
        self.gui = GUI(self.player)
        pygame.display.flip()

    @logging
    def load_level(self):
        level = LEVEL_LOADER.get_random_level()
        self.background.setup(level['BACKGROUND'])
        wall_image = level['WALL']
        level_map = level['MAP']
        # tile_image = levels.GAME['TILE_IMAGE']
        with open(level_map) as file:
            lvl_map = file.readlines()
        player_coordinates = 100, 100
        LEVEL_MAP = lvl_map
        for i in range(len(lvl_map)):
            for j in range(len(lvl_map[i])):
                x, y = j * 64, i * 64
                a = lvl_map[i][j]
                if a == '.':
                    pass
                elif a == '#':
                    Wall(x=x, y=y, image=wall_image)
                elif a == '@':
                    x_add = - 32 + PLAYER_COORDINATES[0]
                    y_add = - 32 + PLAYER_COORDINATES[1]
                    player_coordinates = -x + x_add, -y + y_add
                elif a == '!':
                    f = Enemy(x, y)
                    f.load_image(load_image(name=Enemy.IMAGES_1[0]))
                else:
                    pass
        print(player_coordinates)
        for sprite in WORLD.sprites():
            sprite.move(*player_coordinates)

    def update(self):
        ALL_SPRITES.update()
        self.gui.update()
