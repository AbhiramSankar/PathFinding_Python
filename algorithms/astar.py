import math
import heapq
from algorithms.base import PathfindingAlgorithm

class AStar(PathfindingAlgorithm):
    def __init__(self, grid, start=None, goal=None):
        super().__init__(grid, start, goal)

    def heuristic(self, node):
        gx, gy = self.goal
        dx = gx - node.x
        dy = gy - node.y
        dh = self.grid.get_height(gx, gy) - node.height
        return math.sqrt(dx * dx + dy * dy + dh * dh)

    def find_path(self):
        start_node = self.grid.get_node(*self.start)
        goal_node = self.grid.get_node(*self.goal)

        # Initialize costs
        for row in self.grid.nodes:
            for n in row:
                n.g = float('inf')
                n.parent = None

        start_node.g = 0
        open_list = []
        heapq.heappush(open_list, (0 + self.heuristic(start_node), start_node))

        while open_list:
            _, current = heapq.heappop(open_list)

            if (current.x, current.y) == self.goal:
                return self.extract_path(current)

            for neighbor in self.grid.neighbors(current):
                tentative_g = current.g + self.cost(current, neighbor)
                if tentative_g < neighbor.g:
                    neighbor.g = tentative_g
                    neighbor.parent = current
                    f_score = tentative_g + self.heuristic(neighbor)
                    heapq.heappush(open_list, (f_score, neighbor))

        return []  # No path found

    def extract_path(self, node):
        path = []
        while node:
            path.append((node.x, node.y))
            node = node.parent
        return path[::-1]

    def cost(self, a, b):
        dz = b.height - a.height
        return math.sqrt((b.x - a.x) ** 2 + (b.y - a.y) ** 2 + dz * dz)

def find_path(grid, start=None, goal=None):
    return AStar(grid, start, goal).find_path()
