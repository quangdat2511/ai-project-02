import random
from state.agent import *

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
        # Logic to initialize the world with pits, wumpus, and gold
        count = 0
        # Create Wumpus in random
        while count < self.K:
            x, y = random.randint(0, self.N - 1), random.randint(0, self.N - 1)
            if (x, y) != (0, 0) and not self.grid[x][y].has_wumpus:
                self.grid[x][y].has_wumpus = True
                count += 1

        # Create pits
        for x in range(self.N):
            for y in range(self.N):
                if (x, y) != (0, 0) and not self.grid[x][y].has_wumpus:
                    if random.random() < self.p:
                        self.grid[x][y].has_pit = True

        # Create Gold
        while True:
            x, y, = random.randint(0, self.N - 1), random.randint(0, self.N - 1)
            if (x, y) != (0, 0) and not self.grid[x][y].has_pit and not self.grid[x][y].has_wumpus:
                self.grid[x][y].has_gold = True
                break

    def perform_action(self, agent: Agent, action: Action) -> Percept:
        pass
    
    def __str__(self):
        result = ""
        for y in reversed(range(self.N)):  # từ trên xuống dưới
            for x in range(self.N):
                cell = self.grid[x][y]
                content = "."
                if cell.has_wumpus:
                    content = "W"
                elif cell.has_pit:
                    content = "P"
                elif cell.has_gold:
                    content = "G"
                result += f"{content} "
            result += "\n"
        result += "\n"
        return result
    
    def display_with_agent(self, agent: Agent):
        result = ""
        for y in reversed(range(self.N)):
            for x in range(self.N):
                if (x, y) == agent.position:
                    result += "A "  # Agent's current position
                else:
                    cell = self.grid[x][y]
                    if cell.has_wumpus:
                        result += "W "
                    elif cell.has_pit:
                        result += "P "
                    elif cell.has_gold:
                        result += "G "
                    else:
                        result += ". "
            result += "\n"
        print(result)