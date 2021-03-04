import pygame


FULLSCREEN = eval(open('fs.txt', 'r').read())

if FULLSCREEN:
    video = pygame.display.Info()
    SIZE = video.current_w, video.current_h
    SCREEN = pygame.display.set_mode(flags=pygame.FULLSCREEN)
else:
    SIZE = 800, 600
    SCREEN = pygame.display.set_mode(SIZE)

PLAYER_COORDINATES = SIZE[0] // 2, SIZE[1] // 2


BACKGROUND = pygame.sprite.Group()      # группа для пола
ALL_SPRITES = pygame.sprite.Group()     # группа для всех спрайтов
ENTITIES = pygame.sprite.Group()        # группа для сущностей
OBSTACLES = pygame.sprite.Group()       # группа для фоновых
WORLD = pygame.sprite.Group()           # группа для всего, кроме игрока
PLAYER = pygame.sprite.Group()          # группа для игрока
ENEMIES = []                            # список врагов

LEVEL_MAP = None                        # Изменяемая "константа" для карты уровня

SOUND_PISTOL_SHOOT = pygame.mixer.Sound(file='sounds\\bang_08.ogg')
SOUND_MACHINE_GUN = pygame.mixer.Sound(file='sounds\\bang_06.ogg')
