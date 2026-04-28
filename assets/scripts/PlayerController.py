from foxvoid import *
from typing import Optional


set_pixel_art_mode(True)


class PlayerController(Component):
    def __init__(self):
        super().__init__()
        self.speed = 400.0
        self.jump_force = -700.0

        # State tracker to remember which way the player is looking
        self.facing_right = True

        self._transform: Optional[Transform2d] = None
        self._rigidbody: Optional[RigidBody2d] = None
        self._animator: Optional[Animator2d] = None

    def start(self):
        Debug.log("PlayerController start sequence!")
        self._transform = self.game_object.get_component(Transform2d)
        self._rigidbody = self.game_object.get_component(RigidBody2d)
        self._animator = self.game_object.get_component(Animator2d)
        
    def update(self, delta_time: float):
        # Ensure all components are loaded before executing logic
        if self._transform is None or self._rigidbody is None or self._animator is None:
            return
        
        is_moving = False

        # Fetch the absolute world position, ignoring the hierarchy complexity
        global_pos = self._transform.get_global_position()

        # Handle movement and flip state in Global Space
        if Input.is_action_down("walk_right"):
            global_pos.x += self.speed * delta_time
            self.facing_right = True
            is_moving = True
            
        elif Input.is_action_down("walk_left"):
            global_pos.x -= self.speed * delta_time
            self.facing_right = False
            is_moving = True

        # If the player moved, we push the new global position back to the Engine.
        # The C++ Transform2d component will automatically do the reverse math 
        # to find the correct local position, even if the player is parented!
        if is_moving:
            self._transform.set_global_position(global_pos)

        # Handle jumping
        if Input.is_action_pressed("jump") and self._rigidbody.is_grounded:
            self._rigidbody.velocity.y = self.jump_force

        # Resolve animations based on current state
        if is_moving:
            if self.facing_right:
                self._animator.play("walk_right")
            else:
                self._animator.play("walk_left")
        else:
            if self.facing_right:
                self._animator.play("idle_right")
            else:
                self._animator.play("idle_left")

    def on_collision(self, collision: Collision2D):
        pass

    def on_animation_event(self, event_name: str):
        if event_name == "test":
            Debug.log("Test OK")
