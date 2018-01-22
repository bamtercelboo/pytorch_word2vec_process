# @Author : bamtercelboo
# @Datetime : 2018/1/21 9:43
# @File : filterVocab_suda_corpus_by_feat.py
# @Last Modify Time : 2018/1/21 9:43
# @Contact : bamtercelboo@{gmail.com, 163.com}

"""
    FILE :  filterVocab_suda_corpus_by_feat.py
    FUNCTION : None
"""


import os
import sys
import re


# def read_feat_embedding(path_feat=None):
#     print("Reading Feature Embedding.......")
#     feat_list = []
#     with open(path_feat, encoding="UTF-8") as f:
#         now_line = 0
#         for line in f.readlines():
#             now_line += 1
#             sys.stdout.write("\rhandling with {} line.".format(now_line))
#             line = line.strip().split(" ")
#             feat_list.append(line[0][(line[0].find("@") + 1):])
#             feat_list.append(line[0])
#     f.close()
#     feat_list = list(set(feat_list))
#     print("\nRead Feature Finished.")
#     return feat_list


def read_feat_embedding(path_feat=None):
    print("Reading Feature Embedding.......")
    feat_dict = {}
    with open(path_feat, encoding="UTF-8") as f:
        now_line = 0
        for line in f.readlines():
            now_line += 1
            sys.stdout.write("\rhandling with {} line.".format(now_line))
            line = line.strip().split(" ")
            feat_dict[line[0][(line[0].find("@") + 1):]] = 0
            feat_dict[line[0]] = 0
    f.close()
    print("\nRead Feature Finished.")
    return feat_dict


def read_feat_embedding_speedup(path_feat=None):
    print("Reading Feature Embedding.......")
    feat_dict = {}
    with open(path_feat, encoding="UTF-8") as f:
        now_line = 0
        for line in f.readlines():
            now_line += 1
            line = line.strip().split(" ")
            # print(line)
            sys.stdout.write("\rhandling with {} line.".format(now_line))
            if line[0][0] != "F":
                continue
            print(line[0])
            word_index = line[0].find("@") + 1
            word = line[0][word_index:]
            # print(word)
            if word not in feat_dict:
                feat_dict[word] = 0
            feat_dict[line[0]] = 0
    f.close()
    print("\nRead Feature Finished.")
    return feat_dict


def handle_feat_embedding(feat_list=None):
    print("Handling Feature Embedding.......")
    now_line = 0
    all_line = len(feat_list)
    # print(feat_list)
    feat_F_list = []
    F = ["F"]
    for line in feat_list:
        now_line += 1
        sys.stdout.write("\rhandling with {} line, all {} lines.".format(now_line, all_line))
        if line[0] not in F:
            continue
        word_index = line.find("@") + 1
        word = line[word_index:]
        if word not in feat_F_list:
            feat_F_list.append(word)
        feat_F_list.append(line)
    print("\nHandle Feature Finished.")
    return feat_F_list


def write_filter_corpus(file=None, corpus_line=None):
    file.writelines(corpus_line)
    # for line in corpus_line:
    #     file.write(line + "\n")
    # file.write("\n")


def handle_corpus_contextFeat(path_corpus=None, feat_F_list=None, path_filter_corpus=None):
    print("Handleing Corpus Feature......")
    file = open(path_filter_corpus, encoding="UTF-8", mode="w")
    with open(path_corpus, encoding="UTF-8") as f:
        now_line = 0
        for line in f:
            now_line += 1
            sys.stdout.write("\rhandling with {} line.".format(now_line))
            line = line.strip().split(" ")
            if line[0] not in feat_F_list:
                continue
            for context in line[1:]:
                if context not in feat_F_list:
                    line.remove(context)
            line = str(line).replace("[", "").replace("]", "").replace("'", "").replace(",", " ") + "\n"
            file.writelines(line)
    f.close()
    print("\nHandle Corpus Finished.")


if __name__ == "__main__":
    path_feat = "./enwiki.emb.feature.small_0120"
    path_corpus = "./enwiki-20150112_text.context_ngram_small_0120.txt"
    path_filter_corpus = "./enwiki-20150112_text.context_ngram_richfeat_0120.txt"

    # path_feat = "/home/lzl/mszhang/suda_file0120/file/file0120/richfeat/enwiki.emb.feature"
    # path_corpus = "/home/lzl/mszhang/data-enwiki/file/enwiki-20150112_text_context_ngram_all/enwiki-20150112_text.context_ngram_all.txt"
    # path_filter_corpus = "/home/lzl/mszhang/suda_file0120/file/file0120/richfeat/filter_corpus/enwiki-20150112_text.context_ngram_filtered_richfeat_all.txt"

    # path_feat = "/data/mszhang/ACL2017-Word2Vec/experiments-final/for-liuzonglin/file0120/richfeat/enwiki.emb.feature"
    # path_corpus = "/data/mszhang/ACL2017-Word2Vec/data/save_enwiki_20150112_text_context_ngram_allcorpus/enwiki_20150112_text_context_ngram_allcorpus_sorted/enwiki-20150112_text_context_ngram_allcorpus_split_sorted_all_m"
    # path_filter_corpus = "/data/mszhang/ACL2017-Word2Vec/experiments-final/for-liuzonglin/file0120/richfeat/filter_corpus_fichfeat0120_1.txt"

    # feat_list = read_feat_embedding(path_feat=path_feat)
    feat_list = read_feat_embedding_speedup(path_feat=path_feat)
    handle_corpus_contextFeat(path_corpus=path_corpus, feat_F_list=feat_list, path_filter_corpus=path_filter_corpus)




