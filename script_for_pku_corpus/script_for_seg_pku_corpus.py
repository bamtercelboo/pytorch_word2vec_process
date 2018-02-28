# @Author : bamtercelboo
# @Datetime : 2018/2/28 12:44
# @File : script_for_seg_pku_corpus.py
# @Last Modify Time : 2018/2/28 12:44
# @Contact : bamtercelboo@{gmail.com, 163.com}

"""
    FILE :  script_for_seg_pku_corpus.py
    FUNCTION : None
"""

import os
import sys


def clean_pku_corpus_for_seg(pku_cleaned_del_space_tag=None, pku_seg_corpus=None):
    if os.path.exists(pku_seg_corpus):
        os.remove(pku_seg_corpus)
    file = open(pku_seg_corpus, encoding="UTF-8", mode="w")
    now_line = 0
    with open(pku_cleaned_del_space_tag, encoding="UTF-8") as f:
        for line in f:
            now_line += 1
            sys.stdout.write("\rhandling with {} line.".format(now_line))
            # print(line)
            line = line.strip().split(" ")
            tag_line = ""
            for word in line:
                if word.find("_") == -1:
                    continue
                word = word[:word.find("_")]
                word += " "
                tag_line += word
            file.writelines(tag_line[:-1] + "\n")
    file.close()
    print("\nHandle Finished.")
    file.close()


def clean_pku_corpus_for_seg_none_gold(pku_seg_gold_corpus=None, pku_seg_none_gold_corpus=None):
    if os.path.exists(pku_seg_none_gold_corpus):
        os.remove(pku_seg_none_gold_corpus)
    file = open(pku_seg_none_gold_corpus, encoding="UTF-8", mode="w")
    now_line = 0
    with open(pku_seg_gold_corpus, encoding="UTF-8") as f:
        for line in f:
            now_line += 1
            sys.stdout.write("\rhandling with {} line.".format(now_line))
            line = line.replace(" ", "")
            file.writelines(line)
    file.close()
    print("\nHandle Finished.")
    file.close()


if __name__ == "__main__":
    print("cleaning pku seg corpus")

    # pku_cleaned_del_space_tag = "./data/seg/pku_corpus_spilit_cleaned_del_space_tag/863corpus_train_cleaned_del_space_tag.txt"
    # pku_seg_corpus = "./data/seg/pku_seg_corpus/863corpus_seg_train.txt"
    # clean_pku_corpus_for_seg(pku_cleaned_del_space_tag=pku_cleaned_del_space_tag,
    #                          pku_seg_corpus=pku_seg_corpus)

    pku_seg_gold_corpus = "./data/seg/pku_seg_corpus/863corpus_seg_train.txt"
    pku_seg_none_gold_corpus = "./data/seg/pku_seg_none_gold_corpus/863corpus_seg_none_gold_train.txt"
    clean_pku_corpus_for_seg_none_gold(pku_seg_gold_corpus=pku_seg_gold_corpus,
                                       pku_seg_none_gold_corpus=pku_seg_none_gold_corpus)

