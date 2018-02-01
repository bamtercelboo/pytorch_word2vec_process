# @Author : bamtercelboo
# @Datetime : 2018/1/27 10:05
# @File : handle_extracted_corpus_and_sorted.py
# @Last Modify Time : 2018/1/27 10:05
# @Contact : bamtercelboo@{gmail.com, 163.com}

"""
    FILE :  handle_extracted_corpus_and_sorted.py
    FUNCTION : None
"""

import os
import sys


def handle_extracted_corpus(path_extracted_corpus=None, path_extracted_corpus_handled=None):
    if os.path.exists(path_extracted_corpus_handled):
        os.remove(path_extracted_corpus_handled)
    file = open(path_extracted_corpus_handled, encoding="UTF-8", mode="w")

    with open(path_extracted_corpus, encoding="UTF-8") as f:
        now_line = 0
        word_dict = {}
        for line in f:
            now_line += 1
            sys.stdout.write("\rHandling with the {} line.".format(now_line))
            line = line.strip().split(" ")
            if line.__len__() % 2 != 0:
                continue
            if line[0] not in word_dict:
                window_dict = {}
                for i in range(0, len(line[2:]), 2):
                    if line[i + 2] not in window_dict:
                        window_dict[line[i + 2]] = int(line[i + 3])
                    else:
                        window_dict[line[i + 2]] += int(line[i + 3])
                word_dict[line[0]] = window_dict
            else:
                # print(word_dict)
                for i in range(0, len(line[2:]), 2):
                    if line[i + 2] not in word_dict[line[0]]:
                        word_dict[line[0]][line[i + 2]] = int(line[i + 3])
                    else:
                        word_dict[line[0]][line[i + 2]] += int(line[i + 3])
    print("writing file......")
    now_word = 0
    all_word = len(word_dict)
    for k, v in word_dict.items():
        now_word += 1
        sys.stdout.write("\rHandling with the {} word, all {} words.".format(now_word, all_word))
        file.write(k + " " + str(v["count"]))
        for kv, vv in v.items():
            file.write(" " + kv + " " + str(vv))
        file.write("\n")
    print("Handle Finished")
    f.close()
    file.close()


def judge_same(judge_dict=None):
    same = False
    if len(judge_dict) == 1:
        same = True
    return same


def handle_extracted_corpus_smallmem(path_extracted_corpus=None, path_extracted_corpus_handled=None):
    if os.path.exists(path_extracted_corpus_handled):
        os.remove(path_extracted_corpus_handled)
    file = open(path_extracted_corpus_handled, encoding="UTF-8", mode="w")

    with open(path_extracted_corpus, encoding="UTF-8") as f:
        now_line = 0
        word_dict = {}
        judge_dict = {}
        for line in f:
            now_line += 1
            sys.stdout.write("\rHandling with the {} line.".format(now_line))
            line = line.strip().split(" ")
            if line.__len__() % 2 != 0:
                continue
            judge_dict[line[0]] = 1
            judge = judge_same(judge_dict)
            if judge is False:
                for k, v in word_dict.items():
                    v = dict(sorted(v.items(), key=lambda t: t[1], reverse=True))
                    file.write(k + " " + str(v["count"]))
                    for kv, vv in v.items():
                        file.write(" " + kv + " " + str(vv))
                    file.write("\n")
                judge_dict = {}
                word_dict = {}
            if line[0] not in word_dict:
                window_dict = {}
                for i in range(0, len(line[2:]), 2):
                    if line[i + 2] not in window_dict:
                        window_dict[line[i + 2]] = int(line[i + 3])
                    else:
                        window_dict[line[i + 2]] += int(line[i + 3])
                word_dict[line[0]] = window_dict
            else:
                # print(word_dict)
                for i in range(0, len(line[2:]), 2):
                    if line[i + 2] not in word_dict[line[0]]:
                        word_dict[line[0]][line[i + 2]] = int(line[i + 3])
                    else:
                        word_dict[line[0]][line[i + 2]] += int(line[i + 3])
    for k, v in word_dict.items():
        v = dict(sorted(v.items(), key=lambda t: t[1], reverse=True))
        file.write(k + " " + str(v["count"]))
        for kv, vv in v.items():
            file.write(" " + kv + " " + str(vv))
        file.write("\n")
    print("\nHandle Finished")
    f.close()
    file.close()


if __name__ == "__main__":
    # path_extracted_corpus = "./embedding/enwiki-20150112_text_context_ngram_allcorpus_stastic_similar_small.txt"
    # path_extracted_corpus_handled = "./embedding/enwiki-20150112_text_handled_stastic_small_extracted_handled.txt"

    path_extracted_corpus = "/home/lzl/mszhang/suda_file0120/extracted_sentence_corpus_sorted/extracted_Conll2003_statstic.txt"
    path_extracted_corpus_handled = "/home/lzl/mszhang/suda_file0120/extracted_sentence_corpus_sorted/extracted_Conll2003_statstic_handled_sorted.txt"

    # handle_extracted_corpus(path_extracted_corpus=path_extracted_corpus, path_extracted_corpus_handled=path_extracted_corpus_handled)
    # handle_extracted_corpus(path_extracted_corpus=path_extracted_corpus, path_extracted_corpus_handled=path_extracted_corpus_handled)
    handle_extracted_corpus_smallmem(path_extracted_corpus=path_extracted_corpus, path_extracted_corpus_handled=path_extracted_corpus_handled)
