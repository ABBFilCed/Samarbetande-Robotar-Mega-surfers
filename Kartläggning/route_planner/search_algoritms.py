import util

def DFSSearch(node, graph, goal):
    frontier = util.Stack()
    exploredNodes = []
    startState = node
    startNode = (startState, [], 0)
    frontier.push(startNode)
    while not frontier.isEmpty():
        currentState, actions, currentCost = frontier.pop()
        print("Current state is: ", currentState)
        if currentState not in exploredNodes:
            exploredNodes.append(currentState)

            if goal == currentState:
                print(startState, "to", goal, actions, "Cost:", currentCost)
                return actions
        
            else:
                successors = graph[currentState]
                for succState, succCost in successors:
                    newAction = actions + [succState]
                    newCost = currentCost + succCost
                    newNode = (succState, newAction, newCost)
                    print(newNode)
                    frontier.push(newNode)
    
    return actions

def BFSSearch(node, graph, goal):
    frontier = util.Queue()
    exploredNodes = []
    startState = node
    startNode = (startState, [], 0)
    frontier.push(startNode)
    while not frontier.isEmpty():
        currentState, actions, currentCost = frontier.pop()
        print("Current state is: ", currentState)
        if currentState not in exploredNodes:
            exploredNodes.append(currentState)

            if goal == currentState:
                print(startState, "to", goal, actions, "Cost:", currentCost)
                return actions
        
            else:
                successors = graph[currentState]
                for succState, succCost in successors:
                    newAction = actions + [succState]
                    newCost = currentCost + succCost
                    newNode = (succState, newAction, newCost)
                    print(newNode)
                    frontier.push(newNode)
    
    return actions

def UCSearch(node, graph, goal):
    frontier = util.PriorityQueue()
    exploredNodes = {}
    startState = node
    startNode = (startState, [], 0)
    frontier.push(startNode, 0)
    while not frontier.isEmpty():
        currentState, actions, currentCost = frontier.pop()
        print("Current state is: ", currentState)
        if currentState not in exploredNodes or currentCost < exploredNodes[currentState]:
            exploredNodes[currentState] = currentCost

            if goal == currentState:
                print(startState, "to", goal, actions, "Cost:", currentCost)
                return actions
        
            else:
                successors = graph[currentState]
                for succState, succCost in successors:
                    newAction = actions + [succState]
                    newCost = currentCost + succCost
                    newNode = (succState, newAction, newCost)
                    print(newNode)
                    frontier.push(newNode, newCost)
    
    return actions


def nullHeuristic(state):
    return 0

def GSearch(node, graph, goal, heuristic = nullHeuristic):
    frontier = util.PriorityQueue()
    exploredNodes = []
    startState = node
    startNode = (startState, [], 0)
    frontier.push(startNode, 0)
    while not frontier.isEmpty():
        currentState, actions, currentCost = frontier.pop()
        exploredNodes.append((currentState, currentCost)) 
        print("Current state is: ", currentState)

        if goal == currentState:
            print(startState, "to", goal, actions, "Cost:", currentCost)
            return actions
    
        else:
            successors = graph[currentState]
            for succState, succCost in successors:
                newAction = actions + [succState]
                newCost = currentCost+succCost
                newNode = (succState, newAction, newCost)

                G_explored = False

                for explored in exploredNodes:
                    exploredState, exploredCost = explored
                    if succState == exploredState:
                        G_explored = True
                    
                if not G_explored:
                    print(newNode)
                    frontier.push(newNode, newCost+heuristic(succState))
                    exploredNodes.append((succState, newCost))
    
    return actions

def ASearch(node, graph, goal, heuristic = nullHeuristic):
    frontier = util.PriorityQueue()
    exploredNodes = []
    startState = node
    startNode = (startState, [], 0)
    frontier.push(startNode, 0)
    while not frontier.isEmpty():
        currentState, actions, currentCost = frontier.pop()
        exploredNodes.append((currentState, currentCost)) 
        print("Current state is: ", currentState)

        if goal == currentState:
            print(startState, "to", goal, actions, "Cost:", currentCost)
            return actions
    
        else:
            successors = graph[currentState]
            for succState, succCost in successors:
                newAction = actions + [succState]
                newCost = currentCost+succCost
                newNode = (succState, newAction, newCost)

                A_explored = False

                for explored in exploredNodes:
                    exploredState, exploredCost = explored
                    if succState == exploredState and newCost >= exploredCost:
                        A_explored = True
                    
                if not A_explored:
                    print(newNode)
                    frontier.push(newNode, newCost+heuristic(succState))
                    exploredNodes.append((succState, newCost))
    
    return actions
