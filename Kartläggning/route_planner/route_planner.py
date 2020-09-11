import json
import random

import pygame
import numpy as np

import util
import search_algoritms
from world import World
from nodes import Nodes
from settings import Settings
import route_functions as rf


def run_route_planner():
    """Runs the whole program."""
    settings = Settings()
    pygame.init()
    screen = pygame.display.set_mode(
        (settings.screen_width, settings.screen_height))
    pygame.display.set_caption("Route Planner 1.0")

    world = World(settings.map_width, settings.map_height)
    world.matrix = [["601", "500", "310", "614", "600", "610"],
                    ["530", "400", "310", "510", "533", "100"],
                    ["100", "100", "102", "530", "620", "100"],
                    ["100", "100", "100", "100", "100", "100"],
                    ["100", "100", "100", "100", "100", "100"],
                    ["630", "100", "100", "100", "100", "620"]]

    nodes = Nodes(world.matrix)

    while True:
        rf.update_matrix(world.matrix, nodes.nodes_dict)
        rf.update_screen(screen, settings, world.matrix, nodes)
        rf.check_events()


run_route_planner()


"""#for node in nodes.nodes_dict:
    #  print(node + " : ", nodes.nodes_dict[node])
    world.set_new_val(3, 0, "003")
    start_pos = "[1, 1]"
    for i in range(0, len(world.matrix)):
        for j in range(0, len(world.matrix[i])):
            if world.matrix[i][j] == "003":
                goal_pos = str([i, j])
                #print (goal_pos)
                break

    search_algoritms.ASearch(start_pos, nodes.nodes_dict, goal_pos)"""
