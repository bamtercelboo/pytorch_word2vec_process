# @Author : bamtercelboo
# @Datetime : 2018/2/27 8:32
# @File : test.py
# @Last Modify Time : 2018/2/27 8:32
# @Contact : bamtercelboo@{gmail.com, 163.com}

"""
    FILE :  test.py
    FUNCTION : None
"""

string_a = "'台湾是中国领土不可分割的一部分。完成祖国统一,是大势所趋,民心所向。任何企图制造“两个中国”、“一中一台”、“台湾独立”的图谋,都注定要更失败。希望台湾当局以民族大义为重,拿出诚意,采取实际的行动,推动两岸经济文化交流和人员往来,促进两岸直接通邮、通航、通商的早日实现,并尽早回应我们发出的在一个中国的原则下两岸进行谈判的郑重呼吁。'"
string_b = "'台湾是中国领土不可分割的一部分。完成祖国统一,是大势所趋,民心所向。任何企图制造“两个中国”、“一中一台”、“台湾独立”的图谋,都注定要失败。希望台湾当局以民族大义为重,拿出诚意,采取实际的行动,推动两岸经济文化交流和人员往来,促进两岸直接通邮、通航、通商的早日实现,并尽早回应我们发出的在一个中国的原则下两岸进行谈判的郑重呼吁。'"
if string_a == string_b:
    print("equal")

import torch
from torch.autograd import Variable
a = Variable(torch.LongTensor(2))
print(a)
print(a.data[1].__class__)


