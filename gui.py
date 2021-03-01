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


class Menu:
    def __init__(self):
        self.buttons = []

    def show_pause(self):
        font = pygame.font.Font(None, 50)
        lst = ["PLAY", "SCORE", "SETTINGS", "QUIT"]
        lst1 = []
        for i in range(len(lst)):
            text = font.render(lst[i], True, (255, 255, 255))
            lst1.append(text)
        for i in range(len(lst1)):
            text = lst1[i]
            text_x = SIZE[0] // 2 - text.get_width() // 2
            text_y = SIZE[1] // 4 + i * SIZE[1] // (len(lst1) * 2) - text.get_height()
            text_w = text.get_width()
            text_h = text.get_height()
            pygame.draw.rect(SCREEN, (0, 0, 0), (text_x - 10, text_y - 10,
                                                 text_w + 20, text_h + 20))
            self.buttons.append([(text_x - 10, text_y - 10, text_w + 20, text_h + 20), lst[i]])
            SCREEN.blit(text, (text_x, text_y))

    def check(self, pos):
        x1, y1 = pos
        for i in self.buttons:
            x, y, w, h = i[0]
            name = i[1]
            if x1 - x > 0 and x1 - x - w < 0 and y1 - y > 0 and y1 - y - h < 0:
                return name