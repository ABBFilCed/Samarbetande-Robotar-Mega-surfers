import random


class Settings:
    """Class that holds all the settings."""

    def __init__(self):
        # Map size.
        self.map_width = 6
        self.map_height = 6

        # Screen sizes.
        self.screen_width = 1200
        self.toolbar_width = 300
        self.screen_height = 900
        self.part_width = int(
            (self.screen_width-self.toolbar_width)/self.map_width)
        self.part_height = int(self.screen_height/self.map_height)
        self.node_line_thickness = 3

        # Color settings.
        self.bg_color = 100, 100, 100
        self.unset_color = 50, 50, 50
        self.unknown_color = 110, 110, 110
        self.node_color = 0, 255, 0
        self.route_color = 255, 0, 0

        # File paths.
        self.img_parts_path = 'images/parts/'
        self.img_obj_path = 'images/placable_objects/'

        # Decides which route to show.
        self.view_route = 0

        # Mqtt settings
        self.broker = "maqiatto.com"
        self.username = "jesper.jansson@abbindustrigymnasium.se"
        self.password = "1234"
        self.topic = "map"
        self.robot_1_topic = "robot1"

    def get_client_id(self):
        client_id = "backend" + str(random.randint(1111, 9999))
        return client_id
