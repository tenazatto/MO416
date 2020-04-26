from search import Problem


class PacmanProblem(Problem):
    """Finding a path on a 2D grid with obstacles. Obstacles are (x, y) cells."""

    def __init__(self, initial=(0, 0), goal=(30, 30), obstacles=(), **kwds):
        Problem.__init__(self, initial=initial, goal=goal, **kwds)
        self.obstacles = obstacles

    directions = [(0, -1), (-1, 0), (1, 0), (0, +1)]

    def action_cost(self, s, action, s1): return straight_line_distance(s, s1)

    def h(self, node): return straight_line_distance(node.state, self.goal)

    def result(self, state, action):
        "Both states and actions are represented by (x, y) pairs."
        return action if action not in self.obstacles else state

    def actions(self, state):
        """You can move one cell in any of `directions` to a non-obstacle cell."""
        x, y = state
        return {(x + dx, y + dy) for (dx, dy) in self.directions} - self.obstacles

def straight_line_distance(A, B):
    "Straight-line distance between two points."
    return sum(abs(a - b)**2 for (a, b) in zip(A, B)) ** 0.5