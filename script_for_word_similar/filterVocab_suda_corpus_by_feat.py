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


def read_feat_embedding(path_feat=None):
    print("Reading Feature Embedding.......")
    feat_list = []
    with open(path_feat, encoding="UTF-8") as f:
        now_line = 0
        for line in f:
            now_line += 1
            sys.stdout.write("\rhandling with {} line.".format(now_line))
            if line[0] != "F":
                continue
            line = line.strip().split(" ")
            word_index = line[0].find("@") + 1
            word = line[0][word_index:]
            if word not in feat_list:
                feat_list.append(word)
            feat_list.append(line[0])
    f.close()
    print("\nRead Feature Finished.")
    return feat_list


def write_filter_corpus(file=None, corpus_line=None):
    for word in corpus_line:
        file.write(word + " ")
    file.write("\n")


def handle_corpus_contextFeat(path_corpus=None, feat_list=None, path_filter_corpus=None):
    print("Handleing Corpus Feature......")
    file = open(path_filter_corpus, encoding="UTF-8", mode="w")
    with open(path_corpus, encoding="UTF-8") as f:
        now_line = 0
        for line in f:
            now_line += 1
            sys.stdout.write("\rhandling with {} line.".format(now_line))
            line = line.strip().split(" ")
            if line[0] not in feat_list:
                continue
            for context in line[1:]:
                if context not in feat_list:
                    line.remove(context)
            write_filter_corpus(file=file, corpus_line=line)
    f.close()
    print("\nHandle Corpus Finished.")


if __name__ == "__main__":
    path_feat = "./enwiki.emb.feature.small_0120"
    path_corpus = "./enwiki-20150112_text.context_ngram_small_0120.txt"
    path_filter_corpus = "./enwiki-20150112_text.context_ngram_richfeat_0120.txt"

    # path_feat = "./enwiki.emb.feature.small_0120"
    # path_corpus = "./enwiki-20150112_text.context_ngram_small_0120.txt"
    # path_filter_corpus = "./enwiki-20150112_text.context_ngram_richfeat_0120.txt"

    feat_list = read_feat_embedding(path_feat=path_feat)
    handle_corpus_contextFeat(path_corpus=path_corpus, feat_list=feat_list, path_filter_corpus=path_filter_corpus)




