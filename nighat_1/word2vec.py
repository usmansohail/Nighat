import gensim.downloader as api
import pickle
import os
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
import gensim, logging
from nltk.corpus import wordnet, gutenberg, brown, conll2000

logging.basicConfig(format='%(asctime)s : %(levelname)s :%(message)s', level=logging.INFO)


# CONSTANTS
WORD_EMBEDDING_MODEL_OUTPUT = "pickles/w2v.p"
MODEL_NAME = "pickles/w2v_model.model"
VECTORS = "pickles/vectors.kv"

class Word_2_Vec:

    def __init__(self):
        pass

    def read_corperea(self, corpus):
        sentences = corpus.sents()
        return_list = [None] * len(sentences)
        for i, sentence in enumerate(sentences):
            sentence = str(" ").join(sentence)
            return_list[i] = gensim.utils.simple_preprocess(sentence)
        return return_list

    def train(self, corpus, vector_size=150, window=10, min_count=2, workers=10, epochs=10):
        corpus = self.read_corperea(corpus)
        self.model = gensim.models.Word2Vec(
            corpus,
            size=vector_size,
            window=window,
            min_count=min_count,
            workers=workers)

        self.model.train(corpus, total_examples=len(corpus), epochs=epochs)
        pickle.dump(self.model, open(WORD_EMBEDDING_MODEL_OUTPUT, 'wb'))
        self.model.save(MODEL_NAME)

    def load_model(self, model_name):
        self.model = gensim.models.Word2Vec.load(model_name)



# w = Word_2_Vec()
# print(w.read_corperea(gutenberg))
# w.train(gutenberg)
#
# word_1 = "dirty"
#
# w.model.wv.most_similar(positive=word_1)

model = Word_2_Vec()
# model.train(gutenberg)
model.load_model(MODEL_NAME)

word_1 = "and"
# model.model.wv.most_similar(positive=word_1)

vector = model.model.wv['dirty']
print(vector)

# fname = gensim.utils.get_tmpfile(VECTORS)
# word_vectors = model.model.wv
# word_vectors.save(fname)

word_vectors = api.load("glove-wiki-gigaword-100")

result = word_vectors.most_similar(positive=['woman', 'king'], negative=['man'])
result = word_vectors.most_similar(positive=['feeling', 'fire'])
result = word_vectors.most_similar(positive=['sign', 'vehicle'])
result = word_vectors.most_similar(positive=['much', 'wave'])
result = word_vectors.most_similar(positive=['question', 'time'])

word_combos = [['desire', 'feeling', 'fire'], ['street sign', 'sign', 'vehicle'], ['rough seas', 'much', 'wave'],
               ['when', 'question', 'time'], ['where', 'question', 'earth'], ['who', 'question', 'person'],
               ['school uniform', 'cloths', 'school'], ['sign', 'thing', 'information'], ['speech', 'activity', 'mouth'],
               ['sunglasses', 'sun', 'glasses'], ['tourist', 'visitor', 'place']]

for combo in word_combos:
    result = word_vectors.most_similar(positive=combo[1::])
    print(combo[0], ' = ', combo[1], " + ", combo[2], ":")
    print("{}: {:4f}".format(*result[0]))
    print('\n\n')


# class input_sentences(object):
#     def __init__(self, dirname):
#         self.dirname = dirname
#
#     def __iter__(self):
#         for fname in os.listdir(self.dirname):
#             for line in open(os.path.join(self.dirname, fname)):
#                 yield
#
#         for dir_name, sub_dir_list, file_list in os.walk(self.dirname):
#             for file in file_list:
#                 if file.lower().endswith('.txt'):
#                     for line in open(os.path.join('','')):
#                         print()
#
#
# for dir_name, sub_dir_list, file_list in os.walk('.'):
#     for file in file_list:
#         if file.lower().endswith('.txt'):
#             print(os.path.dirname(os.path.abspath(__file__).encode('utf-8')) )
#                   # '/word2vec/' + str(dir_name) + str(file))