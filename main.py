from state import *

if __name__ == "__main__":
    # Khởi tạo môi trường và agent
    env = Environment(N=8)  # 8x8 grid
    agent = Agent()

    agent.play(env)
    print("Game Over!")
