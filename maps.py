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

def render_level_to_surface(gmap, size):
    # Create a new surface
    level_surface = pygame.Surface(size)
    level_surface.fill(gmap.background_color)

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

    page = 1
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
        self.background_color = (69, 75, 27) # (53, 94, 59)  # (0, 158, 96)
        self.path_thickness = 20
        self.path_color = (96, 130, 182) # (178, 190, 181)

        # Path for the left face
        #left_path = [
            #(50, 100), (200, 100), (200, 200), (300, 250), (200, 300), (200, 500), (50, 500)
        #]

        ## Path for the right face
        #right_path = [
            #(650, 100),(500, 100),(500, 200),(400, 250),(500, 300),(500, 500),(650, 500)
        #]

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

#class Rubbish2(Map):
    #def __init__(self):
        #self.name = "Rubbish2"
        #self.difficulty = 2
        #self.paths = [[(50, 100), (100, 100), (500, 300), (300, 300), (200, 450), (650, 500)]]
        #self.background_color = (50, 25, 0)
        #self.path_thickness = 15
        #self.path_color = (0, 211, 211)


# dont need to be a dictionary
#map_classes  = {1: PicnicPlace, 2: Spiral, 3: Staircase, 4: Diamond, 5: Valley, 6: Square}
map_classes  = [PicnicPlace, Spiral, Staircase, Diamond, Valley, Square, Vase, Eagle]

difficulty  = {1: "Easy", 2: "Medium", 3: "Hard", 4: "Expert"}
