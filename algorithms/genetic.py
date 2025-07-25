import random
import math
import config
from utils.metrics import path_cost

# Direction vectors: up, right, down, left
DIRECTIONS = [(0,-1), (1,0), (0,1), (-1,0)]

def random_individual():
    return [random.randrange(len(DIRECTIONS)) for _ in range(config.MAX_STEPS_GA)]

def decode_path(ind, grid, start, goal):
    x,y = start
    path = [(x,y)]
    for gene in ind:
        dx,dy = DIRECTIONS[gene]
        nx,ny = x+dx, y+dy
        if 0 <= nx < grid.width and 0 <= ny < grid.height:
            node = grid.get_node(nx,ny)
            if not node.is_obstacle:
                x,y = nx,ny
                path.append((x,y))
                if (x,y) == goal:
                    break
    return path

def fitness(ind, grid, start, goal):
    p = decode_path(ind, grid, start, goal)
    cost_val = path_cost(p, grid)
    if p[-1] != goal:
        # penalize by straight‑line distance
        gx,gy = goal; lx,ly = p[-1]
        penalty = math.hypot(gx-lx, gy-ly) * max(grid.width, grid.height)
        cost_val += penalty
    return cost_val, p

def tournament_selection(pop, scores, k=3):
    competitors = random.sample(list(zip(pop, scores)), k)
    competitors.sort(key=lambda x: x[1])
    return competitors[0][0]

def crossover(a, b):
    pt = random.randrange(1, len(a))
    return a[:pt] + b[pt:]

def mutate(ind):
    for i in range(len(ind)):
        if random.random() < config.MUTATION_RATE:
            ind[i] = random.randrange(len(DIRECTIONS))

def find_path(grid, start=None, goal=None):
    history = []
    if start is None: start = config.START
    if goal  is None: goal  = config.GOAL

    pop = [random_individual() for _ in range(config.POPULATION_SIZE)]
    best_score = float('inf')
    best_path = []

    for _ in range(config.GENERATIONS):
        scores = []
        best_gen_fitness = float('inf')

        for ind in pop:
            sc, p = fitness(ind, grid, start, goal)
            scores.append(sc)
            if sc < best_gen_fitness:
                best_gen_fitness = sc
                if sc < best_score and p[-1] == goal:
                    best_score = sc
                    best_path = p

        history.append(best_gen_fitness)

        # evolve
        new_pop = []
        for _ in range(config.POPULATION_SIZE):
            p1 = tournament_selection(pop, scores)
            p2 = tournament_selection(pop, scores)
            child = crossover(p1, p2)
            mutate(child)
            new_pop.append(child)
        pop = new_pop

    return best_path, history
