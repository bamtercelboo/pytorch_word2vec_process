

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


def read_tagged_file(tagged_file=None):
    print("Reading tagged_file File......")
    tagged_dict = {}
    now_line = 0
    with open(tagged_file, encoding="UTF-8") as f:
        for line in f:
            now_line += 1
            sys.stdout.write("\rhandling with {} line.".format(now_line))
            # if now_line == 10000:
            #     break
            line = strQ2B(line)
            line = cht_to_chs(line)
            line = line.strip().split(" ")
            if len(line) != 2:
                continue
            tagged_dict[line[0]] = line[1]

    print("\nRead Tagged File Finished")
    return tagged_dict


def tag_corpus(tagged_dict=None, untagged_file=None, save_tagged_file=None):
    print("tagging corpus......")
    if os.path.exists(save_tagged_file):
        os.remove(save_tagged_file)
    file = open(save_tagged_file, encoding="UTF-8", mode="w")
    now_line = 0
    with open(untagged_file, encoding="UTF-8") as f:
        for line in f:
            now_line += 1
            sys.stdout.write("\rhandling with {} line.".format(now_line))
            line = strQ2B(line)
            line = cht_to_chs(line)
            new_line = ""
            line = line.strip().split("  ")
            for word in line:
                if word in tagged_dict:
                    word += ("/" + tagged_dict[word])
                    word += "  "
                    new_line += word
            if new_line == "":
                continue
            file.writelines(new_line[:-2])
            file.write("\n")
    file.close()
    print("\nTagged Corpus Finished.")


if __name__ == "__main__":
    print("tag pku test corpus")
    tagged_file = "./data/pku/pku.test.utf8"
    untagged_file = "./data/pku/pku.test.a2b"
    save_tagged_file = "./data/pku_tag/pku.test.a2b.tag.txt"

    tagged_dict = read_tagged_file(tagged_file=tagged_file)
    tag_corpus(tagged_dict=tagged_dict, untagged_file=untagged_file, save_tagged_file=save_tagged_file)




