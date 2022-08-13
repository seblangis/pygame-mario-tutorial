from overworld.overworld import Overworld


class Game:

    def __init__(self, surface):
        self.max_level = 2
        self.overworld = Overworld(0, self.max_level, surface)

    def run(self):
        self.overworld.run()
