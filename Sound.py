import pygame

class Sound (object):
    channel = pygame.mixer.Channel (2)
    opening = pygame.mixer.Sound ("assets/sound/opening_song.wav")
    pickUp_small = pygame.mixer.Sound ("assets/sound/waka_waka.wav")
    pickUp_large = pygame.mixer.Sound ("assets/sound/eating_cherry.wav")
    eatGhost = pygame.mixer.Sound ("assets/sound/eating_ghost.wav")
    death = pygame.mixer.Sound ("assets/sound/pacmandies.wav")
    lose = pygame.mixer.Sound ("assets/sound/gameover.wav")
    win = pygame.mixer.Sound ("assets/sound/youwin.wav")
