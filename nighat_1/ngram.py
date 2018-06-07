import nltk
from nltk.util import ngrams
from nltk.corpus import gutenberg

gut = list(gutenberg.words())

bigram = {}
trigram = {}
fourgram = {}

def extract_sentence(n, sent, dict):
    temp = ngrams(sent, n)
    for ngram in temp:
        try:
            dict[ngram] += 1
        except KeyError:
            dict[ngram] = 1

for sent in gutenberg.sents():
    extract_sentence(2, sent, bigram)
    extract_sentence(3, sent, trigram)
    extract_sentence(4, sent, fourgram)

def percentage_dictionary(dict):
    denominator = len(list(dict.keys()))
    for key in dict.keys():
        dict[key] = float(dict[key]) / float(denominator)

percentage_dictionary(bigram)
percentage_dictionary(trigram)
percentage_dictionary(fourgram)

for i in range(10):
    key = list(trigram.keys())[i]
    print(key, ": ", trigram[key])
print(len(bigram))



