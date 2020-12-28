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
cpText = pygame.font.SysFont('comicsansms.ttf', 25)


# Sprites
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


# Sprite group
all_sprites = pygame.sprite.Group()

cloud1 = Cloud("cloud1.png")
all_sprites.add(cloud1)
cloud2 = Cloud("cloud2.png")
all_sprites.add(cloud2)
cloud3 = Cloud("cloud3.png")
all_sprites.add(cloud3)


def textObjects(text, font, colour):
    textSurface = font.render(text, True, colour)
    return textSurface, textSurface.get_rect()


def wordList(fp="rafterms.txt"):
    """
        Collects the terms and selects parses them
        into a dictionary format, answers{[word/phrase] : [meaning]}

        Pass in list of words to the func (e.g. rafterms.txt)
 """

    answers = {}
    with open(resource_folder + "/" + fp, "r") as f:
        for line in f.readlines():
            answer = line.split("-")[0].strip()
            meaning = line.split("-")[1].strip()
            answers[answer] = meaning
    return answers


def cockpit():
    cpSurf = pygame.Surface((WIDTH, HEIGHT))
    cpSurf.set_colorkey(BLACK)
    hudLeft = pygame.draw.polygon(
        cpSurf, GUNMETAL, [(200, 200), (150, 450), (230, 450), (230, 200)], 0)
    hudRight = pygame.draw.polygon(cpSurf, GUNMETAL, [
        (600, 200), (650, 450), (570, 450), (570, 200)], 0)
    hudSurf = pygame.Surface((WIDTH, HEIGHT))
    hudSurf.set_colorkey(BLACK)
    hudSurf.set_alpha(100)
    hudGlass = pygame.draw.polygon(
        screen, WHITE, [(230, 200), (260, 170), (540, 170), (570, 200), (570, 450), (540, 480), (260, 480), (230, 450)], 0)
    cpSurf.blit(hudSurf, (0, 0))

    return cpSurf


def chooseAns():
    answers = wordList()
    answer, description = random.choice(list(answers.items()))
    return answer, description


def moveClouds():
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


def game():
    answer, description = chooseAns()
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
        moveClouds()

        ## DRAW / RENDER ##
        screen.fill(SKYBLUE)
        all_sprites.draw(screen)
        cPit = cockpit()
        screen.blit(cPit, (0, 0))

        # *After drawing everything*, flip the drawing to the display.
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    game()
