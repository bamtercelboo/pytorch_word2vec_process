# @Author : bamtercelboo
# @Datetime : 2018/1/22 19:32
# @File : handle_corpu_to_sorted.py
# @Last Modify Time : 2018/1/22 19:32
# @Contact : bamtercelboo@{gmail.com, 163.com}

"""
    FILE :  handle_corpu_to_sorted.py
    FUNCTION : None
"""
import os
import sys


def sort_corpus(path_data=None, path_save_sorted=None):
    print("sort file.......")
    if os.path.exists(path_save_sorted):
        os.remove(path_save_sorted)
    file = open(path_save_sorted, encoding="UTF-8", mode="w")
    with open(path_data, encoding="UTF-8") as f:
        now_line = 0
        for line in f:
            now_line += 1
            sys.stdout.write("\rhandling with {} line.".format(now_line))
            word_dict = {}
            line = line.strip().split(" ")
            feat = line[2:]
            feat_dict = {}
            for i in range(0, len(feat), 2):
                feat_dict[feat[i]] = int(feat[i + 1])
            feat_dict = dict(sorted(feat_dict.items(), key=lambda t: t[1], reverse=True))
            word_dict[line[0]] = feat_dict["count"]
            write(file=file, word_dict=word_dict, feat_dict=feat_dict)
    f.close()
    file.close()
    print("\nSort File Finished.")


def write(file=None, word_dict=None, feat_dict=None):
    str_w = ""
    str_feat = ""
    for k, v in word_dict.items():
        str_w += (k + " " + str(v) + " ")
    for k, v in feat_dict.items():
        str_feat += (k + " " + str(v) + " ")
    file.writelines(str_w + str_feat + "\n")


if __name__ == "__main__":

    # path_data = "./embedding/filter_corpus_fichfeat0120_stastic_small.txt"
    # path_save_sorted = "./embedding/filter_corpus_fichfeat0120_stastic_sorted_small.txt"
    
    path_data = "/home/lzl/mszhang/suda_file0120/corpus/filter_corpus_fichfeat0120_stastic/filter_corpus_fichfeat0120_stastic.txt"
    path_save_sorted = "/home/lzl/mszhang/suda_file0120/corpus/filter_corpus_fichfeat0120_stastic_sorted/silter_corpus_richfeat0120_stastic_sorted.txt"
    
    sort_corpus(path_data=path_data, path_save_sorted=path_save_sorted)


