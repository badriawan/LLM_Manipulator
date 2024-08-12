def extend_to_square(x, y, step_size=15):
    # Create 4 new coordinates forming a square with the given step size
    return [
        (x - step_size, y - step_size),
        (x + step_size, y - step_size),
        (x - step_size, y + step_size),
        (x + step_size, y + step_size)
    ]

def square_expansion(x, y):
    step_size = 15
    return extend_to_square(x, y, step_size)

def transform_coordinates(coordinates, original_plane, new_plane):
    # Calculate the min and max x and y values for original plane
    original_x_min = min(coord[0] for coord in original_plane)
    original_x_max = max(coord[0] for coord in original_plane)
    original_y_min = min(coord[1] for coord in original_plane)
    original_y_max = max(coord[1] for coord in original_plane)

    # Calculate the min and max x and y values for new plane
    new_x_min = min(coord[0] for coord in new_plane)
    new_x_max = max(coord[0] for coord in new_plane)
    new_y_min = min(coord[1] for coord in new_plane)
    new_y_max = max(coord[1] for coord in new_plane)

    x_scale = (new_x_max - new_x_min) / (original_x_max - original_x_min)
    y_scale = (new_y_max - new_y_min) / (original_y_max - original_y_min)

    def transform_coordinate(coord):
        x, y = coord
        new_x = new_x_min + (x - original_x_min) * x_scale
        new_y = new_y_min + (y - original_y_min) * y_scale
        return new_x, new_y

    return [transform_coordinate(coord) for coord in coordinates]
