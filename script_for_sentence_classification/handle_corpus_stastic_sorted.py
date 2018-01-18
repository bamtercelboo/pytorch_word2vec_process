# @Author : bamtercelboo
# @Datetime : 2018/1/18 9:57
# @File : handle_corpus_stastic_sorted.py
# @Last Modify Time : 2018/1/18 9:57
# @Contact : bamtercelboo@{gmail.com, 163.com}

"""
    FILE :  handle_corpus_stastic_sorted.py
    FUNCTION : after handle_corpus.py, data stastic and context n-gram sorted by the frequency of context n-gram
"""

import os
import sys


def handle_corpus_stastic_sorted(path_corpus_context=None, path_corpus_stastic_sorted=None):
    """
    :param path_corpus_context:
    :param path_corpus_stastic_sorted:
    :return:
    :Function: make a statistics on a file, then sort the file by the feature, then write it to file,
               but notice that the first file is disorder, not sorted
    """
    print("Handling data stastic...... ")
    with open(path_corpus_context, encoding="UTF-8") as f:
        word_dict = {}
        now_line = 0
        for line in f:
            now_line += 1
            sys.stdout.write("\rhandling with {} line.".format(now_line))
            line_list = line.strip("\n").strip(" ").split(" ")
            # print(line_list)
            word = line_list[0]
            if word not in word_dict:
                window_dict = {}
                for win_word in line_list[1:]:
                    if win_word not in window_dict:
                        window_dict[win_word] = int(1)
                    else:
                        window_dict[win_word] += 1
                window_dict["count"] = int(1)
                word_dict[word] = window_dict
            else:
                word_dict[word]["count"] += int(1)
                for win_word in line_list[1:]:
                    if win_word in word_dict[word]:
                        word_dict[word][win_word] += 1
                    else:
                        word_dict[word][win_word] = 1
        print("\nFinished")
        f.close()

    if os.path.exists(path=path_corpus_stastic_sorted):
        os.remove(path=path_corpus_stastic_sorted)
    file = open(path_corpus_stastic_sorted, mode="w", encoding="UTF-8")
    print("Writing file......")
    now_word = 0
    len_word_dict = len(word_dict)
    for word in word_dict:
        now_word += 1
        sys.stdout.write("\rwriting {} word, all {} words.".format(now_word, len_word_dict))
        word_dict[word] = dict(sorted(word_dict[word].items(), key=lambda t: t[1], reverse=True))
        file.write(word + " " + str(word_dict[word]["count"]))
        for word_value in word_dict[word]:
            file.write(" " + word_value + " " + str(word_dict[word][word_value]))
        file.write("\n")
    file.close()


def judge_same(judge_list=None):
    judge_list = list(set(judge_list))
    same = False
    if len(judge_list) == 1:
        same = True
    return same


def handle_ordercorpus_stastic_sorted(path_corpus_context=None, path_corpus_stastic_sorted=None):
    """
    :param path_corpus_context:
    :param path_corpus_stastic_sorted:
    :return: NOne
    :Function: make a statistics on a file, then sort the file by the feature, then write it to file,
               but notice that the first file is order, it is sorted
    """
    print("Handling data stastic...... ")
    if os.path.exists(path=path_corpus_stastic_sorted):
        os.remove(path=path_corpus_stastic_sorted)
    file = open(path_corpus_stastic_sorted, mode="w", encoding="UTF-8")
    with open(path_corpus_context, encoding="UTF-8") as f:
        word_dict = {}
        now_line = 0
        judge_list = []
        for line in f:
            now_line += 1
            sys.stdout.write("\rhandling with {} line.".format(now_line))
            line_list = line.strip("\n").strip(" ").split(" ")
            word = line_list[0]
            judge_list.append(word)
            judge = judge_same(judge_list)
            if judge is False:
                judge_list = []
                for w in word_dict:
                    word_dict[w] = dict(sorted(word_dict[w].items(), key=lambda t: t[1], reverse=True))
                    file.write(w + " " + str(word_dict[w]["count"]))
                    for word_value in word_dict[w]:
                        file.write(" " + word_value + " " + str(word_dict[w][word_value]))
                    file.write("\n")
                word_dict = {}
            if word not in word_dict:
                window_dict = {}
                for win_word in line_list[1:]:
                    if win_word not in window_dict:
                        window_dict[win_word] = int(1)
                    else:
                        window_dict[win_word] += 1
                window_dict["count"] = int(1)
                word_dict[word] = window_dict
            else:
                word_dict[word]["count"] += int(1)
                for win_word in line_list[1:]:
                    if win_word in word_dict[word]:
                        word_dict[word][win_word] += 1
                    else:
                        word_dict[word][win_word] = 1

        print("\nHandle Finished")
    f.close()
    file.close()


if __name__ == "__main__":
    # path_corpus_context = "./embedding/enwiki-20150112_text_small_50_context-gram.txt"
    # path_corpus_stastic_sorted = "./embedding/enwiki-20150112_text_small_50_context-gram_stat_sorted.txt"

    # path_corpus_context = "./embedding/enwiki-20150112_text_small_50_context-gram.txt"
    # path_corpus_stastic_sorted = "./embedding/enwiki-20150112_text_small_50_context-gram_stat_sorted.txt"

    # handle_corpus_stastic_sorted(path_corpus_context=path_corpus_context,
    #                              path_corpus_stastic_sorted=path_corpus_stastic_sorted)

    # ***************************************************************************************

    path_ordercorpus_context = "./embedding/enwiki-20150112_text_small_50_context-gram_sorted.txt"
    path_corpus_stastic_sorted = "./embedding/enwiki-20150112_text_small_50_context-gram_static_sorted.txt"

    # path_corpus_context = "./embedding/enwiki-20150112_text_small_50_context-gram.txt"
    # path_corpus_stastic_sorted = "./embedding/enwiki-20150112_text_small_50_context-gram_stat_sorted.txt"

    handle_ordercorpus_stastic_sorted(path_corpus_context=path_ordercorpus_context,
                                      path_corpus_stastic_sorted=path_corpus_stastic_sorted)



