import copy
import time
import os
from dataclasses import dataclass
from core.environment import *
from core.agent import *
from typing import List

@dataclass
class ExperimentResult:
    score: int
    actions: int
    time: float
    success: bool

def run_experiments(N: int, K: int, p: float, mode: str, M: int) -> Tuple[List, List]:
    """
        Chạy M lần trên map với các tham số N, K, p, và mode
        Trả về 2 list kết quả của smart agent và random agent, mỗi list sẽ có M phần tử

        Mỗi phần tử kết quả là dict chứa score, steps, steps, time, win (success)
    """

    smart_agent_results: List[ExperimentResult] = []
    random_agent_results: List[ExperimentResult] = []

    is_advanced = (mode == "advanced")
    for i in range(M):
        print(f"Experiment {i + 1}/{M}")
        # 1. Initialize for 2 agents
        env_for_smart = Environment(N=N, K=K, p=p, advanced_mode=is_advanced)
        env_for_random = copy.deepcopy(env_for_smart)
        
        # 2. Smart agent
        print("Smart agent is running now.")
        smart_agent = Agent(K=K, is_moving_wumpus=is_advanced)
        start_time_smart = time.perf_counter()
        smart_agent.play(env_for_smart)
        end_time_smart = time.perf_counter()

        smart_result = ExperimentResult(
            score=smart_agent.score,
            actions=smart_agent.action_count,
            time=round(end_time_smart - start_time_smart, 6),
            success=smart_agent.climbed_out
        )
        smart_agent_results.append(smart_result)
        print("Smart agent stopped running.")

        # 3. Random Agent
        print("Random agent is running now")
        random_agent = RandomAgent()
        start_time_random = time.perf_counter()
        random_agent.play(env_for_random)
        end_time_random = time.perf_counter()

        random_result = ExperimentResult(
            score=random_agent.score,
            actions=random_agent.action_count,
            time=round(end_time_random - start_time_random, 6),
            success=random_agent.climbed_out
        )
        random_agent_results.append(random_result)
        print("Random agent stopeed running")
    
    return smart_agent_results, random_agent_results

def run_and_save_results(N: int, K: int, p: float, mode: str, M: int):
    # Now, shall we begin the experiment ? (Kiryu Sento)
    print(f"Let's start the experiment: N={N}, K={K}, mode='{mode}', M={M}")
    smart_results, random_results = run_experiments(N, K, p, mode, M)

    output_dir = "output"
    filename = os.path.join(output_dir, f"result_{mode}.txt")

    with open(filename, 'w', encoding='utf-8') as f:
        # Configure
        f.write("=" * 55 + "\n")
        f.write("Experiment Result\n")
        f.write("=" * 55 + "\n")
        f.write(f"Configure:\n")
        f.write(f" - Grid size(N): {N}.\n")
        f.write(f" - Number of wumpus(K): {K}.\n")
        f.write(f" - Pit density(p): {p}.\n")
        f.write(f" - Mode: {mode}.\n")
        f.write(f" - Number of test (M): {M}.\n")
        f.write("=" * 55 + "\n\n")

        # Details
        f.write("-" * 20 + "Smart Agent result" + "-" * 20 + "\n")
        for i, res in enumerate(smart_results):
            f.write(f"Attempt {i+1}: Win={res.success}, Score={res.score}, "
                    f"Actions={res.actions}, Time={res.time}s\n")
        f.write("-" * 20 + "Random Agent result" + "-" * 20 + "\n")
        for i, res in enumerate(random_results):
            f.write(f"Attempt {i+1}: Win={res.success}, Score={res.score}, "
                    f"Actions={res.actions}, Time={res.time}s\n")
        # --- SUMMARY---
        num_runs = M if M > 0 else 1
        avg_score_smart = sum(r.score for r in smart_results) / num_runs
        success_rate_smart = sum(1 for r in smart_results if r.success) / num_runs
        avg_score_random = sum(r.score for r in random_results) / num_runs
        success_rate_random = sum(1 for r in random_results if r.success) / num_runs
        avg_time_smart = sum(r.time for r in smart_results) / num_runs
        avg_time_random = sum(r.time for r in random_results) / num_runs
        avg_actions_smart = sum(r.actions for r in smart_results) / num_runs
        avg_actions_random = sum(r.actions for r in random_results) / num_runs

        f.write("\n\n" + "="*55 + "\n")
        f.write("SUMMARY\n")
        f.write("="*55 + "\n")
        f.write(f"{'Stats':<20} | {'Smart Agent':^18} | {'Random Agent':^18}\n")
        f.write("-" * 55 + "\n")
        f.write(f"{'Win rate (%)':<20} | {success_rate_smart:^18.3f} | {success_rate_random:^18.3f}\n")
        f.write(f"{'Average score':<20} | {avg_score_smart:^18.2f} | {avg_score_random:^18.2f}\n")
        f.write(f"{'Average time (s)':<20} | {avg_time_smart:^18.6f} | {avg_time_random:^18.6f}\n")
        f.write(f"{'Average actions':<20} | {avg_actions_smart:^18.2f} | {avg_actions_random:^18.2f}\n")

        f.write("="*55 + "\n") 

        # stats for win cases
        smart_win_results = [r for r in smart_results if r.success]
        random_win_results = [r for r in random_results if r.success]

        f.write(f"{'Number of wins':<20} | {len(smart_win_results):^18} | {len(random_win_results):^18}\n")
        avg_win_score_smart = (sum(r.score for r in smart_win_results if r.success) / len(smart_win_results)) if smart_win_results else -1
        avg_win_score_random = (sum(r.score for r in random_win_results if r.success) / len(random_win_results)) if random_win_results else -1
        f.write(f"{'Average win score':<20} | {avg_win_score_smart:^18.2f} | {avg_win_score_random:^18.2f}\n")
        avg_win_time_smart = (sum(r.time for r in smart_win_results if r.success) / len(smart_win_results)) if smart_win_results else -1
        avg_win_time_random = (sum(r.time for r in random_win_results if r.success) / len(random_win_results)) if random_win_results else -1
        f.write(f"{'Average win time (s)':<20} | {avg_win_time_smart:^18.6f} | {avg_win_time_random:^18.6f}\n")
        avg_win_actions_smart = (sum(r.actions for r in smart_win_results if r.success) / len(smart_win_results)) if smart_win_results else -1
        avg_win_actions_random = (sum(r.actions for r in random_win_results if r.success) / len(random_win_results)) if random_win_results else -1
        f.write(f"{'Average win actions':<20} | {avg_win_actions_smart:^18.2f} | {avg_win_actions_random:^18.2f}\n")

        # stats for loss cases
        smart_loss_results = [r for r in smart_results if not r.success]
        random_loss_results = [r for r in random_results if not r.success]

        f.write(f"{'Number of losses':<20} | {len(smart_loss_results):^18} | {len(random_loss_results):^18}\n")
        avg_loss_score_smart = (sum(r.score for r in smart_loss_results) / len(smart_loss_results)) if smart_loss_results else -1
        avg_loss_score_random = (sum(r.score for r in random_loss_results) / len(random_loss_results)) if random_loss_results else -1
        f.write(f"{'Average loss score':<20} | {avg_loss_score_smart:^18.2f} | {avg_loss_score_random:^18.2f}\n")
        avg_loss_time_smart = (sum(r.time for r in smart_loss_results) / len(smart_loss_results)) if smart_loss_results else -1
        avg_loss_time_random = (sum(r.time for r in random_loss_results) / len(random_loss_results)) if random_loss_results else -1
        f.write(f"{'Average loss time (s)':<20} | {avg_loss_time_smart:^18.6f} | {avg_loss_time_random:^18.6f}\n")
        avg_loss_actions_smart = (sum(r.actions for r in smart_loss_results) / len(smart_loss_results)) if smart_loss_results else -1
        avg_loss_actions_random = (sum(r.actions for r in random_loss_results) / len(random_loss_results)) if random_loss_results else -1
        f.write(f"{'Average loss actions':<20} | {avg_loss_actions_smart:^18.2f} | {avg_loss_actions_random:^18.2f}\n")
