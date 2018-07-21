import pickle
from system_tools import SystemTools
from ngram import n_gram

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
    n_g = n_gram(3, .06)
    n_g.load_n_gram()
    combinations = [None]  * 1000
    index = 0
    for i in range(1, 30, 5):
        for j in range(i, 60, 5):
            k = 100 - j - i
            if index < 1000:
                n_g.manual_interpolation([i * .01, j * .01, k * .01])
                combinations[index] = ((i, j, k), n_g.test_n_gram())
                print("Index: ", index, "combo: ", combinations[index][0], " probability: ", combinations[index][1])
                index += 1
    combinations = combinations[:index]
    combinations = sorted(combinations, key=lambda x: x[1])
    pickle.dump(combinations, open('pickles/interpolation_constants.p', 'wb'))
    for c in combinations[-3:]:
        print(c)


# test_ngram()
# test_builder()



# print(get_vals_from_indeces([1, 0, 1, 0], list_of_lists))