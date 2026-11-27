import functools
import pygame


def load_image(path):
    """Load an image, converted to the display format when a window exists (much faster to draw)."""
    image = pygame.image.load(path)
    if pygame.display.get_surface() is not None:
        image = image.convert_alpha()
    return image


@functools.lru_cache(maxsize=None)
def sys_font(name, size, bold=False, italic=False):
    """pygame.font.SysFont, created once per name and size instead of every frame."""
    return pygame.font.SysFont(name, size, bold, italic)
