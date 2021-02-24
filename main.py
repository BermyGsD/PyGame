import pygame
from game import Game
import keys
from constant import *
pygame.init()
pygame.mixer.init()


if __name__ == '__main__':
    pygame.display.flip()
    game = Game(SCREEN)

    # Event'ы и всё связанное с ними
    FPS = 16    # Миллисекунд между обновлениями
    SPEED = 16  # Время между тиками игры (тоже миллисекунды)

    UPDATE_SCREEN_EVENT = pygame.USEREVENT + 1  # Эвент обновление экрана
    pygame.time.set_timer(UPDATE_SCREEN_EVENT, FPS)
    UPDATE_GAME_EVENT = pygame.USEREVENT + 2    # Эвент обновления игры
    pygame.time.set_timer(UPDATE_GAME_EVENT, SPEED)

    update_screen = False  # Обновление изображения в следующей итерации
    update_game = False    # Обновление игры в следующей итерации
    pause = False          # Внезапно, пауза
    # pygame.mouse.set_visible(False)

    while game.running:
        for event in pygame.event.get():
            e_type = event.type

            if e_type == pygame.QUIT:
                exit(0)

            if e_type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause = not pause

            elif e_type == UPDATE_SCREEN_EVENT:
                update_screen = True

            elif e_type == UPDATE_GAME_EVENT:
                update_game = True

        if update_screen:
            if not pause:
                ALL_SPRITES.update()
                SCREEN.fill((0, 0, 0))
                ALL_SPRITES.draw(SCREEN)
                PLAYER.draw(SCREEN)
                game.gui.update()
            else:
                game.gui.create_menu()
            pygame.display.flip()
            update_screen = False

        """if update_game:
            game.update()
            update_game = False"""
