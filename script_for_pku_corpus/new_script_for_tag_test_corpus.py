

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


def search_from_tagged_file(line=None, tagged_file=None, file_tag=None, file_untag=None):

    line_l = line.strip("\n").split("  ")
    w_line = line
    line = line.strip("\n").replace(" ", "")
    # print(line)
    line_length = len(line_l)
    tagged_dict = read(tagged_file=tagged_file, line_length=line_length)
    if line in tagged_dict:
        file_tag.writelines(tagged_dict[line])
        file_tag.write("\n")
    else:
        file_untag.writelines(w_line)
        file_untag.write("\n")


def read(tagged_file=None, line_length=None):
    tagged_dict = {}
    now_line = 0
    with open(tagged_file, encoding="UTF-8") as f:
        new_tag_line = ""
        for line_tag in f:
            now_line += 1
            # if now_line == 1000:
            #     break
            line_tag = strQ2B(line_tag)
            line_tag = cht_to_chs(line_tag)
            line_tag = line_tag.strip("\n").split(" ")
            if len(line_tag) != 2:
                continue
            line_tag = line_tag[0] + "_" + line_tag[1] + " "
            new_tag_line += line_tag
    new_tag_line = new_tag_line.split(" ")
    for i in range(len(new_tag_line) - line_length):
        tag = ""
        word = ""
        for j in range(line_length):
            # print(i, j, line_length, len(new_tag_line))
            index = j + i
            tag += (new_tag_line[index] + " ")
            word += new_tag_line[index][:new_tag_line[index].rfind("_")]
        tagged_dict[word] = tag[:-1]
    return tagged_dict


def tag_corpus(tagged_file=None, untagged_file=None, save_tagged_file=None, save_untagged_file=None):
    print("tagging corpus......")
    if os.path.exists(save_tagged_file):
        os.remove(save_tagged_file)
    if os.path.exists(save_untagged_file):
        os.remove(save_untagged_file)
    file_tag = open(save_tagged_file, encoding="UTF-8", mode="w", buffering=1)
    file_untag = open(save_untagged_file, encoding="UTF-8", mode="w", buffering=1)
    now_line = 0
    with open(untagged_file, encoding="UTF-8") as f:
        for line in f:
            now_line += 1
            # if now_line == 100:
            #     break
            sys.stdout.write("\rhandling with {} line.".format(now_line))
            if line == "\n":
                continue
            line = strQ2B(line)
            line = cht_to_chs(line)
            search_from_tagged_file(line, tagged_file, file_tag, file_untag)

    file_untag.close()
    file_tag.close()
    print("\nTagged Corpus Finished.")


if __name__ == "__main__":
    print("tag pku test corpus")
    tagged_file = "./data/pku/pku.test.utf8"
    untagged_file = "./data/pku/pku.test.a2b"
    save_tagged_file = "./data/pku_tag/pku.test.a2b.tag.txt"
    save_untagged_file = "./data/pku_tag/pku.test.a2b.untag.txt"
    tag_corpus(tagged_file=tagged_file, untagged_file=untagged_file,
               save_tagged_file=save_tagged_file, save_untagged_file=save_untagged_file)





