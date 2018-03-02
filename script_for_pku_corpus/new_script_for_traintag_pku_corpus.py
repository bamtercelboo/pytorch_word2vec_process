# @Author : bamtercelboo
# @Datetime : 2018/2/26 19:09
# @File : script_for_pku_corpus.py
# @Last Modify Time : 2018/2/26 19:09
# @Contact : bamtercelboo@{gmail.com, 163.com}

"""
    FILE :  script_for_pku_corpus.py
    FUNCTION : None
"""

import sys
import os
# import unichr
import re
import chardet
from idna import unichr
from langconv import *


def read_pku_train_corpus(pku_z_corpus=None):
    print("Reading Z File......")
    z_corpus = {}
    now_line = 0
    with open(pku_z_corpus, encoding="UTF-8") as f:
        for line in f:
            now_line += 1
            sys.stdout.write("\rhandling with {} line.".format(now_line))
            # print(line)
            # if now_line == 1000:
            #     break
            if line == "\n":
                continue
            line = strQ2B(line)
            line = cht_to_chs(line)
            # print("line strQ2B", line)
            new_line = handle_sentence(line)
            z_corpus["flag" + new_line.replace(" ", "")] = line.strip("\n")
    print("\nRead Z File Finished")
    return z_corpus


def handle_sentence(line=None):
    line = line.replace("\n", "").split("  ")
    new_line = ""
    for word in line:
        if word == "":
            continue
        if word[:word.find("/")] == "":
            new_line += (word[:word.find("/") - 1])
        else:
            new_line += (word[:word.find("/")])
    return new_line


# 转换繁体到简体
def cht_to_chs(line):
    line = Converter('zh-hans').convert(line)
    line.encode('utf-8')
    return line


# 转换简体到繁体
def chs_to_cht(line):
    line = Converter('zh-hant').convert(line)
    line.encode('utf-8')
    return line


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


def read_pku_corpus(pku_corpus=None):
    print("Reading File......")
    word_dict = {}
    now_line = 0
    with open(pku_corpus, encoding="UTF-8") as f:
        for line in f:
            now_line += 1
            sys.stdout.write("\rhandling with {} line.".format(now_line))
            line = strQ2B(line)
            line = cht_to_chs(line)
            word_dict["flag" + line.replace("\n", "").replace(" ", "")] = line.strip("\n")
            # word_dict[line.replace("\n", "")] = line.strip("\n")
            # word_dict[str(now_line) + "  " + line.replace("\n", "").replace(" ", "")] = line.strip("\n")
    print("\nRead File Finished")
    return word_dict


def handle_data(z_corpus=None, corpus_dict=None, save_corpus=None, save_untag_corpus=None):
    print("Handling with data......")
    if os.path.exists(save_untag_corpus):
        os.remove(save_untag_corpus)
    if os.path.exists(save_corpus):
        os.remove(save_corpus)
    file = open(save_corpus, encoding="UTF-8", mode="w")
    file_untag = open(save_untag_corpus, encoding="UTF-8", mode="w")
    all_line = len(corpus_dict)
    for index, line in enumerate(corpus_dict):
        sys.stdout.write("\rhandling with {} line, all {} lines.".format((index + 1), all_line))
        # if line.replace(" ", "") in z_corpus:
        # print("line", line)
        if line in z_corpus:
            file.writelines(z_corpus[line])
            file.write("\n")
        else:
            file_untag.writelines(corpus_dict[line])
            file_untag.write("\n")
    file.close()
    file_untag.close()
    print("\nHandle Data Finished")


if __name__ == "__main__":
    print("script for pku corpus")
    pku_z_corpus_file = "./data/pku/pku.train.utf8"
    pku_corpus = "./data/pku/pku.split.train"
    save_corpus = "./data/pku_train_tag/pku.split.train.traintag.txt"
    save_untag_corpus = "./data/pku_train_tag/pku.split.train.trainuntag.txt"

    z_corpus = read_pku_train_corpus(pku_z_corpus=pku_z_corpus_file)

    corpus_dict = read_pku_corpus(pku_corpus=pku_corpus)

    handle_data(z_corpus=z_corpus, corpus_dict=corpus_dict, save_corpus=save_corpus, save_untag_corpus=save_untag_corpus)


