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


def read_pku_z_corpus(pku_z_corpus=None):
    print("Reading Z File......")
    z_corpus = {}
    now_line = 0
    with open(pku_z_corpus, encoding="UTF-8") as f:
        for line in f:
            now_line += 1
            sys.stdout.write("\rhandling with {} line.".format(now_line))
            # print(line)
            # if now_line == 100:
            #     break
            line = strQ2B(line)
            line = cht_to_chs(line)
            if line == "\n":
                continue
            # print("line strQ2B", line)
            new_line = handle_sentence(line)
            z_corpus[new_line.replace(" ", "")] = line[(line.find("  ") + 2):].strip("\n")
            # z_corpus[new_line.replace(" ", "")] = line.strip("\n")
    print("\nRead Z File Finished")
    return z_corpus


def handle_sentence(line=None):
    line = line.replace("\n", "").split("  ")
    new_line = ""
    for word in line:
        if word == "" or line.index(word) == 0:
            continue
        if word[:word.find("/")] == "":
            new_line += (word[:word.find("/") - 1])
        else:
            new_line += (word[:word.find("/")])
    return new_line


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
            word_dict[line.replace("\n", "").replace(" ", "")] = line.strip("\n")
    print("\nRead File Finished")
    return word_dict


def handle_data(z_corpus=None, corpus_dict=None, pku_untag_corpus_tagged=None,
                pku_untag_corpus_tagged_from=None, pku_untag_corpus_untag=None):
    print("Handling with data......")
    if os.path.exists(pku_untag_corpus_tagged_from):
        os.remove(pku_untag_corpus_tagged_from)
    if os.path.exists(pku_untag_corpus_tagged):
        os.remove(pku_untag_corpus_tagged)
    if os.path.exists(pku_untag_corpus_untag):
        os.remove(pku_untag_corpus_untag)
    file = open(pku_untag_corpus_tagged, encoding="UTF-8", mode="w")
    file_untag = open(pku_untag_corpus_untag, encoding="UTF-8", mode="w")
    file_from = open(pku_untag_corpus_tagged_from, encoding="UTF-8", mode="w")
    all_line = len(corpus_dict)
    for index, line in enumerate(corpus_dict):
        sys.stdout.write("\rhandling with {} line, all {} lines.".format((index + 1), all_line))
        found = False
        for index_1, z_line in enumerate(z_corpus):
            if line[:10] == z_line[:10]:
                found = True
                file_from.writelines(z_corpus[z_line])
                file_from.write("\n")
                tagged_line = ""
                new_line = corpus_dict[line].split("  ")
                new_z_line = z_corpus[z_line].split("  ")
                new_z_line = new_z_line[(line.find("  ") + 2):]
                # for
                break
        if found is False:
            file_untag.writelines(corpus_dict[line])
            file_untag.write("\n")
    file.close()
    file_untag.close()
    file_from.close()
    print("\nHandle Data Finished")


def read_pku_corpus_del(pku_corpus=None, pku_untag_corpus_del=None):
    print("Reading File......")
    word_dict = {}
    now_line = 0
    if os.path.exists(pku_untag_corpus_del):
        os.remove(pku_untag_corpus_del)
    file = open(pku_untag_corpus_del, encoding="UTF-8", mode="w")
    with open(pku_corpus, encoding="UTF-8") as f:
        for line in f:
            now_line += 1
            sys.stdout.write("\rhandling with {} line.".format(now_line))
            line = strQ2B(line)
            line = cht_to_chs(line)
            if line.find("1998") != -1:
                line = line[:line.find("1998")]
                line += "\n"
            file.writelines(line)
            # file.write("\n")
    print("\nRead File Finished")
    return word_dict


if __name__ == "__main__":
    print("script for pku untag corpus")
    pku_z_corpus_file = "./data/pku/863corpus(含z标记）.txt"
    # pku_z_corpus_file = "./data/pku/863corpus_small.txt"
    pku_untag_corpus = "./data/pku_tag/pku.split.train.863untag_del.txt"
    # pku_untag_corpus_del = "./data/pku_tag/pku.split.train.863untag_del.txt"
    pku_untag_corpus_tagged = "./data/pku_tag/pku.split.dev.863untag.tagged.txt"
    pku_untag_corpus_tagged_from = "./data/pku_tag/pku.split.dev.863untag.tagged_from.txt"
    pku_untag_corpus_untag = "./data/pku_tag/pku.split.dev.863untag.untag.txt"

    # corpus_dict = read_pku_corpus_del(pku_corpus=pku_untag_corpus, pku_untag_corpus_del=pku_untag_corpus_del)

    corpus_dict = read_pku_corpus(pku_untag_corpus)

    z_corpus = read_pku_z_corpus(pku_z_corpus=pku_z_corpus_file)

    handle_data(z_corpus=z_corpus, corpus_dict=corpus_dict, pku_untag_corpus_tagged=pku_untag_corpus_tagged,
                pku_untag_corpus_tagged_from=pku_untag_corpus_tagged_from, pku_untag_corpus_untag=pku_untag_corpus_untag)


