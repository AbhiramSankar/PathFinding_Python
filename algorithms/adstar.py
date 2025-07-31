import math
import heapq
import itertools
from algorithms.base import PathfindingAlgorithm
from algorithms.astar import AStar
import config


class ADStar(PathfindingAlgorithm):
    def __init__(self, grid, start=None, goal=None, epsilon=2.5, epsilon_decay=0.5):
        super().__init__(grid, start, goal)
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.open_list = []
        self.incons = set()
        self.entry_map = {}
        self.counter = itertools.count()
        self.expanded_nodes = 0  # Track work units (node expansions)

    def heuristic(self, node):
        gx, gy = self.goal
        goal_height = self.grid.get_height(gx, gy)
        dx = gx - node.x
        dy = gy - node.y
        dz = goal_height - node.height
        return math.sqrt(dx * dx + dy * dy + dz * dz)

    def compute_key(self, node):
        return min(node.g, node.rhs) + self.epsilon * node.h

    def initialize_nodes(self):
        for row in self.grid.nodes:
            for n in row:
                n.g = float('inf')
                n.rhs = float('inf')
                n.h = self.heuristic(n)
                n.parent = None

    def insert_open(self, node):
        key = self.compute_key(node)
        count = next(self.counter)
        if self.entry_map.get((node.x, node.y)) == key:
            return  # Skip duplicate with same key
        heapq.heappush(self.open_list, (key, count, node))
        self.entry_map[(node.x, node.y)] = key

    def update_vertex(self, node):
        if (node.x, node.y) != self.goal:
            neighbors = self.grid.neighbors(node)
            node.rhs = min((nbr.g + self.cost(node, nbr)) for nbr in neighbors) if neighbors else float('inf')

        if node.g != node.rhs:
            if (node.x, node.y) not in self.incons:
                self.insert_open(node)
            else:
                self.incons.add((node.x, node.y))
        elif (node.x, node.y) in self.incons:
            self.incons.remove((node.x, node.y))

    def cost(self, a, b, alpha=2.0, beta=1.0, power=2):
        dx = b.x - a.x
        dy = b.y - a.y
        dz = abs(b.height - a.height)

        base_dist = math.sqrt(dx ** 2 + dy ** 2)
        penalty_factor = 1 + alpha * (dz ** power)
        segment_cost = (base_dist * penalty_factor) + (beta * (dz ** power))
        return segment_cost

    def compute_shortest_path(self, start_node, max_iter=50000, max_open=80000):
        iterations = 0
        while self.open_list and (
            self.open_list[0][0] < self.compute_key(start_node)
            or start_node.rhs != start_node.g
        ):
            if iterations > max_iter or len(self.open_list) > max_open:
                print("[AD*] Warning: compute_shortest_path cutoff reached.")
                break

            key, _, u = heapq.heappop(self.open_list)
            if self.entry_map.get((u.x, u.y)) != key:
                iterations += 1
                continue

            self.expanded_nodes += 1  # Count expansion

            if u.g > u.rhs:
                u.g = u.rhs
                for nbr in self.grid.neighbors(u):
                    self.update_vertex(nbr)
            else:
                u.g = float('inf')
                self.update_vertex(u)
                for nbr in self.grid.neighbors(u):
                    self.update_vertex(nbr)

            iterations += 1

    def improve_path(self, start_node):
        best_path = []
        phase = 0

        while self.epsilon > 1:
            print(f"[AD*] Phase {phase}: ε={self.epsilon:.2f}, OPEN={len(self.open_list)}")
            self.compute_shortest_path(start_node)

            if start_node.g != float('inf'):
                best_path = self.extract_path(start_node)

            # Move INCONS to OPEN for next phase
            for (x, y) in self.incons:
                node = self.grid.get_node(x, y)
                self.insert_open(node)
            self.incons.clear()

            self.epsilon = max(1, self.epsilon - self.epsilon_decay)
            phase += 1

        # Final phase with ε = 1 for optimality
        print("[AD*] Final phase: ε=1.0, ensuring optimal path...")
        self.epsilon = 1
        self.compute_shortest_path(start_node)

        if start_node.g != float('inf'):
            best_path = self.extract_path(start_node)

        return best_path

    def find_path(self):
        self.expanded_nodes = 0
        self.initialize_nodes()
        start_node = self.grid.get_node(*self.start)
        goal_node = self.grid.get_node(*self.goal)
        goal_node.rhs = 0.0
        self.insert_open(goal_node)

        best_path = self.improve_path(start_node)

        if start_node.g == float('inf') and not best_path:
            print("[AD*] No valid path after AD*. Falling back to A*...")
            path = AStar(self.grid, self.start, self.goal).find_path()
            return path, self.expanded_nodes

        print("[AD*] Returning best path found.")
        final_path = best_path if best_path else self.extract_path(start_node)
        return final_path, self.expanded_nodes

    def replan_after_changes(self, changed_nodes):
        for coords in changed_nodes:
            node = self.grid.get_node(*coords)
            self.update_vertex(node)
        start_node = self.grid.get_node(*self.start)
        return self.improve_path(start_node)

    def extract_path(self, start_node):
        path = [self.start]
        current = start_node
        while (current.x, current.y) != self.goal:
            neighbors = self.grid.neighbors(current)
            if not neighbors:
                break
            current = min(neighbors, key=lambda nbr: nbr.g + self.cost(current, nbr))
            if current.g == float('inf'):
                break
            path.append((current.x, current.y))
        return path


def find_path(grid, start=None, goal=None):
    planner = ADStar(grid, start=start, goal=goal)
    return planner.find_path()
