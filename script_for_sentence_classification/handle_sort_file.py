# @Author : bamtercelboo
# @Datetime : 2018/1/18 14:57
# @File : handle_sort_file.py
# @Last Modify Time : 2018/1/18 14:57
# @Contact : bamtercelboo@{gmail.com, 163.com}

"""
    FILE :  handle_sort_file.py
    FUNCTION : sort so big file about 250G
"""

import os
import sys
import linecache


def read_file(path_file=None):
    print("Reading File......")
    word_list = []
    now_line = 0
    with open(path_file, encoding="UTF-8") as f:
        for line in f:
            now_line += 1
            sys.stdout.write("\rhandling with {} line.".format(now_line))
            line = line.strip().split(" ")
            word_list.append(line[0] + " " + str(now_line))
    word_list = sorted(word_list)
    print("Read File Finished")
    return word_list


def sort_file(sorted_word_list=None, path_data=None, path_save=None):
    print("Sorting File......")
    file = open(path_save, encoding="UTF-8", mode="w")
    all_line = len(sorted_word_list)
    for index, word_line in enumerate(sorted_word_list):
        sys.stdout.write("\rhandling with {} line, all {} lines.".format((index + 1), all_line))
        word_line = word_line.split(" ")
        line = int(word_line[1])
        context = linecache.getline(path_data, line)
        file.writelines(context)
    file.close()
    print("\nSorted File Finished.")


if __name__ == "__main__":
    path_data = "./embedding/enwiki-20150112_text_small_50_context-gram.txt"
    path_save = "./embedding/enwiki-20150112_text_small_50_context-gram_sorted.txt"
    sorted_word_list = read_file(path_file=path_data)
    sort_file(sorted_word_list=sorted_word_list, path_data=path_data, path_save=path_save)


