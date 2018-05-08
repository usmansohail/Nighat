import time
import pickle
from classes import composition_builder
from classes import node
import nltk
from nltk import stem
from nltk.stem.lancaster import LancasterStemmer
from nltk.corpus import wordnet as wn


def get_symbols():
    return list(pickle.load(open('syms-2.p', 'rb')))

def get_symbol_dict():
    return dict(pickle.load(open('id_to_words.p', 'rb')))

def build_word_from_composition():
    syms = get_symbols()

    # create a new builder
    comp_builder = composition_builder()

    for i, sym in enumerate(syms):
        if len(sym.id_composition) > 1:
            comp_builder.insert(sym.id_composition, sym)

    return comp_builder


def id_to_word(ids):
    builder = build_word_from_composition()
    symbols = get_symbol_dict()
    highest_index = 0
    highest_index_altered = False
    composition = []
    i = 0
    while i < (len(ids)):
        temp_composition = []
        for j in range(i+1, len(ids) + 1):
            temp_id_list = ids[i:j]
            if len(temp_id_list) == 1:
                temp_composition.append(symbols[temp_id_list[0]])
            else:
                temp_build = builder.get_symbol(temp_id_list)
                if temp_build is not None and temp_build.id is not None:
                    temp_composition = []
                    temp_composition.append(temp_build.words)
                    highest_index = j
                    highest_index_altered = True
        for c in temp_composition:
            composition.append(c)
        if highest_index_altered:
            i = highest_index
            highest_index_altered = False
        else:
            i += 1


    print("Composition words: ", composition)




builder = build_word_from_composition()

t = [12613, 14390]
temp_list = [8998, 13867]
temp_list_2 = [13867, 8998]

he_she = [16161, 8499]
his_hers = [14688, 24676]

word_parts = [t, temp_list, temp_list_2]
# for l in word_parts:
#     composition = ""
#     for i, id in enumerate(l):
#         if i < len(l) - 1:
#             composition +=
# print(builder.get_symbol(temp_list).words)
# print(builder.get_symbol(temp_list_2).words)
# print("He, she: ", builder.get_symbol(he_she).words)
# print("His, hers: ", builder.get_symbol(his_hers).words)

# id_to_word(t)
# id_to_word(temp_list)
# id_to_word(temp_list_2)
# id_to_word(he_she)
# id_to_word(his_hers)
tt = [16161, 8499, 24676]
id_to_word(tt)

# st = LancasterStemmer()
# #
# start1 = int(round(time.time() * 1000))
# print("###########", start1)
# print(st.stem('running'))
# print(st.stem('action'))
# print(st.stem('question'))
# print(st.stem('divide'))
# print(st.stem('ran'))
# print(st.stem('abide'))
# print(st.stem('formal'))
#
# time2 = int(round(time.time() * 1000))
# print("############", time2 - start1)
# # wn.morphy seems to perform better but also take much longer
# print(wn.morphy('denied', wn.VERB))
# print(wn.morphy('divided', ))
# print(wn.morphy('abide'))
# print(wn.morphy('action'))
# print(wn.morphy('running'))
# print(wn.morphy('greener', wn.ADJ))
#
#
# time3 = int(round(time.time() * 1000))
# print("############", time3 - time2)
#
