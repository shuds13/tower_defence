import pygame
import maps
import pickle
from pathlib import Path
import os

#pygame.init()

#def load_account():
    #filename = "me"
    #path=Path.cwd()
    #with Path(path / Path(filename + ".pickle")).open("r") as f:
        #pickle.load(self, f)

def profile_menu(screen):
    # Window settings
    screen_width, screen_height = 600, 400
    #screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Account Loader")
    #pygame.draw.rect(screen, (245, 245, 220), (0, 0, screen_width, screen_height))

    font = pygame.font.Font(None, 36)

    # TODO: Fow now I'm making profiles dir but will make if does not exist

    # Load profile names from the 'profiles' directory
    profile_files = [f for f in os.listdir('profiles') if f.endswith('.pkl')]
    profiles = []

    # Function to load a selected profile
    def load_profile(filename):
        with open(f'profiles/{filename}', 'rb') as file:
            return pickle.load(file)

    # Main loop
    running = True
    selected_profile = None
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                for i, profile in enumerate(profiles):
                    if profile['rect'].collidepoint(mouse_x, mouse_y):
                        selected_profile = load_profile(profile_files[i])
                        print(f"Loaded profile: {selected_profile}")
                        break
        if selected_profile is not None:
            break

        screen.fill((255, 255, 255))

        # Display profile names
        profiles = []
        y = 20
        for filename in profile_files:
            text_surface = font.render(filename, True, (0, 0, 0))
            text_rect = text_surface.get_rect(topleft=(20, y))
            screen.blit(text_surface, text_rect)
            profiles.append({'filename': filename, 'rect': text_rect})
            y += 40

        pygame.display.flip()

    #pygame.display.quit()
    return selected_profile


class Account():
    def __init__(self, name='Guest'):
        self.name = name
        self.maps_complete = []
        self.maps_aced = []

    # map is keyword, use gmap (game map)
    def complete_map(self, gmap, aced=False):
        if not gmap in self.maps_complete:
            self.maps_complete.append(gmap)
            print(self.maps_complete)

        if aced:
            if not gmap in self.maps_aced:
                self.maps_aced.append(gmap)

    def save(self):
        filename = "me"
        path=Path.cwd() / Path("profiles")
        with Path(path / Path(filename + ".pkl")).open("wb") as f:
            print(f'Here {Path(path / Path(filename + ".pkl"))}')
            pickle.dump(self, f)

    #hmmm nope
    #def load_profile(self):
        #filename = "me"
        #path=Path.cwd()
        #with Path(path / Path(filename + ".pickle")).open("r") as f:
            #pickle.load(self, f)

