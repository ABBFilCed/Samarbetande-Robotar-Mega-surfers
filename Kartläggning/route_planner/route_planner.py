import time

import pygame
import paho.mqtt.client as mqtt

from settings import Settings
from button import Button
from world import World
from nodes import Nodes
from robot import Robot
from mqtt import Mqtt
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

    world.matrix = [["601000", "100100", "100010", "100001", "100000", "100000"],
                    ["100000", "100000", "100100", "100000", "100000", "100000"],
                    ["100000", "100000", "100000", "100000", "100000", "100000"],
                    ["100000", "100000", "100000", "100000", "100000", "100000"],
                    ["100000", "100000", "100000", "100000", "100000", "100000"],
                    ["100000", "100000", "100000", "100000", "100000", "100000"]]

    # Create nodes for the world matrix.
    nodes = Nodes(world.matrix)

    # Make a new robot instance.
    robot = Robot()

    # Init and subscribe to mqtt broker.
    mqtt = Mqtt(settings.broker, settings.get_client_id(),
                settings.username, settings.password, settings.topic)

    buttons = []

    # Print out nodes to check if algoritm is correct.
    """   for node in nodes.nodes_dict:
        print(node + " : ", nodes.nodes_dict[node]) """

    while True:
        # main loop
        rf.update_map(world.matrix, nodes, mqtt.msgs, robot)
        rf.check_events(settings, robot, buttons, next_button, mqtt)
        rf.update_robot_route(world.matrix, nodes.nodes_dict, robot)
        buttons = rf.update_screen(screen, settings, world.matrix,
                                   nodes, next_button, robot)
        """for node in nodes.nodes_dict:
            print(node + " : ", nodes.nodes_dict[node])"""
        # if no more tasks are left, the mission is complete.
        if len(robot.goals) == 0:
            print("Mission Complete!")
            mqtt.client.loop_stop()
            mqtt.client.disconnect()
            break


run_route_planner()
