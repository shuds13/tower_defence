#Maybe this should be maps - and path be part of this module

def point_line_distance(point, line_start, line_end):
    """Calculate the minimum distance between a point and a line segment."""
    # Line segment start and end points
    x1, y1 = line_start
    x2, y2 = line_end

    # Point coordinates
    px, py = point

    # Line segment's length squared
    line_len_sq = (x2 - x1) ** 2 + (y2 - y1) ** 2

    # Calculate the projection
    u = ((px - x1) * (x2 - x1) + (py - y1) * (y2 - y1)) / float(line_len_sq)

    # Determine the nearest point on the line segment
    if u > 1:
        nearest_point = (x2, y2)
    elif u < 0:
        nearest_point = (x1, y1)
    else:
        nearest_point = (x1 + u * (x2 - x1), y1 + u * (y2 - y1))

    # Distance from point to nearest point on the line segment
    dx = px - nearest_point[0]
    dy = py - nearest_point[1]

    return (dx ** 2 + dy ** 2) ** 0.5

def is_valid_position(pos, path, towers):
    """Check if the position is not on the path and not too close to other towers."""
    min_distance_to_path = 20  # Minimum allowed distance from the path
    some_minimum_distance_between_towers = 25

    # Check distance from the path
    for i in range(len(path) - 1):
        if point_line_distance(pos, path[i], path[i + 1]) < min_distance_to_path:
            return False

    # Check distance from other towers
    for tower in towers:
        if (pos[0] - tower.position[0])**2 + (pos[1] - tower.position[1])**2 < some_minimum_distance_between_towers**2:
            return False

    return True
