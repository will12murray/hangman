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
SKYBLUE = (135, 206, 235)

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


# Title screen - Needs buttons for PLAY / QUIT
def title_screen():
    DISPLAYSURF.blit(title_bg, (0, 0))


# Game Screen

class Cloud(pygame.sprite.Sprite):
    def __init__(self, imagePath):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    def move(self):
        self.rect.move_ip(0, 10)
        if self.rect.bottom > 600:
            self.rect.top = 0
            self.rect.center = (random.randint(0, 800), 0)

    def grow(self, x, y):
        self.rect.inflate_ip(x, y)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


def game_screen():
    """
        - Background to be blue sky with clouds spawning
            and scrolling past in the background.
        - Display hanging man
        - Display placeholders
        - Display wrong guesses
    """
    DISPLAYSURF.fill(SKYBLUE)

    # Draw clouds
    C1 = Cloud(
        "/Users/willmurray/Google Drive/Coding/hangman/Resources/cloud1.png")
    # C2 = Cloud("""imagePath2""")
    # C3 = Cloud("""imagePath3""")

    # C2.grow(2, 2)
    # C3.grow(-2, -2)

    C1.move()
    # C2.move()
    # C3.move()

    C1.draw(DISPLAYSURF)
    # C2.draw(DISPLAYSURF)
    # C3.draw(DISPLAYSURF)


## GAME LOOP ##


if __name__ == "__main__":
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # title_screen()
        game_screen()

        pygame.display.update()
        FramePerSec.tick(FPS)
