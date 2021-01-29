import pygame

# Клавиши для игрока
player_keys = {
               'UP': pygame.K_w,
               'DOWN': pygame.K_s,
               'LEFT': pygame.K_a,
               'RIGHT': pygame.K_d,
               'RUN': pygame.K_LSHIFT
               }
player_keys_list = player_keys.values()

# клавиши для игры
game_keys = {
             'PAUSE': pygame.K_ESCAPE
             }
game_keys_list = game_keys.keys()
