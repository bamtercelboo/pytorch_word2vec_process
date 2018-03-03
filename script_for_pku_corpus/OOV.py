import os
import sys
from idna import unichr
from langconv import *

def oov(train_file=None,dev_file=None,truth_file=None):

    now_line = 0
    train_words = set()
    with open(train_file, encoding="UTF-8") as f:
        for line in f:
            temp = line.split(' ')
            for i in temp:
                word = i.split('_')

                if (word[0] not in train_words):
                    train_words.add(word[0])
        f.close()
    count = 0
    # print("train words set")
    # print(train_words.__len__())

    dev_words = set()
    dev_words_num = 0
    with open(dev_file, encoding="UTF-8") as file:
        for line in file:
            temp = line.split(' ')
            for i in temp:
                word = i.split('_')
                if (word[0] not in train_words):
                    dev_words_num+=1
    file.close()
    #print("dev words set")
    #print(dev_words.__len__())


    truth_words = set()
    truth_words_num = 0
    with open(truth_file, encoding="UTF-8") as file:
        for line in file:
            temp = line.split(' ')
            for i in temp:
                word = i.split('_')
                if (word[0] not in train_words):
                    truth_words_num+=1
    file.close()
    # print("truth words set")
    # print(truth_words.__len__())
    print("dev oov")
    print(dev_words_num)
    #print((dev_words-train_words).__len__())
    print("truth oov")
    print(truth_words_num)
    #print((truth_words-train_words).__len__())

if __name__ == "__main__":
    print("clean  all corpus")
    oov("./data/Finial_pku_data/pku_corpus_cleaned_all/pku.split.train.863tag.cleaned.all.txt",
        "./data/Finial_pku_data/pku_corpus_cleaned_all/pku.split.dev.863tag.cleaned.all.txt",
        "./data/Finial_pku_data/pku_corpus_cleaned_all/pku.split.test.863tag.cleaned.all.txt")