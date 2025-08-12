from state import *
import argparse
import time
import copy

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

def run_agent(agent, env):
    start = time.perf_counter()
    agent.play(env)
    end = time.perf_counter()
    return {
        "score": agent.score,
        "time": round(end - start, 6),
        "steps": agent.action_count,
        "win": agent.climbed_out
    }


def main():
    args = parse_args()
    # Khởi tạo môi trường và agent
    args = parse_args()

    # env = Environment(N=args.n, K=args.k, p=args.p, map_id=args.map_id)  # 8x8 grid
    env_original = Environment(N=args.n, K=args.k, p=args.p, map_id=args.map_id)
    print("Running Smart Agent")
    env_for_smart = copy.deepcopy(env_original)
    smart_agent = Agent(K=args.k)
    smart_result = run_agent(smart_agent, env_for_smart)

    print("Running Random Agent")
    env_for_random = copy.deepcopy(env_original)
    random_agnet = RandomAgent()
    random_result = run_agent(random_agnet, env_for_random)

    print("\n=====COMPARISON=======")
    print(f"Smart Agent: {smart_result}")
    print(f"Random Agent: {random_result}")