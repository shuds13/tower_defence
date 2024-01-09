def get_nearest_point_on_path(point, line_start, line_end):
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

    return nearest_point


def too_close_to_path(point, line_start, line_end, w, h):
    # Distance from point to nearest point on the line segment

    nearest_point = get_nearest_point_on_path(point, line_start, line_end)
    px, py = point
    dx = px - nearest_point[0]
    dy = py - nearest_point[1]
    # return (dx ** 2 + dy ** 2) ** 0.5  # old - equal width/height towers
    # this is where could add path_thickness//2 - overlap but for now distance to centre of path.
    return abs(dx) < w//2 and abs(dy) < h//2


def is_valid_position(newtowertype, pos, paths, towers, options_button, gmap):
    """Check if the position is not on the path and not too close to other towers."""

    # TODO should include path thickness
    min_distance_to_path = 25 # Minimum allowed distance from the path
    overlap = 15

    #TODO use collide to see if in side panel
    if pos[0] > 675:  # so no part in side panel
        return False

    if not gmap.can_I_place(pos):
        return False

    w1 = newtowertype.footprint[0]
    h1 = newtowertype.footprint[1]

    if options_button.collidepoint(pos):
        return False

    # TODO tower footprint should matter here also.
    # Check distance from the path
    for path in paths:
        for i in range(len(path) - 1):
            if too_close_to_path(pos, path[i], path[i + 1], w1, h1):
                return False

    # Check distance from other towers
    for tower in towers:
        w2 = tower.__class__.footprint[0]
        h2 = tower.__class__.footprint[1]
        min_x = (w1+w2)//2 - overlap
        min_y = (h1+h2)//2 - overlap
        if abs(pos[0] - tower.position[0]) < min_x and abs(pos[1] - tower.position[1]) < min_y:
            return False
    return True

def create_ghost_image(original_image, alpha=128):
    """Create a semi-transparent version of the given image."""
    ghost_image = original_image.copy()

    # Modify the alpha value of every pixel
    for x in range(ghost_image.get_width()):
        for y in range(ghost_image.get_height()):
            color = ghost_image.get_at((x, y))
            ghost_image.set_at((x, y), (color.r, color.g, color.b, alpha))
    return ghost_image
