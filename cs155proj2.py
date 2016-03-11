import string
import numpy as np

f = open("/Users/Surya/Documents/Junior/Winter2015/cs155/project2data/shakespeare.txt", 'r')

d = {}
index = 0
order = []
O = []

for line in f:
    order = []
    line = "".join(l for l in line if l not in string.punctuation)
    line = string.lower(line)
    line = line.split
    for word in line:
        if word not in d:
            d[word] = index
        order.append(d[word])
    O.append(np.array(order))
    

O = np.array(O)