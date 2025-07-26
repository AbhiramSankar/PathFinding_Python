import math
import heapq
from algorithms.base import PathfindingAlgorithm


class ADStar(PathfindingAlgorithm):
    def __init__(self, grid, start=None, goal=None, epsilon=2.0, epsilon_decay=0.5):
        super().__init__(grid, start, goal)
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay

    def heuristic(self, node):
        gx, gy = self.goal
        dx = gx - node.x
        dy = gy - node.y
        dh = self.grid.get_height(gx, gy) - node.height
        return math.sqrt(dx * dx + dy * dy + dh * dh)

    def compute_key(self, node):
        return min(node.g, node.rhs) + self.epsilon * node.h

    def find_path(self):
        # Initialize nodes
        for row in self.grid.nodes:
            for n in row:
                n.g = float('inf')
                n.rhs = float('inf')
                n.h = self.heuristic(n)
                n.parent = None

        start_node = self.grid.get_node(*self.start)
        goal_node = self.grid.get_node(*self.goal)
        start_node.rhs = 0.0

        open_list = []
        incons_list = set()
        entry_map = {}  # track valid keys to avoid processing stale nodes

        def push(node):
            key = self.compute_key(node)
            heapq.heappush(open_list, (key, node))
            entry_map[(node.x, node.y)] = key

        push(start_node)

        prev_cost = float('inf')
        while self.epsilon >= 1:
            # Improve solution for current epsilon
            while open_list and goal_node.g > open_list[0][0]:
                key, u = heapq.heappop(open_list)

                # Skip outdated entry
                if entry_map.get((u.x, u.y), None) != key:
                    continue

                if u.g > u.rhs:
                    u.g = u.rhs
                    for nbr in self.grid.neighbors(u):
                        self.update_vertex(nbr, push, incons_list)
                else:
                    u.g = float('inf')
                    self.update_vertex(u, push, incons_list)
                    for nbr in self.grid.neighbors(u):
                        self.update_vertex(nbr, push, incons_list)

            # Print progress and check stopping criteria
            if goal_node.g < float('inf'):
                print(f"Epsilon={self.epsilon:.2f}, Path cost={goal_node.g:.2f}")
                if abs(prev_cost - goal_node.g) < 1e-3:  # No improvement
                    break
                prev_cost = goal_node.g

                # Reduce epsilon for next improvement
                if self.epsilon == 1:
                    break
                self.epsilon = max(1, self.epsilon - self.epsilon_decay)

                # Reinsert inconsistency list into open list
                for coords in incons_list:
                    node = self.grid.get_node(*coords)
                    push(node)
                incons_list.clear()
            else:
                break

        return self.extract_path(goal_node)

    def update_vertex(self, node, push, incons_list):
        if (node.x, node.y) != self.start:
            if self.grid.neighbors(node):
                node.rhs = min(nbr.g + self.cost(node, nbr) for nbr in self.grid.neighbors(node))
            else:
                node.rhs = float('inf')

        if node.g != node.rhs:
            push(node)
            incons_list.add((node.x, node.y))

    def cost(self, a, b):
        dz = b.height - a.height
        return math.sqrt((b.x - a.x) ** 2 + (b.y - a.y) ** 2 + dz * dz)

    def extract_path(self, goal_node):
        if goal_node.g == float('inf'):
            return []

        # Backtrack path from goal to start using best neighbor heuristic
        path = [(goal_node.x, goal_node.y)]
        current = goal_node
        while (current.x, current.y) != self.start:
            neighbors = self.grid.neighbors(current)
            if not neighbors:
                break
            current = min(neighbors, key=lambda nbr: nbr.g + self.cost(current, nbr))
            path.append((current.x, current.y))
        return path[::-1]


def find_path(grid, start=None, goal=None):
    return ADStar(grid, start, goal).find_path()