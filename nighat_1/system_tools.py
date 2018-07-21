from nltk.corpus import wordnet, gutenberg, brown, conll2000
import re
import time
import pickle
from classes import composition_builder
from classes import node
import nltk
from nltk import stem
from nltk.stem.lancaster import LancasterStemmer
from nltk.corpus import wordnet as wn
from classes import Gender
from ngram import n_gram
import logging

logging.basicConfig(filename='logs/log1.txt', filemode='w', level=logging.DEBUG)


#TODO ========= optimize code
#TODO ========= re organize code
#TODO ========= tokenize triplets:
    # first get the most likely n-gram, then get  the next most likely n-gram,
    # rather than getting the most likely of all combinations



from nlglib.realisation.simplenlg.realisation import Realiser
from nlglib.microplanning import *

realise = Realiser(host='nlg.kutlak.info')

def get_symbols():
    return list(pickle.load(open('syms-2.p', 'rb')))

def get_symbol_dict():
    return dict(pickle.load(open('id_to_words.p', 'rb')))

def build_word_from_composition():
    syms = get_symbols()

    # create a new builder
    comp_builder = composition_builder()

    for i, sym in enumerate(syms):
        if len(sym.id_composition) > 1:
            comp_builder.insert(sym.id_composition, sym)

    return comp_builder


def id_to_word(ids, immediate_build):
    builder = build_word_from_composition()
    symbols = get_symbol_dict()
    highest_index = 0
    highest_index_altered = False

    composition = []
    gender = None
    i = 0
    while i < (len(ids)):
        temp_composition = []
        for j in range(i+1, len(ids) + 1):
            temp_id_list = ids[i:j]
            if len(temp_id_list) == 1:
                try:
                    temp_composition.append(str(symbols[temp_id_list[0]]).split(','))
                except KeyError:
                    pass
            else:
                temp_build = builder.get_symbol(temp_id_list)
                if temp_build is not None and temp_build.id is not None:
                    temp_composition = []
                    temp_composition.append(temp_build.words)
                    highest_index = j
                    highest_index_altered = True
                    if immediate_build:
                        ids[i] = temp_build.id
                        ids = ids[0:i + 1] + ids[j::]
                elif j == len(ids) and not immediate_build:
                    composition += id_to_word(ids, True)[0]
        for c in temp_composition:
            composition.append(c)
        if highest_index_altered:
            i = highest_index
            highest_index_altered = False
        else:
            i += 1



    # print("Composition words: ", composition)
    return composition, gender


def handle_time(word_list, time):
    return_list = []
    for list in word_list:
        for word in list:
            w = Clause()
            w.predicate = VP(word)
            if time == 'past':
                w['TENSE'] = 'PAST'
            else:
                w['TENSE'] = 'FUTURE'
            return_list.append(realise(w))

    return return_list

def handle_plural(word_list):
    return_list = []
    for list in word_list:
        for word in list:
            if word[-1] == 'y':
                return_list.append(word + 'ies')
            else:
                return_list.append(word + 's')
    return return_list

def build_word(ids):
    indicator = False
    word_list, gender = id_to_word(ids, False)
    for i,list in enumerate(word_list):
        for j, word in enumerate(list):
            if "indicator" in word:
                word_list = word_list[0:i] + word_list[i + 1::]
                i -= 1
                indicator = True
                if "indicator_(possessive" in word:
                    # print(handle_possessive(word_list, gender))
                    return handle_possessive(word_list, gender)
                if "past" in word:
                    return handle_time(word_list, 'past')
                if "future" in word:
                    return handle_time(word_list, 'future')
                if "plural" in word:
                    return handle_plural(word_list)
                if "action" in word:
                    if "live" in word_list[i - 1][0]:
                        return ['is']
                else:
                    list[j] = ' '

            else:
                #clean the word
                regex = re.compile(r"\(.*\)")
                temp = re.sub(regex, '', word)
                temp = temp.replace('_of', '')
                temp = temp.replace('_', '')
                temp = temp.replace('-', '')
                if temp != 'to':
                    temp = temp.replace('to', '')
                if temp != 'be':
                    temp = temp.replace('be', '')

                temp = temp.strip()
                list[j] = temp

    # no indicator found, return first word list
    return word_list[0]




def handle_possessive(word_list, gender):
    return_list = []
    for word in word_list:
        for w in word:
            if 'he' in w:
                if gender == Gender.feminine:
                    return ['hers', 'their']
                else:
                    return ['his', 'their', 'its']
            else:
                return_list.append(str(w + '\'s'))

    return return_list


def build_sentence(list_of_lists):
    words = []
    for list in list_of_lists:
        built_words = build_word(list)
        article_check = True
        if built_words is not None and len(built_words) >= 1:
            for i, word in enumerate(built_words):
                pos = nltk.pos_tag([word])[0]
                if article_check and 'NN' in pos[1] and wordnet.synsets(word):
                    words.append(['', 'a', 'the'])
                    article_check = False
            words.append(built_words)
    n_g = n_gram(3, .06)
    n_g.load_n_gram()
    print("WORDS::::: ", words)
    sentence = n_g.get_most_likely_sentence(words)
    print(sentence, '\n')


