from state import *

def main():
    Dang = Agent(8)
    Dang.add_percept(Percept(False, False), 0, 0)
    Dang.add_percept(Percept(False, False), 1, 0)
    Dang.add_percept(Percept(False, False), 2, 0)
    Dang.add_percept(Percept(False, True), 3, 0)
    x = 4
    y = 0
    query_1 = Literal("Wumpus", x, y, True)
    query_2 = Literal("Pit", x, y, True)

    if Dang.kb.infer(query_1) and Dang.kb.infer(query_2):
        print("(" + str(x) + ", " + str(y) + ") is safe")
    else:
        print("(" + str(x) + ", " + str(y) + ") is not safe")


agent = Agent(N=4)
planner = Planner(agent)

# Đánh dấu các ô đã infer là nguy hiểm hoặc an toàn
agent.kb.add_clause(Clause([Literal("Pit", 1, 0, False)]))       # (1,0) chắc chắn có Pit
agent.kb.add_clause(Clause([Literal("Wumpus", 2, 2, False)]))    # (2,2) chắc chắn có Wumpus
agent.kb.add_clause(Clause([-Literal("Pit", 0, 1, False) ]))    # (0,1) chắc chắn không có Pit
agent.kb.add_clause(Clause([-Literal("Wumpus", 0, 1, False) ])) # (0,1) chắc chắn không có Wumpus

agent.position = (0, 0)
goal = (3, 3)

path = planner.a_star(agent.position, goal)

print("=== Planned Path ===")
for step in path:
    print(step)

# In từng bước cost, nếu bạn thêm debug:
for step in path:
    print(f"Step: {step}, Risk: {planner.risk_score(step)}, Utility: {planner.utility_score(step)}")
# main()