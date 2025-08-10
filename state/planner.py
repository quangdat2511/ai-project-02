import heapq
from typing import List, Tuple, Set, Callable
from .logic import *

class Planner:
    def __init__(self, kb: KnowledgeBase, neighbors_fn: Callable[[Tuple[int, int]], List[Tuple[int, int]]]):
        self.kb = kb
        self._neighbors = neighbors_fn

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
        """Tính điểm rủi ro dựa trên KB"""
        x, y = pos
        score = 0

        # Definitely died
        if self.kb.infer(Literal("Pit", x, y, False)) or self.kb.infer(Literal("Wumpus", x, y, False)):
            return float('inf')

        # has pit
        if not self.kb.infer(-Literal("Pit", x, y, False)):
            score += 3
        # has wumpus
        if not self.kb.infer(-Literal("Wumpus", x, y, False)):
            score += 4

        return score

    def utility_score(self, pos: Tuple[int, int], visited: Set[Tuple[int, int]], current_pos: Tuple[int, int]) -> float:
        # if visited befofe, no utility
        if pos == current_pos:
            return 0
        if pos in visited:
            return 0
        # High risk high reward
        return 1

    def a_star(self, start: Tuple[int, int], goal: Tuple[int, int], visited: Set[Tuple[int, int]]) -> List[Tuple[int, int]]:
        frontier = []
        heapq.heappush(frontier, (0, start))
        came_from = {start: None}
        cost_so_far = {start: 0}

        while frontier:
            _, current = heapq.heappop(frontier)

            if current == goal:
                break

            for next_pos in self._neighbors(current):
                base_cost = 1
                risk_penalty = self.risk_score(next_pos) # High risk high reward (con bạc)
                utility_bonus = self.utility_score(next_pos, visited, start)

                if risk_penalty == float('inf'):
                    continue

                new_cost = cost_so_far[current] + base_cost + risk_penalty - utility_bonus

                if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:
                    cost_so_far[next_pos] = new_cost
                    priority = new_cost + self.heuristic(next_pos, goal)
                    heapq.heappush(frontier, (priority, next_pos))
                    came_from[next_pos] = current

        return self.reconstruct_path(came_from, start, goal)
