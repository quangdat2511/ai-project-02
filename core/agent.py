from typing import Tuple, List, Optional
from .types import *
from .logic import *
from .environment import *
from .planner import *

class Agent:
    def __init__(self, K: int, is_moving_wumpus=False):
        self.position = (0, 0)
        self.direction = Direction.EAST
        self.has_gold = False
        self.has_arrow = True
        self.check_scream = False
        self.is_alive = True
        self.inference_engine = InferenceEngine(K=K)
        self.planner = Planner(self.inference_engine, self._neighbors)
        self.score = 0
        self.climbed_out = False
        self.K = K
        self.action_count = 0  
        self.N = -1     # the agent does not know the size at first
        self.current_percept = None
        self.action_queue = []
        self.is_moving_wumpus = is_moving_wumpus

    def get_actions(self, percept: Percept) -> List[Action]:
        actions = []
        if percept.glitter:
            actions.append(Action.GRAB)
            return actions  
        
        if self.has_gold and self.position == (0, 0):
            actions.append(Action.CLIMB)
            return actions

        # count number of actions left until wumpus is moved for advanced mode
        actions_left = 5 - (self.action_count % 5)

        # print(f"Not has pit: ", self.inference_engine.not_has_pit)
        # print(f"Not has wumpus: ", self.inference_engine.not_has_wumpus)
        # print(f"Has wumpus: ", self.inference_engine.has_wumpus)
        # print(f"Has pit: ", self.inference_engine.has_pit)
        # print(f"Visited: ", self.inference_engine.visited)
        if self.has_gold:
            goal = (0, 0)  
        else:
            safe_unvisited_pos = [pos for pos in self.inference_engine.not_has_pit if pos in self.inference_engine.not_has_wumpus and pos not in self.inference_engine.visited]
            # print(f"Safe unvisited positions: {safe_unvisited_pos}")
            # goal is the closest unvisited cell that is safe
            if not safe_unvisited_pos:
                # print("shoot position: ", self.inference_engine.shoot_position)
                # print("Has arrow: ", self.has_arrow)
                if self.has_arrow and (len(self.inference_engine.has_wumpus) > 0 or self.inference_engine.shoot_position != (-1, -1)):
                    if len(self.inference_engine.has_wumpus) > 0:
                        # get the nearest wumpus from current position
                        nearest_wumpus = min(
                            self.inference_engine.has_wumpus,
                            key=lambda wumpus: abs(wumpus[0] - self.position[0]) + abs(wumpus[1] - self.position[1])
                        )
                        visited_wumpus_neighbors = [pos for pos in self._neighbors(nearest_wumpus) if pos in self.inference_engine.visited]
                        self.inference_engine.shoot_position = visited_wumpus_neighbors[0]

                    if self.inference_engine.shoot_position == self.position:
                        neighbors = self._neighbors(self.position)
                        goal = None
                        for neighbor in neighbors:
                            if self.inference_engine.infer(Literal("Wumpus", *neighbor, False)):
                                goal = neighbor
                                break

                        if goal:
                            # find the direction to shoot
                            dx, dy = (goal[0] - self.position[0], goal[1] - self.position[1])
                            left_direction = self.direction.turn_left()
                            right_direction = self.direction.turn_right()
                            if (dx, dy) == left_direction.value:
                                actions.append(Action.TURN_LEFT)
                            elif (dx, dy) == right_direction.value:
                                actions.append(Action.TURN_RIGHT)
                            elif (dx, dy) != self.direction.value:
                                actions.append(Action.TURN_RIGHT)
                                actions.append(Action.TURN_RIGHT)

                        if self.is_moving_wumpus and actions_left <= len(actions):
                            return actions  
                        
                        actions.append(Action.SHOOT)
                        return actions

                    goal = self.inference_engine.shoot_position
                else:
                    # random neighbor
                    neighbors = self._neighbors(self.position)
                    unvisited_neighbors = [pos for pos in neighbors if pos not in self.inference_engine.visited and not self.inference_engine.infer(Literal("Pit", *pos, False)) and not self.inference_engine.infer(Literal("Wumpus", *pos, False))]
                    if unvisited_neighbors:
                        goal = random.choice(unvisited_neighbors)
                    else:
                        visited_neighbors = [pos for pos in neighbors if pos in self.inference_engine.visited]
                        if visited_neighbors:
                            goal = random.choice(visited_neighbors)
                        else:
                            if self.position == (0, 0):
                                actions.append(Action.CLIMB)
                                return actions

            else:
                goal = min(
                    (pos for pos in safe_unvisited_pos if pos != self.position),
                    key=lambda pos: abs(pos[0] - self.position[0]) + abs(pos[1] - self.position[1]),
                    default=None
                )

        path = self.planner.a_star(start=self.position, goal=goal, visited=self.inference_engine.visited, start_dir=self.direction)

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
                current_direction = right_direction.turn_right()  

            if self.is_moving_wumpus and actions_left <= len(actions):
                return actions  
            actions.append(Action.FORWARD)
            current_position = next_pos

        return actions
            
    def add_percept(self, percept: Percept, x, y):
        if self.has_arrow == False and self.check_scream == False:
            self.check_scream = True
            self._add_scream_axioms(percept.scream)
            if percept.scream and not percept.stench:
                x, y = self.position
                dx, dy = self.direction.value
                nx, ny = x + dx, y + dy
                self.inference_engine.not_has_pit.add((nx, ny))
                self.inference_engine.kb.tell(Clause([-Literal("Pit", nx, ny)]))
        self._add_breeze_axioms(x, y, percept.breeze)
        self._add_stench_axioms(x, y, percept.stench)

    def _add_breeze_axioms(self, x, y, value):
        neighbors = self._neighbors((x, y))
        b = Literal("Breeze", x, y)
        pits = [Literal("Pit", nx, ny) for (nx, ny) in neighbors]
        self.inference_engine.kb.tell(Clause([-Literal("Pit", x, y)]))  # Thêm ô hiện tại là không có Pit
        if value:
            # Breeze(x,y) => (P1 v P2 v ...)
            clause = Clause(pits)
            self.inference_engine.kb.tell(clause)
        else:
            # NOT Breeze => tất cả các Pit kề đều False
            for p in pits:
                self.inference_engine.kb.tell(Clause([-p]))
        
    def _add_stench_axioms(self, x, y, value):
        neighbors = self._neighbors((x, y))
        s = Literal("Stench", x, y)
        wumps = [Literal("Wumpus", nx, ny, False) for (nx,ny) in neighbors]
        self.inference_engine.kb.tell(Clause([-Literal("Wumpus", x, y)]))  # Thêm ô hiện tại là không có Wumpus
        if value:
            # Stench => (W1 v W2 v ...)
            clause = Clause(wumps)
            self.inference_engine.kb.tell(Clause([s]))
            self.inference_engine.kb.tell(Clause([-s]) | clause)
        else:
            # NOT Stench => tất cả Wumpus kề đều False
            self.inference_engine.kb.tell(Clause([-s]))
            for w in wumps:
                self.inference_engine.kb.tell(Clause([s]) | Clause([-w]))
    
    def _add_scream_axioms(self, value: bool):
        #Mục tiêu của percept này là giúp cho agent có thêm thông tin ô kh có W.
        if (value):
            nx, ny = self.position
            dx, dy = self.direction.value
            s = Literal("Scream", -1, -1)
            
            while True:
                nx += dx
                ny += dy
                lit = Literal("Wumpus", nx, ny)
                a = self.inference_engine.infer(-lit)
                if a:#đã biết chắc chắn kh có W thì mũi tên kh dừng ở ô này
                    continue
                elif self.inference_engine.infer(lit): #nếu bắt gặp 1 ô chắc chắn có W 
                    
                    self.inference_engine.kb.tell(Clause([s]))
                    self.inference_engine.kb.tell(Clause([-s]) | Clause([-lit]))
                    
                    self.inference_engine.has_wumpus.discard((nx, ny))
                    self.inference_engine.remove_unit_clause(Literal("Wumpus", nx, ny))
                    self.inference_engine.not_has_wumpus.add((nx, ny))
                    self.inference_engine.kb.tell(Clause([-Literal("Wumpus", nx, ny)]))
                    neighbors = self._neighbors((nx, ny))
                    for neighbor in neighbors:
                        self.inference_engine.remove_stench_clauses(neighbor[0], neighbor[1])
                        self.inference_engine.visited.discard(neighbor)
                    if (self.position + self.direction.value == nx, ny):
                        self.inference_engine.visited.add(self.position)                    
                    break
                else:
                    self.inference_engine.kb.tell(Clause([s]))
                    self.inference_engine.kb.tell(Clause([-s]) | Clause([-lit]))
                    x_min = x_max = y_min = y_max = 0
                    if self.direction == Direction.NORTH:
                        x_min, x_max = nx - 1, nx + 1
                        y_min, y_max = ny, None
                    elif self.direction == Direction.EAST:
                        x_min, x_max = nx, None
                        y_min, y_max = ny - 1, ny + 1
                    elif self.direction == Direction.WEST:
                        x_min, x_max = None, nx
                        y_min, y_max = ny - 1, ny + 1
                    elif self.direction == Direction.SOUTH:
                        x_min, x_max = nx - 1, nx + 1
                        y_min, y_max = None, ny
                    the_sus_wumpus = self.inference_engine.find_first_wumpus_on_path(nx, ny, self.direction)
                    if (the_sus_wumpus != None):
                        sx, sy = the_sus_wumpus
                        self.inference_engine.has_wumpus.discard((sx, sy))
                        self.inference_engine.remove_unit_clause(Literal("Wumpus", sx, sy))
                    removed_positions = self.inference_engine.remove_unit_stench_clause_in_range(x_min, x_max, y_min, y_max)
                    if (self.position + self.direction.value == nx, ny):
                        removed_positions.append(self.position)
                    for pos in removed_positions:
                        self.inference_engine.remove_stench_clauses(pos[0], pos[1])
                        self.inference_engine.visited.discard(pos)
                    if (self.position + self.direction.value == nx, ny):
                        self.inference_engine.visited.add(self.position)                    
                    break
        else: 
            self.inference_engine.not_scream_helper.available = True
            self.inference_engine.not_scream_helper.org_position = self.position
            self.inference_engine.not_scream_helper.shooting_direction = self.direction

    def _valid(self, nx, ny):
        if self.N == -1:
            return 0 <= nx and 0 <= ny
        return 0 <= nx < self.N and 0 <= ny < self.N

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
        if self.action_count > 1000:
            print("Too many actions, stopping the game.")
            self.is_alive = False
            return percept

        if self.is_moving_wumpus == True and self.action_count % 5 == 0:
            self.inference_engine.handle_moving_wumpus()

        if action == Action.FORWARD:
            dx, dy = self.direction.value
            if not percept.bump:
                # Cập nhật vị trí
                self.position = (self.position[0] + dx, self.position[1] + dy)
                if self.position not in self.inference_engine.visited:
                    self.inference_engine.visited.add(self.position)
                    self.add_percept(percept, *self.position)
                    neighbors = self._neighbors(self.position)
                    for neighbor in neighbors:
                        if neighbor not in self.inference_engine.visited:
                            self.inference_engine.infer(Literal("Pit", *neighbor))
                            self.inference_engine.infer(Literal("Wumpus", *neighbor))
                            self.inference_engine.infer(-Literal("Pit", *neighbor))
                            self.inference_engine.infer(-Literal("Wumpus", *neighbor))
            else:
                print("Bumped into a wall, cannot move forward.")
                self.N = max(self.N, self.position[0] + 1, self.position[1] + 1)  # update N
                # filter the valid positions in sets
                self.inference_engine.not_has_pit = {pos for pos in self.inference_engine.not_has_pit if self._valid(*pos)}
                self.inference_engine.not_has_wumpus = {pos for pos in self.inference_engine.not_has_wumpus if self._valid(*pos)}
                self.inference_engine.has_pit = {pos for pos in self.inference_engine.has_pit if self._valid(*pos)}
                self.inference_engine.has_wumpus = {pos for pos in self.inference_engine.has_wumpus if self._valid(*pos)}

            self.score -= 1  
        elif action == Action.TURN_LEFT:
            self.direction = self.direction.turn_left()
            self.score -= 1  
        elif action == Action.TURN_RIGHT:
            self.direction = self.direction.turn_right()
            self.score -= 1 
        elif action == Action.GRAB:
            self.has_gold = True
            self.score += 10
        elif action == Action.SHOOT:
            if self.has_arrow:
                self.has_arrow = False
                self.score -= 10  
                if percept.scream:
                    self.inference_engine.alive_wumpus_count -= 1
                if self.is_moving_wumpus == False or (self.is_moving_wumpus == True and self.action_count % 5 != 0):
                    self.add_percept(percept, *self.position)
                elif self.is_moving_wumpus == True and self.action_count % 5 == 0:
                    self._add_stench_axioms(*self.position, percept.stench)
                    self._add_breeze_axioms(*self.position, percept.breeze)
                    self.inference_engine.visited.add(self.position)
                
                neighbors = self._neighbors(self.position)
                for neighbor in neighbors:
                    if neighbor not in self.inference_engine.visited:
                        self.inference_engine.infer(Literal("Pit", *neighbor))
                        self.inference_engine.infer(Literal("Wumpus", *neighbor))
                        self.inference_engine.infer(-Literal("Pit", *neighbor))
                        self.inference_engine.infer(-Literal("Wumpus", *neighbor))
        elif action == Action.CLIMB:
            if self.position == (0, 0) and self.has_gold:
                self.climbed_out = True
                self.score += 1000
            elif self.position == (0, 0) and not self.has_gold:
                self.climbed_out = True

        self.is_alive = not environment.is_agent_dead(self.position)
        if percept.stench and not percept.breeze:
            self.inference_engine.shoot_position = self.position
        elif percept.stench and self.inference_engine.shoot_position == (-1, -1):
            self.inference_engine.shoot_position = self.position

        self.display(environment)

        return percept

    def play(self, environment: Environment):
        self.display(environment)

        # Get initial percept
        percept = environment.get_percept_in_cell(self.position)
        if percept.stench and not percept.breeze:
            self.inference_engine.shoot_position = self.position
        elif percept.stench and self.inference_engine.shoot_position == (-1, -1):
            self.inference_engine.shoot_position = self.position
            
        self.add_percept(percept, *self.position)
        self.inference_engine.visited.add(self.position)
        neighbors = self._neighbors(self.position)
        for neighbor in neighbors:
            self.inference_engine.infer(Literal("Pit", *neighbor))
            self.inference_engine.infer(Literal("Wumpus", *neighbor))
            self.inference_engine.infer(-Literal("Pit", *neighbor))
            self.inference_engine.infer(-Literal("Wumpus", *neighbor))


        while self.is_alive and not self.climbed_out:
            actions = self.get_actions(percept)
            for action in actions:
                percept = self.perform_action(action, environment)

    def play_one_action(self, environment: Environment):
        if not self.current_percept:
            self.current_percept = environment.get_percept_in_cell(self.position)
            if self.current_percept.stench and not self.current_percept.breeze:
                self.inference_engine.shoot_position = self.position
            elif self.current_percept.stench and self.inference_engine.shoot_position == (-1, -1):
                self.inference_engine.shoot_position = self.position

            self.add_percept(self.current_percept, *self.position)
            self.inference_engine.visited.add(self.position)
            neighbors = self._neighbors(self.position)
            for neighbor in neighbors:
                self.inference_engine.infer(Literal("Pit", *neighbor))
                self.inference_engine.infer(Literal("Wumpus", *neighbor))
                self.inference_engine.infer(-Literal("Pit", *neighbor))
                self.inference_engine.infer(-Literal("Wumpus", *neighbor))
            return None
        
        if len(self.action_queue) == 0:
            actions = self.get_actions(self.current_percept)
            self.action_queue.extend(actions)

        action = self.action_queue.pop(0)
        self.current_percept = self.perform_action(action, environment)

        return action


class RandomAgent:
    def __init__(self):
        self.position = (0, 0)
        self.direction = Direction.EAST
        self.has_gold = False
        self.has_arrow = True
        self.is_alive = True
        self.climbed_out = False
        self.score = 0
        self.action_count = 0

    def get_random_action(self, percept):
        if percept.glitter:
            return Action.GRAB
        if self.has_gold and self.position == (0, 0):
            return Action.CLIMB
        possible_choices = [Action.FORWARD, Action.TURN_LEFT, Action.TURN_RIGHT]
        if self.has_arrow:
            possible_choices.append(Action.SHOOT)
        return random.choice(possible_choices)
    
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
    
    def perform_action(self, action, environment):
        print(f"Performing action: {action.name} at postion {self.position} facing {self.direction.name}")
        percept = environment.perform_action(self.position, self.direction, action)
        self.action_count += 1

        if self.action_count > 200:
            print("Too many action, stopping the game.")
            self.is_alive = False
            return percept
    
        if action == Action.FORWARD:
            if not percept.bump:
                dx, dy = self.direction.value
                self.position = (self.position[0] + dx, self.position[1] + dy)
            self.score -= 1
        elif action == Action.TURN_LEFT:
            self.direction = self.direction.turn_left()
            self.score -= 1
        elif action == Action.SHOOT:
            self.has_arrow = False
            self.score -= 10
        elif action == Action.TURN_RIGHT:
            self.direction = self.direction.turn_right()
            self.score -= 1
        elif action == Action.GRAB:
            self.has_gold = True
            self.score += 10
        elif action == Action.CLIMB:
            if self.position == (0, 0) and self.has_gold:
                self.climbed_out = True
                self.score += 1000

        self.is_alive = not environment.is_agent_dead(self.position)
        self.display(environment)
        return percept

    def play_one_action(self, environment: Environment):
        """
            Play a single action
        """
        percept = environment.get_percept_in_cell(self.position)
        action = self.get_random_action(percept)
        new_percept = self.perform_action(action, environment)
        if not self.is_alive or self.climbed_out:
            return None
        return action
    
    def play(self, environment: Environment):
        self.display(environment)
        percept = environment.get_percept_in_cell(self.position)
        while self.is_alive and not self.climbed_out:
            action = self.get_random_action(percept)
            percept = self.perform_action(action, environment)