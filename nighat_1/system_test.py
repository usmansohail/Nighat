import pickle
from system_tools import SystemTools
from ngram import n_gram
from nltk.corpus import wordnet, gutenberg, brown, conll2000
from nltk.corpus.reader import conll
from nltk.corpus.reader.plaintext import EuroparlCorpusReader
from nltk.tokenize import WordPunctTokenizer
import nltk

def test_builder():
    # create the blissymbolics builder
    system_tools = SystemTools()
    builder = system_tools.build_word_from_composition()

    # open the file with the test set
    book_1 = open("test_sentences/the_blissymbol_opposite_series.txt")

    # for each line, build a sentence
    lines = []
    for i, line in enumerate(book_1):
        if line[0] is not "#":
            l = str(line).split(' ')
            for j, word in enumerate(l):
                l[j] = str(word).split(',')
                l[j] = [int(x.strip()) for x in l[j] if x is not '\n']
            lines.append(l)
            print("Input: ", l)
            system_tools.build_sentence(l)

def test_ngram():
    n_g = n_gram(3, .06, logging=False)
    # n_g.load_n_gram()
    n_g.read_corpus(gutenberg)
    n_g.read_corpus(brown)
    n_g.read_corpus(conll2000)
    combinations = [None]  * 1000
    index = 0
    for i in range(40, 65, 2):
        for j in range(i, 99 - i, 2):
            k = 100 - j - i
            if index < 1000:
                n_g.manual_interpolation([i * .01, j * .01, k * .01])
                print("starting test")
                combinations[index] = ((i, j, k), n_g.test_n_gram())
                print("Index: ", index, "combo: ", combinations[index][0], " probability: ", combinations[index][1])
                index += 1
    combinations = combinations[:index]
    combinations = sorted(combinations, key=lambda x: x[1], reverse=True)
    pickle.dump(combinations, open('pickles/interpolation_constants.p', 'wb'))
    for c in combinations[-3:]:
        print(c)


test_ngram()
# test_builder()


# system_tools = SystemTools()
# print(system_tools.build_word([14133,16455,8993,9004]))

# punkt = WordPunctTokenizer()
# dir = nltk.data.find('corpora/gutenberg')
# # my_tokenizer = nltk.RegexpTokenizer('[a-z|A-Z]+')
# my_tokenizer = nltk.RegexpTokenizer(r'[^a-zA-Z0-9]+')
# reader = nltk.corpus.PlaintextCorpusReader(dir, '.*\.txt', sent_tokenizer=my_tokenizer)
# for sent in reader.sents():
#     print(sent)


# print(get_vals_from_indeces([1, 0, 1, 0], list_of_lists))