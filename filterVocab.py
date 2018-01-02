import sys
import os
d = {}
path_word_vector = "./converted_word_CR.txt"
path_fullVocab = "./fullVocab.txt"
path_filtedVectors = "./filtedVectors.txt"
# for line in open(sys.argv[1], 'r'):
for line in open(path_fullVocab, 'r'):
    # print(line)
    d[line.strip()] = 0

if os.path.exists(path_filtedVectors):
    os.remove(path_filtedVectors)

file = open(path_filtedVectors, "w")
for line in open(path_word_vector):
    _, par, word = line.strip().split()[0].partition("W@")
    if par is not "W@":
        continue
    if word in d:
        file.write(line.replace("W@", ""))
        print(line.strip())
file.close()

