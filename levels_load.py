from os import listdir
from os import path
from random import choice


class LevelLoader:
    def __init__(self, directions):
        self.directions = directions

    def get_path(self, level_name):
        if level_name in self.directions:
            return {
                'BACKGROUND': path.normpath(f'levels/{level_name}/back.png'),
                'WALL':       path.normpath(f'images/environment/wall_1.png'),
                'MAP':        path.normpath(f'levels/{level_name}/map.txt')
            }
        else:
            raise ValueError

    def get_random_level(self):
        return self.get_path(choice(self.directions))


LEVEL_LOADER = LevelLoader(directions=listdir('levels'))
