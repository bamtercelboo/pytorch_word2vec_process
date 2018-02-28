# @Author : bamtercelboo
# @Datetime : 2018/2/27 12:38
# @File : script_for_clean_pku_corpus.py
# @Last Modify Time : 2018/2/27 12:38
# @Contact : bamtercelboo@{gmail.com, 163.com}

"""
    FILE :  script_for_clean_pku_corpus.py
    FUNCTION : None
"""

import os
import sys
from idna import unichr


def clean_pku_corpus(pku_corpus=None, pku_cleaned_corpus=None):
    if os.path.exists(pku_cleaned_corpus):
        os.remove(pku_cleaned_corpus)
    file_cleaned = open(pku_cleaned_corpus, encoding="UTF-8", mode="w")
    now_line = 0
    with open(pku_corpus, encoding="UTF-8") as f:
        for line in f:
            now_line += 1
            sys.stdout.write("\rhandling with {} line.".format(now_line))
            line = strQ2B(line)
            line = line[(line.find("  ") + 2):]
            if line == "\n":
                continue
            judge = handle_digit(line)
            if judge is True:
                # print("judge", judge)
                continue
            # print(line)
            line = line.replace("/", "_")
            line = line.replace("_%", "")
            # print(line)
            file_cleaned.writelines(line)
    file_cleaned.close()
    print("\nHandling PKU Corpus Finished.")


def handle_digit(line=None):
    line = line.strip("\n").split("  ")
    length = len(line)
    digit = 0
    delete_flag = False
    for index, word in enumerate(line):
        word = word[:word.find("/")]
        if word.isdigit():
            digit += 1
    if (digit / length) > 0.4:
        delete_flag = True
    return delete_flag


def strQ2B(ustring):
    """全角转半角"""
    rstring = ""
    for uchar in ustring:
        inside_code = ord(uchar)
        if inside_code == 12288:                              #全角空格直接转换
            inside_code = 32
        elif (inside_code >= 65281 and inside_code <= 65374): #全角字符（除空格）根据关系转化
            inside_code -= 65248
        rstring += unichr(inside_code)
    return rstring


def clean_pku_corpus_space(pku_cleaned_corpus_del=None, pku_cleaned_corpus_del_space=None):
    if os.path.exists(pku_cleaned_corpus_del_space):
        os.remove(pku_cleaned_corpus_del_space)
    file = open(pku_cleaned_corpus_del_space, encoding="UTF-8", mode="w")
    now_line = 0
    with open(pku_cleaned_corpus_del, encoding="UTF-8") as f:
        for line in f:
            now_line += 1
            sys.stdout.write("\rhandling with {} line.".format(now_line))
            # print(line)
            line = line.replace("  ", " ")
            file.writelines(line)
    print("Handle Finished.")
    file.close()


def clean_pku_corpus_space_gold(gold_corpus=None, none_gold_corpus=None):
    if os.path.exists(none_gold_corpus):
        os.remove(none_gold_corpus)
    file = open(none_gold_corpus, encoding="UTF-8", mode="w")
    now_line = 0
    with open(gold_corpus, encoding="UTF-8") as f:
        for line in f:
            now_line += 1
            sys.stdout.write("\rhandling with {} line.".format(now_line))
            # print(line)
            line = line.strip().split(" ")
            none_gold_line = ""
            for word in line:
                word = word[:word.find("_")]
                none_gold_line += word
            print(none_gold_line)
            file.writelines(none_gold_line + "\n")
    file.close()
    print("\nHandle Finished.")
    file.close()


def clean_pku_corpus_space_tag(corpus_dev_cleaned_del_space=None, corpus_dev_cleaned_del_space_tag=None):
    if os.path.exists(corpus_dev_cleaned_del_space_tag):
        os.remove(corpus_dev_cleaned_del_space_tag)
    file = open(corpus_dev_cleaned_del_space_tag, encoding="UTF-8", mode="w")
    now_line = 0
    with open(corpus_dev_cleaned_del_space, encoding="UTF-8") as f:
        for line in f:
            now_line += 1
            sys.stdout.write("\rhandling with {} line.".format(now_line))
            # print(line)
            line = line.strip().split(" ")
            tag_line = ""
            for word in line:
                if word.find("_") == -1:
                    continue
                word += " "
                tag_line += word
            file.writelines(tag_line[:-1] + "\n")
    file.close()
    print("\nHandle Finished.")
    file.close()


if __name__ == "__main__":
    print("cleaning pku corpus")
    # pku_corpus = "./data/pku_corpus_spilit/863corpus_train.txt"
    # pku_cleaned_corpus = "./data/pku_corpus_spilit_cleaned/863corpus_train_cleaned.txt"
    # clean_pku_corpus(pku_corpus=pku_corpus, pku_cleaned_corpus=pku_cleaned_corpus)

    # pku_cleaned_corpus_del = "./data/pku_corpus_spilit_cleaned_del/863corpus_dev_cleaned_del.txt"
    # pku_cleaned_corpus_del_space = "./data/pku_corpus_spilit_cleaned_del_space/863corpus_dev_cleaned_del_space.txt"
    # clean_pku_corpus_space(pku_cleaned_corpus_del=pku_cleaned_corpus_del, pku_cleaned_corpus_del_space=pku_cleaned_corpus_del_space)

    # gold_corpus = "./data/pku_corpus_spilit_cleaned_del_space/863corpus_dev_cleaned_del_space.txt"
    # none_gold_corpus = "./data/pku_none_gold_corpus/863corpus_dev_cleaned_del_space_nonegold.txt"
    # clean_pku_corpus_space_gold(gold_corpus=gold_corpus, none_gold_corpus=none_gold_corpus)

    corpus_dev_cleaned_del_space = "./data/pku_corpus_spilit_cleaned_del_space/863corpus_dev_cleaned_del_space.txt"
    corpus_dev_cleaned_del_space_tag = "./data/pku_corpus_spilit_cleaned_del_space_tag/863corpus_dev_cleaned_del_space_tag.txt"
    clean_pku_corpus_space_tag(corpus_dev_cleaned_del_space=corpus_dev_cleaned_del_space,
                               corpus_dev_cleaned_del_space_tag=corpus_dev_cleaned_del_space_tag)


