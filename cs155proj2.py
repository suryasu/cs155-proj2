import string
import os
import numpy as np

directory = os.path.dirname(os.path.abspath(__file__))
f = open(directory + "/shakespeare.txt", 'r')

d = {}
index = 0
order = []
O = []

for line in f:
    line = line.strip()
    if  line == "" or line[0] in string.digits:
        continue
    order = []
    line = "".join(l for l in line if l not in string.punctuation)
    line = string.lower(line)
    line = line.split()

    for word in line:
        if word not in d:
            d[word] = index
            index += 1
        order.append(d[word])
    O.append(np.array(order))

O = np.array(O)