import pygame
pygame.mixer.init()

snd_blop = pygame.mixer.Sound('sounds/blop.wav')
snd_ting = pygame.mixer.Sound('sounds/ting.wav')
snd_place = pygame.mixer.Sound('sounds/place.wav')
snd_sell = pygame.mixer.Sound('sounds/sell.wav')
snd_pop = pygame.mixer.Sound('sounds/pop.wav')
snd_glue = pygame.mixer.Sound('sounds/splat.wav')
snd_victory = pygame.mixer.Sound('sounds/fanfare.wav')
snd_unlock = pygame.mixer.Sound('sounds/unlock.wav')


sounds = {
    'blop':snd_blop,
    'ting':snd_ting,
    'place':snd_place,
    'sell':snd_sell,
    'pop':snd_pop,
    'glue':snd_glue,
    'victory':snd_victory,
    'unlock':snd_unlock,
    }

def play(snd):
    sounds[snd].play()

# cant just set mixer volume - must do for each sound
def set_volume(vol):
    for sound in sounds.values():
        sound.set_volume(vol)

def get_volume():
    return sounds['blop'].get_volume()
