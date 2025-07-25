import argparse
import time
import os
import copy
from config import START, GOAL
from environment.grid import Grid
from algorithms import astar, adstar, dijkstra, genetic, simulated_annealing
from utils.metrics import path_cost
from utils.logger import log_results_csv, log_convergence_csv
from visualization import pygame_vis, matplotlib_vis
from utils.logger import plot_performance_metrics, plot_convergence


def main():
    parser = argparse.ArgumentParser(description="Pathfinding Optimization")
    parser.add_argument(
        "--algo",
        choices=["astar", "dijkstra", "ga", "sa"],
        default="astar",
        help="Which algorithm to run"
    )
    parser.add_argument(
        "--vis",
        choices=["pygame", "matplotlib"],
        default="matplotlib",
        help="Which visualization backend to use"
    )
    args = parser.parse_args()

    grid = Grid()

    if args.algo == "astar":
        path = astar.find_path(grid)
    elif args.algo == "dijkstra":
        path = dijkstra.find_path(grid)
    elif args.algo == "ga":
        path = genetic.find_path(grid)
    else:  # sa
        path = simulated_annealing.find_path(grid)

    if not path:
        print("No path found.")
        return

    if args.vis == "pygame":
        pygame_vis.display(grid, path)
    else:
        matplotlib_vis.animate(grid, path)
        
def run_all():
    grid = Grid()
    results = {}
    metrics = []

    # Run A*
    start_time = time.time()
    path_astar = astar.find_path(copy.deepcopy(grid), START, GOAL)
    time_astar = time.time() - start_time
    cost_astar = path_cost(path_astar, grid) if path_astar else float('inf')
    reached_astar = path_astar and path_astar[-1] == GOAL
    metrics.append({
        "Algorithm": "A*",
        "Time (s)": round(time_astar, 4),
        "Path Length": len(path_astar),
        "Path Cost": round(cost_astar, 2),
        "Reached Goal": "Yes" if reached_astar else "No"
    })
    results["A*"] = path_astar
    
    # Run AD*
    start_time = time.time()
    path_adstar = adstar.find_path(copy.deepcopy(grid), START, GOAL)
    time_adstar = time.time() - start_time
    cost_adstar = path_adstar and path_cost(path_adstar, grid) or float('inf')
    reached_adstar = path_adstar and path_adstar[-1] == GOAL
    metrics.append({
        "Algorithm": "AD*",
        "Time (s)": round(time_adstar, 4),
        "Path Length": len(path_adstar),
        "Path Cost": round(cost_adstar, 2),
        "Reached Goal": "Yes" if reached_adstar else "No"
    })
    results["AD*"] = path_adstar

    # Run Dijkstra
    start_time = time.time()
    path_dijkstra = dijkstra.find_path(copy.deepcopy(grid), START, GOAL)
    time_dijkstra = time.time() - start_time
    cost_dijkstra = path_cost(path_dijkstra, grid) if path_dijkstra else float('inf')
    reached_dijkstra = path_dijkstra and path_dijkstra[-1] == GOAL
    metrics.append({
        "Algorithm": "Dijkstra",
        "Time (s)": round(time_dijkstra, 4),
        "Path Length": len(path_dijkstra),
        "Path Cost": round(cost_dijkstra, 2),
        "Reached Goal": "Yes" if reached_dijkstra else "No"
    })
    results["Dijkstra"] = path_dijkstra

    # Run GA
    start_time = time.time()
    path_ga, history_ga = genetic.find_path(copy.deepcopy(grid), START, GOAL)
    time_ga = time.time() - start_time
    cost_ga = path_cost(path_ga, grid) if path_ga else float('inf')
    reached_ga = path_ga and path_ga[-1] == GOAL
    metrics.append({
        "Algorithm": "GA",
        "Time (s)": round(time_ga, 4),
        "Path Length": len(path_ga),
        "Path Cost": round(cost_ga, 2),
        "Reached Goal": "Yes" if reached_ga else "No"
    })
    results["GA"] = path_ga
    log_convergence_csv("results/ga_convergence.csv", history_ga, "GA")

    # Run SA
    start_time = time.time()
    path_sa, history_sa = simulated_annealing.find_path(copy.deepcopy(grid), START, GOAL)
    time_sa = time.time() - start_time
    cost_sa = path_cost(path_sa, grid) if path_sa else float('inf')
    reached_sa = path_sa and path_sa[-1] == GOAL
    metrics.append({
        "Algorithm": "SA",
        "Time (s)": round(time_sa, 4),
        "Path Length": len(path_sa),
        "Path Cost": round(cost_sa, 2),
        "Reached Goal": "Yes" if reached_sa else "No"
    })
    results["SA"] = path_sa
    log_convergence_csv("results/sa_convergence.csv", history_sa, "SA")

    # Save summary metrics to CSV
    log_results_csv("results/performance_metrics.csv", metrics)

    plot_performance_metrics()
    plot_convergence()

    # Visualize
    run_game = pygame_vis.display_multiple(grid, results)
    if run_game == "run_matplotlib":
        matplotlib_vis.animate_multiple(grid, results)

if __name__ == "__main__":
    # main()
    run_all()
