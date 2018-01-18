# @Author : bamtercelboo
# @Datetime : 2018/1/18 9:56
# @File : handle_corpus.py
# @Last Modify Time : 2018/1/18 9:56
# @Contact : bamtercelboo@{gmail.com, 163.com}

"""
    FILE :  handle_corpus.py
    FUNCTION : handle enwiki-20150112_text.txt corpus to context n-gram(window_size = 5)
"""


import os
import sys


def handle_corpus_context(path_corpus=None, path_save=None, windows_size=0):
    if os.path.exists(path_save):
        os.remove(path_save)
    file = open(path_save, mode="w", encoding="UTF-8")
    with open(path_corpus, encoding="UTF-8") as f:
        now_line = 0
        for line in f.readlines():
            now_line += 1
            sys.stdout.write("\rhandling with {} line.".format(now_line))
            word_list = line.strip().split(" ")
            for word_index, word in enumerate(word_list):
                file.write(word+" ")
                for i in range(windows_size):
                    if (word_index - i) > 0:
                        file.write("F-" + str(i + 1) + "@" + word_list[word_index - i - 1]+" ")
                for i in range(windows_size):
                    if (word_index + i) < len(word_list) - 1:
                        file.write("F" + str(i + 1) + "@" + word_list[word_index + i + 1] + " ")
                file.write("\n")
    f.close()
    file.close()


if __name__ == "__main__":
    path_corpus = "./embedding/enwiki-20150112_text_small_50.txt"
    path_save = "./embedding/enwiki-20150112_text_small_50_context-gram.txt"

    # path_corpus = "./embedding/enwiki-20150112_text_small_50.txt"
    # path_save = "./embedding/enwiki-20150112_text_small_50_context-gram.txt"

    handle_corpus_context(path_corpus=path_corpus, path_save=path_save, windows_size=5)


