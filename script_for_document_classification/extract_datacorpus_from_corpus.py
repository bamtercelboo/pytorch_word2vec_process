# @Author : bamtercelboo
# @Datetime : 2018/1/24 16:15
# @File : extract_datacorpus_from_corpus.py
# @Last Modify Time : 2018/1/24 16:15
# @Contact : bamtercelboo@{gmail.com, 163.com}

"""
    FILE :  extract_datacorpus_from_corpus.py
    FUNCTION : None
"""

import os
import sys
import re

from collections import defaultdict


def clean_str(string):
    """
    Tokenization/string cleaning for all datasets except for SST.
    Original taken from https://github.com/yoonkim/CNN_sentence/blob/master/process_data.py
    """
    string = re.sub(r"[^A-Za-z0-9(),!?\'\`]", " ", string)
    string = re.sub(r"\'s", " \'s", string)
    string = re.sub(r"\'ve", " \'ve", string)
    string = re.sub(r"n\'t", " n\'t", string)
    string = re.sub(r"\'re", " \'re", string)
    string = re.sub(r"\'d", " \'d", string)
    string = re.sub(r"\'ll", " \'ll", string)
    string = re.sub(r",", " , ", string)
    string = re.sub(r"!", " ! ", string)
    string = re.sub(r"\(", " \( ", string)
    string = re.sub(r"\)", " \) ", string)
    string = re.sub(r"\?", " \? ", string)
    string = re.sub(r"\s{2,}", " ", string)

    return string.strip().lower()


def read_data(path_data=None):
    print("read data from {}".format(path_data))
    with open(path_data, encoding="UTF-8") as f:
        data_list = []
        for line in f:
            line = clean_str(line)
            line = line.split(" ")
            data_list.extend(line[1:])
        data = set(data_list)
        # data = list(set(data_list))
    # print(data)
    print("The Data contains {} word.".format(len(data)))
    print("Read Data Finished.")
    f.close()
    return data


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

    path_data = "./Data/RT2k/rt2k_all.txt"
    path_extract_corpus = "/home/lzl/mszhang/data-enwiki/enwiki-20150112_text_context_ngram_allcorpus_stastic/enwiki-20150112_text_context_ngram_allcorpus_stastic.txt"
    path_extracted_corpus = "/home/lzl/mszhang/suda_file0120/extracted_sentence_corpus_sorted/extracted_RT2k_statstic.txt"

    data_dict = read_data(path_data=path_data)
    extract_corpus(path_extract_corpus=path_extract_corpus, data_dict=data_dict, path_extracted_corpus=path_extracted_corpus)
