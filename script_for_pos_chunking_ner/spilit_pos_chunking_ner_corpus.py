# @Author : bamtercelboo
# @Datetime : 2018/2/2 9:49
# @File : spilit_pos_chunking_ner_corpus.py
# @Last Modify Time : 2018/2/2 9:49
# @Contact : bamtercelboo@{gmail.com, 163.com}

"""
    FILE :  spilit_pos_chunking_ner_corpus.py
    FUNCTION : None
"""

import os
import sys


def Spilit_Data(corpus_path=None, spilited_corpus=None, col=None):
    assert corpus_path is not None, "The Data corpus path Is Not Allow Empty."
    assert spilited_corpus is not None, "The spilited_corpus Path Is Not Allow Empty."
    assert col is not None
    print("Read Corpus From {}".format(corpus_path))
    if os.path.exists(spilited_corpus):
        os.remove(spilited_corpus)
    print("Spilited Corpus Save To {}".format(spilited_corpus))
    file = open(spilited_corpus, encoding="UTF-8", mode="w")
    with open(corpus_path, encoding="UTF-8") as f:
        now_line = 0
        for line in f.readlines():
            now_line += 1
            sys.stdout.write("\rhandling with the {} line".format(now_line))
            if line == "\n":
                file.write(line)
                continue
            line = line.strip().split(" ")
            # if line[0] == "-DOCSTART-":
            #     continue
            file.write(line[0] + " " + line[col - 1] + "\n")
    f.close()
    file.close()
    print("\nSpilit Corpus Finished.")


if __name__ == "__main__":
    corpus_path = "./Data/conll2003_gold/test.txt"
    spilited_corpus = "./Conll2003_NER/test.txt"
    col = 4
    Spilit_Data(corpus_path=corpus_path, spilited_corpus=spilited_corpus, col=col)



