from typing import List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

class Direction(Enum):
    NORTH = (1, 0)
    EAST = (0, 1)
    SOUTH = (-1, 0)
    WEST = (0, -1)

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

class Agent:
    def __init__(self):
        self.position = (0, 0)
        self.direction = Direction.EAST
        self.has_gold = False
        self.has_arrow = True
        self.is_alive = True
        self.kb = KnowledgeBase()
        self.score = 0

    def get_action(self, percept: Percept) -> Optional[Action]:
        pass

class Cell:
    def __init__(self, has_pit: bool = False, has_wumpus: bool = False, has_gold: bool = False):
        self.has_pit = has_pit
        self.has_wumpus = has_wumpus
        self.has_gold = has_gold

    def is_safe(self) -> bool:
        return not (self.has_pit or self.has_wumpus)

class WumpusWorld:
    def __init__(self, N: int = 8, K: int = 2, p: float = 0.2, advanced_mode: bool = False):
        self.N = N
        self.K = K
        self.p = p

        # for advanced mode
        self.advanced_mode = advanced_mode
        self.action_count = 0
        self.wumpus_move_interval = 5

        self.grid = [[Cell() for _ in range(N)] for _ in range(N)]

        self.initialize_world()

    def initialize_world(self):
        pass  # Logic to initialize the world with pits, wumpus, and gold

    def perform_action(self, agent: Agent, action: Action) -> Percept:
        pass




class KnowledgeBase:
    def __init__(self):
        # Facts about cells (using sets for efficiency)
        self.visited = set()
        self.safe = {(0, 0)}  # Start is always safe
        self.has_pit = set()
        self.no_pit = {(0, 0)}
        self.has_wumpus = set()
        self.no_wumpus = {(0, 0)}
        
        # Percept history
        self.stench_at = set()
        self.breeze_at = set()
        self.no_stench_at = set()
        self.no_breeze_at = set()

    def infer(self):
        pass  # Logic to infer knowledge from rules
    