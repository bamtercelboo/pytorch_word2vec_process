# @Author : bamtercelboo
# @Datetime : 2018/1/17 8:26
# @File : handle_richfeat_feat.py
# @Last Modify Time : 2018/1/17 8:26
# @Contact : bamtercelboo@{gmail.com, 163.com}

"""
    FILE :  handle_richfeat_feat.py
    FUNCTION : iov oov all use feat, but notice the difference with subword and parallel,
               the richfeat feature not only contains n-gram feature ,but also has context(window_size=5) feature
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


def read_data(path_data=None):
    # data_list = []
    print("Reading Data form {}".format(path_data))
    with open(path_data, encoding="UTF-8") as f:
        data_list = []
        for line in f:
            line = clean_str(line)
            line = line.split(" ")
            data_list.extend(line[1:])
        # data = list(sorted(set(data_list), reverse=True))
        # data = list(set(data_list))
        data = set(data_list)
    print("Read Data Finished")
    return data


def read_corpus_stastical_sorted(path_corpus=None, fileter_ratio=1.0):
    print("Reading Corpus from {}".format(path_corpus))
    word_dict = {}
    with open(path_corpus, encoding="UTF-8") as f:
        now_line = 0
        for line in f:
            now_line += 1
            sys.stdout.write("\rHandling with the {} line".format(now_line))
            line = line.strip().split(" ")
            window_dict = {}
            for i in range(0, len(line) - 2, 2):
                # filter feature by sorted frequency
                if i > (((len(line) - 2) / 2) * float(fileter_ratio)):
                    break
                window_dict[line[i + 2]] = int(line[i + 3])
            window_dict["count"] = int(line[1])
            word_dict[line[0]] = window_dict
        f.close()
    print("\nRead Corpus Finished.")
    return word_dict


def read_feat_embedding(path_featEmbedding=None):
    print("Reading feature embedding from {}".format(path_featEmbedding))
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
    print("\nRead feature embedding Finished")
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


def context_n_gram(word=None, corpus_dict=None, feat_embed_dict=None):
    # print("context n-gram")
    word_context_vector = 0
    F_num = 0
    count_word = 1
    # print(word)
    word_context_vector_list = []
    if word in corpus_dict:
        count_word = corpus_dict[word]["count"]
        # print("count_word", count_word)
        for word_context_feat in corpus_dict[word]:
            # print(word_win_feat)
            if word_context_feat in feat_embed_dict:
                count_context = corpus_dict[word][word_context_feat]
                list_float = [float(i) for i in feat_embed_dict[word_context_feat.strip()]]
                F_num += count_context
                # print("count_win", count_win)
                word_context_vector_list.append(int(count_context) * np.array(list_float))
                # word_context_vector = np.array(word_context_vector) + int(count_context) * np.array(list_float)
                # print(word_context_vector)
    word_context_vector = np.sum(word_context_vector_list, axis=0)
    return word_context_vector, F_num, count_word


def write_embed(file=None, word=None, word_embed=None):
    file.write(word + " ")
    for vec in word_embed.tolist():
        file.write(str(round(vec, 6)) + " ")
    file.write("\n")


def handle_Embedding(data_list=None, corpus_dict=None, feat_embedding_dict=None, embedding_dim=0,
                     path_Save_wordEmbedding=None):
    print("Handle Embedding......")
    print("Saving to {}".format(path_Save_wordEmbedding))
    file = open(path_Save_wordEmbedding, encoding="UTF-8", mode="w")
    file.write(str(embedding_dim) + "\n")
    all_word = len(data_list)
    now_word = 0
    for word in data_list:
        now_word += 1
        sys.stdout.write("\rhandling with the {} word in data_list, all {} words.".format(now_word, all_word))
        # word n-gram
        feat_sum_embedding, feat_ngram_num = word_n_gram(word=word, feat_embedding_dict=feat_embedding_dict)
        if not isinstance(feat_sum_embedding, np.ndarray):
            # if the word no n-gram in feature, replace with zero
            feat_sum_embedding = np.array(list([0] * embedding_dim))
            feat_ngram_num = 1
        #  context n-gram
        word_context_vector, F_num, count_word = context_n_gram(word=word, corpus_dict=corpus_dict,
                                                                feat_embed_dict=feat_embedding_dict)
        # calculate
        # feat_sum_embedding = feat_sum_embedding / (feat_ngram_num + F_num / count_word)
        feat_sum_embedding = np.divide(feat_sum_embedding, feat_ngram_num + F_num / count_word)
        # word_context_vector_1 = word_context_vector / (count_word * feat_ngram_num + F_num)
        word_context_vector = np.divide(word_context_vector, count_word * feat_ngram_num + F_num)
        # word_context_ngram_embed = feat_sum_embedding + word_context_vector
        word_context_ngram_embed = np.add(feat_sum_embedding, word_context_vector)
        # write file
        write_embed(file=file, word=word, word_embed=word_context_ngram_embed)
    file.close()

    print("\nHandle Embedding Finished")


if __name__ == "__main__":
    # path_data = "./Data/CR/custrev.all"
    # path_data = "./Data/MR/rt-polarity.all"
    # path_corpus = "./embedding/richfeat_enwiki-20150112_text_handled_stastic_sorted.small.txt"
    # path_featEmbedding = "./embedding/richfeat.enwiki.emb.feature.small"
    # path_Save_wordEmbedding = "./embedding/convert_subword_CR.txt"

    # path_data = "./Data/SST2/stsa.fine.all"
    # path_data = "./Data/TREC/TREC.all"
    # path_data = "./Data/MPQA/mpqa.all"
    # path_data = "./Data/SST1/stsa.binary.all"
    path_data = "./Data/CR/custrev.all"
    # path_data = "./Data/MR/rt-polarity.all"
    # path_data = "./Data/Subj/subj.all"
    path_corpus = "/home/lzl/mszhang/suda_file0120/extracted_sentence_corpus_sorted/extracted_CR_statstic_handled_sorted.txt"
    path_featEmbedding = "/home/lzl/mszhang/suda_file0120/file/file0120/richfeat/enwiki.emb.feature"
    path_Save_wordEmbedding = "/home/lzl/mszhang/suda_file0120/sentence_classification_richfeat/enwiki.emb.source_feat30_CR_1.txt"

    data_list = read_data(path_data=path_data)
    corpus_dict = read_corpus_stastical_sorted(path_corpus=path_corpus, fileter_ratio=0.3)
    feat_embed_dict, feat_embed_dim = read_feat_embedding(path_featEmbedding=path_featEmbedding)
    handle_Embedding(data_list=data_list, corpus_dict=corpus_dict, feat_embedding_dict=feat_embed_dict,
                     embedding_dim=feat_embed_dim, path_Save_wordEmbedding=path_Save_wordEmbedding)
