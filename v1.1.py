import pygame
import sys
import random
import time
from pygame.locals import *

# Initialising
pygame.init()

# Setting up FPS
FPS = 30
FramePerSec = pygame.time.Clock()

# Creating Colours
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Creating the Backgrounds
title_bg = pygame.image.load(
    '/Users/willmurray/Google Drive/Coding/hangman/Resources/title_background.jpeg')
game_bg = pygame.image.load(
    '/Users/willmurray/Google Drive/Coding/hangman/Resources/HUD_view.jpg')
game_bg2 = pygame.image.load(
    '/Users/willmurray/Google Drive/Coding/hangman/Resources/bluesky.jpg')
# Other program variables
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Create a screen
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("RAF Hangman")


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    DISPLAYSURF.blit(title_bg, (0, 0))
    pygame.display.update()
    FramePerSec.tick(FPS)
