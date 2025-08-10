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
    def __init__(self, K: int):
        self.clauses = set()
        self.has_wumpus = set()  # các ô có Wumpus
        self.has_pit = set()  # các ô có Pit
        self.not_has_wumpus = set()  # các ô không có Wumpus
        self.not_has_pit = set()  # các ô không có Pit
        self.nearest_stench_and_no_breeze = (-1, -1)
        self.alive_wumpus_count = K
        self.not_scream_helper = ScreamSupport()

    # def simplify_clause(self, clause):
    #     unit_literals = {next(iter(c.literals)) for c in self.clauses if len(c.literals) == 1}
    #     new_literals = set()

    #     for lit in clause.literals:
    #         if -lit in unit_literals:
    #             continue  # loại literal mâu thuẫn với fact
    #         else:
    #             new_literals.add(lit)

    #     if new_literals:
    #         return Clause(new_literals)
    #     else:
    #         return None 

    def add_clause(self, clause):
        self.clauses.add(clause)
        # simplified_clause = self.simplify_clause(clause)
        # if simplified_clause:
        #     self.clauses.add(simplified_clause)
    
    def add_clauses(self, clauses):
        self.clauses.update(clauses)
    
    def infer(self, query: Literal):
        if self.alive_wumpus_count == len(self.has_wumpus) and query.name == "Wumpus":
            if query.is_negated:
                if query.position in self.has_wumpus:
                    return False
                else:
                    return True
            else:
                if query.position in self.has_wumpus:
                    return True
                else:
                    return False
                
        if self.not_scream_helper.available == True and query.name == "Wumpus":
            dx, dy = self.not_scream_helper.shooting_direction.value
            x1, y1 = self.not_scream_helper.org_position
            x2, y2 = query.position
            vx, vy = x2 - x1, y2 - y1
            if (dx == 0 and vx == 0 and dy * vy > 0) or (dy == 0 and vy == 0 and dx * vx > 0):
                if query.position not in self.not_has_wumpus:
                    self.not_has_wumpus.add(query.position)
                    self.add_clause(Clause([-Literal("Wumpus", *query.position)]))
                return query.is_negated

        inference = InferenceEngine(self.clauses)
        if query.name == "Pit" and query.is_negated == False:
            if query.position in self.has_pit:
                return True
            else:
                if inference.resolution(query):
                    print("Call resolution")
                    self.has_pit.add(query.position)
                    self.add_clause(Clause([query]))
                    return True
                else:
                    return False
        elif query.name == "Pit" and query.is_negated == True:
            if query.position in self.not_has_pit:
                return True
            else:
                if inference.resolution(query):
                    print("Call resolution")
                    self.not_has_pit.add(query.position)
                    self.add_clause(Clause([query]))
                    return True
                else:
                    return False
        elif query.name == "Wumpus" and query.is_negated == False:
            if query.position in self.has_wumpus:
                return True
            else:
                if inference.resolution(query):
                    print("Call resolution")
                    self.has_wumpus.add(query.position)
                    self.add_clause(Clause([query]))
                    return True
                else:
                    return False
        elif query.name == "Wumpus" and query.is_negated == True:
            if query.position in self.not_has_wumpus:
                return True
            else:
                if inference.resolution(query):
                    print("Call resolution")
                    self.not_has_wumpus.add(query.position)
                    self.add_clause(Clause([query]))
                    return True
                else:
                    return False

    def remove_stench_clauses(self, target_x, target_y):
        """
        Xóa toàn bộ clause trong KB có chứa literal Stench tại tọa độ (target_x, target_y),
        bất kể literal đó có dấu phủ định hay không.
        """
        to_remove = {clause for clause in self.clauses
                    if any(lit.name == "Stench" and lit.position == (target_x, target_y)
                            for lit in clause.literals)}
        self.clauses -= to_remove
    
    def remove_unit_clause(self, literal):
        clause_to_remove = Clause([literal])
        self.clauses.discard(clause_to_remove)

    def remove_unit_stench_clause_in_range(self, x_min=None, x_max=None, y_min=None, y_max=None):
        removed_positions = []
        for clause in list(self.clauses):  # copy để tránh thay đổi khi duyệt
            if len(clause.literals) == 1:
                lit = next(iter(clause.literals))
                if lit.name == "Stench" and not lit.is_negated:
                    x, y = lit.position
                    if (x_min is None or x >= x_min) and \
                    (x_max is None or x <= x_max) and \
                    (y_min is None or y >= y_min) and \
                    (y_max is None or y <= y_max):
                        self.clauses.discard(clause)
                        removed_positions.append((x, y))

        return removed_positions

class InferenceEngine:
    def __init__(self, clauses):
        self.clauses = clauses
    def resolution(self, query):
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