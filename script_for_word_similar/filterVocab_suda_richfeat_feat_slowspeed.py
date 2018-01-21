# @Author : bamtercelboo
# @Datetime : 2018/1/13 15:36
# @File : filterVocab_suda_richfeat_feat_slowspeed.py
# @Last Modify Time : 2018/1/13 15:36
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
                # window_dict = {}
                window_dict = {}
                for win_word in line_list[1:]:
                    if win_word not in window_dict:
                        window_dict[win_word] = int(1)
                    else:
                        window_dict[win_word] += 1
                window_dict["count"] = int(1)
                # window_dict = dict(sorted(window_dict.items(), key=lambda t: t[1], reverse=True))
                word_dict[word] = window_dict
            else:
                word_dict[word]["count"] += int(1)
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
        word_dict[word] = dict(sorted(word_dict[word].items(), key=lambda t: t[1], reverse=True))
        file.write(word + " " + str(word_dict[word]["count"]))
        for word_value in word_dict[word]:
            file.write(" " + word_value + " " + str(word_dict[word][word_value]))
        file.write("\n")
    file.close()


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


def read_data(path_data_stastic=None, freq=1, highfreq=1):
    word_list = []
    word_dict = {}
    with open(path_data_stastic, encoding="UTF-8") as f:
        now_line = 0
        for line in f:
            now_line += 1
            sys.stdout.write("\rHandling with the {} line".format(now_line))
            line = line.strip().split(" ")
            window_dict = {}
            for i in range(0, len(line) - 2, 2):
                # if i > highfreq:
                #     break
                if i > (((len(line) - 2) / 2) * 0.3):
                    break
                window_dict[line[i + 2]] = int(line[i + 3])
                # if int(line[i + 3]) >= freq:
                #     window_dict[line[i + 2]] = int(line[i + 3])
            window_dict["count"] = int(line[1])
            word_dict[line[0]] = window_dict
        f.close()
    print("Read Finished.")
    return word_dict


def handle_feat_to_small(d=None, vec=None, path_feat=None, save_small_feat_path=None):
    if os.path.exists(save_small_feat_path):
        os.remove(save_small_feat_path)

    file = open(save_small_feat_path, "w")

    for index, word in enumerate(d):
        sys.stdout.write("\rHandling with the {} word in d.".format(index + 1))
        for feat_num in range(3, 7):
            for i in range(0, len(word) - feat_num + 1):
                feat = word[i:(i + feat_num)]
                with open(path_feat, encoding="UTF-8") as f:
                    for line in f:
                        if feat == line.strip().split(" ")[0]:
                            file.writelines(line)
                            break
    f.close()
    file.close()


def handle_feat_to_small_speed(d=None, vec=None, path_feat=None, save_small_feat_path=None):
    if os.path.exists(save_small_feat_path):
        os.remove(save_small_feat_path)

    file = open(save_small_feat_path, "w", encoding="UTF-8")

    for index, word in enumerate(d):
        sys.stdout.write("\rHandling with the {} word in d.".format(index + 1))
        for feat_num in range(3, 7):
            for i in range(0, len(word) - feat_num + 1):
                feat = word[i:(i + feat_num)]
                if feat.strip() in vec:
                    file.write(str(feat))
                    for str_vec in vec[feat.strip()]:
                        file.write(" " + str_vec)
                    file.write("\n")
    now_line = 0
    for f_feat in vec:
        now_line += 1
        sys.stdout.write("\rHandling with the {} line in vec.".format(now_line))
        if f_feat[0] == "F":
            file.write(str(f_feat))
            for str_vec in vec[f_feat.strip()]:
                file.write(" " + str_vec)
            file.write("\n")
    file.close()


def handle_feat(d=None, vec=None, word_dict=None, path_filtedVectors=None):
    # print(vec)
    if os.path.exists(path_filtedVectors):
        os.remove(path_filtedVectors)

    file = open(path_filtedVectors, "w")

    for index, word in enumerate(d):
        sys.stdout.write("\rHandling with the {} word in d.".format(index + 1))
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
                    count_win = word_dict[word[1: len(word) - 1]][word_win_feat]
                    # if count_win < 50:
                    #     continue
                    list_float = [float(i) for i in vec[word_win_feat.strip()]]
                    F_num += count_win
                    # print("count_win", count_win)
                    window_vector = np.array(window_vector) + int(count_win) * np.array(list_float)
                    # print(window_vector)
            window_vector = window_vector / (count_word * feat_num + F_num)
        if feat_contains is True:
            vector = vector / (feat_num + F_num / count_word)
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


def handle_feat_slowspeed(d=None, vec=None, word_dict_path=None, path_filtedVectors=None):
    # print(vec)
    if os.path.exists(path_filtedVectors):
        os.remove(path_filtedVectors)

    file = open(path_filtedVectors, "w")

    for index, word in enumerate(d):
        sys.stdout.write("\rHandling with the {} word in d.".format(index + 1))
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

        # copy with the windows size feature
        word_dict = {}
        with open(word_dict_path, encoding="UTF-8") as f:
            for line_word in f:
                line_word = line_word.strip().split(" ")
                if line_word[0] == word[1: len(word) - 1]:
                    window_dict = {}
                    for i in range(0, len(line_word) - 2, 2):
                        # if i > highfreq:
                        #     break
                        # if i > (((len(line_word) - 2) / 2) * 0.3):
                        #     break
                        window_dict[line_word[i + 2]] = int(line_word[i + 3])
                        # if int(line[i + 3]) >= freq:
                        #     window_dict[line[i + 2]] = int(line[i + 3])
                    window_dict["count"] = int(line_word[1])
                    word_dict[line_word[0]] = window_dict
                    break
                # word_dict[word[1: len(word) - 1]] = line_word[1:]
                # break
        f.close()
        # print(word)
        # print(word_dict)
        window_vector = 0
        F_num = 0
        count_word = 1
        if word[1: len(word) - 1] in word_dict:
            count_word = word_dict[word[1: len(word) - 1]]["count"]
            for word_win_feat in word_dict[word[1: len(word) - 1]]:
                if word_win_feat in vec:
                    count_win = word_dict[word[1: len(word) - 1]][word_win_feat]
                    list_float = [float(i) for i in vec[word_win_feat.strip()]]
                    F_num += count_win
                    window_vector = np.array(window_vector) + int(count_win) * np.array(list_float)
            window_vector = window_vector / (count_word * feat_num + F_num)
        if feat_contains is True:
            vector = vector / (feat_num + F_num / count_word)

        vec_all = window_vector + vector
        # print(vec_all)
        # if vec_all is float(0):
        #     continue
        if isinstance(vec_all, np.ndarray):
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

    # path_feat_vector = "./enwiki.emb.feature.small"
    # windows_size = 5
    #
    # path_data = "/data/mszhang/ACL2017-Word2Vec/data/enwiki-20150112_text.txt"
    # path_feat_vector = "/data/mszhang/ACL2017-Word2Vec/experiments-v0/richfeat/enwiki.emb.feature"
    # path_fullVocab = "./fullVocab.txt"
    # path_filtedVectors = "./suda_richfeat/suda_richfeat_filtedVectors_feat.txt"
    # windows_size = 5

    # copy with the fullvocab
    path_fullVocab = "./fullVocab.txt"
    d = {}
    for line in open(path_fullVocab, 'r'):
        d["<" + line.strip() + ">"] = 0

    # copy with the corpus
    # print("Handling data step one......")
    # path_data = "/data/mszhang/ACL2017-Word2Vec/data/enwiki-20150112_text.txt"
    # path_data = "./enwiki-20150112_text_small_50.txt"
    # save_step1_path = "./enwiki-20150112_text_small.handled.txt"
    # handle_data_step1(path=path_data, save_path=save_step1_path, windows_size=windows_size, d=d)
    # print("Handle data step one Finished")

    # print("Handling data two one......")
    # path_handled = "./enwiki-20150112_text_small.handled.2.txt"
    # handle_data_step2()
    # print("Handle data step two Finished")

    # path_handled = "/data/mszhang/ACL2017-Word2Vec/data/enwiki-20150112_text_handled.txt"
    # path_write = "/data/mszhang/ACL2017-Word2Vec/data/enwiki-20150112_text_handled_stastic.txt"
    # path_handled = "./enwiki-20150112_text_small.handled.2.sorted.txt"
    # path_write = "./suda_data.txt"
    # handle_data_step3(path=path_handled, path_write=path_write)

    # copy with the feature vector
    # path_feat_vector = "/data/mszhang/ACL2017-Word2Vec/experiments-v0/richfeat/enwiki.emb.feature"
    # path_feat_vector = "/home/lzl/mszhang/richfeat/richfeat/enwiki.emb.feature_handled.txt"

    # handle feature

    # path_feat_vector = "./enwiki.emb.feature.small"
    # save_small_feat_path = "./suda_rich.txt"
    # path_feat_vector = "/home/lzl/mszhang/richfeat/richfeat/enwiki.emb.feature"
    # save_small_feat_path = "/home/lzl/mszhang/richfeat/richfeat/enwiki.emb.feature_handled.txt"
    # handle_feat_to_small(d=d, path_feat=path_feat_vector, save_small_feat_path=save_small_feat_path)
    # handle_feat_to_small_speed(d=d, vec=vec, path_feat=path_feat_vector, save_small_feat_path=save_small_feat_path)

    # path_data_stastic = "./enwiki-20150112_text_handled_stastic_small.txt"
    # path_data_stastic = "/home/lzl/mszhang/data-enwiki/file/enwiki-20150112_text_handled_stastic.txt"

    # path_data_stastic = "/data/mszhang/ACL2017-Word2Vec/data/enwiki-20150112_text_handled_stastic.txt"
    # print("reading data......")
    # word_dict = read_data(path_data_stastic=path_data_stastic_sorted, freq=50, highfreq=200)
    # word_dict = read_data(path_data_stastic=path_data_stastic_sorted)

    # path_feat_vector = "/home/lzl/mszhang/richfeat0113/file/enwiki.emb.feature_handled.txt"
    path_feat_vector = "./enwiki.emb.feature.small"
    vec = read_feat(path_feat_vector=path_feat_vector, release_mem=True)
    print("Handling feature......")
    # path_data_stastic_sorted = "/home/lzl/mszhang/data-enwiki/file/enwiki-20150112_text_handled_stastic_sorted.txt"
    path_data_stastic_sorted = "./enwiki-20150112_text_handled_stastic_small.txt"
    path_filtedVectors = "./suda_richfeat0113_filtedVectors_feat.txt"
    # handle_feat(d=d, vec=vec, word_dict=word_dict, path_filtedVectors=path_filtedVectors)
    handle_feat_slowspeed(d=d, vec=vec, word_dict_path=path_data_stastic_sorted, path_filtedVectors=path_filtedVectors)
    print("\nHandle Finished")







