from definition import*

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

main()