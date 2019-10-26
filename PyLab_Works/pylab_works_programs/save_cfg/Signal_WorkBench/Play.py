import pygame
from pygame.locals import *

filename = 'D:/Data_Python/btc/t.wav'
pygame.mixer.init(9766, 8, 1)

soundfile = pygame.mixer.Sound(filename)
soundfile.play()

#pygame.mixer.music.load(filename)
#pygame.mixer.music.play()

print 'aap'