class Settings:
    """Class that holds all the settings."""

    def __init__(self):
        self.map_width = 6
        self.map_height = 6

        self.screen_width = 1200
        self.toolbar_width = 300
        self.screen_height = 900

        self.bg_color = 100, 100, 100
        self.unset_color = 50, 50, 50
        self.unknown_color = 110, 110, 110
        self.node_color = 0, 255, 0

        self.part_width = int(
            (self.screen_width-self.toolbar_width)/self.map_width)
        self.part_height = int(self.screen_height/self.map_height)
        self.img_parts_path = 'images/parts/'
        self.img_obj_path = 'images/placable_objects/'

        self.node_line_thickness = 3
