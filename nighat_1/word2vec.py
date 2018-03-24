import os
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
import gensim, logging
#logging.basicConfig(format='%(asctime:s : %(levelname)s :%(message)s', level=logging.INFO)

class input_sentences(object):
    def __init__(self, dirname):
        self.dirname = dirname

    def __iter__(self):
        for fname in os.listdir(self.dirname):
            for line in open(os.path.join(self.dirname, fname)):
                yield

        for dir_name, sub_dir_list, file_list in os.walk(self.dirname):
            for file in file_list:
                if file.lower().endswith('.txt'):
                    for line in open(os.path.join('','')):
                        print()


for dir_name, sub_dir_list, file_list in os.walk('.'):
    for file in file_list:
        if file.lower().endswith('.txt'):
            print(os.path.dirname(os.path.abspath(__file__).encode('utf-8')) )
                  # '/word2vec/' + str(dir_name) + str(file))