from enum import Enum
from dataclasses import dataclass

class Direction(Enum):
    # Up
    NORTH = (0, 1)
    # Right
    EAST = (1, 0)
    # Down
    SOUTH = (0, -1)
    # Left
    WEST = (-1, 0)

    def turn_left(self):
        dirs = [Direction.NORTH, Direction.WEST, Direction.SOUTH, Direction.EAST]
        return dirs[(dirs.index(self) + 1) % 4]
    
    def turn_right(self):
        dirs = [Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST]
        return dirs[(dirs.index(self) + 1) % 4]

class Action(Enum):
    FORWARD = "Forward"
    TURN_LEFT = "TurnLeft"
    TURN_RIGHT = "TurnRight"
    GRAB = "Grab"
    SHOOT = "Shoot"
    CLIMB = "Climb"

@dataclass
class Percept:
    stench: bool = False
    breeze: bool = False
    glitter: bool = False
    bump: bool = False
    scream: bool = False
    def __init__(self, stench: bool=False, breeze: bool=False, glitter: bool=False, bump: bool=False, scream: bool=False):
        self.stench = stench
        self.breeze = breeze
        self.glitter = glitter
        self.bump = bump
        self.scream = scream
