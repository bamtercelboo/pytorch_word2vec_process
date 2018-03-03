# @Author : bamtercelboo
# @Datetime : 2018/3/3 18:29
# @File : new_script_for_OOV.py
# @Last Modify Time : 2018/3/3 18:29
# @Contact : bamtercelboo@{gmail.com, 163.com}

"""
    FILE :  new_script_for_OOV.py
    FUNCTION : None
"""

import sys
import os


def calculate_OOV(word_dict=None, OOV_file=None):
    print(OOV_file)
    now_line = 0
    oov_count = 0
    w_list = []
    with open(OOV_file, encoding="UTF-8") as f:
        for line in f:
            now_line += 1
            sys.stdout.write("\rhandling with {} line.".format(now_line))
            # if now_line == 1000:
            #     break
            line = line.replace("\n", "").split(" ")
            # print(line)
            for word in line:
                word = word[:word.find("_")]
                w_list.append(word)
                if word not in word_dict:
                    oov_count += 1
    print("\nCorpus sentences", now_line)
    print("Corpus words", len(w_list))
    print("OOV Coount", oov_count)


def read(train_file=None):
    print("read File")
    word_dict = {}
    word_list = []
    now_line = 0
    with open(train_file, encoding="UTF-8") as f:
        for line in f:
            now_line += 1
            sys.stdout.write("\rhandling with {} line.".format(now_line))
            # if now_line == 1000:
            #     break
            line = line.replace("\n", "").split(" ")
            # print(line)
            for word in line:
                word = word[:word.find("_")]
                word_dict[word] = 1
                word_list.append(word)
            # print(line)
    print("\nTrain sentences", now_line)
    return word_dict, word_list


if __name__ == "__main__":
    print("OOV")
    train_file = "./data/Finial_pku_data/pku_corpus_cleaned_all/pku.split.train.863tag.cleaned.all.txt"
    word_dict, word_list = read(train_file=train_file)
    print("Train words", len(word_list))
    OOV_file = "./data/Finial_pku_data/pku_corpus_cleaned_all/pku.split.test.863tag.cleaned.all.txt"
    calculate_OOV(word_dict=word_dict, OOV_file=OOV_file)

