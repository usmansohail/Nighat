import openpyxl as pyxl
from openpyxl import worksheet
import pickle
import re


# get all the characters
def get_characters():
    # open the excel file
    file = open("dictionary.xlsx", 'rb')
    wb = pyxl.load_workbook(file)
    ws = wb.active

    lines = []
    for row in ws.iter_rows():
        if "BCI-AV#" not in str(row[0].value) and row[0].value is not None:
            lines.append((row[0].value, str(row[2].value), str(row[3].value)))

    # create dicts
    num_to_def_dict = {}
    for line in lines:
        words_non_filtered = str(line[1]).split(',')
        words_filtered = []
        # print(words_non_filtered)
        for word in words_non_filtered:
            regex = re.compile(".*?\((.*?)\)")
            remove_string = re.findall(regex, word)
            if len(remove_string) > 0:
                word = word.replace(remove_string[0], '')
                word = word.replace('(', '')
                word = word.replace(')', '')
            if len(word) > 0 and word[-1] is '_':
                word_list = list(word)
                word_list[-1] = ''
                word = "".join(word_list[:-1])
            word = word.replace('_', ' ')
            words_filtered.append(word)
        # print(words_filtered)
        num_to_def_dict[line[0]] = ()

    # "BCI-AV#"
    for i in range(1000, 1005):
        print(lines[i])

    print(lines[-1])

    dict = {}
    for line in lines:
        dict[line[0]] = line[1]

    def_dict = {}
    characters = {}
    for line in lines:
        def_dict[line[0]] = line[2]

        if " - Character" in str(line[2]):
            characters[line[0]] = [line[1], line[2]]

        if " + " in str(line[2]):
            regex = re.compile(r"\(.+\)")
            composition = str(re.findall(regex, str(line[2]).replace('\n', '')))
            composition = composition.replace('(', '')
            composition = composition.replace(')', '')
            composition = composition.replace('[', '')
            composition = composition.replace(']', '')
            composition = composition.replace('\'', '')
            #print("Comp: ", composition)
            regex_2 = re.compile(r":.*")
            remove_string = re.findall(regex_2, str(composition))
            if len(remove_string) > 0:
                composition = composition.replace(remove_string[0], '')
               # print("parts removed: ", remove_string[0])
            regex_2 = re.compile(r": .*")
            remove_string = re.findall(regex_2, str(composition))
            if len(remove_string) > 0:
                composition = composition.replace(remove_string[0], '')
               #print("parts removed: ", remove_string[0])
            if ',' in composition:
                regex = re.compile(r",\w*,*\w*,*\w*,*")
                remove_string = re.findall(regex, composition)
                for i in range(len(remove_string)):
                    composition = composition.replace(remove_string[i], '')
                    #print("remove string:", remove_string)
            print("final string: ", composition, '\n')
            if composition == "":
                print('wtf', line[0], line[1], line[2])



    print(len(characters.keys()))

    pickle.dump(characters, open("bliss_chars.p", 'wb'))


    word_to_id_dict = {}
    ambiguous_words = {}
    for key in dict.keys():
        words = str(dict[key]).split(',')
        for word in words:
            if word in word_to_id_dict.keys():
                # add it to the ambigous words dictionary
                if word in ambiguous_words.keys():
                    ambiguous_words[word].append(key)
                else:
                    ambiguous_words[word] = [key]
                    ambiguous_words[word].append(word_to_id_dict[word][0])
                word_to_id_dict[word].append(key)
                #print(word, "  ", word_to_id_dict[word])
            else:
                word_to_id_dict[word] = [key]

    print(len(word_to_id_dict.keys()))
    pickle.dump(word_to_id_dict, open("word_to_char_id.p", "wb"))
    #for key in ambiguous_words.keys():
    #    print(key, ": ", ambiguous_words[key])

    #print(len(ambiguous_words))



#bliss_dict = dict(pickle.load( open("C:/Users/Usman Sohail/Documents/CSCI-490/corpera/get_corpus_data/bliss_dict.p", 'rb')))
        #for key in bliss_dict.keys():
        #if bliss_dict[key]



get_characters()