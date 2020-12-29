import os
import sys
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


answer, descpription = chooseAns()
print(f"Answer={answer}, descpription={descpription}")
ansMask = mask(answer)
print(f"Mask = {ansMask}")

x, y, z = passer()
print(x, y, z)
