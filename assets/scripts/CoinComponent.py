from foxvoid import *
from PlayerController import PlayerController

class CoinComponent(Component):
    def __init__(self):
        super().__init__()
        self.score_to_add = 100

    def start(self):
        pass

    def update(self, delta_time: float):
        pass

    def on_collision(self, collision: Collision2D):
        if collision.other and collision.other.get_component(PlayerController):
            current_score = Globals.get_int("score")
            Globals.set_int("score", current_score + self.score_to_add)
            self.game_object.destroy()
