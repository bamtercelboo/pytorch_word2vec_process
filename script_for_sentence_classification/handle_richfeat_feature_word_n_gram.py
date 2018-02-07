# @Author : bamtercelboo
# @Datetime : 2018/1/17 10:15
# @File : handle_richfeat_source_feat.py
# @Last Modify Time : 2018/1/17 10:15
# @Contact : bamtercelboo@{gmail.com, 163.com}

"""
    FILE :  handle_richfeat_source_feat.py
    FUNCTION : iov use source;
               oov use feat;
               but notice the difference with subword and parallel,the richfeat feature not only contains n-gram
               feature ,but also has context(window_size=5) feature;
"""



import re
import sys
import os
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

    return string.strip().lower()


def read_data(path_data=None):
    # data_list = []
    print("Reading Data From {}".format(path_data))
    with open(path_data, encoding="UTF-8") as f:
        data_list = []
        for line in f:
            line = clean_str(line)
            line = line.split(" ")
            data_list.extend(line[1:])
        # data = list(sorted(set(data_list), reverse=True))
        data = set(data_list)
    print("Read Data Finished")
    return data


def read_feat_embedding(path_featEmbedding=None):
    print("Reading Feature Embedding {}".format(path_featEmbedding))
    with open(path_featEmbedding, encoding="UTF-8") as f:
        feat_embedding_dict = {}
        feat_embedding_dim = 0
        now_line = 0
        for line in f:
            now_line += 1
            sys.stdout.write("\rreading {} line.".format(now_line))
            line = line.strip().split(" ")
            if len(line) == 1 or len(line) == 2:
                continue
            feat_embedding_dim = len(line) - 1
            feat_embedding_dict[line[0]] = line[1:]
    f.close()
    print("\nRead Feature Embedding Finished")
    return feat_embedding_dict, feat_embedding_dim


def word_n_gram(word=None, feat_embedding_dict=None):
    # print("n-gram")
    feat_embedding = 0
    feat_count = 0
    word = "<" + word + ">"
    feat_embedding_list = []
    # print(word)
    for feat_num in range(3, 7):
        for i in range(0, len(word) - feat_num + 1):
            feat = word[i:(i + feat_num)]
            if feat.strip() in feat_embedding_dict:
                feat_count += 1
                list_float = [float(i) for i in feat_embedding_dict[feat.strip()]]
                feat_embedding_list.append(np.array(list_float))
                # feat_embedding = np.array(feat_embedding) + np.array(list_float)
    feat_embedding = np.sum(feat_embedding_list, axis=0)
    return feat_embedding, feat_count


def write_embed(file=None, word=None, word_embed=None):
    file.write(word + " ")
    for vec in word_embed.tolist():
        file.write(str(round(vec, 6)) + " ")
    file.write("\n")


def handle_Embedding(data_list=None, feat_embedding_dict=None,
                     embedding_dim=0, path_Save_wordEmbedding=None):
    print("Handle Embedding......")
    print("Saving to {}".format(path_Save_wordEmbedding))
    if os.path.exists(path_Save_wordEmbedding):
        os.remove(path_Save_wordEmbedding)
    file = open(path_Save_wordEmbedding, encoding="UTF-8", mode="w")
    file.write(str(embedding_dim) + "\n")
    all_word = len(data_list)
    now_word = 0
    oov_num = 0
    iov_num = 0
    for word in data_list:
        now_word += 1
        sys.stdout.write("\rhandling with the {} word in data_list, all {} words.".format(now_word, all_word))
        # word n-gram
        feat_sum_embedding, feat_ngram_num = word_n_gram(word=word, feat_embedding_dict=feat_embedding_dict)
        if not isinstance(feat_sum_embedding, np.ndarray):
            continue

        # calculate
        feat_sum_embedding = np.divide(feat_sum_embedding, feat_ngram_num)

        # write file
        write_embed(file=file, word=word, word_embed=feat_sum_embedding)
    file.close()
    print("\nHandle Embedding Finished")


if __name__ == "__main__":
    path_data = "./Data/conll2003_gold/conll2003_gold_all.txt"
    # path_data = "./Data/conll2000/data_all.txt"
    # path_featEmbedding = "./embedding/subword.enwiki.emb.feature.small"
    # path_Save_wordEmbedding = "./embedding/convert_subword_IMDB.txt"

    path_data = "./Data/SST2/stsa.fine.all"
    # path_data = "./Data/TREC/TREC.all"
    # path_data = "./Data/MPQA/mpqa.all"
    # path_data = "./Data/SST1/stsa.binary.all"
    # path_data = "./Data/CR/custrev.all"
    # path_data = "./Data/MR/rt-polarity.all"
    # path_data = "./Data/Subj/subj.all"
    path_featEmbedding = "/home/lzl/mszhang/suda_file0120/file/file0120/richfeat/enwiki.emb.feature"
    path_Save_wordEmbedding = "/home/lzl/mszhang/suda_file0120/file/file0120/richfeat/pos_chunking_ner/enwiki.emb.feat_word_ngram_SST2.txt"

    data_list = read_data(path_data=path_data)
    feat_embed_dict, feat_embed_dim = read_feat_embedding(path_featEmbedding=path_featEmbedding)
    handle_Embedding(data_list=data_list, feat_embedding_dict=feat_embed_dict, embedding_dim=feat_embed_dim,
                     path_Save_wordEmbedding=path_Save_wordEmbedding)
