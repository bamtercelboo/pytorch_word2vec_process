# @Author : bamtercelboo
# @Datetime : 2018/1/16 21:41
# @File : handle_parallel_source_feat.py
# @Last Modify Time : 2018/1/16 21:41
# @Contact : bamtercelboo@{gmail.com, 163.com}

"""
    FILE :  handle_parallel_source_feat.py
    FUNCTION : iov use source
               oov use feat
"""

import re
import sys
import numpy as np


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
        for line in f:
            line = clean_str(line)
            line = line.split(" ")
            data_list.extend(line[1:])
        # data = list(sorted(set(data_list), reverse=True))
        data = list(set(data_list))
    return data


def read_source_embedding(path_sourceEmbedding=None):
    print("read source embedding.......")
    with open(path_sourceEmbedding, encoding="UTF-8") as f:
        source_embedding_dict = {}
        source_embedding_dim = 0
        now_line = 0
        for line in f.readlines():
            now_line += 1
            sys.stdout.write("\rreading {} line.".format(now_line))
            line = line.strip().split(" ")
            if len(line) == 1 or len(line) == 2:
                continue
            source_embedding_dim = len(line) - 1
            source_embedding_dict[line[0]] = line[1:]
    f.close()
    print("\nread source embedding Finished")
    return source_embedding_dict, source_embedding_dim


def read_feat_embedding(path_featEmbedding=None):
    print("read feature embedding.......")
    with open(path_featEmbedding, encoding="UTF-8") as f:
        feat_embedding_dict = {}
        feat_embedding_dim = 0
        now_line = 0
        for line in f.readlines():
            now_line += 1
            sys.stdout.write("\rreading {} line.".format(now_line))
            line = line.strip().split(" ")
            if len(line) == 1 or len(line) == 2:
                continue
            feat_embedding_dim = len(line) - 1
            feat_embedding_dict[line[0]] = line[1:]
    f.close()
    print("\nread feature embedding Finished")
    return feat_embedding_dict, feat_embedding_dim


def n_gram(word=None, feat_embedding_dict=None):
    # print("n-gram")
    feat_embedding = 0
    feat_count = 0
    word = "<" + word + ">"
    # print(word)
    for feat_num in range(3, 7):
        for i in range(0, len(word) - feat_num + 1):
            feat = word[i:(i + feat_num)]
            if feat.strip() in feat_embedding_dict:
                feat_count += 1
                list_float = [float(i) for i in feat_embedding_dict[feat.strip()]]
                feat_embedding = np.array(feat_embedding) + np.array(list_float)

    return feat_embedding, feat_count


def write_embed(file=None, word=None, word_embed=None):
    file.write(word + " ")
    for vec in word_embed.tolist():
        file.write(str(round(vec, 6)) + " ")
    file.write("\n")


def handle_Embedding(data_list=None, source_embedding_dict=None, feat_embedding_dict=None, embedding_dim=0,
                     path_Save_wordEmbedding=None):
    print("Handle Embedding......")
    file = open(path_Save_wordEmbedding, encoding="UTF-8", mode="w")
    file.write(str(embedding_dim) + "\n")
    all_word = len(data_list)
    now_word = 0
    oov_num = 0
    iov_num = 0
    for word in data_list:
        now_word += 1
        sys.stdout.write("\rhandling with the {} word in data_list, all {} words.".format(now_word, all_word))
        # print(word)
        if word in source_embedding_dict:
            iov_num += 1
            source_embedding_list = [float(i) for i in source_embed_dict[word]]
            source_embedding = np.array(source_embedding_list)
            write_embed(file=file, word=word, word_embed=source_embedding)
        else:
            oov_num += 1
            feat_embedding, feat_ngram_num = n_gram(word=word, feat_embedding_dict=feat_embedding_dict)
            if not isinstance(feat_embedding, np.ndarray):
                # if the word no n-gram in feature, replace with zero
                feat_embedding = np.array(list([0] * embedding_dim))
                feat_ngram_num = 1
            feat_embedding = feat_embedding / feat_ngram_num
            write_embed(file=file, word=word, word_embed=feat_embedding)
    file.close()
    print("\niov number {} , oov number {}, all words {} == {}".format(iov_num, oov_num, (iov_num + oov_num),
                                                                       len(data_list)))
    print("Handle Embedding Finished")


if __name__ == "__main__":
    path_data = "./Data/CR/custrev.all"
    # path_data = "./Data/MR/rt-polarity.all"
    path_sourceEmbedding = "./embedding/parallel.enwiki.emb.source.small"
    path_featEmbedding = "./embedding/parallel.enwiki.emb.feature.small"
    path_Save_wordEmbedding = "./embedding/convert_subword_MR.txt"

    # path_data = "./Data/CR/custrev.all"
    # path_data = "./Data/MR/rt-polarity.all"
    # path_data = "./Data/Subj/subj.all"
    # path_sourceEmbedding = "/home/lzl/mszhang/suda_file_0113/file/subword/enwiki.emb.source"
    # path_featEmbedding = "/home/lzl/mszhang/suda_file_0113/file/subword/enwiki.emb.feature"
    # path_Save_wordEmbedding = "/home/lzl/mszhang/suda_file_0113/file/context/sentence_classification/enwiki.emb.source_CR.txt"

    data_list = read_data(path_data=path_data)
    # data_list = ["wayulink", "fileski", "promotioned", "asdasd"]
    source_embed_dict, source_embed_dim = read_source_embedding(path_sourceEmbedding=path_sourceEmbedding)
    feat_embed_dict, feat_embed_dim = read_feat_embedding(path_featEmbedding=path_featEmbedding)
    assert source_embed_dim == feat_embed_dim
    handle_Embedding(data_list=data_list, source_embedding_dict=source_embed_dict, feat_embedding_dict=feat_embed_dict,
                     embedding_dim=source_embed_dim, path_Save_wordEmbedding=path_Save_wordEmbedding)
