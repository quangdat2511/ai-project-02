# from gui import *
# if __name__ == "__main__":
#     main()

from state import *
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Wumpus World Simulator")
    parser.add_argument("--n", type=int, default=8, help="Map size")
    parser.add_argument("--k", type=int, default=2, help="Number of Wumpus")
    parser.add_argument("--p", type=float, default=0.2, help="Probility of pit")
    parser.add_argument("--map_id", type=int, default=None, help="ID of a map in example folder")
    return parser.parse_args()

"""
    Câu lệnh để dùng cho CLI
    
    python main.py --n 10 --k 6 --p 0.1 (dùng cho mục đích random map, có thể dùng để sinh xem map để bỏ vào thực nghiệm)
    
    Nếu có map sẵn thì không cần ba tham số trên mà trực tiếp dùng câu dưới đây
    python main.py --map_id i với mọi i chạy từ 1 đến số map hiện có trong folder example
    
    Nếu chỉ gõ python main.py thì tự chạy map với tham số định sẵn có trong class
"""
if __name__ == "__main__":
    # Khởi tạo môi trường và agent
    args = parse_args()

    env = Environment(N=args.n, K=args.k, p=args.p, map_id=args.map_id)  # 8x8 grid
    # env = Environment()
    # fixed_map = [
    #     [".", ".", "P", ".", "P", ".", ".", "."],
    #     [".", ".", "W", ".", "P", ".", ".", "."],
    #     [".", ".", "P", ".", "P", ".", "G", "."],
    #     ["P", "W", "P", ".", "P", "P", ".", "."],
    #     ["P", "P", "P", "P", "P", ".", ".", "."],
    #     [".", ".", ".", "P", ".", ".", "P", "."],
    #     [".", "W", ".", ".", ".", ".", ".", "."],
    #     [".", ".", ".", ".", "P", ".", ".", "."],
    # ]

    # fixed_map = [
    #     [".", ".", "W", ".", "P", ".", ".", "."],
    #     ["P", ".", ".", ".", "P", ".", ".", "."],
    #     [".", ".", ".", ".", "P", ".", "G", "."],
    #     [".", "W", ".", ".", "P", "P", ".", "."],
    #     [".", ".", ".", "P", "P", ".", ".", "."],
    #     [".", ".", ".", "P", ".", ".", "P", "."],
    #     [".", "W", ".", ".", ".", ".", ".", "."],
    #     [".", ".", ".", ".", "P", ".", ".", "."],
    # ]
    # env.initialize_from_map(fixed_map)
    agent = Agent(K=args.k)

    agent.play(env)
    if agent.winning:
        print("You win!")
    else:
        print("Game Over!")