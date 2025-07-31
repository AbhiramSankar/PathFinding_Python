import random
import math
import config
from utils.metrics import path_cost

# Directions for movement: Up, Right, Down, Left
DIRECTIONS = [(0, -1), (1, 0), (0, 1), (-1, 0)]

def random_solution(length):
    """Generate a random sequence of directions."""
    return [random.randint(0, len(DIRECTIONS) - 1) for _ in range(length)]

def decode_path(solution, grid, start, goal):
    """Convert direction sequence into actual path."""
    x, y = start
    path = [(x, y)]
    for move in solution:
        dx, dy = DIRECTIONS[move]
        nx, ny = x + dx, y + dy
        if 0 <= nx < grid.width and 0 <= ny < grid.height:
            node = grid.get_node(nx, ny)
            if not node.is_obstacle:
                x, y = nx, ny
                path.append((x, y))
                if (x, y) == goal:
                    break
    return path

def fitness(solution, grid, start, goal):
    """Fitness = path cost + penalty if goal not reached."""
    path = decode_path(solution, grid, start, goal)
    cost = path_cost(path, grid)
    if path[-1] != goal:  # Penalize if goal not reached
        gx, gy = goal
        lx, ly = path[-1]
        penalty = math.hypot(gx - lx, gy - ly) * max(grid.width, grid.height)
        cost += penalty
    return cost, path

def ssa_pathfinding(grid, start=None, goal=None):
    if start is None:
        start = config.START
    if goal is None:
        goal = config.GOAL

    # SSA Parameters (from paper)
    pop_size = getattr(config, "SSA_POP_SIZE", 30)
    max_iter = getattr(config, "SSA_ITERATIONS", 100)
    max_steps = getattr(config, "MAX_STEPS_SSA", 50)

    PD = int(pop_size * 0.2)  # 20% Producers
    SD = int(pop_size * 0.1)  # 10% Aware of danger
    ST = 0.8                  # Safety threshold
    alpha = 0.8               # Alpha from paper

    # Initialize population
    population = [random_solution(max_steps) for _ in range(pop_size)]
    fitness_values = []
    paths = []
    for sol in population:
        f, p = fitness(sol, grid, start, goal)
        fitness_values.append(f)
        paths.append(p)

    # Best solution
    best_idx = min(range(pop_size), key=lambda i: fitness_values[i])
    best_solution = population[best_idx][:]
    best_path = paths[best_idx][:]
    best_score = fitness_values[best_idx]

    convergence = [best_score]
    iterations = 0

    for t in range(max_iter):
        # Dynamic Environment Update
        if hasattr(grid, "update_dynamic"):
            grid.update_dynamic()

        # Sort by fitness
        sorted_idx = sorted(range(pop_size), key=lambda i: fitness_values[i])
        X_best = population[sorted_idx[0]][:]
        X_worst = population[sorted_idx[-1]][:]

        R2 = random.random()  # Alarm value

        # === Update Producers ===
        for rank, i in enumerate(sorted_idx[:PD]):
            new_sol = population[i][:]
            for j in range(len(new_sol)):
                if R2 < ST:
                    # Wide search mode: equation (3)
                    if random.random() < math.exp(-rank / (alpha * max_iter)):
                        new_sol[j] = random.randint(0, len(DIRECTIONS) - 1)
                else:
                    # Escape predator: equation (3)
                    Q = random.gauss(0, 1)
                    new_sol[j] = random.randint(0, len(DIRECTIONS) - 1)
            population[i] = new_sol

        # === Update Scroungers ===
        for idx, i in enumerate(sorted_idx[PD:], start=PD):
            new_sol = population[i][:]
            if i > pop_size // 2:
                # Eq. (4): Scrounger moves toward worst
                for j in range(len(new_sol)):
                    if random.random() < 0.2:
                        new_sol[j] = random.choice(X_worst)
            else:
                # Follow best solution
                for j in range(len(new_sol)):
                    if random.random() < 0.5:
                        new_sol[j] = X_best[j]
            population[i] = new_sol

        # === Danger-aware sparrows ===
        danger_indices = random.sample(sorted_idx, SD)
        for i in danger_indices:
            new_sol = population[i][:]
            for j in range(len(new_sol)):
                if random.random() < 0.3:
                    K = random.uniform(-1, 1)
                    new_sol[j] = random.randint(0, len(DIRECTIONS) - 1)
            population[i] = new_sol

        # Evaluate all
        for i in range(pop_size):
            f, p = fitness(population[i], grid, start, goal)
            fitness_values[i] = f
            paths[i] = p
            if f < best_score:
                best_score = f
                best_solution = population[i][:]
                best_path = p[:]

        convergence.append(best_score)
        iterations += 1

    return best_path, convergence, iterations * pop_size

# Wrapper for compatibility
def find_path(grid, start=None, goal=None):
    return ssa_pathfinding(grid, start, goal)
