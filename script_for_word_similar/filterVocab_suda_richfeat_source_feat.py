# @Author : bamtercelboo
# @Datetime : 2018/1/11 14:16
# @File : filterVocab_suda_richfeat_source_feat.py
# @Last Modify Time : 2018/1/11 14:16
# @Contact : bamtercelboo@{gmail.com, 163.com}

import os
import sys
import numpy as np


def handle_data_step1(path=None, save_path=None, windows_size=0, d=None):
    if os.path.exists(save_path):
        os.remove(save_path)
    file = open(save_path, mode="w", encoding="UTF-8")
    with open(path, encoding="UTF-8") as f:
        now_line = 0
        for line in f.readlines():
            now_line += 1
            sys.stdout.write("\rhandling with {} line.".format(now_line))
            word_list = line.strip().split(" ")
            for word_index, word in enumerate(word_list):
                word_d = "<" + word + ">"
                # print(word_d, word_index)
                if word_d not in d:
                    continue
                file.write(word+" ")
                for i in range(windows_size):
                    if (word_index - i) > 0:
                        file.write("F-" + str(i + 1) + "@" + word_list[word_index - i - 1]+" ")
                for i in range(windows_size):
                    if (word_index + i) < len(word_list) - 1:
                        file.write("F" + str(i + 1) + "@" + word_list[word_index + i + 1] + " ")
                file.write("\n")
    f.close()
    file.close()


def handle_data_step2(path=None):
    print("filed sorted")


def handle_data_step3(path=None, path_write=None):
    print("Handling data stastic...... ")
    with open(path, encoding="UTF-8") as f:
        list_d = []
        word_dict = {}
        # window_dict = {}
        now_line = 0
        for line in f:
            now_line += 1
            sys.stdout.write("\rhandling with {} line.".format(now_line))
            line_list = line.strip("\n").strip(" ").split(" ")
            # print(line_list)
            word = line_list[0]
            if word not in word_dict:
                window_dict = {}
                for win_word in line_list[1:]:
                    window_dict[win_word] = 1
                window_dict["count"] = 1
                word_dict[word] = window_dict
            else:
                word_dict[word]["count"] += 1
                for win_word in line_list[1:]:
                    if win_word in word_dict[word]:
                        word_dict[word][win_word] += 1
                    else:
                        word_dict[word][win_word] = 1
        print("\nFinished")
        f.close()
    file = open(path_write, mode="w", encoding="UTF-8")
    print("Writing file......")
    now_word = 0
    len_word_dict = len(word_dict)
    for word in word_dict:
        now_word += 1
        sys.stdout.write("\rwriting {} word, all {} words.".format(now_word, len_word_dict))
        file.write(word + " " + str(word_dict[word]["count"]))
        for word_value in word_dict[word]:
            file.write(" " + word_value + " " + str(word_dict[word][word_value]))
        file.write("\n")
    file.close()
    # return word_dict


def read_feat(path_feat_vector=None, release_mem=False):
    vec = {}
    print("reading feature vectors from file......")
    now_line = 0
    # file = open(path_feat_vector, encoding="UTF-8")
    with open(path_feat_vector, encoding="UTF-8") as file:
        for line in file:
            now_line += 1
            sys.stdout.write("\rHandling with the {} line".format(now_line))
            vec[line.strip().split()[0]] = line.strip().split()[1:]
        print("\nFinished")
    file.close()
    return vec


def read_source(path_source_vector=None):
    source = {}
    print("reading source vector from file......")
    now_line = 0
    with open(path_source_vector, encoding="UTF-8") as file:
        for line in file:
            now_line += 1
            sys.stdout.write("\rHandling with the {} line.".format(now_line))
            source[line.strip().split(" ")[0]] = line.strip().split(" ")[1:]
        print("\nFinished")
    file.close()
    return source


def read_data(path_data_stastic=None):
    word_list = []
    word_dict = {}
    with open(path_data_stastic, encoding="UTF-8") as f:
        now_line = 0
        for line in f.readlines():
            now_line += 1
            sys.stdout.write("\rHandling with the {} line".format(now_line))
            line = line.strip().split(" ")
            window_dict = {}
            for i in range(0, len(line) - 2, 2):
                window_dict[line[i + 2]] = int(line[i + 3])
            window_dict["count"] = int(line[1])
            word_dict[line[0]] = window_dict
        f.close()
    print("Read Finished.")
    return word_dict


def handle_feat(d=None, vec=None, word_dict=None, source=None, path_filtedVectors=None):
    # print(vec)
    if os.path.exists(path_filtedVectors):
        os.remove(path_filtedVectors)

    file = open(path_filtedVectors, "w")

    for index, word in enumerate(d):
        sys.stdout.write("\rHandling with the {} word in d.".format(index + 1))

        source_vector = 0
        source_count = 0
        if word[1:len(word) - 1] in source:
            source_count += 1
            list_source = [float(i) for i in source[word[1:len(word)-1]]]
            source_vector = np.array(list_source) + np.array(source_vector)

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
        # if feat_contains is False:
        #     continue
        # vector = vector / feat_num

        # copy with the windows size feature
        window_vector = 0
        F_num = 0
        count_word = 1
        if word[1: len(word) - 1] in word_dict:
            count_word = word_dict[word[1: len(word) - 1]]["count"]
            # print("count_word", count_word)
            for word_win_feat in word_dict[word[1: len(word) - 1]]:
                # print(word_win_feat)
                if word_win_feat in vec:
                    list_float = [float(i) for i in vec[word_win_feat.strip()]]
                    count_win = word_dict[word[1: len(word) - 1]][word_win_feat]
                    F_num += count_win
                    # print("count_win", count_win)
                    window_vector = np.array(window_vector) + int(count_win) * np.array(list_float)
                    # print(window_vector)
            window_vector = window_vector / (count_word * (feat_num + 1) + F_num)
            # window_vector = (window_vector + source_vector) / (count_word * feat_num + F_num)
        if feat_contains is True:
            vector = vector / ((feat_num + 1) + (F_num / count_word))
        # print("window_vector", window_vector)
        # print("vector", vector)
        vec_all = window_vector + vector
        if vec_all is 0:
            continue
        # print(vec_all)
        vector_str = [str(round(i, 6)) for i in vec_all.tolist()]
        vector_str.insert(0, word[1:len(word) - 1])
        # print(vector_str)

        for i in vector_str:
            file.write(i)
            file.write(" ")
        file.write("\n")
    file.close()


if __name__ == "__main__":

    # copy with the fullvocab
    path_fullVocab = "./fullVocab.txt"
    d = {}
    for line in open(path_fullVocab, 'r'):
        d["<" + line.strip() + ">"] = 0

    # copy with the feature vector
    # path_feat_vector = "/data/mszhang/ACL2017-Word2Vec/experiments-v0/richfeat/enwiki.emb.feature"
    path_feat_vector = "./enwiki.emb.feature.small"
    vec = read_feat(path_feat_vector=path_feat_vector, release_mem=True)

    # path_source_vector = "./enwiki.emb.source_small"
    path_source_vector = "./enwiki.emb.source_small"
    source = read_source(path_source_vector=path_source_vector)

    path_data_stastic = "./enwiki-20150112_text_handled_stastic_small.txt"
    # path_data_stastic = "/data/mszhang/ACL2017-Word2Vec/data/enwiki-20150112_text_handled_stastic.txt"
    print("reading data......")
    word_dict = read_data(path_data_stastic=path_data_stastic)

    print("Handling feature......")
    path_filtedVectors = "./suda_richfeat_filtedVectors_source_feat.txt"
    handle_feat(d=d, vec=vec, word_dict=word_dict, source=source, path_filtedVectors=path_filtedVectors)
    print("\nHandle Finished")







