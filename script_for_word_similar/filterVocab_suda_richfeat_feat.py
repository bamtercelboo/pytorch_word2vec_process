# @Author : bamtercelboo
# @Datetime : 2018/1/9 18:22
# @File : filterVocab_richfeat_feat.py.py
# @Last Modify Time : 2018/1/9 18:22
# @Contact : bamtercelboo@{gmail.com, 163.com}

import os
import sys
import numpy as np


def handle_data(path=None, windows_size=0):
    word_dict = {}
    line_list = []
    print("Reading File To List......")
    file = open(path, encoding="UTF-8")
    # file_all_lines = len(file.readlines())
    now_line = 0
    for line in file.readlines():
        now_line += 1
        sys.stdout.write("\rhandling with {} line, all  lines.".format(now_line))
        line_list.append(line.strip().split(" "))
    file.close()
    print("\nStarting Handling Data......")
    line_list_len = len(line_list)
    for id, word_list in enumerate(line_list):
        sys.stdout.write("\rhandling with {} list, all {} lists.".format(id + 1, line_list_len ))
        for word_index, word in enumerate(word_list):
            if word not in word_dict:
                #
                window_dict = {}
                # word_dict[word]["count"] = 1
                for i in range(windows_size):
                    if (word_index - i) > 0:
                        window_dict["F-".join(str(i + 1)).join("@").join(word_list[word_index - i - 1])] = 1
                        # window_dict[os.]
                for i in range(windows_size):
                    if (word_index + i) < len(word_list) - 1:
                        # window_dict["F" + str(i + 1) + "@" + word_list[word_index + i + 1]] = 1
                        window_dict["F".join(str(i + 1)).join("@").join(word_list[word_index + i + 1])] = 1
                window_dict["count"] = 1
                word_dict[word] = window_dict
            else:
                # word in word_dict
                word_dict[word]["count"] += 1
                for i in range(windows_size):
                    if (word_index - i) > 0:
                        # str_word = "F-" + str(i + 1) + "@" + word_list[word_index - i - 1]
                        str_word = "F-".join(str(i + 1)).join("@").join(word_list[word_index - i - 1])
                        if str_word in word_dict[word]:
                            word_dict[word][str_word] += 1
                        else:
                            word_dict[word][str_word] = 1
                for i in range(windows_size):
                    if (word_index + i) < len(word_list) - 1:
                        # str_word = "F" + str(i + 1) + "@" + word_list[word_index + i + 1]
                        str_word = "F".join(str(i + 1)).join("@").join(word_list[word_index + i + 1])
                        if str_word in word_dict[word]:
                            word_dict[word][str_word] += 1
                        else:
                            word_dict[word][str_word] = 1
    return word_dict


def handle_feat(d=None, vec=None, word_dict=None, path_filtedVectors=None):
    # print(vec)
    if os.path.exists(path_filtedVectors):
        os.remove(path_filtedVectors)

    file = open(path_filtedVectors, "w")

    for word in d:
        # word = "<techdo>"
        # copy with the n-gram
        vector = 0
        feat_count = 0
        feat_contains = False
        for feat_num in range(3, 7):
            for i in range(0, len(word) - feat_num + 1):
                feat = word[i:(i + feat_num)]
                if feat.strip() in vec:
                    # print(feat.strip(), vec[feat.strip()])
                    feat_count += 1
                    feat_contains = True
                    list_float = [float(i) for i in vec[feat.strip()]]
                    vector = np.array(vector) + np.array(list_float)
        # print(vector)
        if feat_contains is False:
            continue
        vector = vector / feat_num

        # copy with the windows size feature
        window_vector = 0
        if word[1: len(word) - 1] in word_dict:
            count_word = word_dict[word[1: len(word) - 1]]["count"]
            print("count_word", count_word)
            for word_win_feat in word_dict[word[1: len(word) - 1]]:
                print(word_win_feat)
                if word_win_feat in vec:
                    list_float = [float(i) for i in vec[word_win_feat.strip()]]
                    count_win = word_dict[word[1: len(word) - 1]][word_win_feat]
                    # print("count_win", count_win)
                    window_vector = np.array(window_vector) + int(count_win) * np.array(list_float)
                    print(window_vector)
            window_vector = window_vector / count_word

        # print("window_vector", window_vector)
        # print("vector", vector)
        vec_all = window_vector + vector
        print(vec_all)
        vector_str = [str(round(i, 6)) for i in vec_all.tolist()]
        vector_str.insert(0, word[1:len(word) - 1])
        # print(vector_str)

        for i in vector_str:
            file.write(i)
            file.write(" ")
        file.write("\n")
    file.close()


if __name__ == "__main__":
    # path_data = "./enwiki-20150112_text_small_50.txt"
    # path_feat_vector = "./enwiki.emb.feature.small"
    # path_fullVocab = "./fullVocab.txt"
    # path_filtedVectors = "./suda_aaa_filtedVectors_feat.txt"
    # windows_size = 5

    path_data = "/data/mszhang/ACL2017-Word2Vec/data/enwiki-20150112_text.txt"
    path_feat_vector = "/data/mszhang/ACL2017-Word2Vec/experiments-v0/richfeat/enwiki.emb.feature"
    path_fullVocab = "./fullVocab.txt"
    path_filtedVectors = "./suda_richfeat/suda_richfeat_filtedVectors_feat.txt"
    windows_size = 5

    # copy with the fullvocab
    d = {}
    for line in open(path_fullVocab, 'r'):
        d["<" + line.strip() + ">"] = 0

    # copy with the corpus
    print("Handling data......")
    word_dict = handle_data(path=path_data, windows_size=windows_size)
    print("Handle data Finished")

    # copy with the feature vector
    vec = {}
    print("reading feature vectors from file......")
    now_line = 0
    for line in open(path_feat_vector, encoding="UTF-8"):
        now_line += 1
        sys.stdout.write("\rHandling with the {} line".format(now_line))
        vec[line.strip().split()[0]] = line.strip().split()[1:]
    print("\nFinished")
    print(vec)
    # handle feature
    print("Handling feature......")
    handle_feat(d=d, vec=vec, word_dict=word_dict, path_filtedVectors=path_filtedVectors)
    print("Handle Finished")






