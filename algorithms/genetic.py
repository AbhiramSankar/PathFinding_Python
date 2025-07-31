import random
import math
from utils.metrics import path_cost
import config

# Directions: 0:Up, 1:Right, 2:Down, 3:Left
DIRECTIONS = [(0, -1), (1, 0), (0, 1), (-1, 0)]


def random_individual():
    return [random.randrange(len(DIRECTIONS)) for _ in range(config.MAX_STEPS_GA)]


def decode_path(ind, grid, start, goal):
    x, y = start
    path = [(x, y)]
    for move in ind:
        dx, dy = DIRECTIONS[move]
        nx, ny = x + dx, y + dy
        if 0 <= nx < grid.width and 0 <= ny < grid.height:
            node = grid.get_node(nx, ny)
            if node.is_obstacle:
                continue
            x, y = nx, ny
            path.append((x, y))
            if (x, y) == goal:
                break
    return path


def fitness(ind, grid, start, goal):
    path = decode_path(ind, grid, start, goal)
    cost_val = path_cost(path, grid)  # elevation-aware cost
    if path[-1] != goal:
        gx, gy = goal
        lx, ly = path[-1]
        penalty = math.hypot(gx - lx, gy - ly) * max(grid.width, grid.height)
        cost_val += penalty
    return cost_val, path


def tournament_selection(pop, scores, k=3):
    selected = random.sample(range(len(pop)), k)
    best_idx = min(selected, key=lambda i: scores[i])
    return pop[best_idx]


def two_point_crossover(a, b):
    pt1, pt2 = sorted(random.sample(range(len(a)), 2))
    return a[:pt1] + b[pt1:pt2] + a[pt2:]


def mutate(ind, rate):
    for i in range(len(ind)):
        if random.random() < rate:
            ind[i] = random.randrange(len(DIRECTIONS))


def find_path(grid, start=None, goal=None):
    if start is None:
        start = config.START
    if goal is None:
        goal = config.GOAL

    population = [random_individual() for _ in range(config.POPULATION_SIZE)]
    best_score = float('inf')
    best_path = []
    history = []
    no_improvement = 0

    for gen in range(config.GENERATIONS):
        scores = []
        best_gen_fitness = float('inf')

        for ind in population:
            sc, p = fitness(ind, grid, start, goal)
            scores.append(sc)
            if sc < best_gen_fitness:
                best_gen_fitness = sc
            if sc < best_score and p[-1] == goal:
                best_score = sc
                best_path = p
                no_improvement = 0

        history.append(best_gen_fitness)

        # Sort population by fitness
        ranked_idx = sorted(range(len(population)), key=lambda i: scores[i])
        elite_count = 2
        elite = [population[i][:] for i in ranked_idx[:elite_count]]

        # Adaptive mutation if no improvement for 20 gens
        mutation_rate = config.MUTATION_RATE
        if no_improvement > 20:
            mutation_rate = min(0.5, config.MUTATION_RATE * 2)
        no_improvement += 1

        # Generate new population
        new_population = elite[:]
        while len(new_population) < config.POPULATION_SIZE:
            p1 = tournament_selection(population, scores)
            p2 = tournament_selection(population, scores)
            child = two_point_crossover(p1, p2)
            mutate(child, mutation_rate)
            new_population.append(child)
        population = new_population

    # Calculate work units (proxy for computing power)
    work_units = config.GENERATIONS * config.POPULATION_SIZE

    return best_path, history, work_units


# Wrapper remains the same for compatibility
def find_path_wrapper(grid, start=None, goal=None):
    return find_path(grid, start, goal)
