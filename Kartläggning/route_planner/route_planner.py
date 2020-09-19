import pygame

from settings import Settings
from button import Button
from world import World
from nodes import Nodes
from robot import Robot
import route_functions as rf


def run_route_planner():
    """Runs the whole program."""
    # Initialize global settings and screen.
    settings = Settings()
    pygame.init()
    screen = pygame.display.set_mode(
        (settings.screen_width, settings.screen_height))
    pygame.display.set_caption("Route Planner 1.1")

    # Make a next button.
    next_button = Button(settings, screen, "Next")

    # Hard coded map.
    world = World(settings.map_width, settings.map_height)
    world.matrix = [["601", "500", "310", "614", "600", "610"],
                    ["530", "400", "310", "510", "533", "100"],
                    ["100", "100", "102", "530", "620", "100"],
                    ["100", "100", "100", "100", "100", "100"],
                    ["100", "100", "100", "100", "100", "100"],
                    ["100", "100", "100", "100", "100", "100"]]

    # Create nodes for the world matrix.
    nodes = Nodes(world.matrix)

    # Make a new robot instance.
    robot = Robot()

    # Print out nodes to check if algoritm is correct.
    """   for node in nodes.nodes_dict:
        print(node + " : ", nodes.nodes_dict[node]) """

    while True:
        # main loop
        rf.update_map(world.matrix, nodes)
        rf.check_events(settings, robot)
        rf.update_robot_route(world.matrix, nodes.nodes_dict, robot)
        rf.update_screen(screen, settings, world.matrix,
                         nodes, next_button, robot)
        # if no more tasks are left, the mission is complete.
        if len(robot.goals) == 0:
            print("Mission Complete!")
            break


run_route_planner()
