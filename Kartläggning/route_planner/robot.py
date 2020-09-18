class Robot():

    def __init__(self):
        self.pos = [0, 0]
        self.direction = 0
        self.goals = [{
            'pos': [0, 0],
            'route': [],
            'cost': 0
        }]
        self.current_route = []

    def update_pos(self, pos=False, direction=False):
        if pos:
            self.pos = pos
        if direction:
            self.direction = direction
    
    def append_goal(self, goal):
        self.goals.append(goal)

    def sort_goals(self):
        self.goals = sorted(self.goals, key=lambda item: item["cost"])

    def update_route(self):
        self.current_route = self.goals[0]["route"]