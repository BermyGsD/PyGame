import pygame
import os
pygame.init()

from game import Game
import keys
from constant import *
from gui import *
pygame.mixer.init()


if __name__ == '__main__':
    pygame.display.flip()
    game = Game(SCREEN)

    # Event'ы и всё связанное с ними
    FPS = 16    # Миллисекунд между обновлениями

    UPDATE_SCREEN_EVENT = pygame.USEREVENT + 1  # Эвент обновление экрана
    pygame.time.set_timer(UPDATE_SCREEN_EVENT, FPS)
    UPDATE_GAME_EVENT = pygame.USEREVENT + 2    # Эвент обновления игры

    update_screen = False  # Обновление изображения в следующей итерации
    update_game = False    # Обновление игры в следующей итерации
    pause = True           # Внезапно, пауза
    show_settings = False  # Внезапно, отображение настроек
    game_over = False      # Триггер конца игры
    menu = Menu()
    # pygame.mouse.set_visible(False)

    while game.running:
        for event in pygame.event.get():
            e_type = event.type

            if e_type == pygame.QUIT:
                exit(0)

            if pause:
                if e_type == pygame.MOUSEBUTTONDOWN:
                    button_main = menu.check(event.pos)
                    button_restart = game.gui.check(event.pos)
                    if button_main:
                        if button_main == 'PLAY':
                            pause = False
                        elif button_main == 'QUIT':
                            exit(0)
                        elif button_main == 'SETTINGS':
                            show_settings = True
                        elif button_main == 'BACK':
                            show_settings = False
                        elif button_main == 'NOT FULLSCREEN':
                            open('fs.txt', 'w').write('True')
                        elif button_main == 'FULLSCREEN':
                            open('fs.txt', 'w').write('False')
                    if button_restart:
                        if button_restart == 'RESTART':
                            for i in OBSTACLES.sprites():
                                i.kill()
                            for i in ENEMIES:
                                i.kill()
                            update_screen = False
                            update_game = False
                            pause = True
                            show_settings = False
                            game_over = False
                            game.start(SCREEN)
            if e_type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause = not pause

            elif e_type == UPDATE_SCREEN_EVENT:
                update_screen = True

            elif e_type == UPDATE_GAME_EVENT:
                update_game = True

        if len(ENTITIES) == 0 or game.player.hp <= 0:
            game_over = True
            pause = True

        if update_screen:
            SCREEN.fill((255, 255, 255))
            if not pause and not game_over:
                ALL_SPRITES.update()
                ALL_SPRITES.draw(SCREEN)
                PLAYER.draw(SCREEN)
                game.gui.update()
            else:
                if not game_over:
                    if not show_settings:
                        menu.show_pause()
                    if show_settings:
                        menu.show_settings()
                else:
                    game.gui.show_game_over()
            pygame.display.flip()
            update_screen = False
