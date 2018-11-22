import re
import automata
import bisect
import random



class Gender(object):
    masculine = "masculine"
    feminine = "feminine"


class symbol(object):
    words = []
    composition = []
    id_composition = []
    id = None
    is_word = None
    is_character = None
    is_indicator = None
    morphological_info = []
    extra_word_info  = []
    has_extra_info = False

    def __init__(self, words, composition, id, is_word):
        self.words = words
        self.composition = composition
        self.id = id
        self.is_word = is_word
        self.is_character = not is_word



        # get morph info
        regex = re.compile(r"\(.*\)")
        morph = re.findall(regex, words)
        temp_words = []
        for m in morph:
            temp_words.append(m.replace("(", "").replace(")", ""))

        self.morphological_info = temp_words

        # get extra word info
        self.extra_word_info = re.findall(regex, words)

        if len(self.extra_word_info) > 0:
            self.extra_word_info = self.extra_word_info[0]
            self.has_extra_info = True



        # get indicator info
        if "indicator_(" in words:
            self.is_indicator = True
            self.words = [words]
            # print("in here: ", words)
        else:
            # print("Not in here: ", words)
            self.is_indicator = False
            t = re.sub(regex, '', str(words))
            self.words = str(t).split(',')

        # add extra info word to words list
        if self.has_extra_info:
            # for every word, add the combination of the extra info
            # and the word to the list of words

            temp_word = str(self.extra_word_info).replace("(", '').replace(")", '')
            temp_list_of_words = []
            for word in self.words:
                initial_word = re.sub(regex, '', str(word))
                temp_list_of_words.append(str(temp_word) + " " + initial_word)

            for word in temp_list_of_words:
                self.words.append(word)
            # print(self.words)

    def is_extra_info(self):
        if len(self.extra_word_info) > 0:
            return True
        return False

    def add_composition(self, word, input_id):
        self.composition.append(word)
        self.id_composition.append(input_id)

    def replace_composition(self, word_list, input_id_list):
        self.composition = word_list
        self.id_composition = input_id_list

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


# https://dzone.com/articles/algorithm-week-damn-cool-1


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
        if distance <= k and self.term is not "" and self.object is not None:
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

class node():
    children = None
    symbol = None

    def __init__(self):
        self.children = {}

    def insert_children(self, child):
        try:
            return self.children[child]
        except KeyError:
            self.children[child] = node()
            return self.children[child]

    def insert_symbol(self, symbol):
        self.symbol = symbol

    def get_children(self, input_id):
        try:
            return self.children[input_id]
        except KeyError:
            return None

    def get_symbol(self):
        return self.symbol

class composition_builder():
    parent_node = None

    def __init__(self):
        self.parent_node = node()

    def insert(self, list_of_ids, symbol):
        current_node = self.parent_node

        for i in range(len(list_of_ids)):
            current_node = current_node.insert_children(list_of_ids[i])
        current_node.insert_symbol(symbol)



    def get_symbol(self, list_of_ids):
        current_node = self.parent_node
        for i in range(len(list_of_ids)):
            if current_node == None:
                return symbol("", [], None, False)
            current_node = current_node.get_children(list_of_ids[i])
        if current_node is not None:
            return current_node.get_symbol()
        else:
            return symbol("", [], None, False)
