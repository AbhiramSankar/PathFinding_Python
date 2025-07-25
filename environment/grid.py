import random
from environment.node import Node
from environment.map_loader import load_heightmap
import config

class Grid:
    def __init__(self):
        self.width = config.GRID_WIDTH
        self.height = config.GRID_HEIGHT
        self.nodes = [[None for _ in range(self.width)] for _ in range(self.height)]
        self._generate()

    def _generate(self):
        # Load heights
        if config.USE_HEIGHT_MAP:
            heights = load_heightmap()
        else:
            heights = [[0.0]*self.width for _ in range(self.height)]

        for y in range(self.height):
            for x in range(self.width):
                h = heights[y][x]
                # Never place obstacle on start or goal
                is_obs = (
                    random.random() < config.OBSTACLE_DENSITY
                    and (x, y) not in (config.START, config.GOAL)
                )
                self.nodes[y][x] = Node(x, y, h, is_obs)

    def get_node(self, x, y):
        return self.nodes[y][x]

    def neighbors(self, node):
        dirs = [(0,-1),(1,0),(0,1),(-1,0)]
        result = []
        for dx, dy in dirs:
            nx, ny = node.x + dx, node.y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                nbr = self.get_node(nx, ny)
                if not nbr.is_obstacle:
                    result.append(nbr)
        return result

    def get_height(self, x, y):
        return self.get_node(x, y).height
