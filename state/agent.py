from typing import Tuple, List, Optional
from queue import PriorityQueue
from .types import *
from .logic import *
from .environment import *

class Agent:
    def __init__(self, N: int):
        self.position = (0, 0)
        self.direction = Direction.EAST
        self.has_gold = False
        self.has_arrow = True
        self.is_alive = True
        self.kb = KnowledgeBase()
        self.planner = Planner(self)
        self.score = 0
        self.size = N

        self.visited = set()

    def get_action(self, percept: Percept) -> Optional[Action]:
        pass
    
    def add_percept(self, percept: Percept, x, y):
        self._add_breeze_axioms(x, y, percept.breeze)
        self._add_stench_axioms(x, y, percept.stench)

    def _add_breeze_axioms(self, x, y, value):
        """Breeze ⇔ có Pit ở ô kề"""
        neighbors = self._neighbors(x,y)
        b = Literal("Breeze", x, y)
        pits = [Literal("Pit", nx, ny) for (nx,ny) in neighbors]
        if value:
            # Breeze(x,y) => (P1 v P2 v ...)
            clause = Clause(pits)
            self.kb.add_clause(Clause([b]))
            self.kb.add_clause(Clause([-b]) | clause)
        else:
            # NOT Breeze => tất cả các Pit kề đều False
            self.kb.add_clause(Clause([-b]))
            for p in pits:
                self.kb.add_clause(Clause([b]) | Clause([-p]))
        
    def _add_stench_axioms(self, x, y, value):
        """Stench ⇔ có Wumpus ở ô kề"""
        neighbors = self._neighbors(x,y)
        s = Literal("Stench", x, y)
        wumps = [Literal("Wumpus", nx, ny, False) for (nx,ny) in neighbors]
        if value:
            # Stench => (W1 v W2 v ...)
            clause = Clause(wumps)
            self.kb.add_clause(Clause([s]))
            self.kb.add_clause(Clause([-s]) | clause)
        else:
            # NOT Stench => tất cả Wumpus kề đều False
            self.kb.add_clause(Clause([-s]))
            for w in wumps:
                self.kb.add_clause(Clause([s]) | Clause([-w]))
    
    def _valid(self, nx, ny):
        return 0 <= nx < self.size and 0 <= ny < self.size

    def _neighbors(self, x, y):
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx, ny = x + dx, y + dy
            if self._valid(nx, ny):
                yield (nx, ny)

    def play(self, environment: Environment):
        pass


class Planner:
    def __init__(self, agent: Agent):
        self.agent = agent

    def heuristic(self, a: Tuple[int, int], b: Tuple[int, int]) -> int:
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def reconstruct_path(self, came_from, start, goal):
        path = []
        current = goal
        while current != start:
            path.append(current)
            if current not in came_from or came_from[current] is None:
                return []
            current = came_from[current]
        path.reverse()
        return path

    def risk_score(self, pos: Tuple[int, int]) -> float:
        """Tính điểm rủi ro dựa trên inference"""
        x, y = pos
        kb = self.agent.kb
        score = 0

        # Nếu chắc chắn có Pit/Wumpus => vô cực (không được đi)
        if kb.infer(Literal("Pit", x, y, False)) or kb.infer(Literal("Wumpus", x, y, False)):
            return float('inf')

        # Nếu chưa biết rõ (tức không thể suy ra an toàn) → penalty
        if not kb.infer(-Literal("Pit", x, y, False)):
            score += 3  # nguy cơ Pit

        if not kb.infer(-Literal("Wumpus", x, y, False)):
            score += 4  # nguy cơ Wumpus (cao hơn pit)

        return score  # 0 là an toàn tuyệt đối

    def utility_score(self, pos: Tuple[int, int]) -> float:
        """Giá trị mong đợi khi đến ô này (ví dụ: gần vàng)"""
        # Có thể mở rộng bằng inference: nếu xác suất có vàng cao thì + điểm
        if pos == self.agent.position:
            return 0
        if pos in self.agent.visited:
            return 0
        return 1  # tạm thời coi khám phá là tốt

    def a_star(self, start: Tuple[int, int], goal: Tuple[int, int]) -> List[Tuple[int, int]]:
        frontier = PriorityQueue()
        frontier.put((0, start))
        came_from = {start: None}
        cost_so_far = {start: 0}

        while not frontier.empty():
            _, current = frontier.get()

            if current == goal:
                break

            for next_pos in self.agent._neighbors(*current):
                base_cost = 1
                risk_penalty = self.risk_score(next_pos)  # càng nguy hiểm càng cao
                utility_bonus = self.utility_score(next_pos)  # càng hấp dẫn càng tốt

                if risk_penalty == float('inf'):
                    continue  # không đi vào ô chết chắc

                new_cost = cost_so_far[current] + base_cost + risk_penalty - utility_bonus

                if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:
                    cost_so_far[next_pos] = new_cost
                    priority = new_cost + self.heuristic(next_pos, goal)
                    frontier.put((priority, next_pos))
                    came_from[next_pos] = current

        return self.reconstruct_path(came_from, start, goal)