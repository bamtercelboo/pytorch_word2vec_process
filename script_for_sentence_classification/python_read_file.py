# @Author : bamtercelboo
# @Datetime : 2018/1/24 8:24
# @File : python_read_file.py
# @Last Modify Time : 2018/1/24 8:24
# @Contact : bamtercelboo@{gmail.com, 163.com}

"""
    FILE :  python_read_file.py
    FUNCTION : None
"""

file = open('test.log', 'r')
sizehint = 209715200   # 200M
position = 0
lines = file.readlines(sizehint)
while not file.tell() - position < 0:
    position = file.tell()
    lines = file.readlines(sizehint)