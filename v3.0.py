import pygame
import random
import os
import re
import sys
import time

WIDTH = 800
HEIGHT = 600
FPS = 30

# initialise window, screen and music
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman")
clock = pygame.time.Clock()
pause = False

# Colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
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


# Sprite management
clouds = pygame.sprite.Group()

cloud1 = Cloud("cloud1.png")
cloud2 = Cloud("cloud2.png")
cloud3 = Cloud("cloud3.png")

clouds.add(cloud1, cloud2, cloud3)


def textObjects(text, font, colour):
    textSurface = font.render(text, True, colour)
    return textSurface, textSurface.get_rect()


def textDisplay(texttodisplay, x, y, colour):
    text = pygame.font.SysFont('comicsansms.ttf', 25)
    textSurf, textRect = textObjects(texttodisplay, text, colour)
    textRect.topleft = ((x, y))
    return textSurf, textRect


def wordList(fp="rafterms.txt"):
    """
        Collects the terms and selects parses them
        into a dictionary format, answers{[word/phrase] : [meaning]}

        Pass in list of words to the func (e.g. rafterms.txt)
 """

    answers = {}
    with open(resource_folder + "/" + fp, "r") as f:
        for line in f.readlines():
            answer = line.split("-")[0].strip().upper()
            meaning = line.split("-")[1].strip().upper()
            answers[answer] = meaning
    return answers


def chooseAns():
    answers = wordList()
    answer, description = random.choice(list(answers.items()))
    return answer, description


def hud(opaqueSurf, transparentSurf):
    # HUD graphics
    hudLeft = pygame.draw.polygon(opaqueSurf, GUNMETAL, [(
        200, 200), (150, 450), (230, 450), (230, 200)], 0)
    hudRight = pygame.draw.polygon(opaqueSurf, GUNMETAL, [(
        600, 200), (650, 450), (570, 450), (570, 200)], 0)
    hudGlass = pygame.draw.polygon(transparentSurf, WHITE, [(230, 200), (260, 170), (
        540, 170), (570, 200), (570, 450), (540, 480), (260, 480), (230, 450)], 0)

    # Aircraft graphics
    glareshield = pygame.draw.polygon(
        opaqueSurf, GUNMETAL, [(100, 450), (50, 600), (750, 600), (700, 450)], 0)
    cockpitScreen = pygame.draw.rect(
        opaqueSurf, BLACK, (150, 500, 500, 150), 0)


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

    if cloud2.rect.top > HEIGHT / 3:
        cloud3.update()
    elif cloud2.rect.top <= HEIGHT / 3 and cloud3.rect.top > 0:
        cloud3.update()


def mask(answer, maskList):
    for i in range(len(answer)):
        if answer[i].isalpha():
            maskList.append('_')
        elif answer[i] == " ":
            maskList.append(answer[i])
    return maskList


def msg(status, guess, answer, description):
    # Msg status = 1:Correct, 2: Incorrect, 3: previously guessed,  4:winner, 5:dead
    if status == 1:
        msg = f"Congrats! {guess} is in the answer!"
        colour = GREEN
    elif status == 2:
        msg = f"Unlucky, {guess} is incorrect! Try again!"
        colour = RED
    elif status == 3:
        msg = f"You've already guessed {guess}, try again."
        colour = YELLOW
    elif status == 4:
        msg = f"{answer}."
        colour = GREEN
    elif status == 5:
        msg = f"{answer}"
        colour = RED
    return msg, colour


def reveal(event, active, tries, ansMask, answer, maskList, running, incGuesses):
    msg = ""
    guess = ""
    if ansMask != answer:
        if event.type == pygame.KEYDOWN and active:
            try:
                guess = event.unicode
                if guess in answer:
                    if guess not in maskList:
                        for i in range(len(answer)):
                            if answer[i] == guess:
                                maskList[i] = guess
                        msg = f"Correct! {guess} in answer."
                    else:
                        msg = f"You already guessed {guess}, try again!"
                elif guess not in incGuesses:
                    incGuesses.append(guess)
                    tries += 1
                    msg = f"Incorrect! {guess} is not in the the answer"
                else:
                    msg = f"You already guessed {guess}, try again!"
            except IndexError:
                msg = "Enter a guess!"

    else:
        msg = f"Congratuluations, you completed it! The answer was {answer}!"

        running = False

    return guess, maskList, msg, tries, running


def getInput(x, y, w, h, icol, acol):
    """
    icol = colour_inactive
    acol = colour_active
    """

    input_box = pygame.Rect(x, y, w, h)
    colour_inactive = icol
    colour_active = acol

    return input_box, colour_inactive, colour_active


def unpause():
    global pause
    pygame.mixer.music.unpause()
    pause = False


def paused():
    global pause
    pygame.mixer.music.pause()

    rx, ry, rw, rh = 300, 300, 80, 50
    resumeBox, rcolour_inactive, rcolour_active = getInput(
        rx, ry, rw, rh, WHITE, GREEN)
    rCol = rcolour_inactive

    pqx, pqy, pqw, pqh = 450, 300, 50, 50
    pQBox, pQcolour_inactive, pQcolour_active = getInput(
        pqx, pqy, pqw, pqh, WHITE, RED)
    pQCol = pQcolour_inactive

    while pause:
        for event in pygame.event.get():
            # Check for closing the window
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            # Check for clicking play / quit buttons.
            if resumeBox.collidepoint((pygame.mouse.get_pos())):
                rCol = rcolour_active
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print("RESUME")
                    unpause()
            else:
                rCol = rcolour_inactive

            if pQBox.collidepoint((pygame.mouse.get_pos())):
                pQCol = pQcolour_active
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.quit()
                    sys.exit()
            else:
                pQCol = pQcolour_inactive

        # Create the pause box
        pauseScreen = pygame.Surface((WIDTH * 0.5, HEIGHT * 0.5))
        pauseScreen.set_alpha(50)
        pauseScreen.fill(BLACK)

        pauseSurf, pauseRect = textDisplay("PAUSED", 350, 200, SKYBLUE)
        pauseRect.center = ((400, 200))

        # Create the quit text and surface
        pqSurf, pqRect = textDisplay("QUIT", pqx, pqy, pQCol)
        pqRect.center = ((pqx + pqw / 2, pqy + pqh / 2))
        # Create the resume text and surface
        rSurf, rRect = textDisplay("RESUME", rx, ry, rCol)
        rRect.center = ((rx + rw / 2, ry + rh / 2))

        # Blits
        pygame.draw.rect(pauseScreen, rCol, resumeBox, 0)
        pygame.draw.rect(pauseScreen, pQCol, pQBox, 0)

        screen.blit(pauseScreen, (WIDTH * 0.25, HEIGHT * 0.25))
        screen.blit(pauseSurf, pauseRect)
        screen.blit(pqSurf, pqRect)
        screen.blit(rSurf, rRect)

        pygame.display.update()
        clock.tick(30)


# def msgDelay(obj_surf, obj_rect, duration, msgEnd, surf=screen):
#     """
#     Pauses the prescribed msg for the duration provided.
#     msgEnd = pygame.time.get_ticks() on the message to be displayed
#     surf is surface to be blitted to - default screen
#     """
#     currentTime = pygame.time.get_ticks() + 3000
#     if currentTime < msgEnd:
#         surf.blit(obj_surf, obj_rect)


def game():
    # Game variables
    global pause
    answer, description = chooseAns()
    maskList = []
    ansMask = "".join(mask(answer, maskList))
    incGuesses = []
    active = False
    ib_x, ib_y, ib_w, ib_h = 500, 500, 150, 40
    input_box, colour_inactive, colour_active = getInput(
        ib_x, ib_y+1, ib_w, ib_h, WHITE, GREEN)
    colour = colour_inactive
    tries = 0
    caption = ""
    statusColour = "GREEN"
    guess = "_"
    over = False
    #### GAME LOOP ####
    running = True
    win_status = ""
    message_end_time = 0

    while running:
        # TIME ## - Keep it running at the right speed.
        current_time = pygame.time.get_ticks()
        clock.tick(FPS)

        ## PROCESS INPUT ##
        for event in pygame.event.get():
            # Check for closing the window
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                # If user click on input box:
                if input_box.collidepoint(event.pos):
                    # Toggle the active variable
                    active = not active
                else:
                    active = False
                # change colour of input box
                colour = colour_active if active else colour_inactive

            if active:
                if tries < 11:
                    if ansMask != answer:
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE:
                                pause = True
                                paused()
                            guess = str(event.unicode).upper()
                            if guess.isalpha():
                                if guess in answer:
                                    if guess not in maskList:
                                        for i in range(len(answer)):
                                            if answer[i] == guess:
                                                maskList[i] = guess
                                                caption, statusColour = msg(
                                                    1, guess, answer, description)
                                                message_end_time = pygame.time.get_ticks() + 3000
                                    else:
                                        caption, statusColour = msg(
                                            3, guess, answer, description)
                                        message_end_time = pygame.time.get_ticks() + 3000
                                elif guess not in incGuesses:
                                    incGuesses.append(guess)
                                    caption, statusColour = msg(
                                        2, guess, answer, description)
                                    message_end_time = pygame.time.get_ticks() + 3000
                                    tries += 1
                                else:
                                    caption, statusColour = msg(
                                        3, guess, answer, description)
                                    message_end_time = pygame.time.get_ticks() + 3000
                    else:
                        caption, statusColour = msg(
                            4, guess, answer, description)
                        message_end_time = pygame.time.get_ticks() + 3000
                        # time.sleep(1)
                        win_status = True
                        # gameOver(win_status, answer, description)
                else:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_p or event.key == pygame.K_SPACE:
                            pause = True
                            paused()
                    caption, statusColour = msg(5, guess, answer, description)
                    message_end_time = pygame.time.get_ticks() + 3000
                    # time.sleep(1)
                    win_status = False
                    # gameOver(win_status, answer, description)

        ## UPDATE GAME ##
        moveClouds()
        ansMask = "".join(maskList)

        # Test block
        print('\n----------\n')
        print(f"You guessed {guess}")
        print(f"Message = {caption}")
        print(f"Mask List = {maskList}")
        print(f"Incorrect guesses = {incGuesses}")
        print('\n----------\n')
        if not running:
            print(answer)
            print(description)

        # Display answer text for testing.
        text = pygame.font.SysFont('comicsansms.ttf', 25)
        testTextSurf, testTextRect = textObjects(answer, text, RED)
        testTextRect.topleft = ((0, 0))

        # Create the mask text and surface
        maskSurf, maskRect = textDisplay(ansMask, 160, 550, GREEN)
        # Create the guess text and surface
        guessSurf, guessRect = textDisplay(
            f"Guess a letter: {guess}", ib_x, ib_y, GREEN)
        guessRect.center = ((ib_x + ib_w / 2, ib_y + ib_h / 2))
        # Create the message text and surface
        msgSurf, msgRect = textDisplay(caption, 260, 180, statusColour)
        msgRect.center = (WIDTH / 2, 180)

        """
        Split the text across 2 lines if the textrect is < x = 230

        if msgRect.x < 230:
            print("WIDE")
        else:
            print("Fine")
        """

        ## DRAW/RENDER ##
        screen.fill(SKYBLUE)
        clouds.draw(screen)

        # Draw the hud - making the screen a surface allows the glass to be opaque.
        hudScreen = pygame.Surface((WIDTH, HEIGHT))
        hudScreen.set_colorkey(BLACK)
        hudScreen.set_alpha(75)
        # HUD graphics
        hud(screen, hudScreen)

        # Blits.
        screen.blit(hudScreen, (0, 0))
        # Test text below
        screen.blit(testTextSurf, testTextRect)
        screen.blit(maskSurf, maskRect)
        screen.blit(guessSurf, guessRect)
        if current_time < message_end_time:
            screen.blit(msgSurf, msgRect)

        # Draw the hangman based on number of tries.
        if tries == 1:
            base = pygame.draw.line(screen, GREEN, (300, 430), (500, 430), 10)

        elif tries == 2:
            base = pygame.draw.line(screen, GREEN, (300, 430), (500, 430), 10)
            upright = pygame.draw.line(
                screen, GREEN, (304, 425), (304, 230), 10)

        elif tries == 3:
            base = pygame.draw.line(screen, GREEN, (300, 430), (500, 430), 10)
            upright = pygame.draw.line(
                screen, GREEN, (304, 425), (304, 230), 10)
            diagonalLower = pygame.draw.line(
                screen, GREEN, (308, 380), (360, 430), 5)

        elif tries == 4:
            base = pygame.draw.line(screen, GREEN, (300, 430), (500, 430), 10)
            upright = pygame.draw.line(
                screen, GREEN, (304, 425), (304, 230), 10)
            diagonalLower = pygame.draw.line(
                screen, GREEN, (308, 380), (360, 430), 5)
            diagonalUpper = pygame.draw.line(
                screen, GREEN, (308, 270), (340, 230), 5)

        elif tries == 5:
            base = pygame.draw.line(screen, GREEN, (300, 430), (500, 430), 10)
            upright = pygame.draw.line(
                screen, GREEN, (304, 425), (304, 230), 10)
            diagonalLower = pygame.draw.line(
                screen, GREEN, (308, 380), (360, 430), 5)
            diagonalUpper = pygame.draw.line(
                screen, GREEN, (308, 270), (340, 230), 5)
            topBar = pygame.draw.line(
                screen, GREEN, (300, 230), (450, 230), 10)

        elif tries == 6:
            base = pygame.draw.line(screen, GREEN, (300, 430), (500, 430), 10)
            upright = pygame.draw.line(
                screen, GREEN, (304, 425), (304, 230), 10)
            diagonalLower = pygame.draw.line(
                screen, GREEN, (308, 380), (360, 430), 5)
            diagonalUpper = pygame.draw.line(
                screen, GREEN, (308, 270), (340, 230), 5)
            topBar = pygame.draw.line(
                screen, GREEN, (300, 230), (450, 230), 10)
            rope = pygame.draw.line(screen, GREEN, (448, 230), (448, 280), 5)

        elif tries == 7:
            base = pygame.draw.line(screen, GREEN, (300, 430), (500, 430), 10)
            upright = pygame.draw.line(
                screen, GREEN, (304, 425), (304, 230), 10)
            diagonalLower = pygame.draw.line(
                screen, GREEN, (308, 380), (360, 430), 5)
            diagonalUpper = pygame.draw.line(
                screen, GREEN, (308, 270), (340, 230), 5)
            topBar = pygame.draw.line(
                screen, GREEN, (300, 230), (450, 230), 10)
            rope = pygame.draw.line(screen, GREEN, (448, 230), (448, 280), 5)
            head = pygame.draw.circle(screen, GREEN, (448, 295), 15, 3)

        elif tries == 8:
            base = pygame.draw.line(screen, YELLOW, (300, 430), (500, 430), 10)
            upright = pygame.draw.line(
                screen, YELLOW, (304, 425), (304, 230), 10)
            diagonalLower = pygame.draw.line(
                screen, YELLOW, (308, 380), (360, 430), 5)
            diagonalUpper = pygame.draw.line(
                screen, YELLOW, (308, 270), (340, 230), 5)
            topBar = pygame.draw.line(
                screen, YELLOW, (300, 230), (450, 230), 10)
            rope = pygame.draw.line(screen, YELLOW, (448, 230), (448, 280), 5)
            head = pygame.draw.circle(screen, YELLOW, (448, 295), 15, 3)
            body = pygame.draw.line(screen, YELLOW, (448, 310), (448, 360), 3)

        elif tries == 9:
            base = pygame.draw.line(screen, YELLOW, (300, 430), (500, 430), 10)
            upright = pygame.draw.line(
                screen, YELLOW, (304, 425), (304, 230), 10)
            diagonalLower = pygame.draw.line(
                screen, YELLOW, (308, 380), (360, 430), 5)
            diagonalUpper = pygame.draw.line(
                screen, YELLOW, (308, 270), (340, 230), 5)
            topBar = pygame.draw.line(
                screen, YELLOW, (300, 230), (450, 230), 10)
            rope = pygame.draw.line(screen, YELLOW, (448, 230), (448, 280), 5)
            head = pygame.draw.circle(screen, YELLOW, (448, 295), 15, 3)
            body = pygame.draw.line(screen, YELLOW, (448, 310), (448, 360), 3)
            arms = pygame.draw.line(screen, YELLOW, (433, 330), (462, 330), 3)

        elif tries == 10:
            base = pygame.draw.line(screen, YELLOW, (300, 430), (500, 430), 10)
            upright = pygame.draw.line(
                screen, YELLOW, (304, 425), (304, 230), 10)
            diagonalLower = pygame.draw.line(
                screen, YELLOW, (308, 380), (360, 430), 5)
            diagonalUpper = pygame.draw.line(
                screen, YELLOW, (308, 270), (340, 230), 5)
            topBar = pygame.draw.line(
                screen, YELLOW, (300, 230), (450, 230), 10)
            rope = pygame.draw.line(screen, YELLOW, (448, 230), (448, 280), 5)
            head = pygame.draw.circle(screen, YELLOW, (448, 295), 15, 3)
            body = pygame.draw.line(screen, YELLOW, (448, 310), (448, 360), 3)
            arms = pygame.draw.line(screen, YELLOW, (433, 330), (462, 330), 3)
            leftLeg = pygame.draw.line(
                screen, YELLOW, (448, 360), (438, 410), 3)

        elif tries == 11:
            base = pygame.draw.line(screen, RED, (300, 430), (500, 430), 10)
            upright = pygame.draw.line(
                screen, RED, (304, 425), (304, 230), 10)
            diagonalLower = pygame.draw.line(
                screen, RED, (308, 380), (360, 430), 5)
            diagonalUpper = pygame.draw.line(
                screen, RED, (308, 270), (340, 230), 5)
            topBar = pygame.draw.line(
                screen, RED, (300, 230), (450, 230), 10)
            rope = pygame.draw.line(screen, RED, (448, 230), (448, 280), 5)
            head = pygame.draw.circle(screen, RED, (448, 295), 15, 3)
            body = pygame.draw.line(screen, RED, (448, 310), (448, 360), 3)
            arms = pygame.draw.line(screen, RED, (433, 330), (462, 330), 3)
            leftLeg = pygame.draw.line(
                screen, RED, (448, 360), (438, 410), 3)
            rightLeg = pygame.draw.line(
                screen, RED, (448, 360), (457, 410), 3)

        pygame.draw.rect(screen, colour, input_box, 2)

        # *After drawing everything*, flip the drawing to the display.
        pygame.display.flip()

        if win_status != "":
            gameOver(win_status, answer, description)
    pygame.quit()
    sys.exit()


def titleScreen():
    """
    Opening screen to start / quit the game from. This will load the a new game if the player clicks the button new game
    """
    # Define the playBox
    px, py, pw, ph = 500, 100, 100, 50
    playBox, play_colour_inactive, play_colour_active = getInput(
        px, py, pw, ph, WHITE, GREEN)
    playCol = play_colour_inactive

    # Define the quitBox
    qx, qy, qw, qh = 500, 200, 100, 50
    quitBox, quit_colour_inactive, quit_colour_active = getInput(
        500, 200, 100, 50, WHITE, RED)
    quitCol = quit_colour_inactive

    open = True
    while open:
        # TIME ## - Keep it running at the right speed.
        clock.tick(FPS)

        ## PROCESS INPUT ##
        for event in pygame.event.get():
            # Check for closing the window
            if event.type == pygame.QUIT:
                open = False
            # Check for clicking play / quit buttons.
            if playBox.collidepoint((pygame.mouse.get_pos())):
                playCol = play_colour_active
                if event.type == pygame.MOUSEBUTTONDOWN:
                    game()
            else:
                playCol = play_colour_inactive

            if quitBox.collidepoint((pygame.mouse.get_pos())):
                quitCol = quit_colour_active
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.quit()
                    sys.exit()
            else:
                quitCol = quit_colour_inactive

        ## DRAW / RENDER ##

        # Load the background image
        title_bg = pygame.image.load(
            resource_folder + "/title_background.jpeg")

        # Create the quit text and surface
        quitSurf, quitRect = textDisplay("QUIT", qx, qy, quitCol)
        quitRect.center = ((qx + qw / 2, qy + qh / 2))
        # Create the play text and surface
        playSurf, playRect = textDisplay("PLAY", px, py, playCol)
        playRect.center = ((px + pw / 2, py + ph / 2))

        # Blits
        screen.blit(title_bg, (0, 0))
        screen.blit(playSurf, playRect)
        screen.blit(quitSurf, quitRect)
        pygame.draw.rect(screen, playCol, playBox, 2)
        pygame.draw.rect(screen, quitCol, quitBox, 2)

        ## UPDATE ##
        pygame.display.flip()

    pygame.quit()
    sys.exit()


def gameOver(win_status, answer, description):
    """
    Game over screen to restart / quit the game from.
    """

    if win_status:
        msg = "CONGRATULATIONS!"
    else:
        msg = "UNLUCKY!"

    # Define the playBox
    px, py, pw, ph = 650, 100, 100, 50
    playBox, play_colour_inactive, play_colour_active = getInput(
        px, py, pw, ph, WHITE, GREEN)
    playCol = play_colour_inactive

    # Define the quitBox
    qx, qy, qw, qh = 650, 200, 100, 50
    quitBox, quit_colour_inactive, quit_colour_active = getInput(
        qx, qy, qw, qh, WHITE, RED)
    quitCol = quit_colour_inactive

    open = True
    while open:
        # TIME ## - Keep it running at the right speed.
        clock.tick(FPS)

        ## PROCESS INPUT ##
        for event in pygame.event.get():
            # Check for closing the window
            if event.type == pygame.QUIT:
                open = False
            # Check for clicking play / quit buttons.
            if playBox.collidepoint((pygame.mouse.get_pos())):
                playCol = play_colour_active
                if event.type == pygame.MOUSEBUTTONDOWN:
                    game()
            else:
                playCol = play_colour_inactive

            if quitBox.collidepoint((pygame.mouse.get_pos())):
                quitCol = quit_colour_active
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.quit()
                    sys.exit()
            else:
                quitCol = quit_colour_inactive

        ## DRAW / RENDER ##

        # Load the background image
        title_bg = pygame.image.load(
            resource_folder + "/GO_background.jpg")

        # Create the quit text and surface
        quitSurf, quitRect = textDisplay("QUIT", qx, qy, quitCol)
        quitRect.center = ((qx + qw / 2, qy + qh / 2))
        # Create the play text and surface
        playSurf, playRect = textDisplay("REPLAY", px, py, playCol)
        playRect.center = ((px + pw / 2, py + ph / 2))
        # Game Over
        goSurf, goRect = textDisplay("GAME OVER", 400, 100, BLACK)
        goRect.center = ((WIDTH/2, HEIGHT/2-150))
        # WIN / LOSE text & surface
        ansSurf, ansRect = textDisplay(msg, 400, 100, BLACK)
        ansRect.center = ((WIDTH / 2, HEIGHT / 2 - 100))
        # answer text & surface
        aSurf, aRect = textDisplay(f"Answer: {answer}", 400, 100, BLACK)
        aRect.center = ((WIDTH / 2, HEIGHT / 2 - 50))
        # Decription text & surface
        desSurf, desRect = textDisplay(
            f"Meaning: {description}", 400, 200, BLACK)
        desRect.center = ((WIDTH / 2, HEIGHT / 2))

        # Blits

        screen.blit(title_bg, (0, 0))
        screen.blit(playSurf, playRect)
        screen.blit(quitSurf, quitRect)
        screen.blit(goSurf, goRect)
        screen.blit(ansSurf, ansRect)
        screen.blit(aSurf, aRect)
        screen.blit(desSurf, desRect)

        pygame.draw.rect(screen, playCol, playBox, 2)
        pygame.draw.rect(screen, quitCol, quitBox, 2)

        ## UPDATE ##
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    titleScreen()
