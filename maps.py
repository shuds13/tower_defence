import pygame
import navigation as nav


def render_level_to_surface(gmap, size):
    # Create a new surface
    level_surface = pygame.Surface(size)
    level_surface.fill(gmap.background_color)

    # Draw the background
    #level_surface.blit(background_image, (0, 0))

    # Draw the path
    for path in gmap.paths:
        for i in range(len(path) - 1):
            pygame.draw.line(level_surface, gmap.path_color, path[i], path[i + 1], 5)

    return level_surface

def create_thumbnail(level_surface, thumbnail_size):
    return pygame.transform.scale(level_surface, thumbnail_size)


def options_window(display, surface, window_size):
    pygame.draw.rect(surface, (245, 245, 220), (0, 0, window_size[0], window_size[1]))  # alt color


def map_window(display, surface, window_size):
    #window_size = (900, 600)
    #pygame.draw.rect(surface, (159, 226, 191), (0, 0, window_size[0], window_size[1]))
    pygame.draw.rect(surface, (245, 245, 220), (0, 0, window_size[0], window_size[1]))  # alt color
    #window = pygame.display.set_mode(window_size)
    window_width = window_size[0]
    chosen = False

    font_title = pygame.font.SysFont('Arial', 24, bold=True)  # Choose a font and size
    font = pygame.font.SysFont(None, 24)

    map_name_text = font_title.render("Choose a map", True, (0, 0, 0))  # Black text
    map_name_rect = map_name_text.get_rect(midleft=(10, 10))
    surface.blit(map_name_text, map_name_rect.topleft)

    #loop and call
    width = 180
    height = 120

    start_y = 80
    #x = window_width//2 - width//2
    x = 60  # 200 works with col_size 4
    y = start_y  # 10 works with col_size 4
    #col_size = 4  # max is 4
    col_size = 3  # max is 4

    map_rects = []
    maps = []
    gmap = None
    # map is keyword - so gmap = game map
    for count, map_class in enumerate(map_classes.values()):
        #create? Well if I want to eventually to show thumbnails of maps will need create something
        gmap = map_class()

        # if not using thumbnails
        #map_name_rect = nav.draw_button(surface, gmap.name.upper(), (x, y), (width, height))

        # if using thumbnails
        level_surface = render_level_to_surface(gmap, (700, 600))  # map size without side window
        thumbnail = create_thumbnail(level_surface, (width, height))
        surface.blit(thumbnail, (x,y))
        map_image_rect = thumbnail.get_rect(topleft=(x,y))

        map_name_text = font.render(gmap.name.upper(), True, (0, 0, 0))  # Black text
        map_name_rect = map_name_text.get_rect(topleft=(x, y+120))
        surface.blit(map_name_text, map_name_rect.topleft)


        y+=150
        map_rects.append(map_image_rect)
        maps.append(gmap)
        if (count+1) % col_size == 0:
            y = start_y
            x += width+20

    display.flip()
    # loop to detect clicks
    noclicks = True
    map_id = None
    while noclicks:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                noclicks = False
                return None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                map_id = process_click(map_rects, mouse_pos)
                if map_id is not None:
                    noclicks = False
                    break
    gmap = maps[map_id]
    return gmap


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
        self.paths = [[(0, 400), (200, 100), (200, 400), (600, 400), (600, 200), (520, 200), (520, 600)]]
        self.background_color = (53, 94, 59)  # (0, 158, 96)
        self.path_thickness = 20
        self.path_color = (178, 190, 181)


class Staircase(Map):
    def __init__(self):
        self.name = "Staircase"
        self.paths = [[(50, 100), (200, 100), (200, 300), (400, 300), (400, 500), (650, 500)]]
        self.background_color = (50, 25, 0)
        self.path_thickness = 15
        self.path_color = (0, 211, 211)


class Diamond(Map):
    def __init__(self):
        self.name = "Diamond"
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
        self.background_color = (0, 71, 171)
        self.path_thickness = 20
        self.path_color = (0, 163, 108)

        path1 = [(250, 0), (250, 600)]
        path2 = [(450, 0), (450, 600)]
        path3 = [(0, 200), (700, 200)]
        path4 = [(0, 400), (700, 400)]
        self.paths = [path1, path2, path3, path4]


map_classes  = {1: PicnicPlace, 2: Staircase, 3: Diamond, 4:Valley, 5:Square}
