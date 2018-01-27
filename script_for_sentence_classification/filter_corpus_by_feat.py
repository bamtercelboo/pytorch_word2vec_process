# @Author : bamtercelboo
# @Datetime : 2018/1/26 10:57
# @File : filter_corpus_by_feat.py
# @Last Modify Time : 2018/1/26 10:57
# @Contact : bamtercelboo@{gmail.com, 163.com}

"""
    FILE :  filter_corpus_by_feat.py
    FUNCTION : None
"""

import os
import sys


def read_vocab(path_vocab=None):
    vocab = []
    with open(path_vocab, encoding="UTF-8") as f:
        for line in f:
            vocab.append(line.strip())
    vocab_dict = set(vocab)
    f.close()
    return vocab_dict


def filter_corpus_by_feat(vocab_dict=None, path_corpus=None, path_save_corpus=None):
    if os.path.exists(path_save_corpus):
        os.remove(path_save_corpus)
    file = open(path_save_corpus, encoding="UTF-8", mode="w")
    now_line = 0
    with open(path_corpus, encoding="UTF-8") as f:
        for line in f:
            now_line += 1
            sys.stdout.write("\rhandling with {} line".format(now_line))
            word = line[:line.find(" ")]
            if word in vocab_dict:
                file.writelines(line)
    f.close()
    file.close()
    print("\nHandle Finished.")


if __name__ == "__main__":
    path_vocab = "./enwiki.emb.feature.vocab.txt"
    # path_corpus = "./embedding/richfeat_enwiki-20150112_text_handled_stastic_sorted.small.txt"
    # path_save_corpus = "./embedding/richfeat_enwiki-20150112_text_handled_stastic_sorted.small_filter.txt"
    path_corpus = "/data/mszhang/ACL2017-Word2Vec/experiments-final/for-liuzonglin/file0120/extracted_sentence_corpus/SST1/extracted_SST2_statstic_handled_sorted.txt"
    path_save_corpus = "/data/mszhang/ACL2017-Word2Vec/experiments-final/for-liuzonglin/file0120/extracted_sentence_corpus/SST1/extracted_SST2_statstic_handled_sorted_filtered.txt"
    vocab_dict = read_vocab(path_vocab=path_vocab)
    filter_corpus_by_feat(vocab_dict=vocab_dict, path_corpus=path_corpus, path_save_corpus=path_save_corpus)
