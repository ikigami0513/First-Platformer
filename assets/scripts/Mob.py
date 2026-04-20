from foxvoid import *
from PlayerController import PlayerController
from typing import Optional

class Mob(Component):
    def __init__(self):
        super().__init__()

        # Movement settings
        self.speed = 100.0
        self.direction = -1.0  # -1.0 moves lefts, 1.0 moves right

        self._rigidbody: Optional[RigidBody2d] = None
        self._transform: Optional[Transform2d] = None
        self._animator: Optional[Animator2d] = None

    def start(self):
        self._rigidbody = self.game_object.get_component(RigidBody2d)
        self._transform = self.game_object.get_component(Transform2d)
        self._animator = self.game_object.get_component(Animator2d)

        # Trigger the correct animation right when the mob spawns
        self._update_animation()

    def update(self, delta_time: float):
        if self._rigidbody is None:
            return
        
        # Apply horizontal movement
        self._rigidbody.velocity.x = self.speed * self.direction

    def on_collision(self, collision: Collision2D):
        # Handle interaction with the Player
        if collision.other and collision.other.get_component(PlayerController):
            # The player landed on top (Normal points up)
            if collision.normal.y > 0.5:
                player_rb = collision.other.get_component(RigidBody2d)
                if player_rb:
                    player_rb.velocity.y = -500.0  # Bounce effect

                self.game_object.destroy()
                return
            else:
                # The player touched the sides or the bottom!
                # TODO: Deal damage to the player or reload the scene here
                pass

        # Handle environmental collisions (Walls, other Mobs, TileMap)
        # If the normal is mostly horizontal, we hit on obstacle.
        if abs(collision.normal.x) > 0.5:
            # The normal vector points away from the surface we hit.
            if collision.normal.x > 0:
                self.direction = 1.0
            else:
                self.direction = -1.0

            # Tell the Animator to switch to the correct walking animation
            self._update_animation()

    def _update_animation(self):
        # Helpe method to keep the code DRY (Don't Repeat Yourself)
        if self._animator is not None:
            if self.direction == 1.0:
                self._animator.play("right")
            else:
                self._animator.play("left")
