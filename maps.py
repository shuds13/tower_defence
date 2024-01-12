import pygame
import navigation as nav
import time
import spiral
from accounts import profile_menu, new_profile

crown_img = pygame.image.load('images/crown.png')
crown_img = pygame.transform.scale(crown_img, (50, 50))
crownace_img = pygame.image.load('images/crown_ace.png')
crownace_img = pygame.transform.scale(crownace_img, (50, 50))
save_img = pygame.image.load('images/save.png')
save_img = pygame.transform.scale(save_img, (40, 40))
right_img = pygame.image.load('images/right_chevron.png')
right_img = pygame.transform.scale(right_img, (60, 60))
left_img =  pygame.transform.flip(right_img, True, False)

maps_per_page = 6
periodic_arrows = True

# May put this elsewhere
def get_bounding_box(polygon):
    min_x = min(polygon, key=lambda point: point[0])[0]
    min_y = min(polygon, key=lambda point: point[1])[1]
    max_x = max(polygon, key=lambda point: point[0])[0]
    max_y = max(polygon, key=lambda point: point[1])[1]

    return min_x, min_y, max_x, max_y

def is_point_inside_bounding_box(pos, bounding_box):
    x, y = pos
    min_x, min_y, max_x, max_y = bounding_box
    return min_x <= x <= max_x and min_y <= y <= max_y

def is_rect_in_box(center_x, center_y, rect_w, rect_h, bounding_box):
    min_x, min_y, max_x, max_y = bounding_box
    overlap = 10
    rect_w -= overlap
    rect_h -= overlap
    rect_x = center_x - rect_w / 2
    rect_y = center_y - rect_h / 2

    # Check if all corners of the rectangle are inside the bounding box
    return (bounding_box[0] <= rect_x <= bounding_box[2] and
            bounding_box[0] <= rect_x + rect_w <= bounding_box[2] and
            bounding_box[1] <= rect_y <= bounding_box[3] and
            bounding_box[1] <= rect_y + rect_h <= bounding_box[3])

def in_shape(pos, polygon):
    bounding_box = get_bounding_box(polygon)
    #print(bounding_box)
    return is_point_inside_bounding_box(pos, bounding_box)


def render_level_to_surface(gmap, size):
    # Create a new surface
    level_surface = pygame.Surface(size)
    level_surface.fill(gmap.background_color)
    gmap.paint_features(level_surface)

    # Draw the background
    #level_surface.blit(background_image, (0, 0))

    # Draw the path
    for path in gmap.paths:
        for i in range(len(path) - 1):
            # Increased thickness from 5 to 10, looks better in thumbnails
            pygame.draw.line(level_surface, gmap.path_color, path[i], path[i + 1], 10)

    return level_surface

def create_thumbnail(level_surface, thumbnail_size):
    return pygame.transform.scale(level_surface, thumbnail_size)


def options_window(display, surface, window_size):
    pygame.draw.rect(surface, (245, 245, 220), (0, 0, window_size[0], window_size[1]))  # alt color



def display_maps_page(display, surface, account, maps_page, width, height):

    start_x = 120
    start_y = 80
    col_size = 2
    x_offset = width+60
    y_offset = 200
    x = start_x
    y = start_y

    map_rects = []
    maps = []
    gmap = None

    font = pygame.font.SysFont(None, 24)

    for count, map_class in enumerate(maps_page):
        gmap = map_class()

        # Construct thumbnails
        level_surface = render_level_to_surface(gmap, (700, 600))  # map size without side window
        thumbnail = create_thumbnail(level_surface, (width, height))
        surface.blit(thumbnail, (x,y))
        map_image_rect = thumbnail.get_rect(topleft=(x,y))

        maptxt = gmap.name.upper() + " (" + difficulty[gmap.difficulty] + ")"
        map_name_text = font.render(maptxt, True, (0, 0, 0))  # Black text
        map_name_rect = map_name_text.get_rect(topleft=(x, y+120))
        surface.blit(map_name_text, map_name_rect.topleft)

        # This is the class
        if account is not None:
            pygame.display.set_caption("Menu selection (Profile: " + account.name + ")")
            if type(gmap) in account.maps_complete:
                if type(gmap) in account.maps_aced:
                    crown = crownace_img
                else:
                    crown = crown_img
                #crown_rect = crown.get_rect(topleft=(x, y+70))  # Appears over bottom left of map
                crown_rect = crown.get_rect(center=(x+width//2, y))
                surface.blit(crown, crown_rect.topleft)

            if gmap.name in account.maps_in_progress:
                save_rect = save_img.get_rect(center=(x, y+60))
                surface.blit(save_img, save_rect.topleft)
        else:
            pygame.display.set_caption("Menu selection")

        y+=y_offset
        map_rects.append(map_image_rect)
        maps.append(gmap)
        if (count+1) % col_size == 0:
            y = start_y
            x += x_offset

    return map_rects, maps


def get_nmaps_npages():
    nmaps = len(map_classes)
    npages = nmaps // maps_per_page + 1
    return nmaps, npages

def draw_map_window(display, surface, window_size, account=None, page=1):
    pygame.draw.rect(surface, (245, 245, 220), (0, 0, window_size[0], window_size[1]))  # alt color
    window_width = window_size[0]
    window_height = window_size[1]

    font_title = pygame.font.SysFont('Arial', 24, bold=True)  # Choose a font and size
    map_menu_text = font_title.render("Choose a map", True, (0, 0, 0))  # Black text
    map_menu_rect = map_menu_text.get_rect(center=(window_width//2, 20))
    surface.blit(map_menu_text, map_menu_rect.topleft)

    #loop and call
    width = 180
    height = 120

    nmaps, npages = get_nmaps_npages()

    start_map = (page-1)*maps_per_page
    end_map = min(start_map+maps_per_page, nmaps)
    maps_page = map_classes[start_map:end_map]
    map_rects, maps = display_maps_page(display, surface, account, maps_page, width, height)

    # Draw new/load profile buttons
    x = window_width//3 - 100
    y = window_height - 100
    load_account_rect = nav.draw_button(surface, "Load Profile", (x, y), (200, 60))
    x = window_width*2//3 - 100
    new_account_rect = nav.draw_button(surface, "New Profile", (x, y), (200, 60))

    rarrow_rect = None
    if nmaps > maps_per_page and (periodic_arrows or npages > page):
        rarrow_rect = right_img.get_rect(center=(window_width-70, window_height//2-60))
        surface.blit(right_img, rarrow_rect.topleft)

    larrow_rect = None
    if nmaps > maps_per_page and (periodic_arrows or page > 1):
        larrow_rect = left_img.get_rect(center=(50, window_height//2-60))
        surface.blit(left_img, larrow_rect.topleft)

    display.flip()
    return map_rects, maps, larrow_rect, rarrow_rect, load_account_rect, new_account_rect


def map_window(display, surface, window_size, account=None):

    page = 2 #1
    map_rects, maps, larrow_rect, rarrow_rect, load_account_rect, new_account_rect = draw_map_window(display, surface, window_size, account, page)

    # loop to detect clicks
    noclicks = True
    map_id = None
    while noclicks:
        time.sleep(0.1)  # Reduce idle CPU usage
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                noclicks = False
                return None, None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if new_account_rect.collidepoint(mouse_pos):
                    new_account = new_profile(surface)
                    if new_account is not None:
                        account = new_account
                    map_rects, maps, larrow_rect, rarrow_rect, _, _  = draw_map_window(display, surface, window_size, account, page)

                if load_account_rect.collidepoint(mouse_pos):
                    new_account = profile_menu(surface)
                    if new_account is not None:
                        account = new_account
                    map_rects, maps, larrow_rect, rarrow_rect, _, _  = draw_map_window(display, surface, window_size, account, page)

                if rarrow_rect and rarrow_rect.collidepoint(mouse_pos):
                    if periodic_arrows:
                        nmaps, npages = get_nmaps_npages()
                        page = page + 1 if page < npages else 1
                    else:
                        page += 1
                    map_rects, maps, larrow_rect, rarrow_rect, _, _  = draw_map_window(display, surface, window_size, account, page)

                if larrow_rect and larrow_rect.collidepoint(mouse_pos):
                    if periodic_arrows:
                        nmaps, npages = get_nmaps_npages()
                        page = page - 1 if page > 1 else npages
                    else:
                        page -= 1
                    map_rects, maps, larrow_rect, rarrow_rect, _, _  = draw_map_window(display, surface, window_size, account, page)


                map_id = process_click(map_rects, mouse_pos)
                if map_id is not None:
                    noclicks = False
                    break
    gmap = maps[map_id]
    return gmap, account


def process_click(map_rects, mouse_pos):
    # Upgrade tower
    for i, map_rect in enumerate(map_rects):
        if map_rect.collidepoint(mouse_pos):
            return i
    return None


def map_select():
    draw_map_window()

class Map():
    def __init__(self):
        pass

    def paint_features(self, window):
        pass

    def can_I_place(self, pos, w, h):
        return True


class PicnicPlace(Map):
    def __init__(self):
        self.name = "Picnic Place"
        self.difficulty = 1
        self.paths = [[(0, 400), (200, 100), (200, 400), (600, 400), (600, 200), (520, 200), (520, 600)]]
        self.background_color = (53, 94, 59)  # (0, 158, 96)
        self.path_thickness = 20
        self.path_color = (178, 190, 181)


class Staircase(Map):
    def __init__(self):
        self.name = "Staircase"
        self.difficulty = 2
        self.paths = [[(50, 100), (200, 100), (200, 300), (400, 300), (400, 500), (650, 500)]]
        self.background_color = (50, 25, 0)
        self.path_thickness = 15
        self.path_color = (0, 211, 211)


class Diamond(Map):
    def __init__(self):
        self.name = "Diamond"
        self.difficulty = 2
        #self.paths = [[(0, 100), (300, 250), (400, 250), (700, 100)]]
        self.background_color = (192, 64, 0) #(242, 140, 40) # (53, 94, 59)  # (0, 158, 96)
        self.path_thickness = 20
        self.path_color = (244, 187, 68) # (201, 169, 166)

        path1 = [(100, 0), (360, 360), (600, 0)]
        path2 = [(100, 600), (360, 200), (600, 600)]
        self.paths = [path1, path2]


class Valley(Map):
    def __init__(self):
        self.name = "Valley"
        self.difficulty = 3
        #self.paths = [[(0, 100), (300, 250), (400, 250), (700, 100)]]
        self.background_color = (69, 75, 27) # (53, 94, 59)  # (0, 158, 96)
        self.path_thickness = 20
        self.path_color = (96, 130, 182) # (178, 190, 181)

        path1 = [(0, 100), (300, 260), (400, 260), (700, 100)]
        path2 = [(0, 500), (300, 340), (400, 340), (700, 500)]
        self.paths = [path1, path2]


class Square(Map):
    def __init__(self):
        self.name = "Square"
        self.difficulty = 3
        self.background_color = (54, 69, 79) # (0, 71, 171)
        self.path_thickness = 20
        self.path_color = (233, 220, 201) #(255, 255, 240) # (255,255,255) # (0, 163, 108)

        # The middle point makes no diff to map,
        # but makes diff when King's explode - blobs converge on next point.
        # Perhaps should have both middle points
        path1 = [(250, 0), (250, 400), (250, 600)]
        path2 = [(450, 0), (450, 400), (450, 600)]
        path3 = [(0, 200), (450, 200), (700, 200)]
        path4 = [(0, 400), (450, 400), (700, 400)]
        self.paths = [path1, path2, path3, path4]


class Spiral(Map):
    def __init__(self):
        self.name = "Spiral"
        self.difficulty = 1
        self.background_color = (0, 71, 171)
        self.path_thickness = 20
        self.path_color = (0, 163, 108)
        self.paths = [spiral.spiral_path]

#coe to think of it what happened to that other map I made - I know it wasn't planned to be permanent but hey...

# Initial paths dont look as good as could but actually is quite a good maps from strategic viewpoint.
class Vase(Map):
    def __init__(self):
        self.name = "Rubin's Vase"
        self.difficulty = 4
        #self.paths = [[(0, 100), (300, 250), (400, 250), (700, 100)]]
        self.background_color =  (48, 25, 52) # (40, 40, 43) # (69, 75, 27)
        self.path_thickness = 20
        self.path_color = (100, 149, 237) # (25, 25, 112) # (96, 130, 182)

        # Path for the left face
        left_path = [
            (50, 0), (180, 70), (200, 200), (170, 230), (300, 350),
            (200, 360), (200,400), (160, 420), (200, 430), (200, 500), (50, 600)
        ]

        # Path for the right face
        right_path = [
            (650, 0), (520, 70), (500, 200), (530, 230), (400, 350),
            (500, 360), (500,400), (540, 420), (500, 430), (500, 500), (650, 600)
        ]
        self.paths = [left_path, right_path]


# Maps for testing
class Eagle(Map):
    def __init__(self):
        self.name = "Eagle"
        self.difficulty = 1
        self.paths = [[(50, 100), (100, 100), (500, 300), (300, 300), (200, 450), (650, 500)]]
        self.background_color = (50, 25, 0)
        self.path_thickness = 15
        self.path_color = (0, 211, 211)


# Maps for testing
class Nonsense(Map):
    def __init__(self):
        self.name = "Nonsense"
        self.difficulty = 3
        self.background_color = (2, 48, 32) #(50, 25, 0)
        self.path_thickness = 18
        self.path_color = (0, 28, 211)  # blues are near invisible.
        #path1 = [(100, 0), (360, 360), (600, 0)]
        #path2 = [(100, 600), (360, 200), (600, 600)]
        path1 = [(700,300),(500,300),(350,200),(200,300),(0,300)]
        path2 = [(700,300),(500,300),(350,400),(200,300),(0,300)]
        path3 = [(700,300),(600,300),(350,100),(100,300),(0,300)]
        path4 = [(700,300),(600,300),(350,500),(100,300),(0,300)]
        self.paths = [path1,path2,path3,path4]

class Castle(Map):
    def __init__(self):
        self.name = "Castle"
        self.difficulty = 2
        self.background_color = (92, 64, 51) # (193, 154, 107) #(184, 115, 51) # (50, 25, 0)
        self.path_thickness = 20
        self.path_color = (0,0,0) # (92, 64, 51)  # (0, 211, 211)
        self.color_inside = (193, 154, 107)

        self.castle_path = [
            (100, 550), # Bottom left of the castle
            (100, 350), # Left tower start
            (175, 250), # Left tower top
            (250, 350), # Left tower end
            (250, 150), # Middle tower start
            (350, 50),  # Middle tower top
            (450, 150), # Middle tower end
            (450, 350), # Right tower start
            (525, 250), # Right tower top
            (600, 350), # Right tower end
            (600, 550), # Bottom right of the castle
            (400, 550), # Right side of the door
            (400, 450), # Right Top of the door
            (350, 400), # Top of the door
            (300, 450), # Left Top of the door
            (300, 550), # Left side of the door
            (100, 550)  # Back to the start
        ]

        self.paths = [self.castle_path]

        self.door_color = (165, 42, 42) #(0,0,0)
        self.window_color = (0,0,0)

        self.door = [
            (400, 550), # Right side of the door
            (400, 450), # Right Top of the door
            (350, 400), # Top of the door
            (300, 450), # Left Top of the door
            (300, 550), # Left side of the door
            (400, 550), # Right side of the door
        ]
        self.doorbox = (300, 400, 400, 550)

        self.middle_window = [
            (320, 300), # Left tower end
            (320, 150), # Middle tower start
            (350, 100),  # Middle tower top
            (380, 150), # Middle tower end
            (380, 300), # Right tower start
            (320, 300), # Left tower end
        ]
        self.middle_window_box = (320, 125, 380, 300)

        self.left_window = [
            (140, 500), # Bottom left of the castle
            (140, 350), # Left tower start
            (175, 300), # Left tower top
            (210, 350), # Left tower end
            (210, 500), # Middle tower start
            (140, 500), # Bottom left of the castle

        ]
        self.left_window_box = (140, 325, 210, 500)

        self.right_window = [
            (140+350, 500), # Bottom left of the castle
            (140+350, 350), # Left tower start
            (175+350, 300), # Left tower top
            (210+350, 350), # Left tower end
            (210+350, 500), # Middle tower start
            (140+350, 500), # Bottom left of the castle
        ]
        self.right_window_box = (490, 325, 560, 500)


    # May make so can only place on inside of castle - or in dark areas (door and windows)
    def paint_features(self, window):
        #door_color = (165, 42, 42) #(0,0,0)
        pygame.draw.polygon(window, self.color_inside, self.castle_path)

        pygame.draw.polygon(window, self.door_color, self.door)
        pygame.draw.polygon(window, self.window_color, self.middle_window)  # windows prob make black
        pygame.draw.polygon(window, self.window_color, self.left_window)  # windows prob make black
        pygame.draw.polygon(window, self.window_color, self.right_window)  # windows prob make black

    def can_I_place(self, pos, w, h):
        # Bounding box round polygon is too high at peak, so do manually.
        #if (
            #in_shape(pos, self.door)
            #or in_shape(pos, self.left_window)
            #or in_shape(pos, self.right_window)
            #or in_shape(pos, self.middle_window)
        #):
            #return True
        #print(pos)
        if is_rect_in_box(pos[0], pos[1], w, h, self.doorbox):
            return True
        if is_rect_in_box(pos[0], pos[1], w, h, self.left_window_box):
            return True
        if is_rect_in_box(pos[0], pos[1], w, h, self.right_window_box):
            return True
        if is_rect_in_box(pos[0], pos[1], w, h, self.middle_window_box):
            return True
        return False

# dont need to be a dictionary
#map_classes  = {1: PicnicPlace, 2: Spiral, 3: Staircase, 4: Diamond, 5: Valley, 6: Square}
map_classes  = [PicnicPlace, Spiral, Staircase, Diamond, Valley, Square, Castle, Vase, Nonsense] # Eagle]

difficulty  = {1: "Easy", 2: "Medium", 3: "Hard", 4: "Expert"}
