from system_tools import SystemTools

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

# def get_vals_from_indeces(index_list, list_of_lists):
#     return_list = [None] * len(index_list)
#     for i, index in enumerate(index_list):
#         return_list[i] = list_of_lists[i][index_list[i]]
#     return return_list
#
#
# def get_combos(list_of_lists, length):
#     # count the number of combinations by multiplying length of all word_lists
#     len_of_combos = 1
#     for word_slot in list_of_lists:
#         len_of_combos *= len(word_slot)
#
#     # track the combinations
#     combinations = []
#
#     list_of_indexes = [[]]
#     combo_index = 0
#     queue = []
#
#     len_l_of_l = len(list_of_lists)
#     for n in range(length):
#         # print("Length of list_of_lists = ", len(list_of_lists))
#         # create a list of indexes for each position
#         # n is the number of word postions
#         len_l_of_l_n = len(list_of_lists[n])
#         len_of_l_of_i = len(list_of_indexes)
#
#         # print("Length of list_of_indexes = ", len_of_l_of_i)
#         temp_list = [None] * (len_of_l_of_i * len_l_of_l_n)
#
#         index = 0
#         for s in range(len_l_of_l_n):
#             for i in list_of_indexes:
#                 temp_index = i + [s]
#                 temp_val = get_vals_from_indeces(temp_index, list_of_lists)
#                 if '' not in temp_val:
#                     temp_list[index] = temp_index
#                     index += 1
#                 else:
#                     temp_queue_list = list_of_lists[:n] + list_of_lists[n + 1:]
#                     if temp_queue_list not in queue:
#                         queue.append(temp_queue_list)
#
#         while None in temp_list:
#             temp_list.remove(None)
#         list_of_indexes = temp_list
#
#     for l in queue:
#         combinations += get_combos(l, length)
#
#     for i, ind in enumerate(list_of_indexes):
#         # print(self.get_combo_from_indeces(ind, list_of_lists))
#         combinations.append(get_vals_from_indeces(ind, list_of_lists))
#     # print("List of indexes: ", list_of_indexes)
#     # print("List of combos: ", combinations)
#
#     return combinations


# # list_of_lists = [['a', 'b'], ['c', ''], ['d', 'e'], ['f', 'g']]
# list_of_lists = [['a', 'b'], ['1', ''], ['e', 'f'], ['g', 'h']]
# print(get_combos(list_of_lists, 3))
#


test_builder()



# print(get_vals_from_indeces([1, 0, 1, 0], list_of_lists))