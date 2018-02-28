# @Author : bamtercelboo
# @Datetime : 2018/2/27 19:26
# @File : script_for_stastic_pos-tag.py
# @Last Modify Time : 2018/2/27 19:26
# @Contact : bamtercelboo@{gmail.com, 163.com}

"""
    FILE :  script_for_stastic_pos-tag.py
    FUNCTION : None
"""

import os
import sys


def handle_pos_tag(corpus_file=None):

    word_count = 0
    pos_tag = {}
    now_line = 0
    with open(corpus_file, encoding="UTF-8") as f:
        for line in f:
            now_line += 1
            sys.stdout.write("\rhandling with {} line.".format(now_line))
            line = line.replace("\n", "").split("  ")
            word_count += len(line)
            for word in line:
                # print(word.rfind("_"))
                if word.rfind("_") == -1:
                    continue
                tag = word[(word.rfind("_") + 1):]
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
    file.writelines("corpus" + "  " + corpus_file)
    file.write("\n")
    file.writelines("word_count" + "  " + str(word_count))
    file.write("\n")
    for key, value in pos_tag.items():
        file.write(key + "  " + str(value) + "\n")
    file.close()
    print("Write Finished")


if __name__ == "__main__":
    print("stastical pos-tag")
    corpus_file = "./data/pku_corpus_spilit_cleaned/863corpus_train_cleaned.txt"
    save_file = "./data/pku_corpus_spilit_cleaned/863corpus_train_cleaned_statistics.txt"
    pos_tag, word_count = handle_pos_tag(corpus_file=corpus_file)
    print(pos_tag, word_count)
    write(pos_tag=pos_tag, word_count=word_count, save_file=save_file, corpus_file=corpus_file)
