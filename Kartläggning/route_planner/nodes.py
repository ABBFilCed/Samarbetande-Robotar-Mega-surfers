class Nodes:
    """Creates nodes to pass to a search_algoritm:"""

    def __init__(self, world_matrix):
        self.world_matrix = world_matrix
        self.nodes_dict = self.get_nodes(self.world_matrix)

    def node_down(self, node, r, c):
        if r < len(self.world_matrix[r]) - 1:
            node.append([str([r+1, c]), 1])
        return node

    def node_up(self, node, r, c):
        if r > 0:
            node.append([str([r-1, c]), 1])
        return node

    def node_right(self, node, r, c):
        if c < len(self.world_matrix) - 1:
            node.append([str([r, c+1]), 1])
        return node

    def node_left(self, node, r, c):
        if c > 0:
            node.append([str([r, c-1]), 1])
        return node

    def get_nodes(self, world_matrix):
        """Gets nodes for a fiven world."""
        nodes_dict = {}
        for r in range(0, len(world_matrix)):
            for c in range(0, len(world_matrix[r])):
                if int(world_matrix[r][c][0]) > 2:
                    node = []
                    if int(world_matrix[r][c][0]) == 3:
                        if int(world_matrix[r][c][1]) == 0:
                            node = self.node_down(node, r, c)
                            node = self.node_up(node, r, c)
                        elif int(world_matrix[r][c][1]) == 1:
                            node = self.node_right(node, r, c)
                            node = self.node_left(node, r, c)
                    elif int(world_matrix[r][c][0]) == 4:
                        node = self.node_down(node, r, c)
                        node = self.node_up(node, r, c)
                        node = self.node_right(node, r, c)
                        node = self.node_left(node, r, c)
                    elif int(world_matrix[r][c][0]) == 5:
                        if int(world_matrix[r][c][1]) == 0:
                            node = self.node_down(node, r, c)
                            node = self.node_right(node, r, c)
                            node = self.node_left(node, r, c)
                        elif int(world_matrix[r][c][1]) == 1:
                            node = self.node_down(node, r, c)
                            node = self.node_up(node, r, c)
                            node = self.node_left(node, r, c)
                        elif int(world_matrix[r][c][1]) == 2:
                            node = self.node_up(node, r, c)
                            node = self.node_right(node, r, c)
                            node = self.node_left(node, r, c)
                        elif int(world_matrix[r][c][1]) == 3:
                            node = self.node_up(node, r, c)
                            node = self.node_down(node, r, c)
                            node = self.node_right(node, r, c)
                    elif int(world_matrix[r][c][0]) == 6:
                        if int(world_matrix[r][c][1]) == 0:
                            node = self.node_down(node, r, c)
                            node = self.node_right(node, r, c)
                        elif int(world_matrix[r][c][1]) == 1:
                            node = self.node_down(node, r, c)
                            node = self.node_left(node, r, c)
                        elif int(world_matrix[r][c][1]) == 2:
                            node = self.node_up(node, r, c)
                            node = self.node_left(node, r, c)
                        elif int(world_matrix[r][c][1]) == 3:
                            node = self.node_up(node, r, c)
                            node = self.node_right(node, r, c)
                    nodes_dict[str([r, c])] = node
        return nodes_dict

    def update_nodes(self, world_matrix, settin):
        """Gets new nodes when called."""
        self.world_matrix = world_matrix
        self.nodes_dict = self.get_nodes(self.world_matrix)
