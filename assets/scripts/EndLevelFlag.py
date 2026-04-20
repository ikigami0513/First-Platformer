from foxvoid import *
from PlayerController import PlayerController
from typing import Optional

class EndLevelFlag(Component):
    def __init__(self):
        super().__init__()
        self.is_level_finish = False

        # Animation settings
        self.tile_frame_a_id = 111
        self.tile_frame_b_id = 112
        self.animation_speed = 0.2  # Time in seconds between each frame

        # Internal state for animation
        self._animation_timer = 0.0
        self._is_frame_a = True

        self._tilemap: Optional[TileMap] = None

    def start(self):
        self._tilemap = self.game_object.get_component(TileMap)

    def update(self, delta_time: float):
        if self.is_level_finish:
            SceneManager.load_scene("assets/scenes/LevelSelectionScene.scene")
            return
        
        # Handle the tile animation
        if self._tilemap is not None:
            # Accumulate the elapsed time
            self._animation_timer += delta_time

            # When the timer exceeds the speed threshold, swap the frame
            if self._animation_timer >= self.animation_speed:
                # Reset the timer (subtracting keeps it more accurate than setting to 0)
                self._animation_timer -= self.animation_speed
                
                # Toggle the frame state
                self._is_frame_a = not self._is_frame_a
                
                # Determine which tile ID to use based on the current state
                current_tile_id = self.tile_frame_a_id if self._is_frame_a else self.tile_frame_b_id
                
                # Update the tile on layer 0 at grid coordinates (X: 0, Y: 0)
                self._tilemap.set_tile(0, 0, 0, current_tile_id)

    def on_collision(self, collision: Collision2D):
        if collision.other and collision.other.get_component(PlayerController) and not self.is_level_finish:
            self.is_level_finish = True
