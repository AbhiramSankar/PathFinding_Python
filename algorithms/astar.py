import math
import heapq
from algorithms.base import PathfindingAlgorithm

class AStar(PathfindingAlgorithm):
    def heuristic(self, node):
        gx, gy = self.goal
        dx = gx - node.x
        dy = gy - node.y
        dh = self.grid.get_height(gx, gy) - node.height
        return math.sqrt(dx*dx + dy*dy + dh*dh)

    def find_path(self):
        # Reset nodes
        for row in self.grid.nodes:
            for n in row:
                n.g = float('inf')
                n.h = 0.0
                n.f = float('inf')
                n.parent = None

        start_node = self.grid.get_node(*self.start)
        goal_node = self.grid.get_node(*self.goal)

        start_node.g = 0.0
        start_node.h = self.heuristic(start_node)
        start_node.f = start_node.h

        open_set = [(start_node.f, start_node)]
        closed = set()
        expanded_nodes = 0  # Track work units

        while open_set:
            _, current = heapq.heappop(open_set)
            expanded_nodes += 1  # Count node expansions

            if (current.x, current.y) == self.goal:
                path = []
                while current:
                    path.append((current.x, current.y))
                    current = current.parent
                return path[::-1], expanded_nodes  # Return path + work units

            closed.add((current.x, current.y))

            for nbr in self.grid.neighbors(current):
                if (nbr.x, nbr.y) in closed:
                    continue
                dz = abs(nbr.height - current.height)
                dx = nbr.x - current.x
                dy = nbr.y - current.y

                base_dist = math.sqrt(dx ** 2 + dy ** 2)
                penalty_factor = 1 + 2.0 * (dz ** 2)  # alpha = 2.0, power = 2
                segment_cost = (base_dist * penalty_factor) + (1.0 * (dz ** 2))  # beta = 1.0

                tentative_g = current.g + segment_cost

                if tentative_g < nbr.g:
                    nbr.parent = current
                    nbr.g = tentative_g
                    nbr.h = self.heuristic(nbr)
                    nbr.f = nbr.g + nbr.h
                    heapq.heappush(open_set, (nbr.f, nbr))

        return [], expanded_nodes

def find_path(grid, start=None, goal=None):
    return AStar(grid, start, goal).find_path()
