from state import *

def main():
    WumpusWorld = Environment()
    WumpusWorld.initialize_environment()
    agent = Agent(WumpusWorld.N)
    agent.add_percept(Percept(0, 0), 0, 0)
    percept1 = WumpusWorld.perform_action((0, 0), Direction.EAST, Action.FORWARD)
    agent.add_percept(percept1, 1, 0)
    print(agent.kb.infer(-Literal("Wumpus", 2, 0)) and agent.kb.infer(-Literal("Pit", 2, 0)))


# agent = Agent(N=4)
# planner = Planner(agent)

# # Đánh dấu các ô đã infer là nguy hiểm hoặc an toàn
# agent.kb.add_clause(Clause([Literal("Pit", 1, 0, False)]))       # (1,0) chắc chắn có Pit
# agent.kb.add_clause(Clause([Literal("Wumpus", 2, 2, False)]))    # (2,2) chắc chắn có Wumpus
# agent.kb.add_clause(Clause([-Literal("Pit", 0, 1, False) ]))    # (0,1) chắc chắn không có Pit
# agent.kb.add_clause(Clause([-Literal("Wumpus", 0, 1, False) ])) # (0,1) chắc chắn không có Wumpus
# # Đánh dấu các ô đã infer là nguy hiểm hoặc an toàn
# agent.kb.add_clause(Clause([Literal("Pit", 1, 0, False)]))       # (1,0) chắc chắn có Pit
# agent.kb.add_clause(Clause([Literal("Wumpus", 2, 2, False)]))    # (2,2) chắc chắn có Wumpus
# agent.kb.add_clause(Clause([-Literal("Pit", 0, 1, False) ]))    # (0,1) chắc chắn không có Pit
# agent.kb.add_clause(Clause([-Literal("Wumpus", 0, 1, False) ])) # (0,1) chắc chắn không có Wumpus

# agent.position = (0, 0)
# goal = (3, 3)
# agent.position = (0, 0)
# goal = (3, 3)

# path = planner.a_star(agent.position, goal)
# path = planner.a_star(agent.position, goal)

# print("=== Planned Path ===")
# for step in path:
#     print(step)
# print("=== Planned Path ===")
# for step in path:
#     print(step)

# # In từng bước cost, nếu bạn thêm debug:
# for step in path:
#     print(f"Step: {step}, Risk: {planner.risk_score(step)}, Utility: {planner.utility_score(step)}")
# main()