# @Author : bamtercelboo
# @Datetime : 2018/3/2 23:08
# @File : new_script_for_ungold_pku_corpus.py
# @Last Modify Time : 2018/3/2 23:08
# @Contact : bamtercelboo@{gmail.com, 163.com}

"""
    FILE :  new_script_for_ungold_pku_corpus.py
    FUNCTION : None
"""

import os
import sys


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


if __name__ == "__main__":
    print("ungolg corpus")
    gold_corpus = "./data/pku_corpus_cleaned_all/pku.split.train.863tag.cleaned.all.txt"
    none_gold_corpus = "./data/pku_corpus_cleaned_all_ungold/pku.split.train.863tag.cleaned.all.ungold.txt"
    clean_pku_corpus_space_gold(gold_corpus=gold_corpus, none_gold_corpus=none_gold_corpus)