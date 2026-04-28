from foxvoid import *

class Item(ScriptableObject):
    def __init__(self):
        super().__init__()
        self.item_name = "ItemName"
        self.damage: int = 0
