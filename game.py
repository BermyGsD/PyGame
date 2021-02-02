import pygame
import keys
from sprites import *
from log import logging


def check_obstacle(x1, y1, x2, y2):  # TODO сделать метод определения наличия препятствия между двумя точками (Glepp to Pasha)
    return False


class Game:
    @logging
    def __init__(self, screen):
        self.all_sprites = pygame.sprite.Group()         # группа для всех спрайтов
        self.entities = pygame.sprite.Group()            # группа для сущностей
        self.obstacles = pygame.sprite.Group()           # группа для фоновых
        self.all_without_player = pygame.sprite.Group()  # группа для всего, кроме игрока

        # Должен быть способ сделать это без кучи почти не отличающихся групп. Но я не знаю, как (Pasha)
        self.running = True
        self.screen = screen
        self.background = BackGround(self.all_sprites, self.all_without_player)
        self.load_level()
        self.player = Player(self.all_sprites, self.entities, obstacles=self.obstacles, world=self.all_without_player)
        self.all_sprites.draw(self.screen)
        self.gui = GUI(self.screen, self.player)
        pygame.display.flip()

    @logging
    def load_level(self):
        from levels import test
        self.background.setup(test.GAME['BACKGROUND'])
        wall_image = test.GAME['WALL_IMAGE']
        for wall_coordinates in test.GAME['WALLS']:
            x, y = wall_coordinates
            Wall(self.obstacles, self.all_sprites, self.all_without_player, x=x, y=y, image=wall_image)


    def update(self):
        self.all_sprites.update()
        self.gui.update()
