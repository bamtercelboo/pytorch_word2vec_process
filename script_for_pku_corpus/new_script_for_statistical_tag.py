# @Author : bamtercelboo
# @Datetime : 2018/3/2 7:10
# @File : new_script_for_statistical_tag.py
# @Last Modify Time : 2018/3/2 7:10
# @Contact : bamtercelboo@{gmail.com, 163.com}

"""
    FILE :  new_script_for_statistical_tag.py
    FUNCTION : None
"""

import os
import sys


def statistical_pos_tag(corpus_file=None):

    word_count = 0
    pos_tag = {}
    now_line = 0
    with open(corpus_file, encoding="UTF-8") as f:
        for line in f:
            now_line += 1
            sys.stdout.write("\rhandling with {} line.".format(now_line))
            line = line.replace("\n", "").split(" ")
            word_count += len(line)
            for word in line:
                if word.find("_") == -1:
                    continue
                tag = word[(word.find("_") + 1):]
                if tag in pos_tag:
                    pos_tag[tag] += 1
                else:
                    pos_tag[tag] = 1
        print("\nhandle Finished.")
        return pos_tag, word_count


def write(pos_tag=None, word_count=None, save_file=None, corpus_file=None):
    print("Writing To File......")
    if os.path.exists(save_file):
        os.remove(save_file)
    file = open(save_file, encoding="UTF-8", mode="w")
    file.writelines("corpus" + " " + corpus_file)
    file.write("\n")
    file.writelines("word_count" + " " + str(word_count))
    file.write("\n")
    for key, value in pos_tag.items():
        file.write(key + " " + str(value) + "\n")
    file.close()
    print("Write Finished")


def merge_tag(data=None, save_all_tag=None):
    if os.path.exists(save_all_tag):
        os.remove(save_all_tag)
    file = open(save_all_tag, encoding="UTF-8", mode="w")
    tag_dict = {}
    with open(data, encoding="UTF-8") as f:
        for line in f:
            line = line.split(" ")
            if line[0] not in tag_dict:
                tag_dict[line[0]] = int(line[1])
            else:
                tag_dict[line[0]] += int(line[1])
    print(tag_dict)
    for tag, count in tag_dict.items():
        file.writelines(tag + " " + str(count) + "\n")
    file.close()


if __name__ == "__main__":
    print("statistical pos-tag")
    # corpus_file = "./data/pku_tag_cleaned/pku.test.a2b.tag.cleaned.txt"
    # save_file = "./data/pku_statistical_tag/pku.test.a2b.tag.cleaned.sta.txt"
    # corpus_file = "./data/pku_tag_cleaned/pku.split.train.863tag.cleaned.txt"
    # save_file = "./data/pku_statistical_tag/pku.split.train.863tag.cleaned.sta.txt"
    # pos_tag, word_count = statistical_pos_tag(corpus_file=corpus_file)
    # print(pos_tag, word_count)
    # write(pos_tag=pos_tag, word_count=word_count, save_file=save_file, corpus_file=corpus_file)

    data = "./data/pku_statistical_tag/pku_tag_all.txt"
    save_all_tag = "./data/pku_statistical_tag/pku_tag_all_set.txt"
    merge_tag(data=data, save_all_tag=save_all_tag)



