# @Author : bamtercelboo
# @Datetime : 2018/1/16 15:08
# @File : handle_subword.py
# @Last Modify Time : 2018/1/28 09:31
# @Contact : bamtercelboo@{gmail.com, 163.com}

"""
    FILE :  handle_context.py
    FUNCTION : None
"""

import re
import sys
import os


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
    # data_list = []
    print("Read Data From {}".format(path_data))
    with open(path_data, encoding="UTF-8") as f:
        data_list = []
        now_line = 0
        for line in f:
            now_line += 1
            sys.stdout.write("\rreading {} line.".format(now_line))
            line = clean_str(line)
            line = line.split(" ")
            data_list.extend(line[1:])
        # data = list(sorted(set(data_list), reverse=True))
        data = set(data_list)
        # print(data)
    print("\nRead Data Finished.")
    return data


def read_source_embedding(path_sourceEmbedding=None):
    print("Read Source Embedding From {}".format(path_sourceEmbedding))
    with open(path_sourceEmbedding, encoding="UTF-8") as f:
        embedding_dict = {}
        embedding_dim = 0
        now_line = 0
        for line in f.readlines():
            now_line += 1
            sys.stdout.write("\rreading {} line.".format(now_line))
            line = line.strip().split(" ")
            if len(line) == 1 or len(line) == 2:
                continue
            embedding_dim = len(line) - 1
            embedding_dict[line[0]] = line[1:]
    f.close()
    print("\nRead Source Embedding Finished.")
    return embedding_dict, embedding_dim


def handle_Embedding(data_list=None, embedding_dict=None, embedding_dim=0, path_Save_wordEmbedding=None):
    print("Handle Embedding......")
    if os.path.exists(path_Save_wordEmbedding):
        os.remove(path_Save_wordEmbedding)
    file = open(path_Save_wordEmbedding, encoding="UTF-8", mode="w")
    file.write(str(embedding_dim) + "\n")
    all_word = len(data_list)
    now_word = 0
    oov_embedding = 0
    oov_num = 0
    iov_num = 0
    for word in data_list:
        now_word += 1
        sys.stdout.write("\rhandling with the {} word in data_list, all {} words.".format(now_word, all_word))
        if word in embedding_dict:
            iov_num += 1
            file.write(word + " ")
            for vec in embedding_dict[word]:
                file.write(vec + " ")
            file.write("\n")
        # else:
        #     oov_num += 1
        #     file.write(word + " ")
        #     for vec in range(embedding_dim):
        #         file.write(str(oov_embedding) + " ")
        #     file.write("\n")
    file.close()
    print("\niov number {} , oov number {}, all words {} == {}".format(iov_num, oov_num, (iov_num + oov_num),
                                                                        len(data_list)))
    print("Handle Embedding Finished")


if __name__ == "__main__":
    # path_data = "./Data/IMDB/imdb_testall.txt"
    # path_sourceEmbedding = "./embedding/subword.enwiki.emb.source.small"
    # path_Save_wordEmbedding = "./embedding/converted_subword_MR.txt"

    # path_data = "./Data/IMDB/imdb_data_all.txt"
    path_data = "./Data/RT2k/rt2k_all.txt"
    path_sourceEmbedding = "/home/lzl/mszhang/suda_file0120/file/file0120/context/enwiki.emb.source"
    path_Save_wordEmbedding = "/home/lzl/mszhang/suda_file0120/file/file0120/context/document_classification/enwiki.emb.source_RT2k_OOV.txt"

    data_list = read_data(path_data=path_data)
    embedding_dict, embedding_dim = read_source_embedding(path_sourceEmbedding=path_sourceEmbedding)
    handle_Embedding(data_list=data_list, embedding_dict=embedding_dict, embedding_dim=embedding_dim,
                     path_Save_wordEmbedding=path_Save_wordEmbedding)

