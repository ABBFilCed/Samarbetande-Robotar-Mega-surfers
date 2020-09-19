import sys
import json

import pygame

import search_algoritms


def update_map(matrix, nodes):
    """Updates if any new unknown parts are found."""
    for node in nodes.nodes_dict:
        for pos in nodes.nodes_dict[node]:
            pos = json.loads(pos[0])
            # Sets a reachable undiscovered part to a new value.
            if matrix[pos[0]][pos[1]] == "100":
                matrix[pos[0]][pos[1]] = "200"
    # Update nodes so the robot can navigate to unknown parts.
    nodes.update_nodes(matrix)


def new_route(robot, nodes_dict, goal_pos):
    """Creates a new route."""
    route, cost, = search_algoritms.ASearch(
        str(robot.pos), nodes_dict, goal_pos)
    # Starting position is not included in the route list returned from ASearch().
    route.insert(0, str(robot.pos))
    robot.append_goal(
        {
            'pos': goal_pos,
            'route': route,
            'cost': cost
        }
    )


def check_for_goals(world_matrix, nodes_dict, robot):
    """Append routes for new goals."""
    for r in range(0, len(world_matrix)):
        for c in range(0, len(world_matrix[r])):
            # Creates a new task if a lego piece or road is found.
            if int(world_matrix[r][c][2]) == 3 or int(world_matrix[r][c][0]) == 2:
                goal_pos = str([r, c])
                goals = []
                for goal in robot.goals:
                    goals.append(goal['pos'])
                # Only appends route for non-existing tasks.
                if not goal_pos in goals:
                    new_route(robot, nodes_dict, goal_pos)


def update_robot_route(world_matrix, nodes_dict, robot):
    """Find new tasks, sort by lenght, update current route if a shorter is found."""
    check_for_goals(world_matrix, nodes_dict, robot)
    if robot.goals:
        robot.sort_goals()
        robot.update_route()


def get_part_type(world_matrix, screen, settings, rect, r, c):
    """Returns filepath to correct path and orientation."""
    file_path = False
    rotations = False
    if world_matrix[r][c].startswith("1"):
        pygame.draw.rect(screen, settings.unset_color, rect)
    elif world_matrix[r][c].startswith("2"):
        pygame.draw.rect(screen, settings.unknown_color, rect)
    else:
        file_path = settings.img_parts_path
        if world_matrix[r][c].startswith("3"):
            file_path += 'straight'
        elif world_matrix[r][c].startswith("4"):
            file_path += '4_way'
        elif world_matrix[r][c].startswith("5"):
            file_path += 't_junction'
        elif world_matrix[r][c].startswith("6"):
            file_path += 'curve'
        rotations = int(world_matrix[r][c][1])
        file_path += ".bmp"
    return file_path, rotations


def place_img(file_path, screen, rect, rotations=0):
    """Place an image in a given rect and rotate if needed."""
    image = pygame.image.load(file_path)
    image.convert()
    image.set_colorkey((110, 110, 110))
    if rotations > 0:
        # Rotates clockwise.
        image = pygame.transform.rotate(image, -90 * rotations)
    screen.blit(image, rect)


def get_placable_objects(settings, world_matrix, r, c):
    """Return filepath for placeable object."""
    obj_file_path = settings.img_obj_path
    if int(world_matrix[r][c][2]) == 1:
        obj_file_path += 'lyftkran'
    elif int(world_matrix[r][c][2]) == 2:
        obj_file_path += 'dumper'
    elif int(world_matrix[r][c][2]) == 3:
        obj_file_path += 'lego'
    elif int(world_matrix[r][c][2]) == 4:
        obj_file_path += 'container'
    obj_file_path += '.bmp'
    return obj_file_path


def draw_part(settings, world_matrix, r, c, screen):
    """Draws a part of the map."""
    rect = pygame.Rect(settings.part_width*c, settings.part_height *
                       r, settings.part_width, settings.part_height)
    rect.centerx = (settings.part_width*c + settings.part_width/2)
    part_file_path, rotations = get_part_type(
        world_matrix, screen, settings, rect, r, c)
    if part_file_path:
        place_img(part_file_path, screen, rect, rotations)
    if int(world_matrix[r][c][2]) > 0:
        obj_file_path = get_placable_objects(settings, world_matrix, r, c)
        place_img(obj_file_path, screen, rect)


def draw_map(screen, settings, world_matrix):
    """Draws the whole map."""
    for r in range(0, len(world_matrix)):
        for c in range(0, len(world_matrix[r])):
            draw_part(settings, world_matrix, r, c, screen)


def get_node_rect(width, height, settings, node_pos, v_just=0, h_just=0):
    """Gets the correct rect for a node."""
    rect = pygame.Rect((settings.part_width * (node_pos[1]-h_just)) + (settings.part_width/2) - (settings.node_line_thickness/2), (settings.part_height *
                                                                                                                                   (node_pos[0]-v_just)) + (settings.part_height/2) - (settings.node_line_thickness/2), width, height)
    return rect


def get_node(pos, node_pos, settings):
    if pos[0] == node_pos[0] and node_pos[1] < pos[1]:
        rect = get_node_rect(settings.part_width,
                             settings.node_line_thickness, settings, node_pos)
    elif pos[0] == node_pos[0] and node_pos[1] > pos[1]:
        rect = get_node_rect(
            settings.part_width, settings.node_line_thickness, settings, node_pos, h_just=1)
    elif pos[1] == node_pos[1] and node_pos[0] < pos[0]:
        rect = get_node_rect(settings.node_line_thickness,
                             settings.part_width, settings, node_pos)
    elif pos[1] == node_pos[1] and node_pos[0] > pos[0]:
        rect = get_node_rect(settings.node_line_thickness,
                             settings.part_width, settings, node_pos, v_just=1)
    return rect


def draw_nodes(screen, settings, nodes):
    """Displays nodes on screen."""
    for node in nodes:
        for pos in nodes[node]:
            node_pos = json.loads(node)
            pos = json.loads(pos[0])
            rect = get_node(pos, node_pos, settings)
            pygame.draw.rect(screen, settings.node_color, rect)


def draw_route(route, screen, settings):
    """Displays route on screen."""
    for p in range(0, len(route)-1):
        pos = json.loads(route[p])
        next_pos = json.loads(route[p+1])
        rect = get_node(pos, next_pos, settings)
        pygame.draw.rect(screen, settings.route_color, rect)


def update_screen(screen, settings, world_matrix, nodes, next_button, robot):
    """Update images on the screen and flip to the new screen"""
    # Redraw the screen during each pass through the loop.
    screen.fill(settings.bg_color)
    draw_map(screen, settings, world_matrix)
    draw_nodes(screen, settings, nodes.nodes_dict)
    if robot.goals:
        draw_route(robot.goals[settings.view_route]['route'], screen, settings)
    next_button.draw_button()

    pygame.display.flip()


def check_events(settings, robot):
    """Respond to keypresses and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                sys.exit()
            elif event.key == pygame.K_RIGHT:
                if settings.view_route < len(robot.goals)-1:
                    settings.view_route += 1
            elif event.key == pygame.K_LEFT:
                if settings.view_route > 0:
                    settings.view_route -= 1
