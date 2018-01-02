import sys
import os
import numpy as np
d = {}
# path_word_vector = "./eng.feat.model.small"
# path_fullVocab = "./fullVocab.txt"
# path_filtedVectors = "./filtedVectors_feat.txt"

path_word_vector = "/home/lzl/mszhang/subword/subword/eng.feat.model"
path_fullVocab = "./fullVocab.txt"
path_filtedVectors = "./subword/subword_filtedVectors_feat.txt"

for line in open(path_fullVocab, 'r'):
    d["<" + line.strip() + ">"] = 0
# print(d)

vec = {}
print("reading feat vectors from file......")
for line in open(path_word_vector, encoding="UTF-8"):
    vec[line.strip().split()[0]] = line.strip().split()[1:]
print("Finished")
# print(vec)
if os.path.exists(path_filtedVectors):
    os.remove(path_filtedVectors)

file = open(path_filtedVectors, "w")

for word in d:
# word = "<the>"
    vector = 0
    feat_count = 0
    feat_contains = False
    for feat_num in range(3, 7):
        for i in range(0, len(word) - feat_num + 1):
            feat = "S@" + str(feat_num) + "#" + word[i:(i+feat_num)]
            # for line in open(path_word_vector, encoding="UTF-8"):
                # print(line)
            if feat.strip() in vec:
                print(feat.strip(), vec[feat.strip()])
                feat_count += 1
                feat_contains = True
                list_float = [float(i) for i in vec[feat.strip()]]
                vector = np.array(vector) + np.array(list_float)
    # print(vector)
    if feat_contains is False:
        continue
    vector = vector / feat_num
    vector_str = [str(round(i, 6)) for i in vector.tolist()]
    vector_str.insert(0, word[1:len(word) -1])
    # print(vector_str)
    for i in vector_str:
        file.write(i)
        file.write(" ")
    file.write("\n")
file.close()

