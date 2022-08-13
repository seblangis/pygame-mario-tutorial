from mario.game_data import levels
from overworld.game_data import levels as overworld_levels
from mario.level import Level
from overworld.overworld import Overworld


class Game:

    def __init__(self, surface):
        self.surface = surface
        self.overworld = Overworld(0, 0, surface, self.select_level)

        self.level = None

    def select_level(self, index):
        self.level = Level(levels[index], self.surface, self.quit_level)

    def quit_level(self, success):
        if success:
            self.overworld.max_level = overworld_levels[self.overworld.current_level]['unlock']

        self.level = None
        self.overworld.reset_cooldown()

    def run(self):
        if self.level:
            self.level.run()
        else:
            self.overworld.run()
