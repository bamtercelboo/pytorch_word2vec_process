import sys
import os
import numpy as np

# path_word_vector = "./converted_word_MR.txt"
# path_feat_vector = "./eng.feat.model.small"
# path_fullVocab = "./fullVocab.txt"
# path_filtedVectors = "./filtedVectors_word_feat.txt"

path_word_vector = "/home/lzl/mszhang/subword/subword/eng.word.model"
path_feat_vector = "/home/lzl/mszhang/subword/subword/eng.feat.model"
path_fullVocab = "./fullVocab.txt"
path_filtedVectors = "./subword/subword_filtedVectors_word_feat.txt"


def handle_iov_word(word):
    # print(word)
    if word in word_vec:
        word_vec[word].insert(0, word)
        print(word_vec[word])
        for i in word_vec[word]:
            file.write(i)
            file.write(" ")
        file.write("\n")
        # file.write(word_vec[word])
        # print(word_vec[word])


def handle_oov_word(word):
    vector = 0
    feat_count = 0
    # feat_contains = False
    for feat_num in range(3, 7):
        for i in range(0, len(word) - feat_num + 1):
            feat = "S@" + str(feat_num) + "#" + word[i:(i + feat_num)]
            if feat.strip() in feat_vec:
                print(feat.strip(), feat_vec[feat.strip()])
                feat_count += 1
                # feat_contains = True
                list_float = [float(i) for i in feat_vec[feat.strip()]]
                vector = np.array(vector) + np.array(list_float)
    # print("rrrrrrrrrrrrrrrr", vector.__class__)
    # if vector != 0:
    if isinstance(vector, np.ndarray):
        vector = vector / feat_num
        vector_str = [str(round(i, 6)) for i in vector.tolist()]
        vector_str.insert(0, word[1:len(word) - 1])
        # print(vector_str)
        for i in vector_str:
            file.write(i)
            file.write(" ")
        file.write("\n")


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
    if vocab_word in word_vec:
        handle_iov_word(vocab_word)
    else:
        handle_oov_word(vocab)
file.close()
