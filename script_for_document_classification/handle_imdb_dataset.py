# @Author : bamtercelboo
# @Datetime : 2018/1/27 13:33
# @File : handle_imdb_dataset.py
# @Last Modify Time : 2018/1/27 13:33
# @Contact : bamtercelboo@{gmail.com, 163.com}

"""
    FILE :  handle_imdb_dataset.py
    IMDB Dataset Download From : http://ai.stanford.edu/%7Eamaas/data/sentiment/aclImdb_v1.tar.gz
    FUNCTION : The download file is splited, the script handle the all spilited file to train, test two file
"""

import os
import sys


def handle_imdb(path_dir=None, path_file_save=None, save_mode=None, polarity=None):
    if not os.path.isdir(path_dir):
        print("The path {} is not a folder directory")
        exit()
    if save_mode is None or polarity is None:
        print("The parameter os save_mode or polarity is not allow to empty.")
        exit()
    file_save = open(path_file_save, encoding="UTF-8", mode=save_mode)
    files = os.listdir(path=path_dir)
    now_file = 0
    all_files = len(files)
    for file in files:
        now_file += 1
        sys.stdout.write("\rhandling with the {} file, all {} files.".format(now_file, all_files))
        f = open(os.path.join(path_dir, file))
        for line in f:
            file_save.writelines(polarity + " " + line + "\n")
        f.close()
    file_save.close()
    print("\nHandle Finished")


if __name__ == "__main__":
    # path_dir = "./Data/test/pos"
    # path_file_save = "./imdb_test.txt"
    # save_mode = "w"
    # polarity = "0"
    path_dir = "/home/lzl/worksapce/All_Corpus/Text_Classification/aclImdb/train/neg"
    path_file_save = "./imdb_train.txt"
    save_mode = "w"
    polarity = "0"
    handle_imdb(path_dir=path_dir, path_file_save=path_file_save, save_mode=save_mode, polarity=polarity)
