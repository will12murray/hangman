import os
import sys
import pygame
# locals module includes functions like "Rect" to create a rectangle object, and many constants like "QUIT, HWSURFACE" that are used to interact with the rest of pygame
from pygame.locals import *

if not pygame.font:
    print('Warning, fonts disabled.')
if not pygame.mixer:
    print('Warning, sound disabled.')

# Loading images / sounds.


def load_image(name, colorkey=None):
    fullname = os.path.join(
        '/Users/willmurray/Google Drive/Coding/hangman/', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image: ', name)
        raise SystemExit(message)
    image = image.convert()
