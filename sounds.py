import pygame
pygame.mixer.init()

# Channels kept for one-off tower sounds, so a flood of hit sounds cannot use them all up
special_sounds = {'nighthawk', 'fireball'}
num_reserved = pygame.mixer.set_reserved(len(special_sounds))
reserved_channels = [pygame.mixer.Channel(i) for i in range(num_reserved)]

snd_blop = pygame.mixer.Sound('sounds/blop.wav')
snd_ting = pygame.mixer.Sound('sounds/ting.wav')
snd_place = pygame.mixer.Sound('sounds/place.wav')
snd_sell = pygame.mixer.Sound('sounds/sell.wav')
snd_pop = pygame.mixer.Sound('sounds/pop.wav')
snd_glue = pygame.mixer.Sound('sounds/splat.wav')
snd_victory = pygame.mixer.Sound('sounds/fanfare.wav')
snd_unlock = pygame.mixer.Sound('sounds/unlock.wav')
snd_nighthawk = pygame.mixer.Sound('sounds/power_up_ray.wav')
snd_fireball = pygame.mixer.Sound('sounds/small_fireball.wav')
snd_ting_deep = pygame.mixer.Sound('sounds/ting_deep.wav')


sounds = {
    'blop':snd_blop,
    'ting':snd_ting,
    'ting_deep':snd_ting_deep,
    'place':snd_place,
    'sell':snd_sell,
    'pop':snd_pop,
    'glue':snd_glue,
    'victory':snd_victory,
    'unlock':snd_unlock,
    'nighthawk':snd_nighthawk,
    'fireball':snd_fireball,
    }

def play(snd):
    if snd in special_sounds and reserved_channels:
        # Use a free reserved channel, or restart the first one if both are busy
        channel = next((c for c in reserved_channels if not c.get_busy()), reserved_channels[0])
        channel.play(sounds[snd])
    else:
        sounds[snd].play()

# cant just set mixer volume - must do for each sound
def set_volume(vol):
    for sound in sounds.values():
        sound.set_volume(vol)

def get_volume():
    return sounds['blop'].get_volume()
