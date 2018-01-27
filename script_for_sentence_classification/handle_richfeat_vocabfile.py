# @Author : bamtercelboo
# @Datetime : 2018/1/26 10:28
# @File : handle_richfeat_vocabfile.py
# @Last Modify Time : 2018/1/26 10:28
# @Contact : bamtercelboo@{gmail.com, 163.com}

"""
    FILE :  handle_richfeat_vocabfile.py
    FUNCTION : None
"""

import os
import sys


def handle_rich_feature(path_feature=None, path_feature_word=None):
    if os.path.exists(path_feature_word):
        os.remove(path_feature_word)

    F = set()
    F.add("F")
    vocab = []
    print("Read Feature From {}".format(path_feature))
    with open(path_feature, encoding="UTF-8") as f:
        now_line = 0
        for line in f:
            now_line += 1
            sys.stdout.write("\rhandling with the {} line.".format(now_line))
            if line[0] not in F:
                continue
            line = line.strip().split(" ")
            index = line[0].find("@") + 1
            vocab.append(line[0][index:])
        vocab = set(vocab)
    f.close()
    print("Read Feature Finished.")

    print("Writing File To {}".format(path_feature_word))
    file = open(path_feature_word, encoding="UTF-8", mode="w")
    all_words = len(vocab)
    now_word = 0
    for word in vocab:
        now_word += 1
        sys.stdout.write("\rhandling with the {} word, all {} words.".format(now_word, all_words))
        file.write(word + "\n")
    print("Writing File Finished")
    file.close()


if __name__ == "__main__":
    path_feature = "./embedding/richfeat.enwiki.emb.feature.small"
    path_feature_word = "./embedding/richfeat.enwiki.emb.feature.vocab"
    handle_rich_feature(path_feature=path_feature, path_feature_word=path_feature_word)