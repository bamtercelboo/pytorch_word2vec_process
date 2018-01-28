# @Author : bamtercelboo
# @Datetime : 2018/1/28 13:05
# @File : handle_rt2k_dataset.py
# @Last Modify Time : 2018/1/28 13:05
# @Contact : bamtercelboo@{gmail.com, 163.com}

"""
    FILE :  handle_rt2k_dataset.py
    RT-2k Dataset Download From: http://www.cs.cornell.edu/people/pabo/movie%2Dreview%2Ddata/review_polarity.tar.gz
    FUNCTION : Merge the spilited file, and the motional polarity is marked.
"""

import os
import sys


def handle_rt2k(path_dir=None, path_file_save=None, save_mode=None, polarity=None):
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
        # file_save.write(polarity)
        str_line = polarity + " "
        for line in f:
            str_line += " " + line.strip("\n")
        # print(str_line)
        file_save.writelines(str_line + "\n")
        f.close()
    file_save.close()
    print("\nHandle Finished")


if __name__ == "__main__":
    # path_dir = "./Data/rt2k_test/neg"
    # path_file_save = "./rt2k_test.txt"
    # save_mode = "w"
    # polarity = "0"
    path_dir = "/home/lzl/worksapce/All_Corpus/Text_Classification/review_polarity/txt_sentoken/neg"
    path_file_save = "./rt2k_all.txt"
    save_mode = "w"
    polarity = "0"
    handle_rt2k(path_dir=path_dir, path_file_save=path_file_save, save_mode=save_mode, polarity=polarity)


