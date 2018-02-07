# @Author : bamtercelboo
# @Datetime : 2018/1/29 15:01
# @File : handle_richfeat_context.py
# @Last Modify Time : 2018/1/29 15:01
# @Contact : bamtercelboo@{gmail.com, 163.com}

"""
    FILE :  handle_richfeat_context.py
    FUNCTION : None
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

    return string.strip().lower()


def read_data(path_data=None, windows_size=5):
    # data_list = []
    print("Reading Data From {}".format(path_data))
    with open(path_data, encoding="UTF-8") as f:
        data_dict = {}
        now_line = 0
        for line in f:
            now_line += 1
            sys.stdout.write("\rreading with the {} line.".format(now_line))
            line = clean_str(line)
            line = line.split(" ")
            value = line[1:]
            for word_index, word in enumerate(value):
                context_dict = {}
                for i in range(windows_size):
                    if (word_index - i) > 0:
                        context_dict["F-" + str(i + 1) + "@" + value[word_index - i - 1]] = 0
                for i in range(windows_size):
                    if (word_index + i) < len(value) - 1:
                        context_dict["F" + str(i + 1) + "@" + value[word_index + i + 1]] = 0
                word = str(now_line) + "-" + str(word_index) + "#" + word
                data_dict[word] = set(context_dict)
        # data = list(sorted(set(data_list), reverse=True))
    print("Read Data Finished")
    return data_dict


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
    feat_embedding = 0
    feat_count = 0
    word = "<" + word + ">"
    feat_embedding_list = []
    for feat_num in range(3, 7):
        for i in range(0, len(word) - feat_num + 1):
            feat = word[i:(i + feat_num)]
            if feat.strip() in feat_embedding_dict:
                feat_count += 1
                list_float = [float(i) for i in feat_embedding_dict[feat.strip()]]
                feat_embedding_list.append(np.array(list_float))
    feat_embedding = np.sum(feat_embedding_list, axis=0)
    return feat_embedding, feat_count


def context(context_dict=None, feat_embed_dict=None):
    context_num = 0
    context_embed_list = []
    context_embed = 0
    for context in context_dict:
        if context in feat_embed_dict:
            context_num += 1
            list_float = [float(i) for i in feat_embed_dict[context]]
            context_embed_list.append(np.array(list_float))
    context_embed = np.sum(context_embed_list, axis=0)
    return context_embed, context_num


def write_embed(file=None, word=None, word_embed=None):
    file.write(word + " ")
    for vec in word_embed.tolist():
        file.write(str(round(vec, 6)) + " ")
    file.write("\n")


def handle_Embedding(data_dict=None,feat_embedding_dict=None, embedding_dim=0, path_Save_wordEmbedding=None):
    print("Handle Embedding......")
    print("Saving to {}".format(path_Save_wordEmbedding))
    file = open(path_Save_wordEmbedding, encoding="UTF-8", mode="w")
    file.write(str(embedding_dim) + "\n")
    all_word = len(data_dict)
    now_word = 0
    for labled_word in data_dict:
        now_word += 1
        sys.stdout.write("\rhandling with the {} word in data_list, all {} words.".format(now_word, all_word))
        # word n-gram
        word = labled_word[(labled_word.find("#") + 1):]
        feat_sum_embedding, feat_ngram_num = word_n_gram(word=word, feat_embedding_dict=feat_embedding_dict)
        if not isinstance(feat_sum_embedding, np.ndarray):
            # if the word no n-gram in feature, replace with zero
            feat_sum_embedding = np.array(list([0] * embedding_dim))
            feat_ngram_num = 1
        # context
        context_embed, context_num = context(context_dict=data_dict[labled_word], feat_embed_dict=feat_embedding_dict)
        # calculate
        word_context_ngram_embed = np.divide(np.add(feat_sum_embedding, context_embed), np.add(feat_ngram_num, context_num))
        # write file
        write_embed(file=file, word=labled_word, word_embed=word_context_ngram_embed)
    file.close()

    print("\nHandle Embedding Finished")


if __name__ == "__main__":
    # path_data = "./Data/CR/custrev.all"
    # path_featEmbedding = "./embedding/richfeat.enwiki.emb.feature.small"
    # path_Save_wordEmbedding = "./embedding/convert_subword_CR.txt"

    # path_data = "./Data/CR/custrev.all"
    path_data = "./Data/MR/rt-polarity.all"
    path_featEmbedding = "/home/lzl/mszhang/suda_file0120/file/file0120/richfeat/enwiki.emb.feature"
    path_Save_wordEmbedding = "/home/lzl/mszhang/suda_file0120/sentence_classification_richfeat/enwiki.emb.context_CR.txt"

    data_dict = read_data(path_data=path_data)
    feat_embed_dict, feat_embed_dim = read_feat_embedding(path_featEmbedding=path_featEmbedding)
    handle_Embedding(data_dict=data_dict, feat_embedding_dict=feat_embed_dict, embedding_dim=feat_embed_dim,
                     path_Save_wordEmbedding=path_Save_wordEmbedding)

