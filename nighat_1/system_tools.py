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

class SystemTools:

    def __init__(self):
        self.realise = Realiser(host='nlg.kutlak.info')
        self.ngram = n_gram(3, .06)
        self.ngram.load_n_gram()

    def get_symbols(self):
        return list(pickle.load(open('pickles/syms-2.p', 'rb')))

    def get_symbol_dict(self):
        return dict(pickle.load(open('pickles/id_to_words.p', 'rb')))

    def build_word_from_composition(self):
        syms = self.get_symbols()

        # create a new builder
        comp_builder = composition_builder()

        for i, sym in enumerate(syms):
            if len(sym.id_composition) > 1:
                comp_builder.insert(sym.id_composition, sym)

        return comp_builder


    def id_to_word(self, ids, immediate_build):
        builder = self.build_word_from_composition()
        symbols = self.get_symbol_dict()
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
                        composition += self.id_to_word(ids, True)[0]
            for c in temp_composition:
                composition.append(c)
            if highest_index_altered:
                i = highest_index
                highest_index_altered = False
            else:
                i += 1



        # print("Composition words: ", composition)
        return composition, gender


    def handle_time(self, word_list, time):
        return_list = []
        for list in word_list:
            for word in list:
                w = Clause()
                w.predicate = VP(word)
                if time == 'past':
                    w['TENSE'] = 'PAST'
                else:
                    w['TENSE'] = 'FUTURE'
                return_list.append(self.realise(w))

        return return_list

    def handle_plural(self, word_list):
        return_list = []
        for list in word_list:
            for word in list:
                if word[-1] == 'y':
                    return_list.append(word + 'ies')
                else:
                    return_list.append(word + 's')
        return return_list

    def build_word(self, ids):
        indicator = False
        word_list, gender = self.id_to_word(ids, False)
        for i,list in enumerate(word_list):
            for j, word in enumerate(list):
                if "indicator" in word:
                    word_list = word_list[0:i] + word_list[i + 1::]
                    i -= 1
                    indicator = True
                    if "indicator_(possessive" in word:
                        # print(handle_possessive(word_list, gender))
                        return self.handle_possessive(word_list, gender)
                    if "past" in word:
                        return self.handle_time(word_list, 'past')
                    if "future" in word:
                        return self.handle_time(word_list, 'future')
                    if "plural" in word:
                        return self.handle_plural(word_list)
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




    def handle_possessive(self, word_list, gender):
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


    def build_sentence(self, list_of_lists):
        words = []
        for list in list_of_lists:
            built_words = self.build_word(list)
            article_check = True
            if built_words is not None and len(built_words) >= 1:
                for i, word in enumerate(built_words):
                    pos = nltk.pos_tag([word])[0]
                    if article_check and 'NN' in pos[1] and wordnet.synsets(word):
                        words.append(['', 'a', 'the'])
                        article_check = False
                words.append(built_words)
        print("WORDS::::: ", words)
        sentence = self.get_most_likely_sentence(words)
        print(sentence, '\n')

    def get_combo_from_indeces(self, indecs, list_of_ists):
        temp_combo = [None] * (len(indecs))
        num_nulls = 0
        for i in range(len(indecs)):
            temp_val = list_of_ists[i][indecs[i]]
            temp_combo[i] = temp_val
            if temp_val is '':
                num_nulls += 1
        for i in range(num_nulls):
            temp_combo.remove('')
        return temp_combo

    def get_vals_from_indeces(self, index_list, list_of_lists):
        return_list = [None] * len(index_list)
        for i, index in enumerate(index_list):
            return_list[i] = list_of_lists[i][index_list[i]]
        return return_list

    def get_combos(self, list_of_lists, length):
        # count the number of combinations by multiplying length of all word_lists
        len_of_combos = 1
        for word_slot in list_of_lists:
            len_of_combos *= len(word_slot)

        # track the combinations
        combinations = []

        list_of_indexes = [[]]
        combo_index = 0
        queue = []

        len_l_of_l = len(list_of_lists)
        for n in range(length):
            # print("Length of list_of_lists = ", len(list_of_lists))
            # create a list of indexes for each position
            # n is the number of word postions
            len_l_of_l_n = len(list_of_lists[n])
            len_of_l_of_i = len(list_of_indexes)

            # print("Length of list_of_indexes = ", len_of_l_of_i)
            temp_list = [None] * (len_of_l_of_i * len_l_of_l_n)

            index = 0
            for s in range(len_l_of_l_n):
                for i in list_of_indexes:
                    temp_index = i + [s]
                    temp_val = self.get_vals_from_indeces(temp_index, list_of_lists)
                    if '' not in temp_val:
                        temp_list[index] = temp_index
                        index += 1
                    else:
                        temp_queue_list = list_of_lists[:n] + list_of_lists[n + 1:]
                        if temp_queue_list not in queue:
                            queue.append(temp_queue_list)

            while None in temp_list:
                temp_list.remove(None)
            list_of_indexes = temp_list

        for l in queue:
            combinations += self.get_combos(l, length)

        for i, ind in enumerate(list_of_indexes):
            # print(self.get_combo_from_indeces(ind, list_of_lists))
            combinations.append(self.get_vals_from_indeces(ind, list_of_lists))
        # print("List of indexes: ", list_of_indexes)
        # print("List of combos: ", combinations)

        return combinations

    def get_most_likely_n_gram(self, n_gram_list):
        probabilities = [None] * len(n_gram_list)
        for i, gram in enumerate(n_gram_list):
            probabilities[i] = (self.ngram.get_n_gram_probability(gram), gram)
            probabilities = [x for x in probabilities if (type(x) is not None)]
        probabilities = sorted(probabilities, key=lambda x: x[0])
        return probabilities[-1]

    def get_most_likely_sentence(self, list_of_lists):
        return_list = [None] * (len(list_of_lists))
        slice_start = 0
        slice_end = self.ngram.n

        # count the number of potential blank words in the first n words
        not_blanks = 0
        i = 0
        while not_blanks < self.ngram.n:
            if '' not in list_of_lists[i]:
                not_blanks += 1
            i += 1

        first_n_words = list_of_lists[:i]
        first_n_words = self.get_most_likely_n_gram(self.get_combos(first_n_words, self.ngram.n))
        return_list[:slice_end] = first_n_words[1]
        print("first N words: ", first_n_words)

        while slice_end < len(list_of_lists):
            slice_end += 1
            slice_start += 1

            # get probability for each next word
            combos = [None] * (len(list_of_lists[slice_end - 1]))
            combo_index = 0
            temp_n_gram = [None] * (self.ngram.n)
            most_likely_combo_2 = (0, 0)
            for word in list_of_lists[slice_end - 1]:
                if word is '':
                    combos[combo_index] = (0, '')
                    combo_index += 1
                    combos_2 = [None] * (len(list_of_lists[slice_end]))
                    combo_2_index = 0
                    for second_word in list_of_lists[slice_end]:
                        temp_n_gram = return_list[slice_start:slice_end - 1] + [second_word]
                        combos_2[combo_2_index] = (self.ngram.get_n_gram_probability(temp_n_gram), second_word)
                        combo_2_index += 1
                    combos_2 = sorted(combos_2, key=lambda x: x[0])
                    most_likely_combo_2 = combos_2[-1]
                else:
                    temp_n_gram = return_list[slice_start:slice_end - 1] + [word]
                    combos[combo_index] = (self.ngram.get_n_gram_probability(temp_n_gram), word)
                    combo_index += 1
            combos = sorted(combos, key=lambda x: x[0])
            if most_likely_combo_2[0] > combos[-1][0]:
                return_list[slice_end - 1] = most_likely_combo_2[1]
                list_of_lists = list_of_lists[:slice_end] + list_of_lists[slice_end + 1:]
                return_list = return_list[:slice_end] + return_list[slice_end + 1:]
            else:
                return_list[slice_end - 1] = combos[-1][1]

        return return_list

    def get_dictionary(self, word, n):
        temp_dict = self.ngram.n_grams[n][word]
        keys = sorted(dict(temp_dict).keys())
        for key in keys:
            print(key, ": ", temp_dict[key])
        print(self.ngram.n_grams[n][word])





