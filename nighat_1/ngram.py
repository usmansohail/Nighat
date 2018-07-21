import cmath
import re
import nltk
from nltk.util import ngrams
from nltk.corpus import gutenberg, brown, conll2000
import cmath
import pickle
import string
import logging

# setup logger
# logging.basicConfig(filename='logs/log1.txt', filemode='w', level=logging.DEBUG)


#TODO: optimize for time
#TODO: log stuff

class n_gram:

    def __init__(self, n, seed):
        logging.info('\n\n\n ### %s -Gram Info:', n)

        self.n = n
        self.count_dictionary = {}
        self.n_grams = {}
        self.corpus = None
        self.regex = re.compile(r"^(a-zA-Z0-9)")
        self.interpolation_lamdas = {}
        self.interpolation_setup(seed)
        self.num_words = 0

        # create dictionary for all n-grams [1 - n)
        for i in range(1, self.n + 1):
            self.n_grams[i] = {}

    def load_n_gram(self):
        self.n_grams = pickle.load(open('n_grams.p', 'rb'))
        self.num_words = pickle.load(open('num_words.p', 'rb'))

    def read_corpus(self, corpus):
        logging.info('Reading corpus')
        self.corpus = corpus.sents()
        self.num_words += len(corpus.words())
        for sentence in self.corpus:
            temp_list = [str(x).lower() for x in sentence if x is not ('.' or ',' or '?' or ';' or ':' or '%' or '*' or
                                                                       '[' or ']')]

            for n in range(1, self.n + 1):
                sent_ngrams = ngrams(temp_list, n)
                for n_gram in sent_ngrams:
                    current_dictionary = self.n_grams[n]
                    for i, word in enumerate(n_gram):
                        if i < n - 1:
                            try:
                                current_dictionary = current_dictionary[word]
                            except KeyError:
                                current_dictionary[word] = {}
                                current_dictionary = current_dictionary[word]
                        else:
                            try:
                                current_dictionary[word] += 1
                            except KeyError:
                                current_dictionary[word] = 1
        pickle.dump(self.n_grams, open('n_grams.p', 'wb'))
        pickle.dump(self.num_words, open('num_words.p', 'wb'))

        logging.info('Done reading corpus')

    def interpolation_setup(self, seed):
        lambda_start = 1
        for i in range(self.n, 0, -1):
            self.interpolation_lamdas[i] = lambda_start
            lambda_start *= seed
        logging.info("Interpolation lambdas: %s", self.interpolation_lamdas)

    def get_gram_counts(self, words):
        n_gram_counts = {}
        for i in range(1, self.n + 1):
            current_dictionary = self.n_grams[i]
            temp_words = words[-i:]
            # print("Temp words: ", temp_words)
            for w, word in enumerate(temp_words):
                if w < i - 1:
                    try:
                        current_dictionary = current_dictionary[word]
                    except KeyError:
                        n_gram_counts[i] = (0, self.num_words)
                        break
                else:
                    try:
                        n_gram_counts[i] = (current_dictionary[word], len(current_dictionary.keys()))
                    except KeyError:
                        n_gram_counts[i] = (1, self.num_words)
        return n_gram_counts

    def get_n_gram_probability(self, words):
        counts = self.get_gram_counts(words)
        probability = 0
        for i in range(1, self.n + 1):
            try:
                if not (counts[i][0] == 0 or counts[i][1] == 0):
                    probability += self.interpolation_lamdas[i] * float((counts[i][0] / counts[i][1]))
            except KeyError:
                pass
        return float(probability)

    def get_sentence_probability(self, sentence):
        sentence = [str(x).lower() for x in sentence if x != '']
        sent_ngrams = list(ngrams(sentence, self.n))
        probs = [None] * len(sent_ngrams)
        for i, curr_gram in enumerate(sent_ngrams):
            temp = self.get_n_gram_probability(curr_gram)

            probs[i] = temp

        return_prob = 1
        for prob in probs:
            return_prob *= prob
        return return_prob

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
            probabilities[i] = (self.get_n_gram_probability(gram), gram)
            probabilities = [x for x in probabilities if (type(x) is not None)]
        probabilities = sorted(probabilities, key=lambda x: x[0])
        return probabilities[-1]

    def get_most_likely_sentence(self, list_of_lists):
        return_list = [None] * (len(list_of_lists))
        slice_start = 0
        slice_end = self.n

        # count the number of potential blank words in the first n words
        not_blanks = 0
        i = 0
        while not_blanks < self.n:
            if '' not in list_of_lists[i]:
                not_blanks += 1
            i += 1

        first_n_words = list_of_lists[:i]
        first_n_words = self.get_most_likely_n_gram(self.get_combos(first_n_words, self.n))
        return_list[:slice_end] = first_n_words[1]
        print("first N words: ", first_n_words)

        while slice_end < len(list_of_lists):
            slice_end += 1
            slice_start += 1

            # get probability for each next word
            combos = [None] * (len(list_of_lists[slice_end - 1]))
            combo_index = 0
            temp_n_gram = [None] * (self.n)
            most_likely_combo_2 = (0, 0)
            for word in list_of_lists[slice_end - 1]:
                if word is '':
                    combos[combo_index] = (0, '')
                    combo_index += 1
                    combos_2 = [None] * (len(list_of_lists[slice_end]))
                    combo_2_index = 0
                    for second_word in list_of_lists[slice_end]:
                        temp_n_gram = return_list[slice_start:slice_end - 1] + [second_word]
                        combos_2[combo_2_index] = (self.get_n_gram_probability(temp_n_gram), second_word)
                        combo_2_index += 1
                    combos_2 = sorted(combos_2, key=lambda x: x[0])
                    most_likely_combo_2 = combos_2[-1]
                else:
                    temp_n_gram = return_list[slice_start:slice_end - 1] + [word]
                    combos[combo_index] = (self.get_n_gram_probability(temp_n_gram), word)
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
        temp_dict = self.n_grams[n][word]
        keys = sorted(dict(temp_dict).keys())
        for key in keys:
            print(key, ": ", temp_dict[key])
        print(self.n_grams[n][word])






