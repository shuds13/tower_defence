import pygame
import textwrap

r1 = "Click on towers on the right, and click on the map to place."
r12 = "Ghosts are coming. The wizard can see them, but other towers need a little help."
r30 = "Report from scouts, trolls spotted!"
r33 = "Meteors are reinforced and come fast."
r40 = "A king this way comes."
r47 = "Prepare for round 47. If you have money to spend, I would spend it now!"

hints = {
    1: r1,
    12: r12,
    30: r30,
    33: r33,
    40: r40,
    47: r47,
    }


def _render_text_box(screen, text, font, max_line_width, box_bottom, box_left, text_color, bg_color):
    words = text.split(' ')
    lines = []
    while words:
        line = ''
        while words and font.size(line + words[0])[0] <= max_line_width:
            line += words.pop(0) + " "
        lines.append(line)

    # Calculate the height of the text box
    line_height = font.get_linesize()
    box_height = len(lines) * line_height

    # Calculate the top and left of the box
    box_top = box_bottom - box_height - 10
    #box_left = 240

    # Draw the background rectangle
    pygame.draw.rect(screen, (0,0,0), (box_left-2, box_top-2, max_line_width+24, box_height + 14))
    hint_button = pygame.draw.rect(screen, bg_color, (box_left, box_top, max_line_width+20, box_height+10))

    # Render the text line by line
    y = box_top
    for line in lines:
        text_surface = font.render(line, True, text_color)
        screen.blit(text_surface, (box_left+10, y+5))
        y += line_height

    return hint_button


def generate_hint(window, round_num, inset):
    hint = hints.get(round_num)
    if hint is None:
        return
    font = pygame.font.SysFont('Arial', 20)
    # Move to allow for inset window if on right
    box_left = 240
    if inset['active']:
        if inset['x'] == inset['xr']:
            box_left = 40
    hint_button = _render_text_box(window, hint, font, 400, 580, box_left, (0,0,0), (182, 208, 226))
    return hint_button

