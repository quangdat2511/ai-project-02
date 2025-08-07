from typing import Tuple, List, Optional
from queue import PriorityQueue
from .types import *
from .logic import *
from .environment import *

class Agent:
    def __init__(self):
        self.position = (0, 0)
        self.direction = Direction.EAST
        self.has_gold = False
        self.has_arrow = True
        self.is_alive = True
        self.kb = KnowledgeBase()
        self.planner = Planner(self)
        self.score = 0
        self.winning = False

        self.visited = set()
        self.action_count = 0  # Đếm số hành động đã thực hiện

    def get_actions(self, percept: Percept) -> List[Action]:
        actions = []
        if percept.glitter:
            actions.append(Action.GRAB)
            return actions  # ưu tiên lấy vàng
        
        if self.has_gold and self.position == (0, 0):
            actions.append(Action.CLIMB)
            return actions

        if self.has_gold:
            goal = (0, 0)  # nếu có vàng thì luôn hướng về góc trên bên trái
        else:
            safe_unvisited_pos = [pos for pos in self.kb.not_has_pit if pos in self.kb.not_has_wumpus and pos not in self.visited]
            print(f"Safe unvisited positions: {safe_unvisited_pos}")
            # goal is the closest unvisited cell that is safe
            if not safe_unvisited_pos:
                # random unvisited neighbor if no safe unvisited positions
                print("No safe unvisited positions, choosing a random neighbor.")
                neighbors = list(self._neighbors(*self.position))
                unvisited_neighbors = [pos for pos in neighbors if pos not in self.visited]
                goal = unvisited_neighbors[0] if unvisited_neighbors else None
                if goal is None:
                    print("No unvisited neighbors, staying put.")
                    # choose random neighbor to avoid getting stuck
                    goal = neighbors[0] if neighbors else None
            else:
                goal = min(safe_unvisited_pos, key=lambda pos: abs(pos[0] - self.position[0]) + abs(pos[1] - self.position[1]), default=None)

        print(f"Current position: {self.position}, Goal: {goal}")
        path = self.planner.a_star(start=self.position, goal=goal)
        next_pos = path[0] if len(path) > 0 else None

        # check making turns
        if next_pos:
            left_direction = self.direction.turn_left()
            right_direction = self.direction.turn_right()
            dx, dy = (next_pos[0] - self.position[0], next_pos[1] - self.position[1])
            if (dx, dy) == left_direction.value:
                actions.append(Action.TURN_LEFT)
            elif (dx, dy) == right_direction.value:
                actions.append(Action.TURN_RIGHT)
            elif (dx, dy) != self.direction.value:
                actions.append(Action.TURN_RIGHT)
                actions.append(Action.TURN_RIGHT)
        
        actions.append(Action.FORWARD)
        return actions
            
    def add_percept(self, percept: Percept, x, y):
        self._add_breeze_axioms(x, y, percept.breeze)
        self._add_stench_axioms(x, y, percept.stench)

    def _add_breeze_axioms(self, x, y, value):
        """Breeze ⇔ có Pit ở ô kề"""
        neighbors = self._neighbors(x,y)
        b = Literal("Breeze", x, y)
        pits = [Literal("Pit", nx, ny) for (nx,ny) in neighbors]
        self.kb.add_clause(Clause([-Literal("Pit", x, y)]))  # Thêm ô hiện tại là không có Pit
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
        self.kb.add_clause(Clause([-Literal("Wumpus", x, y)]))  # Thêm ô hiện tại là không có Wumpus
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
        return 0 <= nx and 0 <= ny
    
    def _neighbors(self, x, y):
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx, ny = x + dx, y + dy
            if self._valid(nx, ny):
                yield (nx, ny)

    def display(self, env: Environment):
        grid_str = ""
        N = env.N
        for y in reversed(range(N)):
            for x in range(N):
                if (x, y) == self.position:
                    grid_str += "A "  # Agent
                else:
                    c = env.grid[x][y]
                    if c.has_wumpus: grid_str += "W "
                    elif c.has_pit:  grid_str += "P "
                    elif c.has_gold: grid_str += "G "
                    else:             grid_str += ". "
            grid_str += "\n"
        print(grid_str)

    def perform_action(self, action: Action, environment: Environment) -> Percept:
        print(f"Performing action: {action.name} at position {self.position} facing {self.direction.name}")
        
        
        percept = environment.perform_action(self.position, self.direction, action)

        self.action_count += 1
        if self.action_count > 50:
            print("Too many actions, stopping the game.")
            self.is_alive = False
            return percept


        if action == Action.FORWARD:
            dx, dy = self.direction.value
            if not percept.bump:
                # Cập nhật vị trí
                self.position = (self.position[0] + dx, self.position[1] + dy)
            else:
                print("Bumped into a wall, cannot move forward.")
                self.visited.add((self.position[0] + dx, self.position[1] + dy))  # Đánh dấu ô hiện tại là đã thăm

            self.score -= 1  
        elif action == Action.TURN_LEFT:
            self.direction = self.direction.turn_left()
            self.score -= 1  # Quay trái mất điểm
        elif action == Action.TURN_RIGHT:
            self.direction = self.direction.turn_right()
            self.score -= 1  # Quay phải mất điểm
        elif action == Action.GRAB:
            self.has_gold = True
            self.score += 10
        elif action == Action.SHOOT:
            if self.has_arrow:
                self.has_arrow = False
                self.score -= 10  # Bắn mất mũi tên
        elif action == Action.CLIMB:
            if self.position == (0, 0) and self.has_gold:
                self.winning = True
                self.score += 1000

        self.is_alive = not environment.is_agent_dead(self.position)

        self.display(environment)

        return percept

    def play(self, environment: Environment):
        self.display(environment)

        percept = environment.get_percept_in_cell(self.position)
        while self.is_alive and not self.winning:
            if self.position not in self.visited:
                self.visited.add(self.position)
                self.add_percept(percept, *self.position)
                
                for neighbor in self._neighbors(*self.position):
                    if neighbor not in self.visited:
                        if self.kb.infer(Literal("Pit", *neighbor)):
                            self.kb.has_pit.add(neighbor)
                            self.kb.add_clause(Clause([Literal("Pit", *neighbor)]))
                        if self.kb.infer(Literal("Wumpus", *neighbor)):
                            self.kb.has_wumpus.add(neighbor)
                            self.kb.add_clause(Clause([Literal("Wumpus", *neighbor)]))
                        if self.kb.infer(-Literal("Pit", *neighbor)):
                            self.kb.not_has_pit.add(neighbor)
                            self.kb.add_clause(Clause([-Literal("Pit", *neighbor)]))
                        if self.kb.infer(-Literal("Wumpus", *neighbor)):
                            self.kb.not_has_wumpus.add(neighbor)
                            self.kb.add_clause(Clause([-Literal("Wumpus", *neighbor)]))

            actions = self.get_actions(percept)
            for action in actions:
                percept = self.perform_action(action, environment)

            


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
        # if kb.infer(Literal("Pit", x, y, False)) or kb.infer(Literal("Wumpus", x, y, False)):
        #     return float('inf')
        if (x, y) in kb.has_pit or (x, y) in kb.has_wumpus:
            return float('inf')

        # Nếu chưa biết rõ (tức không thể suy ra an toàn) → penalty
        # if not kb.infer(-Literal("Pit", x, y, False)):
        if (x, y) not in kb.not_has_pit:
            score += 3  # nguy cơ Pit

        # if not kb.infer(-Literal("Wumpus", x, y, False)):
        if (x, y) not in kb.not_has_wumpus:
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