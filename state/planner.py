from state.agent import *
from state.logic import *
from typing import Tuple, List
from queue import PriorityQueue

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