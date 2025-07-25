class PathfindingAlgorithm:
    def __init__(self, grid, start=None, goal=None):
        import config
        self.grid = grid
        self.start = start if start is not None else config.START
        self.goal = goal if goal is not None else config.GOAL

    def find_path(self):
        raise NotImplementedError
