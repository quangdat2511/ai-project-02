import random
from typing import Tuple
from .types import *

class Cell:
    def __init__(self, has_pit: bool = False, has_wumpus: bool = False, has_gold: bool = False):
        self.has_pit = has_pit
        self.has_wumpus = has_wumpus
        self.has_gold = has_gold

    def is_safe(self) -> bool:
        return not (self.has_pit or self.has_wumpus)

class Environment:
    def __init__(self, N: int = 8, K: int = 2, p: float = 0.2, advanced_mode: bool = False):
        self.N = N
        self.K = K
        self.p = p

        # for advanced mode
        self.advanced_mode = advanced_mode
        self.action_count = 0
        self.wumpus_move_interval = 5

        self.grid = [[Cell() for _ in range(N)] for _ in range(N)]

        self.initialize_environment()

    def initialize_environment(self):
        # Logic to initialize the environment with pits, wumpus, and gold
        count = 0
        # Create Wumpus in random
        while count < self.K:
            x, y = random.randint(0, self.N - 1), random.randint(0, self.N - 1)
            if (x, y) != (0, 0) and not self.grid[x][y].has_wumpus:
                self.grid[x][y].has_wumpus = True
                count += 1

        # Create pits
        pit_count = int(self.N * self.N * 0.2)
        placed_bit = 0
        all_position = [(x, y) for x in range(self.N) for y in range(self.N) if (x, y) != (0, 0) and not self.grid[x][y].has_wumpus]
        random.shuffle(all_position)

        for pos in all_position:
            if placed_bit >= pit_count:
                break
            x, y = pos
            self.grid[x][y].has_pit = True
            placed_bit += 1
        
        # Create Gold
        while True:
            x, y, = random.randint(0, self.N - 1), random.randint(0, self.N - 1)
            if (x, y) != (0, 0) and not self.grid[x][y].has_pit and not self.grid[x][y].has_wumpus:
                self.grid[x][y].has_gold = True
                break

    def perform_action(self, position: Tuple[int, int], direction: Direction, action: Action) -> Percept:
        x, y = position
        dx, dy = direction.value
        if action == Action.FORWARD:
            # Move the agent forward
            new_position = (x + dx, y + dy)
            return self.get_percept_in_cell(new_position)

        if action == Action.GRAB:
            self.grid[x][y].has_gold = False  # Agent grabs gold
            return self.get_percept_in_cell(position)

        percept = self.get_percept_in_cell(position)
        if action == Action.SHOOT:
            percept = self.get_percept_in_cell(position)
            for step in range(1, self.N):
                target_x, target_y = x + dx * step, y + dy * step
                if not self._valid(target_x, target_y):
                    break
                if self.grid[target_x][target_y].has_wumpus:
                    self.grid[target_x][target_y].has_wumpus = False
                    percept = self.get_percept_in_cell(position)
                    percept.scream = True
                    return percept  # Wumpus killed
            return percept

        return percept

    def get_percept_in_cell(self, position: Tuple[int, int]) -> Percept:
        x, y = position
        if not self._valid(x, y):
            return Percept(bump=True)

        cell = self.grid[x][y]
        neighbors = self._neighbors(x, y)
        percept = Percept(
            stench=any(self.grid[nx][ny].has_wumpus for nx, ny in neighbors),
            breeze=any(self.grid[nx][ny].has_pit for nx, ny in neighbors),
            glitter=cell.has_gold
        )
        return percept

    def is_agent_dead(self, position: Tuple[int, int]) -> bool:
        x, y = position
        return (self.grid[x][y].has_pit or self.grid[x][y].has_wumpus)

    def _valid(self, x: int, y: int) -> bool:
        return 0 <= x < self.N and 0 <= y < self.N
    
    def _neighbors(self, x: int, y: int) -> list:
        neighbors = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if self._valid(nx, ny):
                neighbors.append((nx, ny))
        return neighbors

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
    
    def initialize_from_map(self, map_data: list[list[str]]):
        """
        Khởi tạo map từ dữ liệu truyền vào (map_data là list 2D).
        Kích thước map sẽ được set lại theo dữ liệu này.
        """
        self.N = len(map_data)
        self.grid = [[Cell() for _ in range(self.N)] for _ in range(self.N)]

        for y in range(self.N):
            for x in range(self.N):
                symbol = map_data[y][x]
                if symbol == "W":
                    self.grid[x][y].has_wumpus = True
                elif symbol == "P":
                    self.grid[x][y].has_pit = True
                elif symbol == "G":
                    self.grid[x][y].has_gold = True
                # "." thì giữ nguyên mặc định (ô trống)

        # Đếm lại số Wumpus
        self.K = sum(cell.has_wumpus for row in self.grid for cell in row)