# from gui import *
# if __name__ == "__main__":
#     main()

from state import *

if __name__ == "__main__":
    # Khởi tạo môi trường và agent
    env = Environment(N=8, K=2)  # 8x8 grid
    agent = Agent(K=2)

    agent.play(env)
    if agent.winning:
        print("You win!")
    else:
        print("Game Over!")