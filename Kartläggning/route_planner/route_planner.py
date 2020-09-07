import util
import search_algoritms
import numpy as np
import json
import random
import tkinter


def CreateWorld(width, height, costs=False):
    world = np.zeros((height, width))
    if costs == True:
        for r in range(0, len(world)):
            for c in range(0, len(world[r])):
                world[r][c] = random.randint(0, 8)
    print(world)
    return world


def CreateNodes(world):
    nodes_dict = {}

    for r in range(0, len(world)):
        for c in range(0, len(world[r])):
            if world[r][c] != 8:
                node = []
                if c < len(world) - 1 and world[r][c+1] != 8:
                    node.append([str([r, c+1]), 1 + world[r][c+1]])
                if c > 0 and world[r][c-1] != 8:
                    node.append([str([r, c-1]), 1 + world[r][c-1]])
                if r < len(world[r]) - 1 and world[r+1][c] != 8:
                    node.append([str([r+1, c]), 1 + world[r+1][c]])
                if r > 0 and world[r-1][c] != 8:
                    node.append([str([r-1, c]), 1 + world[r-1][c]])
                nodes_dict[str([r, c])] = node

    return nodes_dict

#nodes = CreateNodes(CreateWorld(8, 8))

#nodes = CreateNodes(CreateWorld(8, 8, True))

n_rows = 8
world = CreateWorld(n_rows, n_rows)
world[3][0] = 3 
nodes = CreateNodes(world)

for node in nodes:
    print(node + " : ", nodes[node])
# print(json.loads(node))

start_pos = "[1, 1]"
for i in range(0, len(world)):
    for j in range(0, i):
        if world[i][j] == 3:
            goal_pos = str([i, j])
            print (goal_pos)
            break

#search_algoritms.DFSSearch(start_pos, nodes, goal_pos)

#search_algoritms.BFSSearch(start, nodes, end)

#search_algoritms.UCSearch(start, nodes, end)

#search_algoritms.GSearch(start_pos, nodes, goal)

search_algoritms.ASearch(start_pos, nodes, goal_pos)
