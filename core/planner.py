import heapq
from typing import List, Tuple, Set, Callable
from .logic import *

class Planner:
    def __init__(self, data: InferenceEngine, neighbors_fn: Callable[[Tuple[int, int]], List[Tuple[int, int]]]):
        self.data = data
        self._neighbors = neighbors_fn

    def heuristic(self, a: Tuple[int, int], b: Tuple[int, int]) -> int:
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def reconstruct_path(self, came_from, start, goal):
        path = []
        current = goal
        while current != start:
            pos, _ = current
            path.append(pos)
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
        if self.data.infer(Literal("Pit", x, y, False)) or self.data.infer(Literal("Wumpus", x, y, False)):
            return float('inf')

        # has pit
        if not self.data.infer(-Literal("Pit", x, y, False)):
            score += 1000
        # has wumpus
        if not self.data.infer(-Literal("Wumpus", x, y, False)):
            score += 1000

        return score

    def utility_score(self, pos: Tuple[int, int], visited: Set[Tuple[int, int]], current_pos: Tuple[int, int]) -> float:
        # if visited befofe, no utility
        if pos == current_pos:
            return 0
        if pos in visited:
            return 0
        # High risk high reward
        return 1

    def a_star(self, start: Tuple[int, int], goal: Tuple[int, int], visited: Set[Tuple[int, int]], start_dir: Direction) -> List[Tuple[int, int]]:
        frontier = []
        counter = 0
        start_state = (start, start_dir)
        heapq.heappush(frontier, (0, counter, start_state))
        counter += 1
        came_from = {start_state: None}
        cost_so_far = {start_state: 0}

        closest_state = start_state
        closest_dist = self.heuristic(start, goal)

        while frontier:
            _, _, current_state = heapq.heappop(frontier)
            current_pos, current_dir = current_state

            dist_to_goal = self.heuristic(current_pos, goal)
            if dist_to_goal < closest_dist:
                closest_state = current_state
                closest_dist = dist_to_goal

            if current_pos == goal:
                return self.reconstruct_path(came_from, start_state, current_state)

            for next_pos in self._neighbors(current_pos):
                # Tìm hướng mới
                dx, dy = next_pos[0] - current_pos[0], next_pos[1] - current_pos[1]
                for d in Direction:
                    if d.value == (dx, dy):
                        new_dir = d
                        break

                # Tính chi phí quay
                turn_cost = 0
                if new_dir != current_dir:
                    if new_dir == current_dir.turn_left() or new_dir == current_dir.turn_right():
                        turn_cost = 1
                    else:
                        turn_cost = 2

                base_cost = 1
                risk_penalty = self.risk_score(next_pos)
                if risk_penalty == float('inf'):
                    continue
                utility_bonus = self.utility_score(next_pos, visited, start)

                new_cost = cost_so_far[current_state] + base_cost + turn_cost + risk_penalty - utility_bonus
                next_state = (next_pos, new_dir)

                if next_state not in cost_so_far or new_cost < cost_so_far[next_state]:
                    cost_so_far[next_state] = new_cost
                    priority = new_cost + self.heuristic(next_pos, goal)
                    heapq.heappush(frontier, (priority, counter, next_state))
                    counter += 1
                    came_from[next_state] = current_state

        # Không tìm được đường đến goal, trả về đường đến trạng thái gần goal nhất
        return self.reconstruct_path(came_from, start_state, closest_state)
