# from gui import *
from execute import *
if __name__ == "__main__":
    main()



# if __name__ == "__main__":
    # # Khởi tạo môi trường và agent
    # args = parse_args()

    # # env = Environment(N=args.n, K=args.k, p=args.p, map_id=args.map_id)  # 8x8 grid
    # env_original = Environment(N=args.n, K=args.k, p=args.p, map_id=args.map_id)
    # print("Running Smart Agent")
    # env_for_smart = copy.deepcopy(env_original)
    # smart_agent = Agent(K=args.k)
    # smart_result = run_agent(smart_agent, env_for_smart)

    # print("Running Random Agent")
    # env_for_random = copy.deepcopy(env_original)
    # random_agnet = RandomAgent()
    # random_result = run_agent(random_agnet, env_for_random)

    # print("\n=====COMPARISON=======")
    # print(f"Smart Agent: {smart_result}")
    # print(f"Random Agent: {random_result}")
#     env = Environment()
#     fixed_map = [
#         [".", ".", "P", ".", "P", ".", ".", "."],
#         [".", ".", "W", ".", "P", ".", ".", "."],
#         [".", ".", "P", ".", "P", ".", "G", "."],
#         ["P", "W", "P", ".", "P", "P", ".", "."],
#         ["P", "P", "P", "P", "P", ".", ".", "."],
#         [".", ".", ".", "P", ".", ".", "P", "."],
#         [".", "W", ".", ".", ".", ".", ".", "."],
#         [".", ".", ".", ".", "P", ".", ".", "."],
#     ]

#     fixed_map = [
#         [".", ".", "W", ".", "P", ".", ".", "."],
#         ["P", ".", ".", ".", "P", ".", ".", "."],
#         [".", ".", ".", ".", "P", ".", "G", "."],
#         [".", "W", ".", ".", "P", "P", ".", "."],
#         [".", ".", ".", "P", "P", ".", ".", "."],
#         [".", ".", ".", "P", ".", ".", "P", "."],
#         [".", "W", ".", ".", ".", ".", ".", "."],
#         [".", ".", ".", ".", "P", ".", ".", "."],
#     ]
#     env.initialize_from_map(fixed_map)
    
#     agent = Agent(K=args.k)

#     agent.play(env)
#     if agent.winning:
#         print("You win!")
#     else:
#         print("Game Over!")