class Nodes:
    """Creates nodes to pass to a search_algoritm:"""

    def __init__(self, world_matrix):
        """Initialize a new node_dict."""
        #self.world_matrix = world_matrix
        self.nodes_dict = self.get_nodes(world_matrix)

    def node_down(self, node, r, c, world_matrix):
        """Return a node under the current node."""
        if r < len(world_matrix[r]) - 1:
            node.append([str([r+1, c]), 1])
        return node

    def node_up(self, node, r, c):
        """Return a node over the current node."""
        if r > 0:
            node.append([str([r-1, c]), 1])
        return node

    def node_right(self, node, r, c, world_matrix):
        """Return a node to the right of the current node."""
        if c < len(world_matrix) - 1:
            node.append([str([r, c+1]), 1])
        return node

    def node_left(self, node, r, c):
        """Return a node to the left of the current node."""
        if c > 0:
            node.append([str([r, c-1]), 1])
        return node

    def get_nodes(self, world_matrix):
        """Gets nodes for a given world."""
        nodes_dict = {}
        for r in range(0, len(world_matrix)):
            for c in range(0, len(world_matrix[r])):
                if int(world_matrix[r][c][0]) > 2:
                    node = []
                    if int(world_matrix[r][c][0]) == 3:
                        if int(world_matrix[r][c][1]) == 0:
                            node = self.node_down(node, r, c, world_matrix)
                            node = self.node_up(node, r, c)
                        elif int(world_matrix[r][c][1]) == 1:
                            node = self.node_right(node, r, c, world_matrix)
                            node = self.node_left(node, r, c)
                    elif int(world_matrix[r][c][0]) == 4:
                        node = self.node_down(node, r, c, world_matrix)
                        node = self.node_up(node, r, c)
                        node = self.node_right(node, r, c, world_matrix)
                        node = self.node_left(node, r, c)
                    elif int(world_matrix[r][c][0]) == 5:
                        if int(world_matrix[r][c][1]) == 0:
                            node = self.node_down(node, r, c, world_matrix)
                            node = self.node_right(node, r, c, world_matrix)
                            node = self.node_left(node, r, c)
                        elif int(world_matrix[r][c][1]) == 1:
                            node = self.node_down(node, r, c, world_matrix)
                            node = self.node_up(node, r, c)
                            node = self.node_left(node, r, c)
                        elif int(world_matrix[r][c][1]) == 2:
                            node = self.node_up(node, r, c)
                            node = self.node_right(node, r, c, world_matrix)
                            node = self.node_left(node, r, c)
                        elif int(world_matrix[r][c][1]) == 3:
                            node = self.node_up(node, r, c)
                            node = self.node_down(node, r, c, world_matrix)
                            node = self.node_right(node, r, c, world_matrix)
                    elif int(world_matrix[r][c][0]) == 6:
                        if int(world_matrix[r][c][1]) == 0:
                            node = self.node_down(node, r, c, world_matrix)
                            node = self.node_right(node, r, c, world_matrix)
                        elif int(world_matrix[r][c][1]) == 1:
                            node = self.node_down(node, r, c, world_matrix)
                            node = self.node_left(node, r, c)
                        elif int(world_matrix[r][c][1]) == 2:
                            node = self.node_up(node, r, c)
                            node = self.node_left(node, r, c)
                        elif int(world_matrix[r][c][1]) == 3:
                            node = self.node_up(node, r, c)
                            node = self.node_right(node, r, c, world_matrix)
                    nodes_dict[str([r, c])] = node
                elif int(world_matrix[r][c][0]) == 2:
                    nodes_dict[str([r, c])] = []
        return nodes_dict

    def update_nodes(self, world_matrix):
        """Gets new nodes when called."""
        self.nodes_dict = self.get_nodes(world_matrix)
