from .types import*
class ScreamSupport:
    def __init__(self):
        self.available = False
        self.org_position = None
        self.shooting_direction = Direction.EAST

class Literal:
    def __init__(self, name, x, y, is_negated=False):
        self.name = name
        self.position = (x, y)   
        self.is_negated = is_negated
    
    def __str__(self):
        s = f"{self.name}{self.position}" if self.position else self.name
        return f"~{s}" if self.is_negated else s

    def __neg__(self):
        return Literal(self.name, self.position[0], self.position[1], not self.is_negated)

    def __eq__(self, other):
        return (self.name, self.position, self.is_negated) == (other.name, other.position, other.is_negated)

    def __hash__(self):
        return hash((self.name, self.position, self.is_negated))

class Clause:
    def __init__(self, literals):
        self.literals = set(literals)
    
    def __str__(self):
        return " v ".join(str(lit) for lit in self.literals)
    
    def is_empty(self):
        return len(self.literals) == 0
    
    def __eq__(self, other):
        return isinstance(other, Clause) and self.literals == other.literals
    
    def __hash__(self):
        return hash(frozenset(self.literals))
    
    def __or__(self, other):
        return Clause(self.literals.union(other.literals))
    
    def resolve(self, other):
        resolvents = set()
        for l1 in self.literals:
            if -l1 in other.literals:
                new_literals = (self.literals | other.literals) - {l1, -l1}
                resolvents.add(Clause(new_literals))
        return resolvents

class KnowledgeBase:
    def __init__(self):
        self.clauses = set()

    def tell(self, clause):
        self.clauses.add(clause)

    def ask(self, query):
        negated_query = Clause([-query])
        new_clauses = set()
        kb_clauses = set(self.clauses.union({negated_query}))
        while True:
            clause_list = list(kb_clauses)
            n = len(clause_list)
            for i in range(n):
                for j in range(i + 1, n):
                    ci = clause_list[i]
                    cj = clause_list[j]
                    resolvents = ci.resolve(cj)
                    for res in resolvents:
                        if res.is_empty():
                            return True  # derived empty clause, proven
                        new_clauses.add(res)

            if new_clauses.issubset(kb_clauses):
                return False  # no progress
            kb_clauses |= new_clauses

class InferenceEngine:
    def __init__(self, K: int):
        self.kb = KnowledgeBase()
        self.visited = set()
        self.alive_wumpus_count = K
        self.has_wumpus = set()
        self.has_pit = set()  # các ô có Pit
        self.not_has_wumpus = set()  # các ô không có Wumpus
        self.not_has_pit = set()  # các ô không có Pit
        self.shoot_position = (-1, -1)
        self.not_scream_helper = ScreamSupport()

    def infer(self, query: Literal):
        if self.alive_wumpus_count == len(self.has_wumpus) and query.name == "Wumpus":
            #Not Wumpus at x, y?
            if query.is_negated:
                #If in has_wumpus
                if query.position in self.has_wumpus:
                    return False
                #If not in has_wumpus
                else:
                    self.not_has_wumpus.add(query.position)
                    self.kb.tell(Clause([-Literal("Wumpus", *query.position)]))
                    return True
            #Wumpus at x, y?
            else:
                if query.position in self.has_wumpus:
                    return True
                else:
                    self.not_has_wumpus.add(query.position)
                    self.kb.tell(Clause([-Literal("Wumpus", *query.position)]))
                    return False
                    
        if self.not_scream_helper.available == True and query.name == "Wumpus":
            dx, dy = self.not_scream_helper.shooting_direction.value
            x1, y1 = self.not_scream_helper.org_position
            x2, y2 = query.position
            vx, vy = x2 - x1, y2 - y1
            if (dx == 0 and vx == 0 and dy * vy > 0) or (dy == 0 and vy == 0 and dx * vx > 0):
                if query.position not in self.not_has_wumpus:
                    self.not_has_wumpus.add(query.position)
                    self.kb.tell(Clause([-Literal("Wumpus", *query.position)]))
                return query.is_negated

        if query.name == "Pit" and query.is_negated == False:
            if query.position in self.has_pit:
                self.not_has_wumpus.add(query.position)
                self.kb.tell(Clause([-Literal("Wumpus", *query.position)]))
                return True
            elif query.position in self.not_has_pit:
                return False
            else:
                # print("Call resolution")
                if self.kb.ask(query):
                    self.has_pit.add(query.position)
                    self.kb.tell(Clause([query]))
                    return True
                else:
                    return False
        elif query.name == "Pit" and query.is_negated == True:
            if query.position in self.not_has_pit:
                return True
            elif query.position in self.has_pit:
                self.not_has_wumpus.add(query.position)
                self.kb.tell(Clause([-Literal("Wumpus", *query.position)]))
                return False
            else:
                # print("Call resolution")
                if self.kb.ask(query):
                    self.not_has_pit.add(query.position)
                    self.kb.tell(Clause([query]))
                    return True
                else:
                    return False
        elif query.name == "Wumpus" and query.is_negated == False:
            if query.position in self.has_wumpus:
                self.not_has_pit.add(query.position)
                self.kb.tell(Clause([-Literal("Pit", *query.position)]))
                return True
            elif query.position in self.not_has_wumpus:
                return False
            else:
                # print("Call resolution")
                if self.kb.ask(query):
                    self.has_wumpus.add(query.position)
                    self.kb.tell(Clause([query]))
                    return True
                else:
                    return False
        elif query.name == "Wumpus" and query.is_negated == True:
            if query.position in self.not_has_wumpus:
                return True
            elif query.position in self.has_wumpus:
                self.not_has_pit.add(query.position)
                self.kb.tell(Clause([-Literal("Pit", *query.position)]))
                return False
            else:
                # print("Call resolution")
                if self.kb.ask(query):
                    self.not_has_wumpus.add(query.position)
                    self.kb.tell(Clause([query]))
                    return True
                else:
                    return False
                
    def remove_stench_clauses(self, x, y):
        """
        Xóa toàn bộ clause trong KB có chứa literal Stench tại tọa độ (target_x, target_y),
        bất kể literal đó có dấu phủ định hay không.
        """
        to_remove = {clause for clause in self.kb.clauses
                    if any(lit.name == "Stench" and lit.position == (x, y)
                            for lit in clause.literals)}
        self.kb.clauses -= to_remove

    def remove_scream_clauses(self):
        to_remove = {clause for clause in self.kb.clauses
                    if any(lit.name == "Scream" for lit in clause.literals)}
        self.kb.clauses -= to_remove

    def remove_unit_clause(self, literal):
        clause_to_remove = Clause([literal])
        self.kb.clauses.discard(clause_to_remove)

    def remove_unit_stench_clause_in_range(self, x_min=None, x_max=None, y_min=None, y_max=None):
        removed_positions = []
        for clause in list(self.kb.clauses):  # copy để tránh thay đổi khi duyệt
            if len(clause.literals) == 1:
                lit = next(iter(clause.literals))
                if lit.name == "Stench" and not lit.is_negated:
                    x, y = lit.position
                    if (x_min is None or x >= x_min) and \
                    (x_max is None or x <= x_max) and \
                    (y_min is None or y >= y_min) and \
                    (y_max is None or y <= y_max):
                        self.kb.clauses.discard(clause)
                        removed_positions.append((x, y))

        return removed_positions
    
    def remove_all_unit_stench_clause_in_range(self, x_min=None, x_max=None, y_min=None, y_max=None):
        removed_positions = []
        for clause in list(self.kb.clauses):  # copy để tránh thay đổi khi duyệt
            if len(clause.literals) == 1:
                lit = next(iter(clause.literals))
                if lit.name == "Stench":
                    x, y = lit.position
                    if (x_min is None or x >= x_min) and \
                    (x_max is None or x <= x_max) and \
                    (y_min is None or y >= y_min) and \
                    (y_max is None or y <= y_max):
                        self.kb.clauses.discard(clause)
                        removed_positions.append((x, y))

        return removed_positions

    def remove_unit_wumpus_clause(self):
        for clause in list(self.kb.clauses): 
            if len(clause.literals) == 1:
                lit = next(iter(clause.literals))
                if lit.name == "Wumpus":
                    self.kb.clauses.discard(clause)
    
    def handle_moving_wumpus(self):
        #Handle scream
        self.not_scream_helper.available = False
        self.remove_scream_clauses()
        #Handle stench
        positions = self.remove_all_unit_stench_clause_in_range(None, None, None, None)
        for pos in positions:
            self.remove_stench_clauses(*pos)
            # self.visited.discard(pos)
        #Handle has_wumpus
        # for pos in self.has_wumpus:
        #     self.remove_unit_clause(Literal("Wumpus", *pos))
        #     self.visited.discard(pos)
        # self.has_wumpus.clear()
        # #Handle not_has_wumpus
        # for pos in self.not_has_wumpus:
        #     self.remove_unit_clause(-Literal("Wumpus", *pos))
        #     self.visited.discard(pos)
        # self.not_has_wumpus.clear()
        self.remove_unit_wumpus_clause()
        self.has_wumpus.clear()
        self.not_has_wumpus.clear()
        # self.visited.clear()

    def find_first_wumpus_on_path(self, start_x, start_y, direction):
        """
        Tìm vị trí Wumpus đầu tiên trên đường bắn từ (start_x, start_y)
        theo hướng cho trước. Nếu không có trả về None.
        """
        if direction == Direction.NORTH:
            # Cùng cột, y tăng dần
            candidates = [(x, y) for (x, y) in self.has_wumpus if x == start_x and y > start_y]
            return min(candidates, key=lambda pos: pos[1], default=None)

        elif direction == Direction.SOUTH:
            # Cùng cột, y giảm dần
            candidates = [(x, y) for (x, y) in self.has_wumpus if x == start_x and y < start_y]
            return max(candidates, key=lambda pos: pos[1], default=None)

        elif direction == Direction.EAST:
            # Cùng hàng, x tăng dần
            candidates = [(x, y) for (x, y) in self.has_wumpus if y == start_y and x > start_x]
            return min(candidates, key=lambda pos: pos[0], default=None)

        elif direction == Direction.WEST:
            # Cùng hàng, x giảm dần
            candidates = [(x, y) for (x, y) in self.has_wumpus if y == start_y and x < start_x]
            return max(candidates, key=lambda pos: pos[0], default=None)

        return None