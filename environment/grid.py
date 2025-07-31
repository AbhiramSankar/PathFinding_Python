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
            # If no heightmap is used, generate random heights
            heights = [[random.uniform(0.0, 1.0) for _ in range(self.width)] for _ in range(self.height)]

        for y in range(self.height):
            for x in range(self.width):
                h = heights[y][x]
                is_obs = (
                    random.random() < config.OBSTACLE_DENSITY
                    and (x, y) not in (config.START, config.GOAL) # Never place obstacle on start or goal  
                )
                self.nodes[y][x] = Node(x, y, h, is_obs, is_obs)

        #Ensure START and GOAL heights are 0.0
        sx, sy = config.START
        gx, gy = config.GOAL
        self.nodes[sy][sx].height = 0.0
        self.nodes[gy][gx].height = 0.0

    def get_node(self, x, y):
        return self.nodes[y][x]

    def neighbors(self, node):
        dirs = [(0, -1), (1, 0), (0, 1), (-1, 0)]
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
