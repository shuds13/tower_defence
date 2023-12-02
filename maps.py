import pygame


def map_window(display, surface, window_size):
    #window_size = (900, 600)
    pygame.draw.rect(surface, (200, 200, 200), (0, 0, window_size[0], window_size[1]))
    #window = pygame.display.set_mode(window_size)
    width = window_size[0]
    chosen = False

    font_title = pygame.font.SysFont('Arial', 16, bold=True)  # Choose a font and size
    font = pygame.font.SysFont(None, 24)


    #loop and call
    x=0
    y=20
    map_rects = []
    maps = []
    # map is keyword - so gmap = game map
    for map_class in map_classes.values():
        #create? Well if I want to eventually to show thumbnails of maps will need create something
        gmap = map_class()
        map_name_text = font_title.render(gmap.name.upper(), True, (0, 0, 0))  # Black text
        map_name_rect = map_name_text.get_rect(center=(x + width // 2, y))
        surface.blit(map_name_text, map_name_rect.topleft)
        y+=50
        map_rects.append(map_name_rect)
        maps.append(gmap)

    print(f"Maps: {maps}")

    display.flip()
    # loop to detect clicks
    noclicks = True
    while noclicks:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                noclicks = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                map_id = process_click(map_rects, mouse_pos)
                if map_id is not None:
                    print('chosen map')
                    noclicks = False
                    break
                #gmap, noclicks = draw_map_window(window, window_size, mouse_pos)
                #pygame.display.flip()  # Update the full display Surface to the screen

    gmap = maps[map_id]
    print(f"Map is {gmap.name}")

    return gmap


def process_click(map_rects, mouse_pos):
    # Upgrade tower
    for i, map_rect in enumerate(map_rects):
        print(i, map_rect)
        if map_rect.collidepoint(mouse_pos):
            print('here')
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
