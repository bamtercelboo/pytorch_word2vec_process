# coding=utf-8

import random
import os
import sys
import numpy as np
import math
import multiprocessing as mu


def read_word_feat(path_word_vector, path_feat_vector):
    feat_vec = {}
    word_vec = {}
    word_list = []
    print("reading feat vectors from file......")
    now_line = 0
    for line in open(path_feat_vector, encoding="UTF-8"):
        now_line += 1
        feat_vec[line.strip().split()[0]] = line.strip().split()[1:]
        sys.stdout.write("\rHandling with the {} line".format(now_line))
    print("\nFinished")

    print("reading word vectors from file......")
    now_line = 0
    for line in open(path_word_vector, encoding="UTF-8"):
        now_line += 1
        word_vec[line.strip().split()[0]] = line.strip().split()[1:]
        word_list.append(line.strip().split()[0])
        sys.stdout.write("\rHandling with the {} line".format(now_line))
    print("\nFinished")
    return word_list, word_vec, feat_vec


def handle_word(word, word_vec):
    if word in word_vec:
        word_float = [float(i) for i in word_vec[word]]
        word_numpy = np.array(word_float)
    return word_numpy


def handle_feat(word, feat_vec):
    # print(word)
    vector = 0
    feat_count = 0
    word = "<" + word + ">"
    for feat_num in range(3, 7):
        for i in range(0, len(word) - feat_num + 1):
            # feat = "S@" + str(feat_num) + "#" + word[i:(i + feat_num)]
            feat = word[i:(i + feat_num)]
            if feat.strip() in feat_vec:
                # print(feat.strip(), feat_vec[feat.strip()])
                feat_count += 1
                list_float = [float(i) for i in feat_vec[feat.strip()]]
                vector = np.array(vector) + np.array(list_float)

    if isinstance(vector, np.ndarray):
        vector /= feat_num
        return vector, feat_num
    else:
        return vector, feat_num


def cal_error(sample_number, sample_k, word_vec, feat_vec):
    print("calculate error......")
    euclidean_avg = []
    # sample_number_tqdm = tqdm.trange(sample_number)
    for sample_num in range(sample_number):
        sys.stdout.write("\rHandling with the {}/{} sample in {}".format(sample_num, sample_number, sample_k))
        # sample_number_tqdm.set_description("Process:" + str(sample_k))
        sample_word_list = random.sample(word_list, sample_k)
        # print(sample_word_list)
        # sample_word_list_tqdm = tqdm.tqdm(sample_word_list)
        Euclidean = []
        b = []
        for sample_word in sample_word_list:
            # print(sample_word)
            # sample_word_list_tqdm.set_description("Processing......")
            vec_word = handle_word(sample_word, word_vec)
            vec_feat, feat_num = handle_feat(sample_word, feat_vec)
            euc = (vec_word - vec_feat) ** 2
            Euclidean.append(euc.tolist())
            b.append(np.sum(euc.tolist()))
        # a = np.sum(Euclidean)
        # c = np.sum(b)
        euclidean_avg.append(np.sum(Euclidean))
            # # print(euc)
            # Euclidean.append(np.sum(euc.tolist()))
        # euclidean_avg.append(Euclidean)
    error_avg = np.sum(euclidean_avg) / len(euclidean_avg)
    return error_avg


if __name__ == "__main__":
    path_word_vector = "./enwiki.emb.source.small"
    path_feat_vector = "./enwiki.emb.feature.small"
    # path_word_vector = "/data/mszhang/ACL2017-Word2Vec/experiments-v0/subword/enwiki.emb.source"
    # path_feat_vector = "/data/mszhang/ACL2017-Word2Vec/experiments-v0/subword/enwiki.emb.feature"
    path_result = "./suda_error_result_subword.txt"
    word_list, word_vec, feat_vec = read_word_feat(path_word_vector=path_word_vector, path_feat_vector=path_feat_vector)

    if os.path.exists(path_result):
        os.remove(path_result)

    list_sample_k = [100, 500, 1000, 3000, 5000, 8000, 10000]
    # list_sample_k_tqdm = tqdm.tqdm(list_sample_k)
    file = open(path_result, mode="w", buffering=1)
    file.writelines(["sample_number", " ", "sample_k", " ", "error_avg", "\n"])
    for sample_k in list_sample_k:
        # list_sample_k_tqdm.set_description("Processing:")
        error_avg = cal_error(1000, int(sample_k), word_vec, feat_vec)
        file.writelines([str(1000), "    ", str(sample_k), "     ", str(error_avg.round(6)), "\n"])
        print("\nThe result is {}, {}, {}".format(1000, sample_k, error_avg.round(6)))
    file.close()
    


