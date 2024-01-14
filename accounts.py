import pygame
import maps
import pickle
from pathlib import Path
import os

def new_profile(screen):
    screen_width, screen_height = 600, 150
    pygame.display.set_caption("Create New Profile")
    font = pygame.font.Font(None, 40)
    clock = pygame.time.Clock()

    input_active = True
    user_text = ''
    base_prompt = 'Enter Profile Name: '
    error_message = ''

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if input_active:
                    if event.key == pygame.K_RETURN:
                        # Attempt to save profile
                        if not user_text:
                            return  # Do nothing if user_text is empty
                        account, message = save_profile(user_text)
                        if account is not None:
                            return account
                        else:
                            error_message = message
                            user_text = ''  # Clear input for new entry
                    elif event.key == pygame.K_BACKSPACE:
                        user_text = user_text[:-1]
                    else:
                        user_text += event.unicode

        screen.fill((255, 255, 255))
        text_surface = font.render(base_prompt + user_text, True, (0, 0, 0))
        error_surface = font.render(error_message, True, (255, 0, 0))
        screen.blit(text_surface, (50, 50))
        screen.blit(error_surface, (50, 100))
        pygame.display.flip()
        clock.tick(60)


def save_profile(profile_name):
    if not os.path.exists('profiles'):
        os.makedirs('profiles')
    file_path = f'profiles/{profile_name}.pkl'
    if os.path.exists(file_path):
        # Return False with an error message if the file already exists
        return None, "Profile already exists. Please enter a different name."
    account = Account(name=profile_name)
    account.save()
    return account, ''


# Function to load a selected profile
def load_profile(filename):
    with open(f'profiles/{filename}', 'rb') as file:
        return pickle.load(file)


def profile_menu(screen):
    # Window settings
    screen_width, screen_height = 600, 400
    pygame.display.set_caption("Profile Loader")
    font = pygame.font.Font(None, 36)

    # TODO: Fow now I'm making profiles dir but will make if does not exist

    # Load profile names from the 'profiles' directory
    profile_files = [f for f in os.listdir('profiles') if f.endswith('.pkl')]
    profiles = []

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
                        #print(f"Loaded profile: {selected_profile}")
                        break
        if selected_profile is not None:
            break

        screen.fill((255, 255, 255))

        # Display profile names
        profiles = []
        y = 20
        for filename in profile_files:
            text_surface = font.render(os.path.splitext(filename)[0], True, (0, 0, 0))
            text_rect = text_surface.get_rect(topleft=(20, y))
            screen.blit(text_surface, text_rect)
            profiles.append({'filename': filename, 'rect': text_rect})
            y += 40
        pygame.display.flip()
    return selected_profile


class Account():
    """Class to handle user profiles"""
    def __init__(self, name='Guest'):
        self.name = name
        self.maps_complete = []
        self.maps_aced = []
        self.maps_in_progress = {}
        self.dark_mode = False

    def failed_map(self, gmap):
        self.maps_in_progress.pop(gmap.name, None)

    # map is keyword, use gmap (game map)
    def complete_map(self, gmap, aced=False):
        gmap_class = gmap.__class__
        if not gmap_class in self.maps_complete:
            self.maps_complete.append(gmap_class)
        if aced:
            if not gmap_class in self.maps_aced:
                self.maps_aced.append(gmap_class)
        self.maps_in_progress.pop(gmap.name, None)

    def save_map(self, gmap, game):
        #print(f"Saving map {gmap} as level {game.level}")
        self.maps_in_progress[gmap] = game

    def save(self):
        #print(f'saving game {self.name}')
        path=Path.cwd() / Path("profiles")
        with Path(path / Path(self.name + ".pkl")).open("wb") as f:
            pickle.dump(self, f)
