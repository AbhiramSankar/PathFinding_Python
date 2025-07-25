import random
import math
import config
from utils.metrics import path_cost

# Direction vectors: up, right, down, left
DIRECTIONS = [(0,-1), (1,0), (0,1), (-1,0)]

def random_solution(length):
    return [random.randrange(len(DIRECTIONS)) for _ in range(length)]

def decode_path(ind, grid, start, goal):
    x, y = start
    path = [(x, y)]
    for gene in ind:
        dx, dy = DIRECTIONS[gene]
        nx, ny = x + dx, y + dy
        if 0 <= nx < grid.width and 0 <= ny < grid.height:
            node = grid.get_node(nx, ny)
            if not node.is_obstacle:
                x, y = nx, ny
                path.append((x, y))
                if (x, y) == goal:
                    break
    return path

def cost(ind, grid, start, goal):
    path = decode_path(ind, grid, start, goal)
    c = path_cost(path, grid)
    if path[-1] != goal:
        gx, gy = goal
        lx, ly = path[-1]
        penalty = math.hypot(gx - lx, gy - ly) * max(grid.width, grid.height)
        c += penalty
    return c, path

def find_path(grid, start=None, goal=None):
    if start is None:
        start = config.START
    if goal is None:
        goal = config.GOAL

    length = config.MAX_STEPS_GA
    current = random_solution(length)
    curr_cost, curr_path = cost(current, grid, start, goal)
    best = current[:]
    best_cost = curr_cost
    best_path = curr_path[:]

    T = config.TEMPERATURE
    history = []  # per-iteration best cost

    while T > config.MIN_TEMPERATURE:
        neighbor = current[:]
        idx = random.randrange(length)
        neighbor[idx] = random.randrange(len(DIRECTIONS))
        neigh_cost, neigh_path = cost(neighbor, grid, start, goal)
        delta = neigh_cost - curr_cost

        if delta < 0 or random.random() < math.exp(-delta / T):
            current = neighbor
            curr_cost = neigh_cost
            curr_path = neigh_path
            if curr_cost < best_cost and curr_path[-1] == goal:
                best = current[:]
                best_cost = curr_cost
                best_path = curr_path[:]

        history.append(curr_cost)
        T *= config.COOLING_RATE

    return best_path, history
