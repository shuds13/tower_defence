import pygame
import navigation as nav
import time
import sounds
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

lightmode_img = pygame.image.load('images/lightmode.png')
lightmode_img = pygame.transform.scale(lightmode_img, (50, 50))
darkmode_img = pygame.image.load('images/darkmode.png')
darkmode_img = pygame.transform.scale(darkmode_img, (50, 50))

#moon_img = pygame.image.load('images/moon.png')
#moon_img = pygame.transform.scale(moon_img, (50, 50))


house1_img = pygame.image.load('images/house1.png')
house1_img = pygame.transform.scale(house1_img, (160, 140))
house2_img = pygame.image.load('images/house2.png')
house2_img = pygame.transform.scale(house2_img, (160, 140))
house3_img = pygame.image.load('images/house3.png')
house3_img = pygame.transform.scale(house3_img, (160, 140))
tree_img = pygame.image.load('images/tree1.png')
tree1_img = pygame.transform.scale(tree_img, (70, 160))
bigtree_img = pygame.transform.scale(tree_img, (90, 180))
shorttree_img = pygame.transform.scale(tree_img, (90, 60))
shortwidetree_img = pygame.transform.scale(tree_img, (160, 60))

explosion_img = pygame.image.load('images/explosion.png')

# Used in removables so does not store images
img_dict = {
    "bigtree_img": bigtree_img,
    "shorttree_img": shorttree_img,
    "shortwidetree_img": shortwidetree_img,
    "house1_img": house1_img,
    "house2_img": house2_img,
    "house3_img": house3_img,
    }

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

def is_rect_in_box(center_x, center_y, rect_w, rect_h, bounding_box, wh=False):
    min_x, min_y, max_x, max_y = bounding_box
    if wh:  # The rectangle specified x,y,w,h instead of x,y,x,y
        max_x += min_x
        max_y += min_y
        bounding_box = (min_x, min_y, max_x, max_y)

    overlap = 15
    rect_w -= overlap
    rect_h -= overlap
    rect_x = center_x - rect_w / 2
    rect_y = center_y - rect_h / 2

    # Check if all corners of the rectangle are inside the bounding box
    # SH seems a bit overill dont need check rect_x < bb[2] - if checking ect_x + rect_w <= bb[2]
    return (bounding_box[0] <= rect_x <= bounding_box[2] and
            bounding_box[0] <= rect_x + rect_w <= bounding_box[2] and
            bounding_box[1] <= rect_y <= bounding_box[3] and
            bounding_box[1] <= rect_y + rect_h <= bounding_box[3])


def is_rect_out_box(center_x, center_y, rect_w, rect_h, bounding_box, wh=False):
    min_x, min_y, max_x, max_y = bounding_box
    if wh:  # The rectangle specified x,y,w,h instead of x,y,x,y
        max_x += min_x
        max_y += min_y
        bounding_box = (min_x, min_y, max_x, max_y)

    overlap = 10 #10
    rect_w -= overlap
    rect_h -= overlap
    rect_x = center_x - rect_w / 2
    rect_y = center_y - rect_h / 2

    # Check if all corners of the rectangle are inside the bounding box
    return ((bounding_box[2] <= rect_x or rect_x+rect_w <= bounding_box[0]) or
            (bounding_box[3] <= rect_y or rect_y+rect_h <= bounding_box[1]))


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



def display_maps_page(display, surface, account, maps_page, width, height, font_color):

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
        # first cos not really border - solid
        # (but shouldn't matter - yet dont look right to me when black (dark mode - white looks fine)
        #nav.draw_border(surface, x, y, width, height, 4, font_color)

        level_surface = render_level_to_surface(gmap, (700, 600))  # map size without side window
        thumbnail = create_thumbnail(level_surface, (width, height))
        surface.blit(thumbnail, (x,y))
        map_image_rect = thumbnail.get_rect(topleft=(x,y))

        maptxt = gmap.name.upper() + " (" + difficulty[gmap.difficulty] + ")"
        map_name_text = font.render(maptxt, True, font_color)  # Black text
        map_name_rect = map_name_text.get_rect(topleft=(x, y+122))
        #map_name_rect = map_name_text.get_rect(topleft=(x, y+125))  # if border make y bigger
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
    npages = nmaps // maps_per_page + (nmaps % maps_per_page > 0)
    return nmaps, npages

def draw_map_window(display, surface, window_size, account=None, page=1):

    # For backward compatibility (should I still support no account)
    if hasattr(account, "dark_mode"):
        dark_mode = account.dark_mode
    else:
        dark_mode = False  # default should be False
        account.dark_mode = dark_mode
        account.save()

    # light mode
    if dark_mode:
        background_color = (54, 69, 79)
        font_color = (250, 249, 246)
    else:
        background_color =  (245, 245, 220)
        font_color = (0,0,0)

    pygame.draw.rect(surface, background_color, (0, 0, window_size[0], window_size[1]))
    window_width = window_size[0]
    window_height = window_size[1]

    font_title = pygame.font.SysFont('Arial', 24, bold=True)  # Choose a font and size
    map_menu_text = font_title.render("Choose a map", True, font_color)
    map_menu_rect = map_menu_text.get_rect(center=(window_width//2, 20))
    surface.blit(map_menu_text, map_menu_rect.topleft)

    #loop and call
    width = 180
    height = 120

    nmaps, npages = get_nmaps_npages()

    start_map = (page-1)*maps_per_page
    end_map = min(start_map+maps_per_page, nmaps)
    maps_page = map_classes[start_map:end_map]
    map_rects, maps = display_maps_page(display, surface, account, maps_page, width, height, font_color)

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

    if dark_mode:
        ldmode_image = lightmode_img
    else:
        ldmode_image = darkmode_img

    ldmode_rect = ldmode_image.get_rect(center=(window_width-70, window_height-70))
    surface.blit(ldmode_image, ldmode_rect.topleft)

    display.flip()
    return map_rects, maps, larrow_rect, rarrow_rect, ldmode_rect, load_account_rect, new_account_rect


def map_window(display, surface, window_size, account=None):

    page = 1
    map_rects, maps, larrow_rect, rarrow_rect, ldmode_rect, load_account_rect, new_account_rect = draw_map_window(display, surface, window_size, account, page)

    # loop to detect clicks
    noclicks = True
    map_id = None
    while noclicks:
        time.sleep(0.1)  # Reduce idle CPU usage
        for event in pygame.event.get():
            eleft = False
            eright = False
            mouse_pos = None
            if event.type == pygame.QUIT:
                noclicks = False
                return None, None
            elif event.type == pygame.KEYDOWN:
                mouse_pos = None
                if event.key == pygame.K_LEFT:
                    eleft = True
                    mouse_pos = (0,0)  # no doubt a better way but too tired - its 2am
                if event.key == pygame.K_RIGHT:
                    eright = True
                    mouse_pos = (0,0)  # no doubt a better way but too tired - its 2am
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

            if mouse_pos is not None or eleft or eright:

                if new_account_rect.collidepoint(mouse_pos):
                    new_account = new_profile(surface)
                    if new_account is not None:
                        account = new_account
                    map_rects, maps, larrow_rect, rarrow_rect, ldmode_rect, _, _  = draw_map_window(display, surface, window_size, account, page)

                if load_account_rect.collidepoint(mouse_pos):
                    new_account = profile_menu(surface)
                    if new_account is not None:
                        account = new_account
                    map_rects, maps, larrow_rect, rarrow_rect, ldmode_rect, _, _  = draw_map_window(display, surface, window_size, account, page)

                if ldmode_rect.collidepoint(mouse_pos):
                    account.dark_mode = not account.dark_mode
                    account.save()
                    map_rects, maps, larrow_rect, rarrow_rect, ldmode_rect, _, _  = draw_map_window(display, surface, window_size, account, page)

                if rarrow_rect and rarrow_rect.collidepoint(mouse_pos) or eright:
                    if periodic_arrows:
                        nmaps, npages = get_nmaps_npages()
                        page = page + 1 if page < npages else 1
                    else:
                        page += 1
                    map_rects, maps, larrow_rect, rarrow_rect, ldmode_rect,  _, _  = draw_map_window(display, surface, window_size, account, page)

                if larrow_rect and larrow_rect.collidepoint(mouse_pos) or eleft:
                    if periodic_arrows:
                        nmaps, npages = get_nmaps_npages()
                        page = page - 1 if page > 1 else npages
                    else:
                        page -= 1
                    map_rects, maps, larrow_rect, rarrow_rect, ldmode_rect, _, _  = draw_map_window(display, surface, window_size, account, page)


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
        self.alternate_paths = False

    def paint_features(self, window):
        pass

    def can_I_place(self, pos, w, h):
        return True

    def barriers(self):
        """A list of barriers"""
        return []

    def get_removables(self):
        """List of removable objects"""
        return []

    def set_removables(self, removables):
        pass

    def remove(self, rem, display, window):
        sounds.play('place')  #todo choose a sound
        # Need to find a good way to just remove prompt box before showing explosion.
        #sounds.play('pop')  # this is not right either - no better than place sound - need explosion sound
        #expl_img = pygame.transform.scale(explosion_img, (rem.loc[2], rem.loc[3]))
        #explosion_rect = expl_img.get_rect(topleft=(rem.loc[0], rem.loc[1]))
        #window.blit(expl_img, explosion_rect)
        #display.flip()
        #time.sleep(1)
        #pass


class PicnicPlace(Map):
    def __init__(self):
        super().__init__()
        self.name = "Picnic Place"
        self.difficulty = 1
        self.paths = [[(0, 400), (200, 100), (200, 400), (600, 400), (600, 200), (520, 200), (520, 600)]]
        self.background_color = (53, 94, 59)  # (0, 158, 96)
        self.path_thickness = 20
        self.path_color = (178, 190, 181)


class Staircase(Map):
    def __init__(self):
        super().__init__()
        self.name = "Staircase"
        self.difficulty = 2
        self.paths = [[(50, 100), (200, 100), (200, 300), (400, 300), (400, 500), (650, 500)]]
        self.background_color = (50, 25, 0)
        self.path_thickness = 15
        self.path_color = (0, 211, 211)


class Diamond(Map):
    def __init__(self):
        super().__init__()
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
        super().__init__()
        self.name = "Valley"
        self.difficulty = 3
        #self.paths = [[(0, 100), (300, 250), (400, 250), (700, 100)]]
        self.background_color = (69, 75, 27) # (53, 94, 59)  # (0, 158, 96)
        self.path_thickness = 20
        self.path_color = (96, 130, 182) # (178, 190, 181)

        path1 = [(0, 100), (300, 260), (400, 260), (700, 100)]
        path2 = [(0, 500), (300, 340), (400, 340), (700, 500)]
        self.paths = [path1, path2]

        #tmp for testing
        #self.alternate_paths = True


class Square(Map):
    def __init__(self):
        super().__init__()
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
        super().__init__()
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
        super().__init__()
        self.name = "Rubin's Vase"
        self.difficulty = 3
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


# Map for testing
class Eagle(Map):
    def __init__(self):
        super().__init__()
        self.name = "Eagle"
        self.difficulty = 1
        self.paths = [[(50, 100), (100, 100), (500, 300), (300, 300), (200, 450), (650, 500)]]
        self.background_color = (50, 25, 0)
        self.path_thickness = 15
        self.path_color = (0, 211, 211)



class Pentagram(Map):
    def __init__(self):
        super().__init__()
        self.name = "Pentagram"
        self.difficulty = 2
        path1 = [(100,350),(600,350),(200,100),(350,500),(500,100),(100,350)] # star (easy on own)

        path2 = [(100,350),(350,500),(600,350),(500,100),(200,100),(100,350),] #, (150, 500)]
        self.background_color = (145, 56, 49) #(50, 25, 0)
        self.path_thickness = 15
        self.path_color = (196, 180, 84) #(0, 211, 211)
        self.paths = [path1, path2]



# Map for testing
#class Eagles(Map):
    #def __init__(self):
        #self.name = "Eagles"
        #self.difficulty = 1
        #path1 = [(50, 100), (100, 100), (500, 300), (300, 300), (200, 450), (650, 500)]
        #path2 = [(50, 500), (350, 350), (350, 100), (285, 190), (350, 550)] #, (150, 500)]
        #self.background_color = (50, 25, 0)
        #self.path_thickness = 15
        #self.path_color = (0, 211, 211)
        #self.paths = [path1,path2]

class Distortion(Map):
    def __init__(self):
        super().__init__()
        self.name = "Distortion"
        self.difficulty = 3
        self.background_color = (150, 105, 25) #(99, 3, 48) # (0,0,0) #(2, 48, 32) #(50, 25, 0)
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
        super().__init__()
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

class Village(Map):
    def __init__(self):
        super().__init__()
        self.name = "Village"
        self.difficulty = 1
        #self.paths = [[(50, 100), (200, 100), (200, 300), (400, 300), (400, 500), (650, 500)]]
        self.paths = [[(0, 280), (100, 280), (100, 100), (300, 100), (300, 280), (400, 280),
                      (400,100),(600,100),(600,500),(400,500),(400,400), (400,320),(300,320),
                      (300,500),(100,500),(100,320),(0,320)]]
        self.background_color = (2, 48, 32) # (53, 94, 59) #(0,0,0) night
        self.path_thickness = 20
        self.path_color = (238, 220, 130)

        self.house1 = (120, 110, 160, 140)
        self.house2 = (420, 110, 160, 140)
        self.house3 = (120, 350, 160, 140)
        self.house4 = (420, 350, 160, 140)
        self.tree1 = (315, 335, 70, 160)
        self.tree2 = (315, 100, 70, 160)

    def paint_features(self, window):
        window.blit(house1_img, self.house1)
        window.blit(house2_img, self.house2)
        window.blit(house2_img, self.house3)
        window.blit(house1_img, self.house4)
        window.blit(tree1_img, self.tree1)
        window.blit(tree1_img, self.tree2)

    def can_I_place(self, pos, w, h):
        if not is_rect_out_box(pos[0], pos[1], w, h, self.house1, wh=True):
            return False
        if not is_rect_out_box(pos[0], pos[1], w, h, self.house2, wh=True):
            return False
        if not is_rect_out_box(pos[0], pos[1], w, h, self.house3, wh=True):
            return False
        if not is_rect_out_box(pos[0], pos[1], w, h, self.house4, wh=True):
            return False
        if not is_rect_out_box(pos[0], pos[1], w, h, self.tree1, wh=True):
            return False
        if not is_rect_out_box(pos[0], pos[1], w, h, self.tree2, wh=True):
            return False
        return True

    def barriers(self):
        """A list of barriers"""
        return [self.house1, self.house2, self.house3, self.house4]

class DarkForest(Map):
    def __init__(self):
        super().__init__()
        self.name = "Dark Forest"
        self.difficulty = 3
        self.alternate_paths = True
        path1 = [(330, 0), (330, 90), (450, 90), (450, 160), (540, 160), (540, 350),
                (430, 350), (430, 300),(330, 300), (330, 450), (200,450), (200,150),
                (110, 150), (110, 300), (0, 300)]
        path2 = [(180, 0), (180, 150), (110, 150), (110, 340), (200, 340), (200, 240),
                 (330, 240), (330, 550), (470, 550), (470, 350), (540, 350),
                 (540, 310), (700, 310)]
        self.paths = [path1, path2]
        self.background_color = (0,0,0) #night
        self.path_thickness = 15
        #self.path_color = (238, 220, 130)  # dev color
        self.path_color = (0,0,0) # Real color

        self.tree1 = (380, 110, 70, 160)
        self.tree2 = (450, 170, 70, 160)
        self.tree3 = (540, 330, 90, 180)
        self.tree4 = (570, 140, 70, 160)
        self.tree5 = (350, 365, 70, 160)
        self.tree55 = (390, 380, 70, 160)
        self.tree6 = (220, 250, 90, 180)
        self.tree7 = (240, 70, 70, 160)
        self.tree8 = (120, 170, 70, 160)
        self.tree9 = (30, 350, 90, 180)
        self.tree10 = (40, 120, 70, 160)
        self.tree11 = (125, 410, 70, 160)
        #self.moon = (540, 60, 50, 50)

        self.trees = [self.tree1, self.tree2, self.tree3, self.tree4, self.tree5, self.tree55,
                      self.tree6, self.tree7, self.tree8, self.tree9, self.tree10, self.tree11]

    def paint_features(self, window):
        window.blit(tree1_img, self.tree1)
        window.blit(tree1_img, self.tree2)
        window.blit(bigtree_img, self.tree3)
        window.blit(tree1_img, self.tree4)
        window.blit(tree1_img, self.tree5)
        window.blit(tree1_img, self.tree55)
        window.blit(bigtree_img, self.tree6)
        window.blit(tree1_img, self.tree7)
        window.blit(tree1_img, self.tree8)
        window.blit(bigtree_img, self.tree9)
        window.blit(tree1_img, self.tree10)
        window.blit(tree1_img, self.tree11)
        #window.blit(moon_img, self.moon)

    def can_I_place(self, pos, w, h):
        for tree in self.trees:
            if not is_rect_out_box(pos[0], pos[1], w, h, tree, wh=True):
                return False
        return True

    def barriers(self):
        """A list of barriers"""
        return self.trees


class Hermit(Map):
    def __init__(self):
        super().__init__()
        self.name = "Hermit's House"
        self.difficulty = 2
        #self.background_color =  (69, 75, 27) # original
        self.background_color =  (240, 255, 255) # snowy/alpine (kind of like but maybe too bright)
        #self.background_color =  (114, 47, 55) # (Wine) I like this color but maybe not for this map
        #self.background_color =  (99, 3, 48) # again I like but prob not for this map
        #self.background_color = (103, 49, 71) # same again
        #self.background_color = (25, 25, 112) # Again   (128, 70, 27)

         # (53, 94, 59)  # (0, 158, 96)
        self.path_thickness = 20
        self.path_color = (96, 130, 182) # (178, 190, 181)

        path1 = [(350, 0), (350, 100), (200, 100), (200, 300), (130, 300), (130, 450),
                 (270, 450), (270, 300), (130, 300), (130, 450), (80, 450), (80, 600)]

        path2 = [(350, 0), (350, 100), (200, 100), (200, 300), (270, 300), (270, 450),
                 (130, 450), (130, 300), (270, 300),(270, 450), (320, 450), (320, 600)]

        path3 = [(350, 0), (350, 100), (500, 100), (500, 300), (430, 300), (430, 450),
                 (570, 450), (570, 300), (430, 300), (430, 450), (380, 450), (380, 600)]

        path4 = [(350, 0), (350, 100), (500, 100), (500, 300), (570, 300), (570, 450),
                 (430, 450), (430, 300), (570, 300), (570, 450), (620, 450), (620, 600)]

        self.paths = [path1, path2, path3, path4]

        self.tree1 = (215, 110, 90, 180)
        self.tree2 = (400, 110, 90, 180)
        self.house = (270, 300, 160, 140)
        self.obstacles = [self.tree1, self.tree2, self.house]

    def paint_features(self, window):
        window.blit(bigtree_img, self.tree1)
        window.blit(bigtree_img, self.tree2)
        window.blit(house3_img, self.house)


    def can_I_place(self, pos, w, h):
        for obstacle in self.obstacles:
            if not is_rect_out_box(pos[0], pos[1], w, h, obstacle, wh=True):
                return False
        return True

    def barriers(self):
        """A list of barriers"""
        return self.obstacles


# experiment as not really happy with this level. Too easy for its daunting appearance.
class Pentagram2(Map):
    def __init__(self):
        super().__init__()
        self.name = "Pentagram2"
        self.difficulty = 2
        path1 = [(100,350), (600,350), (200,100), (350,500)]

        path2 = [(200,100), (350,500), (500,100), (100,350)]

        path3 = [(100,350),(350,500),(600,350),(500,100),(200,100),(100,350),] #, (150, 500)]
        self.background_color = (145, 56, 49) #(50, 25, 0)
        self.path_thickness = 15
        self.path_color = (196, 180, 84) #(0, 211, 211)
        self.paths = [path1, path2, path3]



class Removable():
    # TODO hmm if store img - will need to remove when pickle - or store image dictionary lookup.
    def __init__(self, location, price, img):
        self.loc = location
        self.price = price
        self.img = img
        self.rect = pygame.Rect(self.loc)


class Hermit2(Map):
    def __init__(self):
        super().__init__()
        self.name = "Hermit's House 2"
        self.difficulty = 2
        #self.background_color =  (69, 75, 27) # original
        #self.background_color =  (240, 255, 255) # snowy/alpine (kind of like but maybe too bright)
        #self.background_color =  (114, 47, 55) # (Wine) I like this color but maybe not for this map
        self.background_color =  (99, 3, 48) # again I like but prob not for this map
        #self.background_color = (103, 49, 71) # same again
        #self.background_color = (25, 25, 112) # Again   (128, 70, 27)

         # (53, 94, 59)  # (0, 158, 96)
        self.path_thickness = 20
        self.path_color = (96, 130, 182) # (178, 190, 181)

        path1 = [(350, 0), (350, 100), (200, 100), (200, 300), (130, 300), (130, 450),
                 (270, 450), (270, 300), (130, 300), (130, 450), (80, 450), (80, 600)]

        path2 = [(350, 0), (350, 100), (200, 100), (200, 300), (270, 300), (270, 450),
                 (130, 450), (130, 300), (270, 300),(270, 450), (320, 450), (320, 600)]

        path3 = [(350, 0), (350, 100), (500, 100), (500, 300), (430, 300), (430, 450),
                 (570, 450), (570, 300), (430, 300), (430, 450), (380, 450), (380, 600)]

        path4 = [(350, 0), (350, 100), (500, 100), (500, 300), (570, 300), (570, 450),
                 (430, 450), (430, 300), (570, 300), (570, 450), (620, 450), (620, 600)]

        self.paths = [path1, path2, path3, path4]

        self.tree1 = Removable((215, 110, 90, 180), 500, "bigtree_img")
        self.tree2 = Removable((400, 110, 90, 180), 500, "bigtree_img")
        self.house = Removable((270, 300, 160, 140), 1000, "house3_img")
        self.removables = [self.tree1, self.tree2, self.house]

        #self.obstacles = [self.tree1.loc, self.tree2.loc, self.house.loc]

    def paint_features(self, window):
        #window.blit(bigtree_img, self.tree1.loc)
        #window.blit(bigtree_img, self.tree2.loc)
        #window.blit(house3_img, self.house.loc)

        # could be obstaclte being a superset of removables but for this test all removable.
        #for ob in self.obstacles:
        for ob in self.removables:
            window.blit(img_dict[ob.img], ob.loc)


    def can_I_place(self, pos, w, h):
        #for obstacle in self.obstacles:
        #print(f"{self.removables=}")
        for obstacle in self.removables:
            if not is_rect_out_box(pos[0], pos[1], w, h, obstacle.loc, wh=True):
                return False
        return True

    def barriers(self):
        """A list of barriers"""
        #return self.obstacles
        #return self.removables
        return [removable.loc for removable in self.removables]

    def get_removables(self):
        return self.removables

    def set_removables(self, removables):
        self.removables = removables

    def remove(self, rem, display, window):
        super().remove(rem, display, window)
        self.removables.remove(rem)


class Tmp(Map):
    def __init__(self):
        super().__init__()
        self.name = "Tmp"
        self.difficulty = 1
        self.background_color = (184, 115, 51) #(53, 94, 59)
        self.path_thickness = 20
        self.path_color = (178, 190, 181)
        self.paths = [[(0, 130), (120, 130),(120, 510),(285, 510),
                       (285, 242),(410, 242),(410, 510),
                       (580, 510),(580, 130), (710, 130)
                       ]]

        self.tree1 = Removable((304, 55, 90, 180), 200, "bigtree_img")
        self.tree2 = Removable((304, 330, 90, 180), 500, "bigtree_img")

        #self.house1 = Removable((1, 150, 160, 140), 750, "house1_img")
        #self.house2 = Removable((1, 290, 160, 140), 300, "house2_img")
        #self.house3 = Removable((1, 440, 160, 140), 300, "house3_img")

        self.tree3 = Removable((15, 150, 160, 140), 500, "bigtree_img")
        self.tree4 = Removable((15, 340, 160, 140), 300, "bigtree_img")
        self.tree5 = Removable((595, 150, 160, 140), 500, "bigtree_img")
        self.tree6 = Removable((595, 340, 160, 140), 300, "bigtree_img")

        self.house4 = Removable((125, 80, 160, 140), 750, "house1_img")
        self.house5 = Removable((125, 220, 160, 140), 750, "house2_img")
        self.house6 = Removable((125, 360, 160, 140), 750, "house3_img")

        self.house7 = Removable((420, 80, 160, 140), 300, "house1_img")
        self.house8 = Removable((420, 220, 160, 140), 500, "house2_img")
        self.house9 = Removable((420, 360, 160, 140), 750, "house3_img")

        self.tree7 = Removable((120, 525, 160, 60), 150, "shortwidetree_img")
        self.tree8 = Removable((420, 525, 160, 60), 150, "shortwidetree_img")
        self.tree9 = Removable((15, 50, 160, 60), 100, "shorttree_img")
        self.tree10 = Removable((595, 50, 160, 60), 100, "shorttree_img")


        # TODO - need to deal with clicking through inset window.
        self.removables = [self.tree1, self.tree2, self.tree3,
                           self.tree4, self.tree5, self.tree6,
                           self.tree7, self.tree8, self.tree9, self.tree10,
                           #self.house1, self.house2, self.house3,
                           self.house4, self.house5, self.house6,
                           self.house7, self.house8, self.house9
                           ]

    # This stuff below might be general enough to be inheritable
    def paint_features(self, window):
        for ob in self.removables:
            window.blit(img_dict[ob.img], ob.loc)

    def can_I_place(self, pos, w, h):
        for obstacle in self.removables:
            if not is_rect_out_box(pos[0], pos[1], w, h, obstacle.loc, wh=True):
                return False
        return True

    def barriers(self):
        """A list of barriers"""
        return [removable.loc for removable in self.removables]

    def get_removables(self):
        return self.removables

    def set_removables(self, removables):
        self.removables = removables

    def remove(self, rem, display, window):
        super().remove(rem, display, window)
        self.removables.remove(rem)



# dont need to be a dictionary
#map_classes  = {1: PicnicPlace, 2: Spiral, 3: Staircase, 4: Diamond, 5: Valley, 6: Square}
map_classes  = [PicnicPlace, Spiral, Staircase, Diamond, Valley, Square,
                Village, Vase, Castle, Pentagram, Distortion, DarkForest,
                Hermit, Tmp] # Eagle]

difficulty  = {1: "Easy", 2: "Medium", 3: "Hard", 4: "Expert"}
