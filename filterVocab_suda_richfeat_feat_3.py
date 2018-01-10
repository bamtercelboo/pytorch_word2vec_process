# @Author : bamtercelboo
# @Datetime : 2018/1/9 18:22
# @File : filterVocab_richfeat_feat.py.py
# @Last Modify Time : 2018/1/9 18:22
# @Contact : bamtercelboo@{gmail.com, 163.com}

import os
import sys
import gc
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
    # if release_mem is True:
    #     del file
    #     gc.collect()
    return vec


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

    # path_feat_vector = "./enwiki.emb.feature.small"
    path_fullVocab = "./fullVocab.txt"
    path_filtedVectors = "./suda_richfeat_filtedVectors_feat.txt"
    windows_size = 5
    #
    # path_data = "/data/mszhang/ACL2017-Word2Vec/data/enwiki-20150112_text.txt"
    # path_feat_vector = "/data/mszhang/ACL2017-Word2Vec/experiments-v0/richfeat/enwiki.emb.feature"
    # path_fullVocab = "./fullVocab.txt"
    # path_filtedVectors = "./suda_richfeat/suda_richfeat_filtedVectors_feat.txt"
    # windows_size = 5

    # copy with the fullvocab
    d = {}
    for line in open(path_fullVocab, 'r'):
        d["<" + line.strip() + ">"] = 0

    # copy with the corpus
    print("Handling data step one......")
    # path_data = "/data/mszhang/ACL2017-Word2Vec/data/enwiki-20150112_text.txt"
    path_data = "./enwiki-20150112_text_small_50.txt"
    # save_step1_path = "./enwiki-20150112_text_small.handled.txt"
    # handle_data_step1(path=path_data, save_path=save_step1_path, windows_size=windows_size, d=d)
    print("Handle data step one Finished")

    print("Handling data two one......")
    path_handled = "./enwiki-20150112_text_small.handled.2.txt"
    # handle_data_step2()
    print("Handle data step two Finished")

    # path_handled = "/data/mszhang/ACL2017-Word2Vec/data/enwiki-20150112_text_handled.txt"
    # path_write = "/data/mszhang/ACL2017-Word2Vec/data/enwiki-20150112_text_handled_stastic.txt"
    path_handled = "./enwiki-20150112_text_small.handled.2.sorted.txt"
    path_write = "./suda_data.txt"
    handle_data_step3(path=path_handled, path_write=path_write)

    # copy with the feature vector
    # path_feat_vector = "/data/mszhang/ACL2017-Word2Vec/experiments-v0/richfeat/enwiki.emb.feature"
    path_feat_vector = "./enwiki.emb.feature.small"
    # vec = read_feat(path_feat_vector=path_feat_vector, release_mem=True)
    # handle feature
    print("Handling feature......")
    # handle_feat(d=d, vec=vec, word_dict=word_dict, path_filtedVectors=path_filtedVectors)
    print("Handle Finished")






