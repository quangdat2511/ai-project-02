# from gui import *
# if __name__ == "__main__":
#     main()

from state import *

if __name__ == "__main__":
    # Khởi tạo môi trường và agent
    env = Environment(N=8, K=3, p = 0.1, map_id=7)  # 8x8 grid
    # env = Environment()
    # fixed_map = [
    #     [".", ".", ".", ".", "P", ".", ".", "."],
    #     [".", ".", ".", ".", "P", ".", ".", "."],
    #     [".", ".", "W", ".", "P", ".", "G", "."],
    #     [".", ".", ".", ".", "P", "P", ".", "."],
    #     ["P", "P", "P", "P", "P", ".", ".", "."],
    #     [".", ".", ".", "P", ".", ".", "P", "."],
    #     [".", "W", ".", ".", ".", ".", ".", "."],
    #     [".", ".", ".", ".", "P", ".", ".", "."],
    # ]
    # env.initialize_from_map(fixed_map)
    agent = Agent(K=3)

    agent.play(env)
    if agent.winning:
        print("You win!")
    else:
        print("Game Over!")