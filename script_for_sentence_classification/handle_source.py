# @Author : bamtercelboo
# @Datetime : 2018/1/15 15:57
# @File : handle_source.py
# @Last Modify Time : 2018/1/15 15:57
# @Contact : bamtercelboo@{gmail.com, 163.com}

"""
    FILE :  handle_source.py
    FUNCTION : None
"""

import re
import sys


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

    return string.strip()


def read_data(path_data=None):
    # data_list = []
    print("read data......")
    with open(path_data, encoding="UTF-8") as f:
        data_list = []
        for line in f.readlines():
            line = line.strip("\n").split(" ")
            data_list.extend(line[1:])
        data = list(set(data_list))
        # print(data_list)
    return data


def read_Embedding(path_wordEmbedding=None):
    print("read word embedding.......")
    with open(path_wordEmbedding, encoding="UTF-8") as f:
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
    print("\nread embedding Finished")
    return embedding_dict, embedding_dim


def handle_Embedding(data_list=None, embedding_dict=None, embedding_dim=0, path_Save_wordEmbedding=None):
    print("Handle Embedding......")
    file = open(path_Save_wordEmbedding, encoding="UTF-8", mode="w")
    file.write(str(embedding_dim) + "\n")
    all_word = len(data_list)
    now_word = 0
    for word in data_list:
        now_word +=1
        sys.stdout.write("\rhandling with the {} word in data_list, all {} words.".format(now_word, all_word))
        if word in embedding_dict:
            file.write(word + " ")
            for vec in embedding_dict[word]:
                file.write(vec + " ")
            file.write("\n")
    file.close()
    print("\nHandle Embedding Finished")


if __name__ == "__main__":
    path_data = "./Data/CR/custrev.all"
    path_wordEmbedding = "./converted_word_MR.txt"
    path_Save_wordEmbedding = "./wordEmbedding_CR.txt"

    # path_data = "./Data/CR/custrev.all"
    # path_wordEmbedding = "./converted_word_MR.txt"
    # path_Save_wordEmbedding = "./wordEmbedding_CR.txt"

    data_list = read_data(path_data=path_data)
    embedding_dict, embedding_dim = read_Embedding(path_wordEmbedding=path_wordEmbedding)
    handle_Embedding(data_list=data_list, embedding_dict=embedding_dict, embedding_dim=embedding_dim,
                     path_Save_wordEmbedding=path_Save_wordEmbedding)

