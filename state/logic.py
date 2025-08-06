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
        return (self.name, self.position, self.is_negated) == (other.name, self.position, other.is_negated)

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
        self.has_wumpus = set()  # các ô có Wumpus
        self.has_pit = set()  # các ô có Pit
        self.not_has_wumpus = set()  # các ô không có Wumpus
        self.not_has_pit = set()  # các ô không có Pit

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
    
    def infer(self, query):
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