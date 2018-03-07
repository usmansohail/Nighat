import re
import automata
import bisect
import random


class symbol:
    words = []
    composition = []
    id = None
    is_word = None
    is_character = None
    is_indicator = None
    morphological_info = []

    def __init__(self, words, composition, id, is_word):
        self.words = words
        self.composition = composition
        self.id = id
        self.is_word = is_word
        self.is_character = not is_word



        # fet morph info
        regex = re.compile(r"\(.*\)")
        morph = re.findall(regex, words)
        temp_words = []
        for m in morph:
            temp_words.append(m.replace("(", "").replace(")", ""))

        self.morphological_info = temp_words

        # get indicator info
        if "indicator_(" in words:
            self.is_indicator = True
            self.words = [words]
            print("in here: ", words)
        else:
            print("Not in here: ", words)
            self.is_indicator = False
            t = re.sub(regex, '', str(words))
            self.words = str(t).split(',')


    def display_info(self):

        if self.is_word:
            print("########## WORD  ###############")
        else:
            print("########## CHAR  ###############")


        print("words: ",  self.words, '\n',
              "Composition: ", self.composition, '\n',
              "ID: ", self.id, '\n',
              "Morph info: ", self.morphological_info, '\n',
              " #########################\n")

    def ind(self):
        if self.is_indicator:
            return True
        else:
            return False

# character object:
# * inherits from symbol
# - enum: place (pre, post, root)
# - string or enum: morphological relationship

class character(symbol):
    morph_relationships = None

    def __init__(self, words, composition, id, is_word, morph_relationships):
        symbol.__init__(words, composition, id, is_word)
        self.morph_relationships = morph_relationships




class BKNode(object):
    def __init__(self, term, object):
        self.term = term
        self.object = object
        self.children = {}

    def insert(self, other, object):
        distance = levenshtein(self.term, other)
        if distance in self.children:
            self.children[distance].insert(other, object)
        else:
            self.children[distance] = BKNode(other, object)

    def search(self, term, k, results=None):
        if results is None:
            results = []
        distance = levenshtein(self.term, term)
        counter = 1
        if distance <= k:
            results.append((distance, self.term, self.object))
        for i in range(max(0, distance - k), distance + k + 1):
            child = self.children.get(i)
            if child:
                counter += child.search(term, k, results)
        return counter


def levenshtein(s1, s2):
    if len(s1) < len(s2):
        return levenshtein(s2, s1)
    if not s1:
        return len(s2)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[
                             j + 1] + 1  # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1  # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]

