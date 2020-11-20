"""This is a game of hangman, created for the JHub coding scheme."""

import sys
import pygame
import time

pygame.init()
clock = pygame.time.Clock()

project_path = "/Users/willmurray/Google Drive/Coding/hangman/"
word_list = project_path + "rafterms.txt"

black = (0, 0, 0)
white = (255, 255, 255)
red = (200, 0, 0)
bright_red = (255, 0, 0)
green = (0, 200, 0)
bright_green = (0, 255, 0)

font = pygame.font.SysFont('comicsansms.ttf', 20)
large = pygame.font.SysFont('comicsansms.ttf', 100)
small = pygame.font.SysFont('comicsansms.ttf', 50)


def word_list(fp=word_list):
    """Collects the terms and selects parses them
        into a dictionary format, answers{[word/phrase] : [meaning]}"""
    answers = {}
    with open(fp, "r") as f:
        for line in f.readlines():
            answer = line.split("-")[0].strip()
            meaning = line.split("-")[1].strip()
            answers[answer] = meaning
    return answers


display_width = 800
display_height = 600

# time.sleep is a placeholder until buttons to start / quit the game are put onto the title screen.
time.sleep(5)

#    Start and Exit Button

#    Background is a roundle / or Hangman is in a HUD as AC is flying through clouds.
#    Displays a box in which the hanging man will be drawn on left
#    Randmomly select from the list of words a random option from the word list
#    Displays placeholders for the answer

# Take input from player
#    Either as a full answer or as a single letter.

#    If single letter, check to see if the letter appears in the word.
#       If player has guessed a letter correctly:
#           Replace all placeholders with that letter

#           Check to see if the answer has been completed
#               If so, declare the player a winner.
#               Ask if they want to play again, or to quit.

#               If not, start the turn again.

#       If player guesses incorreclty:
#           Display the letter in a box for incorrect letters.
#           Draw a new section of the hanging man

#           Check to see if the hanging man has been completed.
#               If so, declare the player a loser.
#               Ask if they want to play again or to quit.

#               If not completed, start the turn again.

#   If word / phrase, check to see if it is the answer.
#       If answer is correct, declare the player a winner.
#       Ask if they want to play again or to quit

#       If answer is not correct:
#           Display the word in the incorrect guesses box.
#           Draw a new section of the hanging man.
#           Check to see if the hanging man has been completed.
#               If so, declare the player a loser.
#               Ask if they want to play again or quit.

#               If not completed, start the turn again.


class Button:
    """Creates a button, and blits it to screen"""

    def __init__(self, text, x=0, y=0, bg="black"):
        self.x = 0
        self.y = 0
        self.change_text()

    def button_click(self, text, active_colour, inactive_colour):
        pass

    def change_text(self, text, bg="black"):
        self.text = font.render(text, 1, pygame.Color("White"))
        self.size = self.text.get_size()
        self.surface = pygame.Surface(self.size)
        self.surface.fill(bg)
        self.surface.blit(self.text, (0, 0))
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])


def show_button(button_name):
    screen.blit(button_name.surface, (button_name.x, button_name.y))


def button_click(event, button_name):
    x, y = pygame.mouse.get_pos()
    if event.type == pygame.MOUSEBUTTONDOWN:
        if pygame.mouse.get_pressed()[0]:
            if button_name.rect.collidepoint(x, y):
                button_name(change_text("clicked"), bg=red)


def home_screen(h, w):
    """Creates a title screen, with start/quit buttons"""
    screen = pygame.display.set_mode((h, w))
    background = pygame.image.load(project_path + "title_typhoon.jpeg")

    screen.blit(background, (0, 0))
    pygame.display.update()
    time.sleep(1)
    # tS, tR = write_text("Hangman", large, black)
    # screen.blit(tS, tR)
    title_img = pygame.image.load(project_path + 'title_roundle.png')
    title = pygame.transform.scale(title_img, (400, 400))
    screen.blit(title, (75, 25))
    pygame.display.update()

    play_button = Button("Play", x=10, y=10, bg="navy")
    #quit_button = Button()


def start_game():
    pass


def leave_game():
    pass


def turn():
    pass


def write_text(msg, size, colour):
    """Func to write text throughout the game.
        text = Text to display, size = large or small """

    def text_objects(msg, font, colour):
        """Nested func which is used to define the msg"""
        textSurface = font.render(msg, True, colour)
        return textSurface, textSurface.get_rect()

    textSurf, textRect = text_objects(msg, size, black)
    textRect.center = ((display_width/2), (display_height/2))
    return textSurf, textRect


def main():
    """Main entry point for the script."""
    home_screen(display_width, display_height)


if __name__ == '__main__':
    answers = word_list()
    main()

    # sys.exit(main())
