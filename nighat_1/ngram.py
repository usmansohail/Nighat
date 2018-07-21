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
        self.n_grams = pickle.load(open('pickles/n_grams.p', 'rb'))
        self.num_words = pickle.load(open('pickles/num_words.p', 'rb'))

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
        pickle.dump(self.n_grams, open('pickles/n_grams.p', 'wb'))
        pickle.dump(self.num_words, open('pickles/num_words.p', 'wb'))

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








