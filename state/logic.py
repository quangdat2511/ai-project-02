class Literal:
    def __init__(self, name, x, y, negated):
        self.name = name
        self.position = (x, y)   # ví dụ ('1','2')
        self.is_negated = negated

    # def __repr__(self):
    #     prefix = '¬' if self.is_negated else ''
    #     args_str = ",".join(map(str, self.args))
    #     return f"{prefix}{self.name}({args_str})"
    
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

    # def __repr__(self):
    #     return " ∨ ".join(map(str, self.literals))
    
    def __str__(self):
        return " v ".join(str(lit) for lit in self.literals)
    
    def is_empty(self):
        return len(self.literals) == 0
    
    def __eq__(self, other):
        return isinstance(other, Clause) and self.literals == other.literals
    
    def __hash__(self):
        return hash(frozenset(self.literals))

class KnowledgeBase:
    def __init__(self):
        self.clauses = set()

    def simplify_clause(self, clause):
        unit_literals = {next(iter(c.literals)) for c in self.clauses if len(c.literals) == 1}
        new_literals = set()

        for lit in clause.literals:
            if -lit in unit_literals:
                continue  # loại literal mâu thuẫn với fact
            else:
                new_literals.add(lit)

        if new_literals:
            return Clause(new_literals)
        else:
            return None 

    def add_clause(self, clause):
        # self.clauses.add(clause)
        simplified_clause = self.simplify_clause(clause)
        if simplified_clause:
            self.clauses.add(simplified_clause)

    def infer(self, query):
        negated_query = Clause([-query])
        new_clauses = set()
        kb_clauses = set(self.clauses.union({negated_query}))
        while True:
            pairs = [ (c1, c2) for c1 in kb_clauses for c2 in kb_clauses if c1 != c2 
                     and next(iter(c1.literals)).name == next(iter(c2.literals)).name]
            for (ci, cj) in pairs:
                # print(ci)
                # print(cj)
                # print()
                resolvents = self.resolve(ci, cj)
                for res in resolvents:
                    if res.is_empty():
                        return True  # derived empty clause, proven
                    new_clauses.add(res)
            if new_clauses.issubset(kb_clauses):
                return False  # no progress
            kb_clauses |= new_clauses
        pass  # Logic to infer knowledge from rules

    def resolve(self, c1, c2):
        resolvents = set()
        for l1 in c1.literals:
            for l2 in c2.literals:
                if l1.name == l2.name and l1.position == l2.position and l1.is_negated != l2.is_negated:
                    new_literals = (c1.literals.union(c2.literals)) - {l1, l2}
                    resolvents.add(Clause(new_literals))
        return resolvents

    # def simplify(self):
    #     simplified = set()
    #     unit_literals = set()

    #     # 1. Thu thập các facts
    #     for clause in self.clauses:
    #         if len(clause.literals) == 1:
    #             unit_literals.add(next(iter(clause.literals)))
    #             simplified.add(clause)

    #     # 2. Duyệt các clause còn lại
    #     for clause in self.clauses:
    #         if len(clause.literals) == 1:
    #             continue  # đã xử lý rồi

    #         new_literals = set()
    #         for lit in clause.literals:
    #             if -lit in unit_literals:
    #                 continue  # literal bị phủ định → loại bỏ
    #             else:
    #                 new_literals.add(lit)

    #         if new_literals:
    #             simplified.add(Clause(new_literals))

    #     self.clauses = simplified
