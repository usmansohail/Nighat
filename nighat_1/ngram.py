import re
import nltk
from nltk.util import ngrams
from nltk.corpus import gutenberg
import cmath
import pickle
import string

#TODO: optimize for time

class n_gram:

    def __init__(self, n, corpus):
        self.n = n
        self.count_dictionary = {}
        self.corpus = list(corpus.sents())
        self.regex = re.compile(r"^(a-zA-Z0-9)")
    def load_n_gram(self):
        self.count_dictionary = pickle.load(open('count_dict.p', 'rb'))

    def read_corpus(self):
        for sentence in self.corpus:
            temp_list = [str(x).translate(string.punctuation) for x in sentence]

            sent_ngrams = ngrams(temp_list, self.n)
            for n_gram in sent_ngrams:
                current_dictionary = self.count_dictionary
                for i, word in enumerate(n_gram):
                    if i < self.n - 1:
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

        pickle.dump(self.count_dictionary, open('count_dict.p', 'wb'))



    def get_n_gram_probability(self, words):
        if len(words) != self.n:
            return None
        current_dictionary = self.count_dictionary
        for i, word in enumerate(words):
            if i < self.n - 1:
                try:
                    current_dictionary = current_dictionary[word]
                except KeyError:
                    return float(1 / len(dict(current_dictionary).keys()))
        try:
            numerator = current_dictionary[words[-1]]
        except KeyError:
            numerator = 1

        return float(numerator / len(list(current_dictionary.keys())))


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

    def get_most_likely_sentence(self, list_of_lists, alpha):
        # get all possible words for each symbol
        total_combinations = 1

        # get the n-gram model
        for list in list_of_lists:
            total_combinations *= len(list)



        list_of_indexes = [[]]
        len_l_of_l = len(list_of_lists)
        for n in range(len_l_of_l):
            # create a list of indexes for each position
            # n is the number of word postions sent in
            len_l_of_l_n = len(list_of_lists[n])
            len_of_l_of_i = len(list_of_indexes)
            temp_list = [None] * (len_of_l_of_i * len_l_of_l_n)

            index = 0
            for s in range(len_l_of_l_n):
                for i in list_of_indexes:
                    temp_list[index] = i + [s]
                    index += 1
            list_of_indexes = temp_list

        len_l_of_i = len(list_of_indexes)

        # build all the combinations of words
        combinations = [None] * (len_l_of_i)
        combinations_index = 0
        for l in range(len(list_of_indexes)):
            combo = [None] * (len(list_of_indexes[l]))
            combo_index = 0
            for index in range(len(list_of_indexes[l])):
                combo[combo_index] = list_of_lists[index][list_of_indexes[l][index]]
                combo_index += 1
            combinations[combinations_index] = combo
            combinations_index += 1
            # create each combination of words

        # get the probabilities of the sentences
        # print("####################### SORTED PROBABILITIES WITH ALPHA = ", alpha)
        probs = [None] * (len_l_of_i)
        for i, combo in enumerate(combinations):
            probs[i] = (self.get_sentence_probability(combo), combo)

        # sort by probabilities
        print(probs)
        probs = sorted(probs, key=lambda combinations: float(combinations[0]))
        print(probs)
        #print(probs)

        # for prob, sentence in probs:
            # print("probability for words: ", sentence, " = ", prob)



        return probs[-1]


n_g = n_gram(3, gutenberg)
n_g.read_corpus()
print(n_g.get_n_gram_probability(['I', 'love', 'you']))
sentence_1 = ['I', 'was', 'walking', 'down', 'the', 'street']
sentence_2 = ['I', 'was', 'walking', 'down', 'the', 'stupid']
print("prob for sentence: ", sentence_1, " = ", n_g.get_sentence_probability(sentence_1))
print("prob for sentence: ", sentence_2, " = ", n_g.get_sentence_probability(sentence_2))
