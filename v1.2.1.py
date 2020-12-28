import pygame
import random
import os

WIDTH = 800
HEIGHT = 600

FPS = 30


# initialise window, screen and music
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman")
clock = pygame.time.Clock()

# Colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
SKYBLUE = (135, 206, 235)
GUNMETAL = (83, 86, 90)
GREY = (128, 128, 128)

# Assets
game_folder = os.path.dirname(__file__)
resource_folder = os.path.join(game_folder, "Resources")

# Sprites:


class Cloud(pygame.sprite.Sprite):
    def __init__(self, imgName):
        super().__init__()
        self.image = pygame.image.load(
            os.path.join(resource_folder, imgName)).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(50, 750), -50)

    def move(self):

        self.rect.x = random.randint(50, 750)

    def update(self):
        self.rect.y += 5
        if self.rect.top > HEIGHT:
            self.rect.top = 0
            self.move()


def hud(opaqueSurf, transparentSurf):
    # HUD graphics
    hudLeft = pygame.draw.polygon(
        opaqueSurf, GUNMETAL, [(200, 200), (150, 450), (230, 450), (230, 200)], 0)
    hudRight = pygame.draw.polygon(opaqueSurf, GUNMETAL, [
        (600, 200), (650, 450), (570, 450), (570, 200)], 0)
    hudGlass = pygame.draw.polygon(
        transparentSurf, WHITE, [(230, 200), (260, 170), (540, 170), (570, 200), (570, 450), (540, 480), (260, 480), (230, 450)], 0)

    # Aircraft graphics
    glareshield = pygame.draw.polygon(
        opaqueSurf, GUNMETAL, [(100, 450), (50, 600), (750, 600), (700, 450)], 0)
    # cockpitBorder = pygame.draw.lines(opaqueSurf, GREY, False, [(150, 600), (150, 500), (650, 500), (650, 600)], 10)

    cockpitScreen = pygame.draw.rect(
        opaqueSurf, BLACK, (150, 500, 500, 150), 0)


def hangingMan(surf):
    # Stocks
    base = pygame.draw.line(surf, GREEN, (300, 430), (500, 430), 10)
    upright = pygame.draw.line(surf, GREEN, (304, 425), (304, 230), 10)
    diagonalLower = pygame.draw.line(surf, GREEN, (308, 380), (360, 430), 5)
    diagonalUpper = pygame.draw.line(surf, GREEN, (308, 270), (340, 230), 5)
    topBar = pygame.draw.line(surf, GREEN, (300, 230), (450, 230), 10)
    rope = pygame.draw.line(surf, GREEN, (448, 230), (448, 280), 5)

    # Body
    head = pygame.draw.circle(surf, GREEN, (448, 295), 15, 3)
    body = pygame.draw.line(surf, GREEN, (448, 310), (448, 360), 3)
    arms = pygame.draw.line(surf, GREEN, (433, 330), (462, 330), 3)
    leftLeg = pygame.draw.line(surf, GREEN, (448, 360), (438, 410), 3)
    rightLeg = pygame.draw.line(surf, GREEN, (448, 360), (457, 410), 3)


# Sprite group
all_sprites = pygame.sprite.Group()

cloud1 = Cloud("cloud1.png")
all_sprites.add(cloud1)
cloud2 = Cloud("cloud2.png")
all_sprites.add(cloud2)
cloud3 = Cloud("cloud3.png")
all_sprites.add(cloud3)


#### GAME LOOP ####
running = True

while running:

    # TIME ## - Keep it running at the right speed.
    clock.tick(FPS)

    ## PROCESS INPUT ##
    for event in pygame.event.get():
        # Check for closing the window
        if event.type == pygame.QUIT:
            running = False

    ## UPDATE GAME ##

    # This allows the clouds to fall sequentially, but they get stuck.
    if cloud3.rect.top > HEIGHT / 3:
        cloud1.update()
    elif cloud3.rect.top < 0:
        cloud1.update()
    elif cloud1.rect.top > 1:
        cloud1.update()

    if cloud1.rect.top > HEIGHT / 3:
        cloud2.update()
    elif cloud1.rect.top < HEIGHT / 3 and cloud2.rect.top > 0:
        cloud2.update()

    if cloud2.rect.top > HEIGHT / 3:
        cloud3.update()
    elif cloud2.rect.top <= HEIGHT / 3 and cloud3.rect.top > 0:
        cloud3.update()

    ## DRAW/RENDER ##
    screen.fill(SKYBLUE)
    all_sprites.draw(screen)

    # Draw the hud - making the screen a surface allows the glass to be opaque.
    hudScreen = pygame.Surface((WIDTH, HEIGHT))
    hudScreen.set_colorkey(BLACK)
    hud(screen, hudScreen)
    hudScreen.set_alpha(75)
    hangingMan(screen)
    screen.blit(hudScreen, (0, 0))

    # *After drawing everything*, flip the drawing to the display.
    pygame.display.flip()


pygame.quit()
