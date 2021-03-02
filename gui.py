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
        self.fs = FULLSCREEN
        self.size = SIZE

    def show_pause(self):
        self.buttons = []
        font = pygame.font.Font(None, 50)
        lst = ["PLAY", "SCORE", "SETTINGS", "QUIT"]
        lst1 = []
        for i in range(len(lst)):
            text = font.render(lst[i], True, (255, 255, 255))
            lst1.append(text)
        for i in range(len(lst1)):
            text = lst1[i]
            text_x = self.size[0] // 2 - text.get_width() // 2
            text_y = self.size[1] // 4 + i * self.size[1] // (len(lst1) * 2) - text.get_height()
            text_w = text.get_width()
            text_h = text.get_height()
            pygame.draw.rect(SCREEN, (0, 0, 0), (text_x - 10, text_y - 10,
                                                 text_w + 20, text_h + 20))
            self.buttons.append([(text_x - 10, text_y - 10, text_w + 20, text_h + 20), lst[i]])
            SCREEN.blit(text, (text_x, text_y))

    def show_settings(self):
        self.buttons = []
        font = pygame.font.Font(None, 50)
        if self.fs:
            lst = ["FULLSCREEN", "BACK"]
        else:
            lst = ["NOT FULLSCREEN", "BACK"]
        lst1 = []
        for i in range(len(lst)):
            text = font.render(lst[i], True, (255, 255, 255))
            lst1.append(text)
        for i in range(len(lst1)):
            text = lst1[i]
            text_x = self.size[0] // 2 - text.get_width() // 2
            text_y = self.size[1] // 4 + i * self.size[1] // (len(lst1) * 2) - text.get_height()
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
