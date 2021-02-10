import pygame


SIZE = 800, 600
SCREEN = pygame.display.set_mode((800, 600))

ALL_SPRITES = pygame.sprite.Group()     # группа для всех спрайтов
ENTITIES = pygame.sprite.Group()        # группа для сущностей
OBSTACLES = pygame.sprite.Group()       # группа для фоновых
WORLD = pygame.sprite.Group()           # группа для всего, кроме игрока