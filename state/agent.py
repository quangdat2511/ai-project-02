from typing import Tuple, List, Optional
from queue import PriorityQueue
from .types import *
from .logic import *
from .environment import *

class Agent:
    def __init__(self, K: int):
        self.position = (0, 0)
        self.direction = Direction.EAST
        self.has_gold = False
        self.has_arrow = True
        self.check_scream = False
        self.is_alive = True
        self.kb = KnowledgeBase(K=K)
        self.planner = Planner(self)
        self.score = 0
        self.winning = False
        self.K = K
        self.visited = set()
        self.action_count = 0  

    def get_actions(self, percept: Percept) -> List[Action]:
        actions = []
        if percept.glitter:
            actions.append(Action.GRAB)
            return actions  # ưu tiên lấy vàng
        
        if self.has_gold and self.position == (0, 0):
            actions.append(Action.CLIMB)
            return actions

        print(f"Not has pit: ", self.kb.not_has_pit)
        print(f"Not has wumpus: ", self.kb.not_has_wumpus)
        print(f"Has wumpus: ", self.kb.has_wumpus)
        print(f"Has pit: ", self.kb.has_pit)
        print(f"Visited: ", self.visited)
        if self.has_gold:
            goal = (0, 0)  # nếu có vàng thì luôn hướng về góc trên bên trái
        else:
            safe_unvisited_pos = [pos for pos in self.kb.not_has_pit if pos in self.kb.not_has_wumpus and pos not in self.visited]
            print(f"Safe unvisited positions: {safe_unvisited_pos}")
            # goal is the closest unvisited cell that is safe
            if not safe_unvisited_pos:
                if self.has_arrow and self.kb.nearest_stench_and_no_breeze != (-1, -1):
                    if self.kb.nearest_stench_and_no_breeze == self.position:
                        # nếu đang ở ô có Stench và không có Breeze, bắn Wumpus
                        actions.append(Action.SHOOT)
                        return actions
                    
                    goal = self.kb.nearest_stench_and_no_breeze  
                else:
                    # random neighbor
                    print("No safe unvisited positions, choosing a random neighbor.")
                    neighbors = self._neighbors(self.position)
                    goal = neighbors[random.randint(0, len(neighbors) - 1)]
            else:
                goal = min(safe_unvisited_pos, key=lambda pos: abs(pos[0] - self.position[0]) + abs(pos[1] - self.position[1]), default=None)

        print(f"Current position: {self.position}, Goal: {goal}")
        path = self.planner.a_star(start=self.position, goal=goal)
        print("Path: ", path)
        # next_pos = path[0] if len(path) > 0 else None

        # check making turns
        # if next_pos:
        current_position = self.position
        current_direction = self.direction
        for next_pos in path:
            left_direction = current_direction.turn_left()
            right_direction = current_direction.turn_right()
            dx, dy = (next_pos[0] - current_position[0], next_pos[1] - current_position[1])
            if (dx, dy) == left_direction.value:
                actions.append(Action.TURN_LEFT)
                current_direction = left_direction
            elif (dx, dy) == right_direction.value:
                actions.append(Action.TURN_RIGHT)
                current_direction = right_direction
            elif (dx, dy) != current_direction.value:
                actions.append(Action.TURN_RIGHT)
                actions.append(Action.TURN_RIGHT)
                current_direction = right_direction.turn_right()  # quay 180 độ

            actions.append(Action.FORWARD)
            current_position = next_pos

        return actions
            
    def add_percept(self, percept: Percept, x, y):
        self._add_breeze_axioms(x, y, percept.breeze)
        self._add_stench_axioms(x, y, percept.stench)
        # if self.has_arrow == False and self.check_scream == False:
        #     self.check_scream = True
        #     self._add_scream_axioms(percept.scream)

    def _add_breeze_axioms(self, x, y, value):
        """Breeze ⇔ có Pit ở ô kề"""
        neighbors = self._neighbors((x, y))
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
        neighbors = self._neighbors((x, y))
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
    
    def _add_scream_axioms(self, value: bool):
        #Mục tiêu của percept này là giúp cho agent có thêm thông tin ô kh có W.
        #Vì vậy nếu W di chuyển sau 5 - k bước thì thông tin kh còn áp dụng được nữa.
        #Các suy luận liên quan đến percept này nên được thiết kế để loại bỏ dễ dàng (nếu cần).
        if (value):
            nx, ny = self.position
            dx, dy = self.direction
            s = Literal("Scream", -1, -1)
            #Đầu tiên là giảm K. Khi giảm K cần hết sức thận trọng, để kết luận kh bị sai thì nếu con
            #W nằm trong has_wumpus thì ta phải xóa nó. Nếu biết vị trí của W bị bắn => Dễ, nếu kh biết
            #thì tạm xóa 1 ô đầu tiên đã biết có W trên hướng đó, còn nếu trong has_wumpus chưa có ô nào trên
            #hướng đó thì kh cần vì điều đó có nghĩa con W bị bắn này ch dc tính vào K.
            while True:
                nx += dx
                ny += dy
                lit = Literal("Wumpus", nx, ny)
                a = self.kb.infer(-lit)
                if a:#đã biết chắc chắn kh có W thì mũi tên kh
                    #dừng ở ô này
                    continue
                elif self.kb.infer(lit): #nếu bắt gặp 1 ô chắc chắn có W 
                    #sau loạt ô chắc chắn kh có W thì => biết chính xác vị trí W bị bắn:
                    self.kb.add_clause(Clause[s])
                    self.kb.add_clause(Clause[-s] | Clause([-lit]))
                    #Remove ô này trong set has_wumpus
                    #thêm trong set no_has_wumpus, remove visited 4 ô xung quanh ô này,
                    #xóa 4 mệnh đề stench và literal liên quan ở 4 ô xung quanh (nếu đang có trong KB)
                    #Làm sao agent có thể đi lại 4 ô đó để kiểm tra?
                    #Hiện tại thuật toán có cho agent đi lại ô visited kh? và khi nào đi
                    break
                else:#Nếu gặp ô chưa có kết luận thì có thêm Scream => not W ở ô đó. Xóa hết tất cả 
                    #mệnh đề về stench ở hướng đó +-1 (là 3 cột hoặc 3 hàng với hàng agent đang đúng
                    #làm trung tâm, đồng thời bỏ visited các ô đó). Đồng thời trên hướng bắn đó nếu
                    #1 hay nhiều ô nào nằm trong has_wumpus thì tạm thời xóa ô đầu tiên gặp (vì có thể 
                    # là con này bị bắn mà ta chưa thể kết luận ở đây, nếu nó còn thì agent sẽ 
                    # tự visit và suy luận lại sau)
                    self.kb.add_clause(Clause[s])
                    self.kb.add_clause(Clause[-s] | Clause([-lit]))
                    break
        else: #Nếu kh nghe scream thì:
            #Nếu agent đang quay về South thì tất cả ô từ vị trí (x, y) -> (x, 0) đều kh có W
            #Nếu agent đang quay về West thì tất cả ô từ vị trí (x, y) -> (0, y) đều kh có W
            #Nếu agent đang quay về Est thì tất cả ô (x', y') sao cho y' = y và x' > x đều kh có W
            #Nếu agent đang quay về North thì tất cả các ô (x', y') sao cho x' = x và y' > y đều kh có W
            #Nên thêm 1 hàm riêng hỗ trợ suy luận has_wumpus dựa trên tập has_wumpus và suy luận này.
            pass
        #Tóm lại, nếu W di chuyển thì sau 5 bước nếu trong KB còn mệnh đề liên quan đến Scream thì xóa đi.
    
    def _valid(self, nx, ny):
        return 0 <= nx and 0 <= ny
    
    def _neighbors(self, position: Tuple[int, int]):
        neighbors = []
        x, y = position
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx, ny = x + dx, y + dy
            if self._valid(nx, ny):
                neighbors.append((nx, ny))
        return neighbors

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
        if self.action_count > 200:
            print("Too many actions, stopping the game.")
            self.is_alive = False
            return percept


        if action == Action.FORWARD:
            dx, dy = self.direction.value
            if not percept.bump:
                # Cập nhật vị trí
                self.position = (self.position[0] + dx, self.position[1] + dy)
                if self.position not in self.visited:
                    self.visited.add(self.position)
                    self.add_percept(percept, *self.position)
                    neighbors = self._neighbors(self.position)
                    for neighbor in neighbors:
                        if neighbor not in self.visited:
                            self.kb.infer(Literal("Pit", *neighbor))
                            self.kb.infer(Literal("Wumpus", *neighbor))
                            self.kb.infer(-Literal("Pit", *neighbor))
                            self.kb.infer(-Literal("Wumpus", *neighbor))
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
                if percept.scream:
                    self.kb.alive_wumpus_count -= 1
        elif action == Action.CLIMB:
            if self.position == (0, 0) and self.has_gold:
                self.winning = True
                self.score += 1000

        self.is_alive = not environment.is_agent_dead(self.position)
        if percept.stench and not percept.breeze:
            self.kb.nearest_stench_and_no_breeze = self.position

        self.display(environment)

        return percept

    def play(self, environment: Environment):
        self.display(environment)

        # Get initial percept
        percept = environment.get_percept_in_cell(self.position)
        self.add_percept(percept, *self.position)
        self.visited.add(self.position)
        neighbors = self._neighbors(self.position)
        for neighbor in neighbors:
            self.kb.infer(Literal("Pit", *neighbor))
            self.kb.infer(Literal("Wumpus", *neighbor))
            self.kb.infer(-Literal("Pit", *neighbor))
            self.kb.infer(-Literal("Wumpus", *neighbor))


        while self.is_alive and not self.winning:
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
        if kb.infer(Literal("Pit", x, y, False)) or kb.infer(Literal("Wumpus", x, y, False)):
            return float('inf')
        # if (x, y) in kb.has_pit or (x, y) in kb.has_wumpus:
            # return float('inf')

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

            neighbors = self.agent._neighbors(current)
            for next_pos in neighbors:
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