# @Author : bamtercelboo
# @Datetime : 2018/1/9 10:29
# @File : filterVocab_suda_source&feat.py.py
# @Last Modify Time : 2018/1/9 10:29
# @Contact : bamtercelboo@{gmail.com, 163.com}

import sys
import os
import numpy as np

path_word_vector = "./enwiki.emb.feature.small"
path_feat_vector = "./enwiki.emb.source.small"
path_fullVocab = "./fullVocab.txt"
path_filtedVectors = "./suda_filtedVectors_source_feat.txt"

# path_word_vector = "/home/lzl/mszhang/subword/subword/eng.word.model"
# path_feat_vector = "/home/lzl/mszhang/subword/subword/eng.feat.model"
# path_fullVocab = "./fullVocab.txt"
# path_filtedVectors = "./subword/subword_filtedVectors_source_feat.txt"


def handle_word(word):
    # print(word)
    if word in word_vec:
        # print("aaaaaaaaa", word_vec[word])
        word_float = [float(i) for i in word_vec[word]]
        word_numpy = np.array(word_float)
    return word_numpy


def handle_feat(word):
    vector = 0
    feat_count = 0
    for feat_num in range(3, 7):
        for i in range(0, len(word) - feat_num + 1):
            # feat = "S@" + str(feat_num) + "#" + word[i:(i + feat_num)]
            feat = word[i:(i + feat_num)]
            if feat.strip() in feat_vec:
                print(feat.strip(), feat_vec[feat.strip()])
                feat_count += 1
                # feat_contains = True
                list_float = [float(i) for i in feat_vec[feat.strip()]]
                vector = np.array(vector) + np.array(list_float)

    if isinstance(vector, np.ndarray):
        return vector, feat_num
    else:
        return None, feat_num


def write(vec_numpy):
    vec_list = vec_numpy.tolist()
    vector_str = [str(round(i, 6)) for i in vec_list]
    vector_str.insert(0, vocab_word)
    print(vector_str)
    for i in vector_str:
        file.write(i)
        file.write(" ")
    file.write("\n")
    # print("eeeeeeee", vec_list)


d = {}
for line in open(path_fullVocab, 'r'):
    d["<" + line.strip() + ">"] = 0

feat_vec = {}
print("reading feat vectors from file......")
for line in open(path_feat_vector, encoding="UTF-8"):
    feat_vec[line.strip().split()[0]] = line.strip().split()[1:]
print("Finished")

word_vec = {}
print("reading word vectors from file......")
for line in open(path_word_vector, encoding="UTF-8"):
    word_vec[line.strip().split()[0]] = line.strip().split()[1:]
print("Finished")

# print(vec)
if os.path.exists(path_filtedVectors):
    os.remove(path_filtedVectors)

file = open(path_filtedVectors, "w")

for vocab in d:
    print(vocab)
    vocab_word = vocab[1:len(vocab) - 1]
    print(vocab_word)
    count = 0
    word_numpy = None
    feat_numpy = None
    # word
    if vocab_word in word_vec:
        count += 1
        word_numpy = handle_word(vocab_word)

    # feat
    feat_numpy, feat_count = handle_feat(vocab)
    if isinstance(feat_numpy, np.ndarray):
        count += feat_count
    else:
        feat_numpy = None

    if word_numpy is not None and feat_numpy is not None:
        print("word_numpy is not None and feat_numpy is not None")
        vec_numpy = word_numpy + feat_numpy
        vec_numpy /= count
        write(vec_numpy)
    elif feat_numpy is not None and word_numpy is None:
        print("feat_numpy is not None and word_numpy is None")
        vec_numpy = feat_numpy / feat_count
        write(vec_numpy)
    elif feat_numpy is None and word_numpy is not None:
        print("feat_numpy is None and word_numpy is not None")
        vec_numpy = word_numpy
        write(vec_numpy)
file.close()
