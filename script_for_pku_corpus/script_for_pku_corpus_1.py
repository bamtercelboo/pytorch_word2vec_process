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
import re
import chardet


def read_pku_z_corpus(pku_z_corpus=None, corpus_dict=None, save_corpus=None, save_untag_corpus=None):
    print("Reading File......")
    write_line = []
    now_line = 0
    if os.path.exists(save_corpus):
        os.remove(save_corpus)
    file = open(save_corpus, encoding="UTF-8", mode="w")
    file_untag = open(save_untag_corpus, encoding="UTF-8", mode="w")
    untag_corpus = {}
    with open(pku_z_corpus, encoding="UTF-8") as f:
        for line in f:
            now_line += 1
            sys.stdout.write("\rhandling with {} line.".format(now_line))
            # print(line)
            if now_line == 1000:
                break
            write_line.append(line)
            new_line = handle_sentence(line)
            # print("new_line", new_line)
            # untag_corpus[] = line[(line.find("  ") + 2):-1]
            if new_line in corpus_dict:
                if new_line == "":
                    continue
                # print("new_line", new_line)
                # print("write", line)
                file.writelines(line[(line.find("  ") + 2):-1])
                file.write("\n")
    file.close()
    print("Read File Finished")
    return untag_corpus


# def handle_sentence(line=None):
#     # new_line = line.replace("/", "")
#     # re.sub("^/.*?  $", "")
#     # new_line = re.sub("/", "", line)
#     new_line = re.sub(r"/?{u}", "", line)
#     return new_line


def handle_sentence(line=None):
    line = line.replace("\n", "").split("  ")
    new_line = ""
    for word in line:
        # print(line.index(word))
        if word == "" or line.index(word) == 0:
            continue
        new_line += (word[:word.find("/")])
        # if line.index(word) != (len(line) - 1):
        #     new_line += "  "
    # print()
    return new_line


def read_pku_corpus(pku_corpus=None):
    print("Reading File......")
    word_dict = {}
    # word_dict = []
    now_line = 0
    with open(pku_corpus, encoding="UTF-8") as f:
        for line in f:
            now_line += 1
            sys.stdout.write("\rhandling with {} line.".format(now_line))
            # print("wewewewe", line.replace("\n", ""))
            # word_dict.append(line.replace("\n", "").replace(" ", ""))
            word_dict[line.replace("\n", "").replace(" ", "")] = line
    print("Read File Finished")
    return word_dict


def handle_untag(corpus_dict=None, untag_corpus=None, save_untag_corpus=None):
    if os.path.exists(save_untag_corpus):
        os.remove(save_untag_corpus)
    file_untag = open(save_untag_corpus, encoding="UTF-8", mode="w")
    for l in corpus_dict:
        if l in untag_corpus:
            continue
        file_untag.writelines(untag_corpus[l])
        file_untag.write("\n")
    file_untag.close()


if __name__ == "__main__":
    print("script for pku corpus")
    pku_z_corpus_file = "./data/pku_corpus/863corpus(含z标记）.txt"
    pku_corpus = "./data/pku_corpus/pku.split.train2"
    save_corpus = "./pku.split.train2.tag.txt"
    save_untag_corpus = "./pku.split.train2.untag.txt"
    corpus_dict = read_pku_corpus(pku_corpus=pku_corpus)
    untag_corpus = read_pku_z_corpus(pku_z_corpus=pku_z_corpus_file, corpus_dict=corpus_dict, save_corpus=save_corpus,
                                     save_untag_corpus=save_untag_corpus)

    handle_untag(corpus_dict=corpus_dict, untag_corpus=untag_corpus, save_untag_corpus=save_untag_corpus)


