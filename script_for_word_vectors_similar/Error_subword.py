# @Author : bamtercelboo
# @Datetime : 2018/1/25 18:50
# @File : Error_subword.py
# @Last Modify Time : 2018/1/25 18:50
# @Contact : bamtercelboo@{gmail.com, 163.com}

"""
    FILE :  Error_subword.py
    FUNCTION :

"""

import os
import sys
import random
import numpy as np


def read_source_feat(path_source_vector, path_feat_vector):
    feat_vec = {}
    source_vec = {}
    source_list = []
    print("reading feat vectors from {}".format(path_feat_vector))
    now_line = 0
    with open(path_feat_vector, encoding="UTF-8") as f:
        for line in f:
            now_line += 1
            feat_vec[line.strip().split()[0]] = line.strip().split()[1:]
            sys.stdout.write("\rHandling with the {} line".format(now_line))
    f.close()
    print("\nFinished")

    print("reading source vectors from {}".format(path_source_vector))
    now_line = 0
    with open(path_source_vector, encoding="UTF-8") as f:
        for line in f:
            now_line += 1
            source_vec[line.strip().split()[0]] = line.strip().split()[1:]
            source_list.append(line.strip().split()[0])
            sys.stdout.write("\rHandling with the {} line".format(now_line))
    f.close()
    print("\nFinished")
    return source_list, source_vec, feat_vec


def word_n_gram(word=None, feat_embedding_dict=None):
    feat_embedding = 0
    feat_count = 0
    word = "<" + word + ">"
    feat_embedding_list = []
    # print(word)
    for feat_num in range(3, 7):
        for i in range(0, len(word) - feat_num + 1):
            feat = word[i:(i + feat_num)]
            if feat.strip() in feat_embedding_dict:
                feat_count += 1
                list_float = [float(i) for i in feat_embedding_dict[feat.strip()]]
                feat_embedding_list.append(np.array(list_float))
                # feat_embedding = np.array(feat_embedding) + np.array(list_float)
    feat_embedding = np.sum(feat_embedding_list, axis=0)
    if feat_count == 0:
        feat_count = 1
    return feat_embedding, feat_count


def handle_feat(word, feat_vec):
    feat_embedding, feat_count = word_n_gram(word=word, feat_embedding_dict=feat_vec)
    feat_embedding_avg = np.divide(feat_embedding, feat_count)

    return feat_embedding_avg, feat_count


def handle_source_feat(word=None, source_embedding_dict=None, feat_embedding_dict=None):
    if word in source_embedding_dict:
        source_embedding_list = [float(i) for i in source_embedding_dict[word]]
        source_embedding = np.array(source_embedding_list)
        feat_sum_embedding, feat_ngram_num = word_n_gram(word=word, feat_embedding_dict=feat_embedding_dict)
        # word_embed = (feat_sum_embedding + source_embedding) / (1 + feat_ngram_num)
        word_embed = np.divide(np.add(feat_sum_embedding, source_embedding), np.add(1, feat_ngram_num))
        return word_embed
    else:
        feat_sum_embedding, feat_ngram_num = word_n_gram(word=word, feat_embedding_dict=feat_embedding_dict)
        if not isinstance(feat_sum_embedding, np.ndarray):
            # if the word no n-gram in feature, replace with zero
            feat_sum_embedding = np.array(list([0] * 100))
            feat_ngram_num = 1
        feat_sum_embedding_avg = np.divide(feat_sum_embedding, feat_ngram_num)
        return feat_sum_embedding_avg


def cal_error(sample_number=None, sample_k=None, source_vec=None, feat_vec=None, source_list=None):
    print("calculate error......")
    euclidean_avg = []
    for sample_num in range(sample_number):
        sys.stdout.write("\rHandling with the {}/{} sample in {}".format(sample_num, sample_number, sample_k))
        sample_word_list = random.sample(source_list, sample_k)
        Euclidean = []
        b = []
        for sample_word in sample_word_list:
            vec_feat, feat_num = handle_feat(sample_word, feat_vec)
            vec_sourcefeat = handle_source_feat(word=sample_word, source_embedding_dict=source_vec,
                                                feat_embedding_dict=feat_vec)
            euc = np.subtract(vec_feat, vec_sourcefeat) ** 2
            Euclidean.append(euc.tolist())
            b.append(np.sum(euc.tolist()))
        euclidean_avg.append(np.sum(Euclidean))
    error_avg = np.sum(euclidean_avg) / len(euclidean_avg)
    return error_avg


if __name__ == "__main__":
    path_source_vector = "./Embedding/enwiki.emb.source_small"
    path_feat_vector = "./Embedding/enwiki.emb.feature.small"
    # path_source_vector = "/data/mszhang/ACL2017-Word2Vec/experiments-final/for-liuzonglin/file0120/subword/enwiki.emb.source"
    # path_feat_vector = "/data/mszhang/ACL2017-Word2Vec/experiments-final/for-liuzonglin/file0120/subword/enwiki.emb.feature"
    path_result = "./Error_result_subword0120.txt"
    source_list, source_vec, feat_vec = read_source_feat(path_source_vector=path_source_vector, path_feat_vector=path_feat_vector)

    if os.path.exists(path_result):
        os.remove(path_result)

    list_sample_k = [100, 500, 1000, 3000, 5000, 8000, 10000]
    # list_sample_k_tqdm = tqdm.tqdm(list_sample_k)
    file = open(path_result, mode="w", buffering=1)
    file.writelines(["sample_number", " ", "sample_k", " ", "error_avg", "\n"])
    for sample_k in list_sample_k:
        # list_sample_k_tqdm.set_description("Processing:")
        error_avg = cal_error(1000, int(sample_k), source_vec, feat_vec, source_list)
        file.writelines([str(1000), "    ", str(sample_k), "     ", str(error_avg.round(6)), "\n"])
        print("\nThe result is {}, {}, {}".format(1000, sample_k, error_avg.round(6)))
    file.close()
