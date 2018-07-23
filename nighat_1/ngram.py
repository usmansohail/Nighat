import cmath
import re
import nltk
from nltk.util import ngrams
from nltk.corpus import gutenberg, brown, conll2000, webtext, nps_chat
import cmath
import pickle
import string
import logging
from classes import levenshtein
from nltk.corpus.reader.plaintext import EuroparlCorpusReader

# setup logger
# logging.basicConfig(filename='logs/log1.txt', filemode='w', level=logging.DEBUG)


#TODO: optimize for time
#TODO: log each n-gram count explicitly

class n_gram:

    def __init__(self, n, seed, logging=True, not_word=10):
        self.logging = logging
        self.logg(('\n\n\n ### %s -Gram Info:', n))

        self.n = n
        self.count_dictionary = {}
        self.n_grams = {}
        self.corpus = None
        self.regex = re.compile(r'[^a-zA-Z0-9]+')
        self.interpolation_lamdas = {}
        self.interpolation_setup(seed)
        self.num_words = 0
        self.total_string = "total###"
        self.words = {}
        self.error_not_word = not_word
        self.first_words = {}

        # create dictionary for all n-grams [1 - n)
        for i in range(1, self.n + 1):
            self.n_grams[i] = {}

    def load_n_gram(self):
        self.n_grams = pickle.load(open('pickles/n_grams.p', 'rb'))
        self.num_words = pickle.load(open('pickles/num_words.p', 'rb'))
        self.words = pickle.load(open('pickles/words.p', 'rb'))
        self.first_words = pickle.load(open('pickles/first_words.p', 'rb'))

    def logg(self, string):
        if self.logging:
            logging.info(*string)

    def clean_sentence(self, words):
        return [str(re.sub(self.regex, '', x)).lower() for x in words
                if str(re.sub(self.regex, '', x)).lower() is not '']

    def read_corpus(self, corpus, treat_as_list=False):
        self.logg('Reading corpus')
        if treat_as_list:
            self.corpus = corpus
            self.num_words += len(corpus)
        else:
            self.corpus = corpus.sents()
            self.num_words += len(corpus.words())
        for sentence in self.corpus:
            temp_list = self.clean_sentence(sentence)
            if len(temp_list) > 0:
                try:
                    self.first_words[temp_list[0]] += 1
                except KeyError:
                    self.first_words[temp_list[0]] = 1


            for n in range(1, self.n + 1):
                sent_ngrams = ngrams(temp_list, n)
                for n_gram in sent_ngrams:
                    current_dictionary = self.n_grams[n]
                    for i, word in enumerate(n_gram):
                        try:
                            self.words[word] += 1
                        except KeyError:
                            self.words[word] = 1
                        if i < n - 1:
                            try:
                                current_dictionary[self.total_string] += 1
                            except KeyError:
                                current_dictionary[self.total_string] = 1
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
                            try:
                                current_dictionary[self.total_string] += 1
                            except KeyError:
                                current_dictionary[self.total_string] = 1
        pickle.dump(self.n_grams, open('pickles/n_grams.p', 'wb'))
        pickle.dump(self.num_words, open('pickles/num_words.p', 'wb'))
        pickle.dump(self.words, open('pickles/words.p', 'wb'))
        pickle.dump(self.first_words, open('pickles/first_words.p', 'wb'))

        self.logg('Done reading corpus')
        print("done reading corpus")

    def interpolation_setup(self, seed):
        lambda_start = 1
        for i in range(self.n, 0, -1):
            self.interpolation_lamdas[i] = lambda_start
            lambda_start *= seed
        self.logg(("Interpolation lambdas: %s", self.interpolation_lamdas))

    def manual_interpolation(self, constants):
        if len(constants) != self.n:
            raise ValueError("the number of constants does not match n")
        for i, c in enumerate(constants):
            self.interpolation_lamdas[i + 1] = c

    def word_status(self, word):
        try:
            self.words[word]
            return 1
        except KeyError:
            return self.error_not_word


    def get_gram_counts(self, words):
        words = [str(w).lower() for w in words]
        self.logg(("\n\n########## words: %s", words))
        n_gram_counts = {}
        for i in range(1, self.n + 1):
            current_dictionary = self.n_grams[i]
            temp_words = words[-i:]
            # print("Temp words: ", temp_words)
            length_temp_words = len(temp_words)
            w = 0
            word = None
            finish_words = True
            while w < length_temp_words and finish_words:
                word = temp_words[w]
                if w < i - 1:
                    try:
                        current_dictionary = current_dictionary[word]
                    except KeyError:
                        n_gram_counts[i] = (1, current_dictionary[self.total_string] * self.word_status(word))
                        finish_words = False
                else:
                    try:
                        n_gram_counts[i] = (current_dictionary[word], current_dictionary[self.total_string])
                    except KeyError:
                        n_gram_counts[i] = (1, current_dictionary[self.total_string] * self.word_status(word))
                w += 1
        return n_gram_counts

    def get_first_n_gram_counts(self, words):
        words = [str(w).lower() for w in words]
        self.logg(("\n\n########## words: %s", words))
        n_gram_counts = {}
        index = 0
        for i in range(1, self.n + 1):
            n_gram_counts[i] = []
            for gram in ngrams(words, i):
                w = 0
                finish_words = True
                current_dictionary = self.n_grams[i]

                while w < i and finish_words:
                    word = gram[w]
                    if w < i - 1:
                        try:
                            current_dictionary = current_dictionary[word]
                        except KeyError:
                            n_gram_counts[i].append((1, current_dictionary[self.total_string] * self.word_status(word)))
                            finish_words = False
                            index += 1
                    else:
                        try:
                            n_gram_counts[i].append((current_dictionary[word], current_dictionary[self.total_string]))
                            index += 1
                        except KeyError:
                            n_gram_counts[i].append((1, current_dictionary[self.total_string] * self.word_status(word)))
                            index += 1
                    w += 1
        return n_gram_counts

    def get_first_gram_probability(self, words):
        counts = self.get_first_n_gram_counts(words)
        probability = 0
        first_word = 1
        try:
            first_word *= (self.first_words[words[0]] / self.num_words)
        except KeyError:
            first_word *= (1 / self.num_words)
        probability += first_word
        self.logg(("First word probability: %f", probability))
        self.logg(("%-10s%-16s%-16s%-16s%-16s%-16s", "n: ", "numerator:", "denominator:", "fraction:",
                     "lambda:", "final result:"))
        for i in range(1, self.n + 1):
            for c in counts[i]:
                try:
                    if not (c[1] == 0):
                        fraction = float(c[0] / c[1])
                        final = self.interpolation_lamdas[i] * fraction
                        final = -cmath.log(final, 2).real
                        probability += final
                        self.logg(("%-10d%-16d%-16d%-16f%-16f%-16f", i, c[0], c[1], fraction,
                                     self.interpolation_lamdas[i], final))
                except KeyError:
                    pass
        self.logg(("final sum of probability: %f", probability))
        return float(probability)

    def get_n_gram_probability(self, words):
        counts = self.get_gram_counts(words)
        probability = 0
        self.logg(("%-10s%-16s%-16s%-16s%-16s%-16s", "n: ", "numerator:", "denominator:", "fraction:",
                     "lambda:", "final result:"))
        for i in range(1, self.n + 1):
            try:
                if not (counts[i][1] == 0):
                    fraction = float(counts[i][0] / counts[i][1])
                    final = self.interpolation_lamdas[i] * fraction
                    final = -cmath.log(final, 2).real
                    probability += final
                    self.logg(("%-10d%-16d%-16d%-16f%-16f%-16f", i, counts[i][0], counts[i][1], fraction,
                                 self.interpolation_lamdas[i], final))
            except KeyError:
                pass
        self.logg(("final sum of probability: %f", probability))
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


    def test_n_gram(self):
        numerator = 0.0
        denominator = 0.0

        for sent in brown.sents():
            sent = self.clean_sentence(sent)
            numerator += cmath.log(self.get_sentence_probability(sent), 20).real
            denominator += 1

        return numerator / denominator