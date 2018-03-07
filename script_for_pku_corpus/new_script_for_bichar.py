# @Author : bamtercelboo
# @Datetime : 2018/3/7 11:45
# @File : new_script_for_bichar.py
# @Last Modify Time : 2018/3/7 11:45
# @Contact : bamtercelboo@{gmail.com, 163.com}

"""
    FILE :  new_script_for_bichar.py
    FUNCTION : None
"""
import os
import sys

def handle_bichar(file_embed=None, save_file=None):
    if os.path.exists(save_file):
        os.remove(save_file)
    file = open(save_file, encoding="UTF-8", mode="w")
    now_line = 0
    with open(file_embed, encoding="UTF-8") as f:
        for line in f:
            now_line += 1
            sys.stdout.write("\rhandling with {} line.".format(now_line))
            print(line)
            line = line.replace("@$", "")
            print(line)
            file.writelines(line)
    file.close()
    print("Handle Finished.")


if __name__ == "__main__":
    print("bichar")
    file_embed = "./giga.pku.bichar.words.small"
    save_file = "./giga.pku.bichar.words.small.txt"
    handle_bichar(file_embed=file_embed, save_file=save_file)

