"""
Tests functionality of the reveal function to take user
input and display it within the mask. Use the .index()!
"""
import os
import random
import re

# Assets
game_folder = os.path.dirname(__file__)
resource_folder = os.path.join(game_folder, "Resources")


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


# def mask(answer):
#     a = answer
#     a = re.sub('\w', '_ ', answer)
#     return a

def mask(answer, maskList):
    for i in range(len(answer)):
        if answer[i].isalpha():
            maskList.append('_')
        elif answer[i] == " ":
            maskList.append(answer[i])
    return maskList


def reveal(ansMask, answer, maskList, running, incGuesses):
    if ansMask != answer:
        try:
            guess = input("\nGuess a letter: \n").upper()[0]
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
                msg = f"Incorrect! {guess} is not in the the answer"
            else:
                msg = f"You already guessed {guess}, try again!"
        except IndexError:
            msg = "Enter a guess!"

    else:
        msg = f"Congratuluations, you completed it! The answer was {answer}!"

        running = False

    return maskList, msg, running


answer, description = chooseAns()
maskList = []
ansMask = "".join(mask(answer, maskList))
incGuesses = []

print(answer)

running = True

while running:

    maskList, msg, running = reveal(
        ansMask, answer, maskList, running, incGuesses)

    print(f"ML = {maskList}")
    print(f"incGuesses = {incGuesses}")
    ansMask = "".join(maskList)
    print(f"Mask = {ansMask}")
    print(msg)
