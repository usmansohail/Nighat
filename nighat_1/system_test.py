from system_tools import build_word_from_composition, build_sentence

# create the blissymbolics builder
builder = build_word_from_composition()

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
        print("L: ", l)
        build_sentence(l)
