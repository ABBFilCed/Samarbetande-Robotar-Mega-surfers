class Robot():

    def __init__(self):
        """Initializes start values."""
        self.pos = [0, 0]
        self.direction = 0
        self.goals = []
        self.short_term_goal = []
        self.current_route = []

    def update_pos(self, pos=False, direction=False):
        """Update position or/and direction."""
        if pos:
            self.pos = pos
        if direction:
            self.direction = direction

    def append_goal(self, goal):
        """Appends a new goal."""
        self.goals.append(goal)

    def sort_goals(self):
        """Sort goals by the length of the routes to them."""
        self.goals = sorted(self.goals, key=lambda item: item["cost"])

    def update_route(self):
        """Set the route to the shortest possible."""
        self.current_route = self.goals[0]["route"]
