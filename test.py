import os
import sys
import random
import re
import pygame


WIDTH = 800
HEIGHT = 600
FPS = 30

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Assets
game_folder = os.path.dirname(__file__)
resource_folder = os.path.join(game_folder, "Resources")

# Colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
SKYBLUE = (135, 206, 235)
GUNMETAL = (83, 86, 90)
GREY = (128, 128, 128)


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


def chooseAns():
    answers = wordList()
    answer, description = random.choice(list(answers.items()))
    return answer, description


def mask(answer):
    a = answer
    a = re.sub('\w', '_ ', answer)
    return a


def passer():
    x = 1
    y = 24
    z = 19
    return x, y, z


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

    return base, upright, diagonalLower, diagonalUpper, topBar, rope, head, body, arms, leftLeg, rightLeg


# answer, descpription = chooseAns()
# print(f"Answer={answer}, descpription={descpription}")
# ansMask = mask(answer)
# print(f"Mask = {ansMask}")
tries = 0
base, upright, diagonalLower, diagonalUpper, topBar, rope, head, body, arms, leftLeg, rightLeg = hangingMan(
    screen)
livesDict = {1: base, 2: upright, 3: diagonalLower, 4: diagonalUpper,
             5: topBar, 6: rope, 7: head, 8: body, 9: arms, 10: leftLeg, 11: rightLeg}

running = True

while running:

    for event in pygame.event.get():
        # Check for closing the window
        if event.type == pygame.QUIT:
            running = False
    # x, y, z = passer()
    # print(x, y, z)
    screen.fill(BLACK)

    screen.blit(base)

    pygame.display.flip()

    clock.tick(FPS)
pygame.quit()
