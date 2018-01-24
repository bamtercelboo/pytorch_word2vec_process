# @Author : bamtercelboo
# @Datetime : 2018/1/23 22:50
# @File : python_mu.py
# @Last Modify Time : 2018/1/23 22:50
# @Contact : bamtercelboo@{gmail.com, 163.com}

"""
    FILE :  python_mu.py
    FUNCTION : None
"""

import os
import sys
from multiprocessing import  Process
import time

def test():
    a = time.time()
    for i in range(100):
        for j in range(1000000):
            print("i " + str(i + j * i))
    b = time.time()
    print("Tiime ", (b - a))


if __name__ == "__main__":
    # for i in range(3):
    #     t = Process(target=test)
    #     t.start()
    #     t.join()

    test()