import string
import os
import numpy as np
import nltk.tag.hmm as hmm

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
        order.append((d[word], None))
    O.append(np.array(order))

num_samples = 20
O = np.array(O)
hmmt = hmm.HiddenMarkovModelTrainer(states=range(num_samples), symbols=range(len(d)))
model = hmmt.train_unsupervised(O, max_iterations=50)

# get probability of emission j given state i
for i in range(num_samples):
    total = 0
    for j in range(len(d)):
        total += model._outputs[i].prob(j)
    assert (abs(total - 1.0) < 1e-6)

# get probability of transitioning to state j from state i
for i in range(num_samples):
    total = 0
    for j in range(num_samples):
        total += model._transitions[i].prob(j)
    assert (abs(total - 1.0) < 1e-6)

# i = 0
# get random emission given state i
# print model._outputs[i].generate()

# get random transition given current state i
# print model._transitions[i].generate()

poem = ""
for i in range(14):
    next_item = model._priors.generate()
    poem += d.keys()[d.values().index(next_item)]
    for j in range(9):
        next_item = model._transitions[next_item].generate()
        poem += " " + d.keys()[d.values().index(model._outputs[next_item].generate())]
    poem += "\n"

print poem

