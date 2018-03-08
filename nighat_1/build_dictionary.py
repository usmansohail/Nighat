import openpyxl
from openpyxl import load_workbook
from openpyxl import Workbook
import pickle
from classes import symbol, character, BKNode, levenshtein
from difflib import SequenceMatcher


# This file will implement methods for getting the symbols from either the ID, or
# the composition words


# import the characters and symbols
chars = pickle.load(open("chars_list.p", 'rb'))
syms = pickle.load(open("symbols_list.p", 'rb'))



# words = []
#
# for sym in syms:
#     words.append(sym.words[0])
#
# bk_dict = BKNode("")
#
# for word in words:
#     bk_dict.insert(word)
#
#
# results = []
# bk_dict.search("run", 1, results)
#
# print(results)

bk_id_dict = BKNode("", None)
def get_bk_dict():
    for sym in syms:
        for word in sym.words:
            bk_id_dict.insert(word, sym.id)

    #results = []

    #bk_id_dict.search("run", 1, results)

    #print(results)


wb = load_workbook('dictionary.xlsx')



def match_longest_string(string1, string2):
    match = SequenceMatcher(None, string1, string2).find_longest_match(0, len(string1), 0, len(string2))
    return match[2]


match_longest_string("run", "to run")
match_longest_string("running", "running to")
match_longest_string("run", "runger")
match_longest_string("run", "brung")


def get_most_likely_symbols(phrase):
    # first get results from BK tree
    results = []
    bk_id_dict.search(phrase, 3, results)

    # of these results, order them by longest common substring
    temp = [None]*len(results)

    for i in range(len(results)):
        # print('w1: ', phrase, ' w2: ', results[i][1])
        # compute score, longest_common_substring / distance
            # add one for the distance case of 0
        score = float(match_longest_string(phrase, results[i][1])) / float(results[i][0] + 1)
        temp[i] = (score, results[i])

    sorted_results = sorted(temp, key=lambda x: x[0], reverse=True)

    # print(phrase, ": \n")
    # for i in range(5):
    #     if i < len(sorted_results):
    #         print("Score: ", sorted_results[i][0], "word: ", sorted_results[i][1])
    # print('\n\n')

    return sorted_results

get_bk_dict()
# (get_most_likely_symbols('gun'))
# (get_most_likely_symbols('run'))
# (get_most_likely_symbols('to expect'))
# (get_most_likely_symbols('anticipate'))



def add_id():
    # display all composition
    for sym in syms[100:120]:
        # print(sym.words, ": ", sym.composition)
        likely_id = []
        if len(sym.composition) > 1:
            for word in sym.composition:
                if word is not '':
                    likely_id = get_most_likely_symbols(word)
                    if len(likely_id) > 1:
                        sym.id_composition.append(likely_id[0][1][2])
        print(sym.words)
        print(sym.composition)
        print(sym.id_composition, '\n')

add_id()