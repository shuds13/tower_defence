import pygame
import maps
import pickle
from pathlib import Path
import os

def new_profile(screen):
    screen_width, screen_height = 600, 150
    #screen = pygame.display.set_mode((screen_width, screen_height))
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

    #profile_data = {'name': profile_name}
    account = Account(name=profile_name)
    account.save()
    #print(f"Profile '{profile_name}' saved.")
    # Return True with an empty message when the save is successful
    return account, ''


# Function to load a selected profile
def load_profile(filename):
    with open(f'profiles/{filename}', 'rb') as file:
        return pickle.load(file)


def profile_menu(screen):
    # Window settings
    screen_width, screen_height = 600, 400
    #screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Account Loader")
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
            text_surface = font.render(filename, True, (0, 0, 0))
            text_rect = text_surface.get_rect(topleft=(20, y))
            screen.blit(text_surface, text_rect)
            profiles.append({'filename': filename, 'rect': text_rect})
            y += 40

        pygame.display.flip()

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
        path=Path.cwd() / Path("profiles")
        with Path(path / Path(self.name + ".pkl")).open("wb") as f:
            pickle.dump(self, f)
