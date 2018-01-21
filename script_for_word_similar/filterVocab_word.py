import sys
import os
d = {}
# path_word_vector = "./converted_word_MR.txt"
# path_fullVocab = "./fullVocab.txt"
# path_filtedVectors = "./filtedVectors_word.txt"

path_word_vector = "/home/lzl/mszhang/fasttext/word.emb.vec"
path_fullVocab = "./fullVocab.txt"
path_filtedVectors = "./fasttext_filtedVectors_word.txt"

for line in open(path_fullVocab, 'r'):
    # print(line)
    d[line.strip()] = 0

if os.path.exists(path_filtedVectors):
    os.remove(path_filtedVectors)

file = open(path_filtedVectors, "w")
for line in open(path_word_vector):
    if line.strip().split()[0] in d:
        file.write(line)
        print(line.strip())
file.close()

