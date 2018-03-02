
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


def handle_word_tag_contact(line=None):
    line = line.strip().split(" ")
    new_line = ""
    for word in line:
        if word.rfind("/") == -1:
            continue
        word = word[:word.rfind("/")] + "_" + word[(word.rfind("/") + 1):] + " "
        new_line += word
    return new_line[:-1]


def clean_corpus(uncleaned_corpus=None, cleaned_corpus=None):
    print("cleaning corpus......")
    if os.path.exists(cleaned_corpus):
        os.remove(cleaned_corpus)
    file = open(cleaned_corpus, encoding="UTF-8", mode="w")
    now_line = 0
    with open(uncleaned_corpus, encoding="UTF-8") as f:
        for line in f:
            now_line += 1
            sys.stdout.write("\rhandling with {} line.".format(now_line))
            # clean 全角 ---> 半角，繁体 ---> 简体
            line = strQ2B(line)
            line = cht_to_chs(line)
            # clean "  " ---> " "
            line = line.replace("  ", " ")
            # clean 1_4_m
            line = handle_word_tag_contact(line)
            # clean / ---> _
            line = line.replace("/", "-")
            file.writelines(line)
            file.write("\n")
    file.close()
    print("\nClean Corpus Finished.")


if __name__ == "__main__":
    print("clean pku all corpus")

    # uncleaned_corpus = "./data/pku_tag/pku.test.a2b.tag.txt"
    # cleaned_corpus = "./data/pku_tag_cleaned/pku.test.a2b.tag.cleaned.txt"
    #
    uncleaned_corpus = "./data/pku_tag/pku.split.test.863tag.txt"
    cleaned_corpus = "./data/pku_tag_cleaned/pku.split.test.863tag.cleaned.txt"
    clean_corpus(uncleaned_corpus=uncleaned_corpus, cleaned_corpus=cleaned_corpus)


