# @Author : bamtercelboo
# @Datetime : 2018/1/23 12:00
# @File : filterVocab_suda_richfeat_source_feat_1.py
# @Last Modify Time : 2018/1/23 12:00
# @Contact : bamtercelboo@{gmail.com, 163.com}

"""
    FILE :  filterVocab_suda_richfeat_source_feat_1.py
    FUNCTION : inv  --- source
               oov  --- feat
"""


import os
import sys
import numpy as np


def read_similar_data(path_similar_data=None):
    print("Reading File from {}".format(path_similar_data))
    data_dict = set()
    with open(path_similar_data, encoding="UTF-8") as f:
        for line in f:
            # data_dict[line.strip()] = 0
            data_dict.add(line.strip())
    f.close()
    print("Read File Finished.")
    return data_dict


def read_feat(path_feat_vector=None):
    feat_dict = {}
    print("Reading Feature Vectors From {}".format(path_feat_vector))
    now_line = 0
    with open(path_feat_vector, encoding="UTF-8") as file:
        for line in file:
            now_line += 1
            sys.stdout.write("\rHandling with the {} line".format(now_line))
            feat_dict[line.strip().split()[0]] = line.strip().split()[1:]
        print("\nReading Feature Finished")
    file.close()
    return feat_dict


def read_source(path_source_vector=None):
    source_dict = {}
    print("Reading Source Vectors From {}".format(path_source_vector))
    now_line = 0
    with open(path_source_vector, encoding="UTF-8") as file:
        for line in file:
            now_line += 1
            sys.stdout.write("\rHandling with the {} line".format(now_line))
            source_dict[line.strip().split()[0]] = line.strip().split()[1:]
        print("\nReading Source Finished")
    file.close()
    return source_dict


def read_sorted_corpus(path_sorted_corpus=None, ratio=1.0):
    print("Reading Sorted Corpus From {}".format(path_sorted_corpus))
    corpus_dict = {}
    with open(path_sorted_corpus, encoding="UTF-8") as f:
        now_line = 0
        for line in f:
            now_line += 1
            sys.stdout.write("\rHandling with the {} line".format(now_line))
            line = line.strip().split(" ")
            window_dict = {}
            for i in range(0, len(line) - 2, 2):
                if i > (((len(line) - 2) / 2) * ratio):
                    break
                window_dict[line[i + 2]] = int(line[i + 3])
            window_dict["count"] = int(line[1])
            corpus_dict[line[0]] = window_dict
        f.close()
    print("\nRead Sorted Corpus Finished")
    return corpus_dict


def word_n_gram(word=None, feat_embedding_dict=None):
    # print("n-gram")
    feat_embedding = 0
    feat_count = 0
    word = "<" + word + ">"
    for feat_num in range(3, 7):
        for i in range(0, len(word) - feat_num + 1):
            feat = word[i:(i + feat_num)]
            if feat.strip() in feat_embedding_dict:
                feat_count += 1
                list_float = [float(i) for i in feat_embedding_dict[feat.strip()]]
                feat_embedding = np.array(feat_embedding) + np.array(list_float)

    return feat_embedding, feat_count


def context_n_gram(word=None, corpus_dict=None, feat_embed_dict=None):
    word_context_vector = 0
    F_num = 0
    count_word = 1
    if word in corpus_dict:
        count_word = corpus_dict[word]["count"]
        for word_context_feat in corpus_dict[word]:
            if word_context_feat in feat_embed_dict:
                count_context = corpus_dict[word][word_context_feat]
                list_float = [float(i) for i in feat_embed_dict[word_context_feat.strip()]]
                F_num += count_context
                word_context_vector = np.array(word_context_vector) + int(count_context) * np.array(list_float)
    return word_context_vector, F_num, count_word


def write_embed(file=None, word=None, word_embed=None):
    file.write(word + " ")
    for vec in word_embed.tolist():
        file.write(str(round(vec, 6)) + " ")
    file.write("\n")


def handle_source_feat(data_dict=None, feat_dict=None, source_dict=None, corpus_dict=None, path_filtedVectors=None):
    print("Handling Feature......")
    if os.path.exists(path_filtedVectors):
        os.remove(path_filtedVectors)
    file = open(path_filtedVectors, encoding="UTF-8", mode="w")

    for index, word in enumerate(data_dict):
        sys.stdout.write("\rHandling with the {} word in d.".format(index + 1))

        source_word_count = 0
        source_word = 0
        if word in source_dict:
            source_word_count += 1
            source_word = np.array([float(i) for i in source_dict[word]])
            write_embed(file=file, word=word, word_embed=source_word)
        else:
            feat_sum_embedding, feat_ngram_num = word_n_gram(word=word, feat_embedding_dict=feat_dict)
            if not isinstance(feat_sum_embedding, np.ndarray):
                # if the word no n-gram in feature, replace with zero
                feat_sum_embedding = np.array(list([0] * 100))
                feat_ngram_num = 1
            #  context n-gram
            word_context_vector, F_num, count_word = context_n_gram(word=word, corpus_dict=corpus_dict,
                                                                    feat_embed_dict=feat_dict)
            # calculate
            feat_sum_embedding = feat_sum_embedding / (feat_ngram_num + F_num / count_word)
            word_context_vector = word_context_vector / (count_word * feat_ngram_num + F_num)
            word_context_ngram_embed = feat_sum_embedding + word_context_vector
            write_embed(file=file, word=word, word_embed=word_context_ngram_embed)
    file.close()
    print("\nHandle Feature Finished")


if __name__ == "__main__":
    # path_similar_data = "./Data/fullVocab.txt"
    # path_feat_vector = "./Embedding/enwiki.emb.feature.small"
    # path_source_vector = "./Embedding/enwiki.emb.feature.small"
    # path_sorted_corpus = "./Embedding/enwiki-20150112_text_handled_stastic_small.extracted.txt"
    # path_filtedVectors = "./Embedding/aa.txt"

    # path_similar_data = "./Data/fullVocab.txt"
    # path_feat_vector = "/home/lzl/mszhang/suda_file0120/file/file0120/richfeat/enwiki.emb.feature"
    # path_sorted_corpus = "/home/lzl/mszhang/suda_file0120/corpus/word_similar/filter_corpus_richfeat0120_stastic_sorted_similar.txt"
    # path_filtedVectors = "./suda_0120/richfeat/suda_richfeat0120_filtedVectors_featall.txt"

    path_similar_data = "./Data/fullVocab.txt"
    path_feat_vector = "/data/mszhang/ACL2017-Word2Vec/experiments-final/for-liuzonglin/file0120/richfeat/enwiki.emb.feature"
    path_source_vector = "/data/mszhang/ACL2017-Word2Vec/experiments-final/for-liuzonglin/file0120/richfeat/enwiki.emb.source"
    path_sorted_corpus = "/data/mszhang/ACL2017-Word2Vec/experiments-final/for-liuzonglin/file0120/richfeat/enwiki-20150112_text_context_ngram_allcorpus_stastic_similar_handled_sorted/enwiki-20150112_text_context_ngram_allcorpus_stastic_similar_handled_sorted.txt"
    path_filtedVectors = "./suda_0120/richfeat/suda_richfeat0120_filtedVectors_source_featall_1.txt"

    data_dict = read_similar_data(path_similar_data=path_similar_data)
    feat_dict = read_feat(path_feat_vector=path_feat_vector)
    source_dict = read_source(path_source_vector=path_source_vector)
    corpus_dict = read_sorted_corpus(path_sorted_corpus=path_sorted_corpus, ratio=1.0)
    handle_source_feat(data_dict=data_dict, feat_dict=feat_dict, source_dict=source_dict, corpus_dict=corpus_dict,
                       path_filtedVectors=path_filtedVectors)
