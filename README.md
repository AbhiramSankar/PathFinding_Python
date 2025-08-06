# Pathfinding Optimization in Dynamic Environments
This project compares traditional algorithms (A*, Dijkstra, AD*) with metaheuristic approaches (GA, SA, SSA) for dynamic pathfinding on a grid with moving obstacles.

## Demo
[▶ Watch Full Demo Video](https://drive.google.com/file/d/1nTeBKO5JrgagV_4PknOpedDLrDVqDrl5/view?usp=sharing)

![Watch the demo](results/simulation_20250731_081004.gif)

## Features
- **Dynamic environment** with moving obstacles and optional height map.
- **Algorithms implemented**:
  - **Baselines:** Dijkstra, A*, AD* (Anytime Dynamic A*)
  - **Metaheuristics:** Genetic Algorithm (GA), Simulated Annealing (SA), Sparrow Search Algorithm (SSA)
- **Visualization:** Real-time simulation using **Pygame**.
- **Performance metrics:** Path cost, computation time, convergence history.

## Project Structure
* [PathFinding_Python](./)
  
  * [algorithms](./algorithms/)
    * [adstar.py](./algorithms/adstar.py)           # Anytime Dynamic A* algorithm
    * [astar.py](./algorithms/astar.py)             # A* pathfinding algorithm
    * [base.py](./algorithms/base.py)               # Base class for all algorithms
    * [dijkstra.py](./algorithms/dijkstra.py)       # Dijkstra's algorithm
    * [genetic.py](./algorithms/genetic.py)         # Genetic Algorithm for pathfinding
    * [simulated_annealing.py](./algorithms/simulated_annealing.py) # SA-based pathfinding
    * [ssa.py](./algorithms/ssa.py)                 # Sparrow Search Algorithm for pathfinding

* [environment](./environment/)
    * [grid.py](./environment/grid.py)              # Grid structure with height map
    * [map_loader.py](./environment/map_loader.py)  # Loads and initializes map data
    * [node.py](./environment/node.py)              # Node representation with properties

* [ui](./ui/)
    * [buttons.py](./ui/buttons.py)                 # UI buttons for Pygame
    * [dynamic_vis.py](./ui/dynamic_vis.py)         # Dynamic environment and Core Pygame rendering visualization
    * [matplotlib_vis.py](./ui/matplotlib_vis.py)   # DEPRICATED - Mathplot environment for visualization
    * [obstacles.py](./ui/obstacles.py)             # Dynamic obstacle generation and handling
    * [pygame_vis.py](./ui/pygame_vis.py)           # DEPRICATED - Previous Pygame rendering logic

* [utils](./utils/)
    * [logger.py](./utils/logger.py)                # Logs performance and results to CSV
    * [metrics.py](./utils/metrics.py)              # Computes path cost and evaluation metrics
    * [path_utils.py](./utils/path_utils.py)        # Path normalization and helper functions
    * [timer.py](./utils/timer.py)                  # Utility for timing algorithm execution

* [results](./results/)                              # Stores outputs, convergence graphs, logs and demo

* [config.py](./config.py)                           # Global settings and hyperparameters
* [dy_main.py](./dy_main.py)                         # Entry point for the program
* [main.py](./main.py)                               # DEPRECATED - Previous entry point
* [README.md](./README.md)                           # Project documentation
* [requirements.txt](./requirements.txt)             # Python dependencies


## Requirements
- Python 3.8+
- Libraries: pygame, matplotlib, pandas, imageio.

## Installation

Clone the repository:
```bash
git clone https://github.com/AbhiramSankar/PathFinding_Python.git
cd PathFinding_Python
```
Install dependencies:
```bash
pip install -r requirements.txt
```
How to run:
```bash
python dy_main.py
```
