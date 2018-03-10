import pickle
from classes import composition_builder
from classes import node


def get_symbols():
    return list(pickle.load(open('syms-2.p', 'rb')))


def build_word_from_composition():
    syms = get_symbols()

    # create a new builder
    comp_builder = composition_builder()

    for i, sym in enumerate(syms):
        if len(sym.id_composition) > 1:
            comp_builder.insert(sym.id_composition, sym)

    return comp_builder

builder = build_word_from_composition()


temp_list = [8998, 13867]
temp_list_2 = [13867, 8998]

print(builder.get_symbol(temp_list).words)
print(builder.get_symbol(temp_list_2).words)