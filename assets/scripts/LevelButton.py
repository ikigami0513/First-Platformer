from foxvoid import *
from typing import Optional

class LevelButton(Component):
    def __init__(self):
        super().__init__()
        self._button: Optional[Button] = None
        self.level_scene_path = ""

    def start(self):
        self._button = self.game_object.get_component(Button)

    def update(self, delta_time: float):
        if self._button and self._button.is_clicked():
            Debug.log(f"button clicked for scene {self.level_scene_path}")
            SceneManager.load_scene(self.level_scene_path)
