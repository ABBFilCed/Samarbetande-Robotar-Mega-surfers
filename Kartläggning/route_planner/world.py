class World:
    """Class that holds map data."""

    def __init__(self, width, height):
        self.width = width
        self.height = height
        # Creates a new matrix
        self.matrix = self.build_matrix(self.width, self.height)

    def build_matrix(self, width, height):
        """Creates an empty matrix with the same dimensions as the given parameters."""
        matrix = []
        for r in range(0, height):
            row = []
            for c in range(0, width):
                row.append(str("100"))
            matrix.append(row)
        return matrix

    def set_new_val(self, x_cordinate, y_cordinate, val):
        """Updates the value for a specific place in the matrix."""
        self.matrix[y_cordinate][x_cordinate] = val
