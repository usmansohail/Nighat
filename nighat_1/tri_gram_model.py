from nltk import trigrams, bigrams, word_tokenize
from collections import Counter, defaultdict
from nltk.tokenize import sent_tokenize, word_tokenize
import pickle
from nltk.util import ngrams
import re

def get_lists():
    return pickle.load(open("list_of_lists.p", 'rb'))

def get_lists_old():
    # get the file
    text_file = open('C:/Users/Usman Sohail/Documents/CSCI-490/corpera/data.v1/wiki.simple', 'rb')

    # read the lines of the file
    content = text_file.readlines()

    # add everything to a raw set of text
    raw_text = ''

    for line in content:
        raw_text += str(line.rstrip())

    # tokenize sentences
    sent_list = sent_tokenize(raw_text)

    # tokenize words
    token_words = word_tokenize(raw_text)

    # create a list of tokenized sentences
    list_of_lists = []
    for sent in sent_list:
        list_of_lists.append(word_tokenize(sent))

    #pickle.dump(list_of_lists, open("C:/Users/Usman Sohail/Documents/CSCI-490/corpera/get_corpus_data/list_of_lists.p", 'wb'))
    pickle.dump(token_words, open('token_words.p', 'wb'))
    return token_words

def get_tri_model():
    # get the lists
    list_of_lists = get_lists()

    # build the model
    model = defaultdict(lambda : defaultdict(lambda : 0))

    for sentence in list_of_lists:
        for word1, word2, word3 in trigrams(sentence, pad_right=True, pad_left=True):
            model[(word1, word2)][word3] += 1


    return model

def get_bi_model():
    # build the model
    model = defaultdict(lambda: defaultdict(lambda: 0))
    list_of_lists = get_lists()
    for sentence in list_of_lists:
        for word1, word2 in bigrams(sentence, pad_right=True, pad_left=True):
            model[word1][word2] += 1

    return model

def get_uni_model():
    model = defaultdict(lambda: defaultdict(lambda: 0))
    list = get_lists()
    for sent in list:
        for word in sent:
            model[word] += 1

    return model


bi_model = get_bi_model()
#uni_model = get_uni_model()




#tri_model = get_tri_model()
#bi_model = get_bi_model()

def add_alpha_prob(w1, w2, alpha):
    # get the size of the vocab
    # vocab = pickle.load(open('vocab.p', 'rb'))
    # size = len(vocab)

    # hard coded for now TODO: fix this
    size = 118639


    return float(bi_model[w1][w2] + alpha) / float(size* alpha + bi_model[w1][w2] + bi_model[w2][w1])



def sentence_likelihood(sentence, alpha):
    # token = get_lists_old()

    # uni = list(ngrams(token, 1))
    # bi = list(ngrams(token, 2))
    # tri = list(ngrams(token, 3))

    # get the probability of the first word
    #prob = get_uni_model()[sentence[0]]
    prob = 1

    # remove blank words
    for i, word in enumerate(sentence):
        if word == "" or word == '':
            sentence = sentence[0:i] + sentence[i + 1::]


    for i in range(1, len(sentence)):
        prob *= add_alpha_prob(sentence[i - 1], sentence[i], alpha)
    return prob



def get_most_likely_sentence(list_of_lists, alpha):
    # get all possible words for each symbol
    total_combinations = 1

    for list in list_of_lists:
        total_combinations *= len(list)



    list_of_indexes = [[]]
    for n in range(len(list_of_lists)):
        # create a list of indexes for each position
        # n is the number of word postions sent in
        temp_list = []

        for s in range(len(list_of_lists[n])):
            for i in list_of_indexes:
                temp_list.append(i + [s])
        list_of_indexes = temp_list

    # build all the combinations of words
    combinations = []
    for l in range(len(list_of_indexes)):
        combo = []
        for index in range(len(list_of_indexes[l])):
            combo.append(list_of_lists[index][list_of_indexes[l][index]])
        combinations.append(combo)
        # create each combination of words

    # get the probabilities of the sentences
    print("####################### SORTED PROBABILITIES WITH ALPHA = ", alpha)
    probs = []
    for combo in combinations:
        probs.append((sentence_likelihood(combo, alpha), combo))

    # sort by probabilities
    probs = sorted(probs, key=lambda probability: probability[0])
    #print(probs)

    # for prob, sentence in probs:
        # print("probability for words: ", sentence, " = ", prob)

    print('\n\n\n')

    return probs[-1]

# l = [16226, 16229]
# q = [14687, 15210, 16223]
# # test_sentence_3 = [14916, 14913, 15918,15686, 12577]
# test_sentence_3 = [['what'], ['is', 'was'], ['your'], ['name', 'address']]
# # test_sentence_4 = [14688, 16967,24829 , 24916]
# # test_sentence_5 = [14688, 24261,24823]
# #get_most_likely_sentence(l)
# #get_most_likely_sentence(q)
# print(get_most_likely_sentence(test_sentence_3, .0001))
# # get_most_likely_sentence(test_sentence_3, .01)
# # get_most_likely_sentence(test_sentence_4, .01)

get_most_likely_sentence([['for'], ['the'], ['boy'], ['and'], ['his'], ['family']], .001)


"""
s = ['I', 'hope', 'this', 'works']
n = ['the', 'man', 'went', 'for', 'a', 'walk']
print(sentence_likelihood(s))

print(sentence_likelihood(n))
"""