# Global configuration and hyperparameters

GRID_WIDTH = 30
GRID_HEIGHT = 30
OBSTACLE_DENSITY = 0.1
USE_HEIGHT_MAP = True
# MOVING_OBSTACLE_COUNT = 2  # Number of dynamic obstacles

START = (0, 0)
GOAL = (GRID_WIDTH - 1, GRID_HEIGHT - 1)

# Genetic Algorithm params
MAX_STEPS_GA = (GRID_WIDTH + GRID_HEIGHT) * 2
POPULATION_SIZE = 50
GENERATIONS = 100
MUTATION_RATE = 0.02

# Simulated Annealing params
TEMPERATURE = 100.0
COOLING_RATE = 0.995
MIN_TEMPERATURE = 0.1
