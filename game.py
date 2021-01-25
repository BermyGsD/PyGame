import pygame
import test
import keys
from sprites import *
from log import logging


def check_obstacle(x1, y1, x2, y2):  # TODO сделать метод определения наличия препятствия между двумя точками (Glepp to Pasha)
    return False


class Game:
    @logging
    def __init__(self, screen):
        self.stack = set()                               # set с int-овыми pygame.K_%Name%
        self.all_sprites = pygame.sprite.Group()         # группа для всех спрайтов
        self.all_objects = pygame.sprite.Group()         # группа для всех объектов(за исключением фоновых)
        self.background_sprites = pygame.sprite.Group()  # группа для фоновых
        self.all_without_player = pygame.sprite.Group()  # группа для всего, кроме игрока

        # Должен быть способ сделать это без кучи почти не отличающихся групп. Но я не знаю, как (Pasha)
        self.running = True
        self.screen = screen
        self.background = BackGround(self.all_sprites, self.all_without_player)
        self.__load_level()
        self.player = Player(self.all_sprites, world=self.all_without_player)
        self.all_sprites.draw(self.screen)
        pygame.display.flip()

    @logging
    def __load_level(self):
        self.background.setup('levels/test/back.png')
        self.all_sprites.draw(self.screen)

    #@logging
    def update(self):
        for event in self.stack:
            pass
        self.all_sprites.update()

    #@logging
    def add_to_stack(self, action) -> None:
        self.stack.add(action)
        if action in keys.player_keys:
            self.player.add_to_stack(action)
