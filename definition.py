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


class Literal:
    def __init__(self, name, x, y, negated):
        self.name = name
        self.position = (x, y)   # ví dụ ('1','2')
        self.is_negated = negated

    # def __repr__(self):
    #     prefix = '¬' if self.is_negated else ''
    #     args_str = ",".join(map(str, self.args))
    #     return f"{prefix}{self.name}({args_str})"
    
    def __str__(self):
        s = f"{self.name}{self.position}" if self.position else self.name
        return f"~{s}" if self.is_negated else s

    def __neg__(self):
        return Literal(self.name, self.position[0], self.position[1], not self.is_negated)

    def __eq__(self, other):
        return (self.name, self.position, self.is_negated) == (other.name, self.position, other.is_negated)

    def __hash__(self):
        return hash((self.name, self.position, self.is_negated))

class Clause:
    def __init__(self, literals):
        self.literals = set(literals)

    # def __repr__(self):
    #     return " ∨ ".join(map(str, self.literals))
    
    def __str__(self):
        return " v ".join(str(lit) for lit in self.literals)
    
    def is_empty(self):
        return len(self.literals) == 0
    
    def __eq__(self, other):
        return isinstance(other, Clause) and self.literals == other.literals
    
    def __hash__(self):
        return hash(frozenset(self.literals))

class KnowledgeBase:
    def __init__(self):
        self.clauses = set()

    def simplify_clause(self, clause):
        unit_literals = {next(iter(c.literals)) for c in self.clauses if len(c.literals) == 1}
        new_literals = set()

        for lit in clause.literals:
            if -lit in unit_literals:
                continue  # loại literal mâu thuẫn với fact
            else:
                new_literals.add(lit)

        if new_literals:
            return Clause(new_literals)
        else:
            return None 

    def add_clause(self, clause):
        # self.clauses.add(clause)
        simplified_clause = self.simplify_clause(clause)
        if simplified_clause:
            self.clauses.add(simplified_clause)

    def infer(self, query):
        negated_query = Clause([-query])
        new_clauses = set()
        kb_clauses = set(self.clauses.union({negated_query}))
        while True:
            pairs = [ (c1, c2) for c1 in kb_clauses for c2 in kb_clauses if c1 != c2 
                     and next(iter(c1.literals)).name == next(iter(c2.literals)).name]
            for (ci, cj) in pairs:
                # print(ci)
                # print(cj)
                # print()
                resolvents = self.resolve(ci, cj)
                for res in resolvents:
                    if res.is_empty():
                        return True  # derived empty clause, proven
                    new_clauses.add(res)
            if new_clauses.issubset(kb_clauses):
                return False  # no progress
            kb_clauses |= new_clauses
        pass  # Logic to infer knowledge from rules

    def resolve(self, c1, c2):
        resolvents = set()
        for l1 in c1.literals:
            for l2 in c2.literals:
                if l1.name == l2.name and l1.position == l2.position and l1.is_negated != l2.is_negated:
                    new_literals = (c1.literals.union(c2.literals)) - {l1, l2}
                    resolvents.add(Clause(new_literals))
        return resolvents

    # def simplify(self):
    #     simplified = set()
    #     unit_literals = set()

    #     # 1. Thu thập các facts
    #     for clause in self.clauses:
    #         if len(clause.literals) == 1:
    #             unit_literals.add(next(iter(clause.literals)))
    #             simplified.add(clause)

    #     # 2. Duyệt các clause còn lại
    #     for clause in self.clauses:
    #         if len(clause.literals) == 1:
    #             continue  # đã xử lý rồi

    #         new_literals = set()
    #         for lit in clause.literals:
    #             if -lit in unit_literals:
    #                 continue  # literal bị phủ định → loại bỏ
    #             else:
    #                 new_literals.add(lit)

    #         if new_literals:
    #             simplified.add(Clause(new_literals))

    #     self.clauses = simplified
