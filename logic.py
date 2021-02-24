"""Поведение ботов и стрельба (наверное)"""
from game import check_obstacle


class AI:
    def __init__(self, enemy, hero):
        self.enemy = enemy
        self.hero = hero

    def attack(self):
        """проверяется доступность героя и либо бот идет в комнату к герою и прячется в укрытие,
         либо шагает из-за него и стреляет"""
        can_see = check_obstacle(self.enemy.x, self.enemy.y, self.hero.x, self.hero.y)
        if not can_see:
            self.go_to_hero()
        angle = self.enemy.angle_to_coordinate()
        self.enemy.fire(angle)

    def go_to_hero(self):
        """поиск пути к герою и движение к нему"""
        pass
