from foxvoid import *
from typing import Optional

class ScoreComponent(Component):
    def __init__(self):
        super().__init__()
        self._text_renderer: Optional[TextRenderer] = None

    def start(self):
        self._text_renderer = self.game_object.get_component(TextRenderer)

    def update(self, delta_time: float):
        if self._text_renderer is not None:
            current_score = Globals.get_int("score")
            self._text_renderer.text = f"Score: {current_score}"
