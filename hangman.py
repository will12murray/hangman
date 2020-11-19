"""This is a game of hangman, created for the JHub coding scheme."""

import sys

# Recover a word list for answers.

# Parse the words so that all items, single words and phrases are read as one answer

# Create title page from PyGame
#    Start and Exit Button
#    Roundle colours flashing hangman title?

# Create PyGame display
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

class hangingMan():
    """Creates the class of the hanging man to display in PyGame."""
    pass


class answer():
    """Pulls an answer from the word list"""
    pass


def turn():
    pass


def main():
    """Main entry point for the script."""
    pass


if __name__ == '__main__':
    sys.exit(main())
