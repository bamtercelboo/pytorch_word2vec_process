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


if __name__ == "__main__":
    print("cleaning pku corpus")
    pku_corpus = "./data/pku_corpus_spilit/863corpus_train.txt"
    pku_cleaned_corpus = "./data/pku_corpus_spilit_cleaned/863corpus_train_cleaned.txt"
    clean_pku_corpus(pku_corpus=pku_corpus, pku_cleaned_corpus=pku_cleaned_corpus)


