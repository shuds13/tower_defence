import pygame
pygame.mixer.init()

snd_blop = pygame.mixer.Sound('blop.wav')
snd_ting = pygame.mixer.Sound('ting.wav')
snd_place = pygame.mixer.Sound('place.wav')
snd_sell = pygame.mixer.Sound('sell.wav')
snd_pop = pygame.mixer.Sound('pop.wav')
snd_glue = pygame.mixer.Sound('splat.wav')
snd_victory = pygame.mixer.Sound('fanfare.wav')


sounds = {
    'blop':snd_blop,
    'ting':snd_ting,
    'place':snd_place,
    'sell':snd_sell,
    'pop':snd_pop,
    'glue':snd_glue,
    'victory':snd_victory,
    }

#print("volume", pygame.mixer.Sound.get_volume())

# TODO try removing mixer everywhere else - then need import sounds here and reference via some key
# dont know why have to set volume for sounds individually rather than for mixer. But need import here
# to avoid having to set volume on every call.
def play(snd):
    #print("sound volume", sounds[snd].get_volume())
    sounds[snd].play()


# annoying cant just set mixer volume - atleast I could reduce some some than others if need to.
def set_volume(vol):
    for sound in sounds.values():
        sound.set_volume(vol)

def get_volume():
    return sounds['blop'].get_volume()



