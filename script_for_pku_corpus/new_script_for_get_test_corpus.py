# @Author : bamtercelboo
# @Datetime : 2018/3/2 15:47
# @File : new_script_for_get_test_corpus.py
# @Last Modify Time : 2018/3/2 15:47
# @Contact : bamtercelboo@{gmail.com, 163.com}

"""
    FILE :  new_script_for_get_test_corpus.py
    FUNCTION : None
"""


import os
import sys
from idna import unichr
from langconv import *


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


def read_file(corpus=None):
    print("Read Corpus From {}".format(corpus))
    exist_corpus = {}
    now_line = 0
    with open(corpus, encoding="UTF-8") as f:
        for line in f:
            now_line += 1
            sys.stdout.write("\rhandling with {} line.".format(now_line))
            # if now_line == 1000:
            #     break
            # print(line)
            line = strQ2B(line)
            line = cht_to_chs(line)
            line = line.replace("  ", "")
            line = line.replace("\n", "")
            exist_corpus[line] = "Existed"
    print("\nRead Corpus Finished.")
    return exist_corpus


def get_corpus(train_dict=None, dev_dict=None, corpus_file=None, save_getted_corpus=None, count=None):
    print("Getting Test Corpus From {}".format(corpus_file))
    if os.path.exists(save_getted_corpus):
        os.remove(save_getted_corpus)
    file = open(save_getted_corpus, encoding="UTF-8", mode="w")
    now_line = 0
    test_count = 0
    with open(corpus_file, encoding="UTF-8") as f:
        for line in f:
            now_line += 1
            sys.stdout.write("\rhandling with {} line.".format(now_line))
            if now_line <= 122711:
                continue
            if test_count == count:
                break
            line = strQ2B(line)
            line = cht_to_chs(line)
            if line == "\n":
                continue
            str_line = line
            str_line = str_line.replace("\n", "").split("  ")
            new_line = ""
            for word in str_line[1:]:
                if word.find("/") == -1:
                    continue
                word = word[:word.find("/")]
                new_line += word
            if (new_line not in train_dict) and (new_line not in dev_dict):
                test_count += 1
                file.writelines(line[(line.find("  ") + 2):])
    file.close()
    print("\nGet Corpus Finished.")


if __name__ == "__main__":
    print("Get Test Corpus From 863Corpus")
    train_file = "./data/pku/pku.split.train"
    dev_file = "./data/pku/pku.split.dev"
    corpus_file = "./data/pku/863corpus(含z标记）.txt"
    save_getted_corpus = "./data/pku/pku.split.test"
    count = 2500
    train_dict = read_file(corpus=train_file)
    dev_dict = read_file(corpus=dev_file)
    get_corpus(train_dict=train_dict, dev_dict=dev_dict, corpus_file=corpus_file,
               save_getted_corpus=save_getted_corpus, count=count)



