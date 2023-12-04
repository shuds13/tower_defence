import pygame
import navigation as nav


def render_level_to_surface(gmap, size):
    # Create a new surface
    level_surface = pygame.Surface(size)
    level_surface.fill(gmap.background_color)

    # Draw the background
    #level_surface.blit(background_image, (0, 0))

    # Draw the path
    for i in range(len(gmap.path) - 1):
        pygame.draw.line(level_surface, gmap.path_color, gmap.path[i], gmap.path[i + 1], 5)

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

    x = window_width//2 - width//2
    y = 20

    map_rects = []
    maps = []
    gmap = None
    # map is keyword - so gmap = game map
    for map_class in map_classes.values():
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


class Staircase(Map):
    def __init__(self):
        self.name = "Staircase"
        self.path = [(50, 100), (200, 100), (200, 300), (400, 300), (400, 500), (650, 500)]
        self.background_color = (50, 25, 0)
        self.path_thickness = 15
        self.path_color = (0, 211, 211)


class PicnicPlace(Map):
    def __init__(self):
        self.name = "Picnic Place"
        self.path = [(0, 400), (200, 100), (200, 400), (600, 400), (600, 200), (520, 200), (520, 600)]
        self.background_color = (53, 94, 59)  # (0, 158, 96)
        self.path_thickness = 20
        self.path_color = (178, 190, 181)

map_classes  = {1: PicnicPlace, 2: Staircase}
