from constant import *


class GUI:
    def __init__(self, player):
        self.player = player
        self.screen = SCREEN

    def update(self):
        pygame.draw.rect(self.screen, (255, 0, 0), ((0, 0), (self.player.hp, 10)))
        font = pygame.font.Font(None, 20)
        text_x, text_y = 0, 20
        text = font.render(f"SCORE: {self.player.score}", True, (255, 255, 255))
        pygame.draw.rect(SCREEN, (0, 0, 0), (text_x, text_y - 10, text.get_width() + text_x, text.get_height() + text_y))
        SCREEN.blit(text, (text_x, text_y))


def show_pause():
    font = pygame.font.Font(None, 50)
    text = font.render("PAUSE", True, (255, 255, 255))
    text_x = SIZE[0] // 2 - text.get_width() // 2
    text_y = SIZE[1] - text.get_height()
    text_w = text.get_width()
    text_h = text.get_height()
    pygame.draw.rect(SCREEN, (0, 0, 0), (text_x - 10, text_y - 10,
                                           text_w + 20, text_h + 20))
    SCREEN.blit(text, (text_x, text_y))