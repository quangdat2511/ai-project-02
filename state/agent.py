from state.logic import *
from enum import Enum
from dataclasses import dataclass
from typing import Optional

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
    def __init__(self, s: bool, b: bool):
        self.stench = s
        self.breeze = b
        glitter: bool = False
        bump: bool = False
        scream: bool = False

class Agent:
    def __init__(self, N: int):
        self.position = (0, 0)
        self.direction = Direction.EAST
        self.has_gold = False
        self.has_arrow = True
        self.is_alive = True
        self.kb = KnowledgeBase()
        self.score = 0
        self.size = N

        self.visited = set()

    def get_action(self, percept: Percept) -> Optional[Action]:
        pass
    
    def add_percept(self, percept: Percept, x, y):
        # if percept.breeze:
        #     percept_literal = Literal("Breeze", x, y, False)
        #     self.kb.add_clause(Clause([percept_literal]))
        # elif percept.stench:
        #     percept_literal = Literal("Stench", x, y, False)
        #     self.kb.add_clause(Clause([percept_literal]))
        self._add_breeze_axioms(x, y, percept.breeze)
        self._add_stench_axioms(x, y, percept.stench)
        # self.kb.simplify()

    def _add_breeze_axioms(self, x, y, value):
        """Breeze ⇔ có Pit ở ô kề"""
        neighbors = self._neighbors(x,y)
        b = Literal("Breeze", x, y, False)
        pits = [Literal("Pit", nx, ny, False) for (nx,ny) in neighbors]
        if value:
            # Breeze(x,y) => (P1 v P2 v ...)
            clause = Clause(pits)
            self.kb.add_clause(clause)
            # Mỗi Pit => Breeze
            # for p in pits:
            #     self.kb.add_clause(Clause([ -p, b ]))
        else:
            # NOT Breeze => tất cả các Pit kề đều False
            for p in pits:
                self.kb.add_clause(Clause([ -p ]))
        
    def _add_stench_axioms(self, x, y, value):
        """Stench ⇔ có Wumpus ở ô kề"""
        neighbors = self._neighbors(x,y)
        s = Literal("Stench", x, y, False)
        wumps = [Literal("Wumpus", nx, ny, False) for (nx,ny) in neighbors]
        if value:
            # Stench => (W1 v W2 v ...)
            clause = Clause(wumps)
            self.kb.add_clause(clause)
            # Mỗi Wumpus => Stench
            # for w in wumps:
            #     self.kb.add_clause(Clause([ -w, s ]))
        else:
            # NOT Stench => tất cả Wumpus kề đều False
            for w in wumps:
                self.kb.add_clause(Clause([ -w ]))
    
    def _valid(self, nx, ny):
        return 0 <= nx < self.size and 0 <= ny < self.size

    def _neighbors(self, x, y):
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx, ny = x + dx, y + dy
            if self._valid(nx, ny):
                yield (nx, ny)