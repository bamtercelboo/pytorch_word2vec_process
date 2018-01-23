# @Author : bamtercelboo
# @Datetime : 2018/1/23 8:31
# @File : extract_similarcorpus_from_corpus.py
# @Last Modify Time : 2018/1/23 8:31
# @Contact : bamtercelboo@{gmail.com, 163.com}

"""
    FILE :  extract_similarcorpus_from_corpus.py
    FUNCTION : None
"""

import os
import sys


def read_data(path_data=None):
    print("Reading File from {}".format(path_data))
    data_dict = set()
    with open(path_data, encoding="UTF-8") as f:
        for line in f:
            # data_dict[line.strip()] = 0
            data_dict.add(line.strip())
    f.close()
    print("Read File Finished.")
    return data_dict


def extract_corpus(path_extract_corpus=None, data_dict=None, path_extracted_corpus=None):
    print("extracting corpus from {}".format(path_extract_corpus))
    if os.path.exists(path_extracted_corpus):
        os.remove(path_extracted_corpus)
    file = open(path_extracted_corpus, encoding="UTF-8", mode="w")
    with open(path_extract_corpus, encoding="UTF-8") as f:
        now_line = 0
        for line in f:
            now_line += 1
            sys.stdout.write("\rhandling with {} line".format(now_line))
            line_list = line.strip().split(" ")
            if line_list[0] in data_dict:
                file.writelines(line)
    f.close()
    file.close()
    print("\nExtract Corpus Finished.")


if __name__ == "__main__":
    # path_data = "./Data/fullVocab.txt"
    # path_extract_corpus = "./Embedding/enwiki-20150112_text_handled_stastic_small.txt"
    # path_extracted_corpus = "./Embedding/enwiki-20150112_text_handled_stastic_small.extracted.txt"

    path_data = "./Data/fullVocab.txt"
    path_extract_corpus = "/home/lzl/mszhang/suda_file0120/corpus/filter_corpus_fichfeat0120_stastic_sorted/filter_corpus_richfeat0120_stastic_sorted.txt"
    path_extracted_corpus = "/home/lzl/mszhang/suda_file0120/corpus/word_similar/filter_corpus_richfeat0120_stastic_sorted_similar.txt"

    data_dict = read_data(path_data=path_data)
    extract_corpus(path_extract_corpus=path_extract_corpus, data_dict=data_dict, path_extracted_corpus=path_extracted_corpus)

